FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Данные (SQLite) лежат в /data — подключите к нему том (Volume), иначе они пропадут при пересборке.
RUN useradd -m appuser && mkdir -p /data && chown appuser /data
USER appuser
ENV DATA_DIR=/data

# Один процесс: лимиты запросов хранятся в памяти процесса.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
