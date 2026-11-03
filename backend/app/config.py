"""Все настройки берутся из переменных окружения (см. .env.example)."""
import os


def _int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")

# Секрет для подписи токенов устройств. ОБЯЗАТЕЛЬНО задайте длинную случайную строку.
SERVER_SECRET = os.environ.get("SERVER_SECRET", "")
# Необязательный общий ключ приложения (заголовок X-App-Key). Пусто = не проверять.
APP_KEY = os.environ.get("APP_KEY", "")

# Куда писать SQLite (резервные копии). На Railway подключите Volume и укажите его путь.
DATA_DIR = os.environ.get("DATA_DIR", "./data")

# Лимиты (на одно устройство).
CHAT_PER_MINUTE = _int("CHAT_PER_MINUTE", 6)
CHAT_PER_DAY = _int("CHAT_PER_DAY", 100)
REGISTER_PER_HOUR_PER_IP = _int("REGISTER_PER_HOUR_PER_IP", 20)
# Общий потолок запросов к ИИ в сутки на весь сервер (защита от неожиданного счёта).
GLOBAL_CHAT_PER_DAY = _int("GLOBAL_CHAT_PER_DAY", 5000)

MAX_BACKUP_BYTES = _int("MAX_BACKUP_BYTES", 512 * 1024)
# Максимальный размер тела обычных запросов (чат, регистрация). Остальное отклоняется до разбора JSON.
MAX_BODY_BYTES = _int("MAX_BODY_BYTES", 64 * 1024)
# Сколько прокси стоит перед сервером (Railway/Cloudflare/Caddy = 1). 0 — прокси нет.
TRUSTED_PROXY_HOPS = _int("TRUSTED_PROXY_HOPS", 1)
CORS_ORIGINS = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]
