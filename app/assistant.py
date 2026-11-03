# -*- coding: utf-8 -*-
"""Клиент AI-помощника: общается с бэкендом MediCare по HTTPS.

Ключ Anthropic в приложении НЕ хранится — он есть только на сервере.
Токен и идентификатор установки лежат в защищённом хранилище (secure_store), а не в medicare.json.
Модуль не зависит от Kivy, поэтому его можно тестировать отдельно.
"""
import json
import os
import ssl
import uuid
import urllib.error
import urllib.parse
import urllib.request

import config


class AssistantError(Exception):
    """kind: 'not_configured' | 'network' | 'auth' | 'rate' | 'server'."""

    def __init__(self, kind, detail=""):
        super().__init__(kind + (": " + detail if detail else ""))
        self.kind = kind
        self.detail = detail


_LOCAL_HOSTS = ("localhost", "127.0.0.1", "10.0.2.2")


def validate_base_url(url, allow_local_http=False):
    """Возвращает нормализованный адрес или \"\", если он небезопасен.

    Принимает только https://хост[:порт] (без логина в адресе). http — только для локальной отладки.
    """
    url = (url or "").strip().rstrip("/")
    if not url:
        return ""
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return ""
    if not parts.hostname or parts.username or parts.password:
        return ""
    if parts.scheme == "https":
        return url
    if parts.scheme == "http" and allow_local_http and parts.hostname in _LOCAL_HOSTS:
        return url
    return ""


def _ssl_context():
    try:
        import certifi  # на Android системные сертификаты Python недоступны
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Не следуем редиректам: ответ 301/302 не должен увести запрос с токеном на другой адрес."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class AssistantClient:
    SECRET_FIELDS = ("token", "install_id")

    def __init__(self, data, store=None):
        """data — тот же словарь, что хранит core.load()/core.save().

        store — SecureStore. Если не передан, создаётся рядом с данными приложения.
        """
        self.data = data
        if store is None:
            import core
            from secure_store import SecureStore
            store = SecureStore(os.path.dirname(core.STORE))
        self.store = store

    # -- миграция старых версий -------------------------------------------
    def migrate_legacy(self):
        """Переносит токен/install_id из medicare.json в защищённое хранилище и удаляет их оттуда.

        Возвращает True, если словарь данных изменился (его нужно сохранить).
        """
        cfg = self.data.get("assistant")
        if not isinstance(cfg, dict):
            return False
        changed = False
        for name in self.SECRET_FIELDS:
            if name in cfg:
                value = cfg.pop(name)
                changed = True
                if isinstance(value, str) and value and not self.store.get(name):
                    self.store.set(name, value)
        if "url" in cfg:           # адрес из файла данных больше не используется (см. config.py)
            cfg.pop("url")
            changed = True
        return changed

    def forget(self):
        """Удаляет токен и идентификатор установки (например, при «удалить мои данные»)."""
        self.store.clear()

    # -- настройки ---------------------------------------------------------
    @property
    def base_url(self):
        raw = os.environ.get("MEDICARE_API_URL") or config.API_URL or ""
        return validate_base_url(raw, allow_local_http=config.ALLOW_LOCAL_HTTP)

    def configured(self):
        return bool(self.base_url)

    # -- HTTP --------------------------------------------------------------
    def _opener(self):
        return urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=_ssl_context()), _NoRedirect())

    def _request(self, path, payload, token=None):
        base = self.base_url
        if not base:
            raise AssistantError("not_configured")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if config.APP_KEY:
            headers["X-App-Key"] = config.APP_KEY
        if token:
            headers["Authorization"] = "Bearer " + token
        req = urllib.request.Request(
            base + path,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers, method="POST",
        )
        try:
            with self._opener().open(req, timeout=config.REQUEST_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise AssistantError("auth")
            if exc.code == 429:
                raise AssistantError("rate")
            raise AssistantError("server", str(exc.code))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise AssistantError("network", str(exc))
        except ValueError as exc:
            raise AssistantError("server", "bad json: %s" % exc)

    def _register(self):
        install_id = self.store.get("install_id") or uuid.uuid4().hex
        out = self._request("/api/v1/register", {"install_id": install_id})
        token = out.get("token") if isinstance(out, dict) else None
        if not isinstance(token, str) or not token:
            raise AssistantError("server", "no token")
        self.store.set("install_id", install_id)
        self.store.set("token", token)
        return token

    # -- публичный API -----------------------------------------------------
    def chat(self, messages, meds, lang):
        """Отправляет историю диалога; возвращает словарь ответа сервера:

        {"reply": str, "urgency": "none|doctor|emergency",
         "proposals": [{name, dose, form, how, times, days, note}, ...]}
        """
        payload = {
            "messages": messages[-20:],
            "lang": lang,
            "meds": [
                {"name": m.get("name", ""), "dose": m.get("dose", ""),
                 "times": m.get("times", []), "days": m.get("days", 0),
                 "how": m.get("how", "any")}
                for m in meds[:50]
            ],
        }
        token = self.store.get("token") or self._register()
        try:
            out = self._request("/api/v1/chat", payload, token)
        except AssistantError as exc:
            if exc.kind != "auth":
                raise
            # токен мог устареть (например, сменили SECRET на сервере)
            token = self._register()
            out = self._request("/api/v1/chat", payload, token)
        if not isinstance(out, dict) or not isinstance(out.get("reply", ""), str):
            raise AssistantError("server", "bad response")
        out.setdefault("urgency", "none")
        if out["urgency"] not in ("none", "doctor", "emergency"):
            out["urgency"] = "none"
        if not isinstance(out.get("proposals"), list):
            out["proposals"] = []
        return out
