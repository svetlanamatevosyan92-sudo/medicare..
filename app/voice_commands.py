# -*- coding: utf-8 -*-
"""Голосовые команды, которые приложение понимает САМО, без сервера и интернета.

Распознаются четыре вида команд на русском, английском и армянском:
  next  — «что дальше», «когда следующий приём»
  today — «расписание на сегодня»
  check — «проверь расписание»
  taken — «я принял парацетамол»  (меняет данные, поэтому всегда с подтверждением)

Всё остальное возвращает None и уходит в чат с ИИ. Разбор осторожный: отрицание
(«я НЕ принял», «забыл», «пропустил») никогда не считается отметкой о приёме.
Без Kivy: тестируется отдельно.
"""
import datetime as dt
import difflib
import re
from collections import namedtuple

import core

Intent = namedtuple("Intent", "kind query")

_NEGATION = re.compile(
    r"\b(не|ещё не|еще не|забыл\w*|пропустил\w*|не успел\w*|not|didn'?t|did not|haven'?t|have not|"
    r"hasn'?t|forgot\w*|missed|skipped|never)\b|\bչեմ\b|\bչըն\w*|\bմոռացա\w*|\bբաց թողե\w*",
    re.IGNORECASE | re.UNICODE)

_TAKEN = [
    re.compile(r"\b(?:я\s+)?(?:принял[аи]?|выпил[аи]?|съел[аи]?)\b(?P<tail>.*)"),
    re.compile(r"\bотмет\w*\s+(?:что\s+)?(?:я\s+)?(?:как\s+)?(?:принят\w*|принял[аи]?|выпил[аи]?)\b(?P<tail>.*)"),
    re.compile(r"\bi\s+(?:have\s+|just\s+)?(?:took|taken|had)\b(?P<tail>.*)"),
    re.compile(r"\bmark\b(?P<tail>.*?)\b(?:as\s+)?taken\b"),
    re.compile(r"\bես\s+ընդունեցի\b(?P<tail>.*)"),
    re.compile(r"\bընդունեցի\b(?P<tail>.*)"),
]

_NEXT = re.compile(
    r"что\s+(?:у\s+меня\s+)?(?:дальше|следующ\w*)|когда\s+(?:мне\s+)?(?:следующ\w*|принимать|пить)|"
    r"следующ\w*\s+(?:приём|прием|лекарств\w*|таблет\w*)|что\s+(?:мне\s+)?(?:принять|выпить|пить)\b|"
    r"what'?s\s+next|what\s+is\s+next|next\s+(?:dose|pill|medicine|medication)|"
    r"when\s+(?:do\s+i\s+|should\s+i\s+)?(?:take|is)\s+(?:my\s+)?next|"
    r"what\s+(?:should|do)\s+i\s+(?:need\s+to\s+)?take|"
    r"հաջորդ\s+(?:ընդունում\w*|դեղ\w*)|ինչ\s+է\s+հաջորդ\w*")

_TODAY = re.compile(
    r"(?:расписани\w*|план\w*|приёмы|приемы|лекарств\w*|что\s+принимать).{0,20}сегодня|"
    r"что\s+на\s+сегодня|покажи\s+(?:расписание|приёмы|приемы)|"
    r"today'?s\s+(?:schedule|medications?|pills|doses|plan)|what\s+(?:do\s+i\s+have|is\s+planned)\s+today|"
    r"այսօրվա\s+(?:ժամանակացույց\w*|ընդունում\w*)|այսօր\s+ինչ")

_CHECK = re.compile(
    r"проверь\s+(?:мо[её]\s+)?(?:расписание|лекарства|приёмы|приемы)|анализ\s+расписания|"
    r"есть\s+ли\s+(?:конфликт\w*|проблем\w*)\s+(?:в\s+)?(?:расписани\w*|лекарств\w*)|"
    r"check\s+(?:my\s+)?(?:schedule|medications?|medicines|pills)|any\s+(?:conflicts|problems)\s+in\s+my\s+(?:schedule|medic\w+)|"
    r"ստուգիր\s+(?:իմ\s+)?(?:ժամանակացույց\w*|դեղ\w*)")

_STOP = {
    "лекарство", "лекарства", "таблетку", "таблетка", "таблетки", "пилюлю", "мое", "моё", "мои", "мой", "мою",
    "свою", "своё", "своё", "свои", "уже", "только", "что", "как", "принятым", "принятое", "принято",
    "ее", "её", "его", "их", "все", "всё", "это", "ничего",
    "it", "them", "this", "that", "one", "all", "some", "the", "my", "pill", "pills", "medicine", "medication", "tablet", "just", "now", "already", "a", "an",
    "իմ", "դեղը", "դեղ", "հաբը",
}


