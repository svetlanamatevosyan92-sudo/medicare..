"""MediCare backend: AI-помощник (прокси к Anthropic) и резервные копии расписания.

Запуск:  uvicorn app.main:app --host 0.0.0.0 --port 8000
"""
import json
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from . import config, db, llm, logic

log = logging.getLogger("medicare")
logging.basicConfig(level=logging.INFO)

limiter = logic.RateLimiter()


@asynccontextmanager
async def lifespan(_app):
    if len(config.SERVER_SECRET) < 24:
        raise RuntimeError("SERVER_SECRET не задан или слишком короткий (нужно >= 24 символов)")
    if not config.ANTHROPIC_API_KEY:
        log.warning("ANTHROPIC_API_KEY не задан: /api/v1/chat будет отвечать 503")
    yield


app = FastAPI(title="MediCare backend", version="1.0.0", lifespan=lifespan,
              docs_url=None, redoc_url=None, openapi_url=None)

class _TooLarge(Exception):
    pass


class BodyLimitMiddleware:
    """Отклоняет слишком большие запросы ДО разбора JSON (защита памяти сервера).

    Проверяет заголовок Content-Length и, на случай chunked-запросов без него,
    считает реально полученные байты.
    """

    def __init__(self, app):
        self.app = app

    async def _reject(self, scope, receive, send):
        resp = JSONResponse({"detail": "too_large"}, status_code=413)
        await resp(scope, receive, send)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        limit = config.MAX_BACKUP_BYTES if scope["path"].startswith("/api/v1/backup") else config.MAX_BODY_BYTES
        declared = dict(scope.get("headers") or []).get(b"content-length")
        if declared is not None:
            try:
                if int(declared) > limit:
                    return await self._reject(scope, receive, send)
            except ValueError:
                return await self._reject(scope, receive, send)

        received = 0

        async def limited_receive():
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > limit:
                    raise _TooLarge()
            return message

        try:
            await self.app(scope, limited_receive, send)
        except _TooLarge:
            await self._reject(scope, receive, send)


app.add_middleware(BodyLimitMiddleware)

if config.CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS,
                       allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["*"])


# ---------------------------------------------------------------- вспомогательное
def client_ip(request: Request):
    peer = request.client.host if request.client else "unknown"
    return logic.client_ip(request.headers.get("x-forwarded-for", ""), peer, config.TRUSTED_PROXY_HOPS)


def check_app_key(x_app_key: str = Header(default="")):
    if config.APP_KEY and not logic.same_secret(x_app_key, config.APP_KEY):
        raise HTTPException(status_code=403, detail="forbidden")


def current_install(authorization: str = Header(default="")):
    token = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    install_id = logic.check_token(config.SERVER_SECRET, token)
    if not install_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    return install_id


# ---------------------------------------------------------------- модели запросов
class RegisterIn(BaseModel):
    install_id: str = Field(max_length=128)


class ChatIn(BaseModel):
    messages: list[dict] = Field(max_length=60)
    lang: str = Field(default="ru", max_length=8)
    meds: list[dict] = Field(default_factory=list, max_length=60)


# ---------------------------------------------------------------- маршруты
@app.get("/health")
def health():
    return {"status": "ok", "ai_configured": bool(config.ANTHROPIC_API_KEY)}


@app.post("/api/v1/register", dependencies=[Depends(check_app_key)])
def register(body: RegisterIn, request: Request):
    if not limiter.allow("reg:" + client_ip(request), config.REGISTER_PER_HOUR_PER_IP, 3600):
        raise HTTPException(status_code=429, detail="rate_limited")
    if not logic.valid_install_id(body.install_id):
        raise HTTPException(status_code=422, detail="bad install_id")
    return {"token": logic.make_token(config.SERVER_SECRET, body.install_id)}


@app.post("/api/v1/chat", dependencies=[Depends(check_app_key)])
def chat(body: ChatIn, install_id: str = Depends(current_install)):
    # обычная функция (не async): FastAPI выполнит её в пуле потоков, и ожидание ответа ИИ не блокирует сервер
    messages = logic.clean_messages(body.messages)
    if not messages or messages[-1]["role"] != "user":
        raise HTTPException(status_code=422, detail="no user message")
    lang = body.lang if body.lang in logic.LANGS else "ru"

    # Страховка: описание экстренных симптомов распознаётся без участия ИИ. Если ИИ недоступен,
    # не настроен или исчерпан лимит — человек всё равно получает указание звонить 112.
    urgent = logic.emergency_floor(messages[-1]["content"])

    def emergency():
        return {"reply": logic.EMERGENCY_REPLY[lang], "urgency": "emergency", "proposals": []}

    if not config.ANTHROPIC_API_KEY:
        if urgent:
            return emergency()
        raise HTTPException(status_code=503, detail="ai_not_configured")
    if not limiter.allow("chat-min:" + install_id, config.CHAT_PER_MINUTE, 60) \
            or not limiter.allow("chat-day:" + install_id, config.CHAT_PER_DAY, 86400) \
            or not limiter.allow("chat-global", config.GLOBAL_CHAT_PER_DAY, 86400):
        if urgent:
            return emergency()
        raise HTTPException(status_code=429, detail="rate_limited")

    system = logic.build_system_prompt(lang, logic.clean_meds_context(body.meds))
    try:
        blocks = llm.call_model(system, messages)
    except Exception as exc:  # сеть, лимиты и ошибки API не должны раскрывать детали клиенту
        log.error("AI call failed: %s: %s", type(exc).__name__, exc)
        if urgent:
            return emergency()
        raise HTTPException(status_code=502, detail="ai_unavailable")

    reply, proposals, urgency = logic.parse_model_blocks(blocks)
    if urgent:
        urgency = "emergency"
    if not reply and proposals:
        reply = logic.DEFAULT_CONFIRM[lang]
    return {"reply": reply, "urgency": urgency, "proposals": proposals}


@app.put("/api/v1/backup", dependencies=[Depends(check_app_key)])
async def put_backup(request: Request, install_id: str = Depends(current_install)):
    raw = await request.body()
    if len(raw) > config.MAX_BACKUP_BYTES:
        raise HTTPException(status_code=413, detail="too_large")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except ValueError:
        raise HTTPException(status_code=422, detail="bad json")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="bad payload")
    return {"updated_at": db.save_backup(install_id, payload)}


@app.get("/api/v1/backup", dependencies=[Depends(check_app_key)])
def get_backup(install_id: str = Depends(current_install)):
    found = db.load_backup(install_id)
    if not found:
        raise HTTPException(status_code=404, detail="no_backup")
    return found


@app.delete("/api/v1/backup", dependencies=[Depends(check_app_key)])
def delete_backup(install_id: str = Depends(current_install)):
    return {"deleted": db.delete_backup(install_id)}
