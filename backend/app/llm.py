"""Вызов модели Anthropic. Отдельный модуль, чтобы его можно было подменить в тестах."""
import threading

from . import config
from .logic import TOOLS

_client = None
_lock = threading.Lock()


def _get_client():
    global _client
    with _lock:
        if _client is None:
            import anthropic  # импорт здесь, чтобы тесты логики не требовали SDK
            _client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY, timeout=20.0, max_retries=1)
        return _client


def call_model(system, messages):
    """Возвращает список блоков [{'type': 'text'|'tool_use', ...}]."""
    resp = _get_client().messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=800,
        system=system,
        tools=TOOLS,
        messages=messages,
    )
    blocks = []
    for b in resp.content:
        if b.type == "text":
            blocks.append({"type": "text", "text": b.text})
        elif b.type == "tool_use":
            blocks.append({"type": "tool_use", "name": b.name, "input": b.input})
    return blocks
