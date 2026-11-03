"""Хранилище резервных копий расписания (SQLite из стандартной библиотеки)."""
import datetime as dt
import json
import os
import sqlite3

from . import config


def _path():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    return os.path.join(config.DATA_DIR, "medicare.sqlite3")


def _connect():
    conn = sqlite3.connect(_path(), timeout=10)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS backups ("
        " install_id TEXT PRIMARY KEY, payload TEXT NOT NULL, updated_at TEXT NOT NULL)"
    )
    return conn


def save_backup(install_id, payload: dict):
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    conn = _connect()
    try:
        with conn:
            conn.execute(
                "INSERT INTO backups (install_id, payload, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(install_id) DO UPDATE SET payload=excluded.payload, updated_at=excluded.updated_at",
                (install_id, json.dumps(payload, ensure_ascii=False), stamp),
            )
    finally:
        conn.close()
    return stamp


def load_backup(install_id):
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT payload, updated_at FROM backups WHERE install_id=?", (install_id,)).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    return {"payload": json.loads(row[0]), "updated_at": row[1]}


def delete_backup(install_id):
    conn = _connect()
    try:
        with conn:
            cur = conn.execute("DELETE FROM backups WHERE install_id=?", (install_id,))
        return cur.rowcount > 0
    finally:
        conn.close()