def _norm(text):
    text = (text or "").lower().replace("ё", "е")
    text = re.sub(r"[^\w\s':-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def parse(text):
    """Возвращает Intent(kind, query) или None, если это не команда (тогда — в чат с ИИ)."""
    text = _norm(text)
    if not text or len(text) > 200:
        return None
    # «проверь расписание» и «что дальше» — только чтение, отрицание на них не влияет
    if _CHECK.search(text):
        return Intent("check", "")
    if _NEXT.search(text):
        return Intent("next", "")
    if _TODAY.search(text):
        return Intent("today", "")
    if _NEGATION.search(text):
        return None                              # «я не принял», «забыл выпить» — не отметка
    for pattern in _TAKEN:
        m = pattern.search(text)
        if m:
            tail = m.group("tail") if "tail" in pattern.groupindex else ""
            words = [w for w in re.split(r"\s+", tail) if w and w not in _STOP]
            return Intent("taken", " ".join(words)[:60])
    return None


# ---- поиск лекарства по названию из распознанной речи --------------------------------------

def match_meds(meds, query, threshold=0.72):
    """Лекарства, чьё название похоже на сказанное (ASR часто искажает окончания и буквы)."""
    query = _norm(query)
    if not query:
        return []
    scored = []
    for med in meds:
        name = _norm(med.get("name", ""))
        if not name:
            continue
        words = query.split()
        score = max([difflib.SequenceMatcher(None, name, query).ratio()] +
                    [difflib.SequenceMatcher(None, name, w).ratio() for w in words])
        if len(name) >= 4 and (name in query or any(len(w) >= 4 and w in name for w in words)):
            score = max(score, 0.9)
        if score >= threshold:
            scored.append((score, med))
    scored.sort(key=lambda s: -s[0])
    return [m for _s, m in scored]


def eligible_doses(data, now, query=""):
    """Приёмы за сегодня, которые ещё не отмечены и которые уже МОЖНО отметить (core.can_mark_taken).

    Без названия — только ближайший к текущему времени приём (все лекарства на это время).
    С названием — все подходящие неотмеченные приёмы этого лекарства.
    Возвращает список (день, время, лекарство).
    """
    today = now.date()
    doses = [(today, tm, med) for tm, med in core.doses_for(data, today)
             if not core.is_taken(data, today, med, tm) and core.can_mark_taken(today, tm, now)]
    if query:
        ids = {m["id"] for m in match_meds([m for _t, m in core.doses_for(data, today)], query)}
        doses = [d for d in doses if d[2]["id"] in ids]
        if len(doses) > 1:           # у лекарства несколько приёмов: берём ближайший к «сейчас»
            doses = _closest(doses, now)
        return doses
    return _closest(doses, now)


def _closest(doses, now):
    if not doses:
        return []

    def gap(d):
        due = dt.datetime.combine(d[0], dt.time.fromisoformat(d[1]))
        return abs((due - now).total_seconds())
    best = min(gap(d) for d in doses)
    nearest_time = next(d[1] for d in doses if gap(d) == best)
    return [d for d in doses if d[1] == nearest_time]


# ---- локальные ответы (читаются вслух, работают без интернета) --------------------------

_V = {
    "ru": {
        "next": "Следующий приём в {tm}: {names}.",
        "overdue": "Приём в {tm} ещё не отмечен: {names}.",
        "tomorrow": "Сегодня приёмов больше нет. Завтра в {tm}: {names}.",
        "none": "В расписании нет приёмов.",
        "today_none": "На сегодня приёмов нет.",
        "today_head": "Сегодня приёмов: {n}.",
        "line": "В {tm} — {names}, {status}.",
        "taken": "принято", "pending": "ещё не принято",
        "more": "И ещё {n}.",
    },
    "en": {
        "next": "Your next dose is at {tm}: {names}.",
        "overdue": "The dose at {tm} is not marked yet: {names}.",
        "tomorrow": "No more doses today. Tomorrow at {tm}: {names}.",
        "none": "There are no doses in your schedule.",
        "today_none": "No doses today.",
        "today_head": "Doses today: {n}.",
        "line": "At {tm}, {names}, {status}.",
        "taken": "taken", "pending": "not taken yet",
        "more": "And {n} more.",
    },
    "hy": {
        "next": "Հաջորդ ընդունումը {tm}-ին է՝ {names}։",
        "overdue": "{tm}-ի ընդունումը դեռ չի նշված՝ {names}։",
        "tomorrow": "Այսօր այլևս ընդունումներ չկան։ Վաղը {tm}-ին՝ {names}։",
        "none": "Ժամանակացույցում ընդունումներ չկան։",
        "today_none": "Այսօր ընդունումներ չկան։",
        "today_head": "Այսօր ընդունումներ՝ {n}։",
        "line": "{tm}-ին՝ {names}, {status}։",
        "taken": "ընդունված է", "pending": "դեռ չի ընդունվել",
        "more": "Եվ ևս {n}։",
    },
}


def _tx(lang):
    return _V.get(lang) or _V["en"]


def _names(doses):
    return ", ".join("%s %s" % (m["name"], m["dose"]) for _tm, m in doses)


def describe_next(data, now, lang="ru"):
    t = _tx(lang)
    today = now.date()
    pending = [(tm, m) for tm, m in core.doses_for(data, today) if not core.is_taken(data, today, m, tm)]
    for tm in sorted({tm for tm, _m in pending}):
        due = dt.datetime.combine(today, dt.time.fromisoformat(tm))
        if due >= now - dt.timedelta(hours=1):
            group = [(x, m) for x, m in pending if x == tm]
            return t["next" if due >= now else "overdue"].format(tm=tm, names=_names(group))
    tomorrow = today + dt.timedelta(days=1)
    later = core.doses_for(data, tomorrow)
    if later:
        first = later[0][0]
        return t["tomorrow"].format(tm=first, names=_names([(x, m) for x, m in later if x == first]))
    return t["none"] if not data.get("meds") else t["today_none"]


def describe_today(data, now, lang="ru", limit=8):
    t = _tx(lang)
    today = now.date()
    items = core.doses_for(data, today)
    if not items:
        return t["today_none"]
    slots = []
    for tm in sorted({tm for tm, _m in items}):
        group = [(x, m) for x, m in items if x == tm]
        done = all(core.is_taken(data, today, m, x) for x, m in group)
        slots.append((tm, group, done))
    parts = [t["today_head"].format(n=len(items))]
    for tm, group, done in slots[:limit]:
        parts.append(t["line"].format(tm=tm, names=_names(group), status=t["taken" if done else "pending"]))
    if len(slots) > limit:
        parts.append(t["more"].format(n=len(slots) - limit))
    return " ".join(parts)
