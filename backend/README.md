# MediCare backend

Сервер для приложения MediCare:

- **AI-помощник** — приложение отправляет сюда диалог, сервер обращается к Anthropic API (ключ хранится только на сервере) и возвращает ответ.
  Помощник может *предложить* лекарство для добавления (`proposals`), но приложение добавляет его только после подтверждения человеком.
- **Резервная копия расписания** (необязательно) — `PUT/GET/DELETE /api/v1/backup`.

Стек: Python 3.12, FastAPI, SQLite (стандартная библиотека). Один Docker-образ — запускается где угодно.

## Переменные окружения

См. `.env.example`. Обязательные: `ANTHROPIC_API_KEY` и `SERVER_SECRET`. Без `SERVER_SECRET` сервер не запустится (так задумано).

## Запуск на Railway

1. Загрузите папку `medicare-backend` в репозиторий GitHub (без файла `.env`).
2. Railway → **New Project → Deploy from GitHub repo**. Railway найдёт `Dockerfile` и `railway.json`.
3. Вкладка **Variables**: добавьте `ANTHROPIC_API_KEY`, `SERVER_SECRET`, `DATA_DIR=/data` (остальные — по желанию).
4. Volume **не нужен**: приложение использует только чат, а резервные копии не отправляет. Если всё же подключите Volume к `/data`, добавьте переменную `RAILWAY_RUN_UID=0` (Railway монтирует том от имени root, а контейнер работает от обычного пользователя — без этой переменной запись в `/data` будет падать с «permission denied»).
5. **Settings → Networking → Generate Domain**. Получите адрес вида `https://xxx.up.railway.app`.
6. Проверка: откройте `https://xxx.up.railway.app/health` — должно быть `{"status":"ok","ai_configured":true}`.

Через CLI вместо GitHub: `railway login && railway init && railway up`.

## Запуск на любом другом сервере (VPS)

```bash
docker build -t medicare-backend .
docker run -d --name medicare --restart unless-stopped -p 8000:8000 \
  --env-file .env -v medicare-data:/data medicare-backend
```

Нужен HTTPS (Android по умолчанию блокирует обычный http). Самый простой путь — Caddy перед контейнером:

```
medicare.example.com {
    reverse_proxy localhost:8000
}
```

Без Docker: `pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000` (переменные — из окружения).

Важно: запускайте **один процесс** (без `--workers`), потому что лимиты запросов хранятся в памяти процесса. Для нескольких копий сервера лимиты нужно вынести в Redis.

## Подключение приложения

В `config.py` приложения впишите `API_URL = "https://xxx.up.railway.app"` **до сборки APK**. Переменные окружения на телефоне не существуют, поэтому адрес и ключ нужно вписать в файл. Проще всего **не задавать `APP_KEY`** на сервере. Если задали — впишите тот же ключ в `APP_KEY` в `config.py`, иначе сервер будет отвечать 403. Для проверки на компьютере достаточно переменной `MEDICARE_API_URL`.

## API

Все запросы с телом — JSON. Если задан `APP_KEY`, нужен заголовок `X-App-Key`.

| Метод | Путь | Описание |
|---|---|---|
| GET | `/health` | Проверка работы |
| POST | `/api/v1/register` | `{"install_id": "<16–64 символа A-Za-z0-9_->"}` → `{"token": "..."}` |
| POST | `/api/v1/chat` | `Authorization: Bearer <token>`; `{"messages":[{"role","content"}], "lang":"ru\|en\|hy", "meds":[...]}` → `{"reply","urgency":"none\|doctor\|emergency","proposals":[{name,dose,form,how,times,days,note}]}` |
| PUT/GET/DELETE | `/api/v1/backup` | Резервная копия JSON (до 512 КБ) для устройства |

Проверка с компьютера:

```bash
URL=https://xxx.up.railway.app
TOKEN=$(curl -s -X POST $URL/api/v1/register -H 'Content-Type: application/json' \
  -d '{"install_id":"test-device-0123456789"}' | python -c "import sys,json;print(json.load(sys.stdin)['token'])")
curl -s -X POST $URL/api/v1/chat -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"lang":"ru","messages":[{"role":"user","content":"Мне назначили аспирин 100 мг, пить утром, 30 дней"}]}'
```

## Безопасность и ограничения (прочитайте)

- Здесь нет входа по логину: устройство получает подписанный токен при первом запуске. Защита от злоупотреблений — лимиты на устройство (`CHAT_PER_MINUTE`, `CHAT_PER_DAY`), на IP при регистрации и общий потолок `GLOBAL_CHAT_PER_DAY`. Задайте лимит расходов в консоли Anthropic.
- Текст переписки и список лекарств уходят в Anthropic API. Это медицинские данные: нужна политика конфиденциальности и информирование пользователя; в ряде стран есть дополнительные требования к хранению и передаче таких данных.
- Сервер не хранит переписку. Хранятся только резервные копии, если приложение их отправляет.
- Помощник не заменяет врача. Промпт запрещает диагнозы и изменение назначений, но модель может ошибаться — поэтому добавление лекарства всегда требует подтверждения в приложении.
- Тесты логики: `python -m unittest discover tests`.
