# -*- coding: utf-8 -*-
"""План фоновых напоминаний: что и когда должно прозвучать, даже если приложение закрыто.

Python считает план и записывает его в alarms.json (в каталоге данных приложения). Нативная
часть на Java (android_src/org/medicare/reminder) читает файл, ставит будильник на ближайшую
запись и показывает уведомление. Так расписание, тихие часы и язык считаются в ОДНОМ месте,
а Java остаётся маленьким и простым.

Правила (совпадают с поведением напоминаний при открытом приложении, см. reminders.py):
  - принятые дозы не напоминаются; выключенные уведомления или тихие часы — тоже;
  - несколько лекарств на одно время — одно уведомление;
  - если приём не отмечен через час — ОДНО нейтральное напоминание: без повторов и без слов,
    будто принять позже безопасно, и без совета удвоить дозу;
  - план на HORIZON_DAYS дней вперёд; в конце — просьба открыть приложение, чтобы напоминания
    продолжились (иначе после горизонта они молча остановились бы).
Без Kivy: тестируется отдельно.
"""
import datetime as dt
import json
import os
import tempfile

import core

HORIZON_DAYS = 14
MISSED_AFTER = dt.timedelta(hours=1)
MAX_ENTRIES = 600
PLAN_FILE = "alarms.json"
BEAT_FILE = "foreground.beat"


def _epoch_ms(naive):
    """Местное «настенное» время -> миллисекунды Unix."""
    return int(naive.timestamp() * 1000)


def _join(meds):
    return ", ".join("%s %s" % (m["name"], m["dose"]) for m in meds)


def build_plan(data, now, texts, horizon_days=HORIZON_DAYS):
    """Возвращает словарь плана (см. PLAN_FILE) или план без записей, если напоминания выключены.

    now — местное время без часового пояса (datetime.now()).
    texts — строки интерфейса: rem_dose_title, rem_missed_title, rem_missed_text,
            rem_refresh_title, rem_refresh_text, rem_channel_name.
    """
    notif = data.get("notif", {}) if isinstance(data, dict) else {}
    enabled = bool(notif.get("all", True)) and bool(notif.get("bg", True)) and bool(notif.get("push", True))
    plan = {
        "version": 1, "generated_ms": _epoch_ms(now),
        "sound": bool(notif.get("sound", True)), "vibrate": bool(notif.get("vib", True)),
        "channel_name": texts.get("rem_channel_name", "MediCare"),
        "alarms": [],
    }
    if not enabled:
        return plan

    quiet = bool(notif.get("quiet"))
    grouped = {}          # (момент, вид) -> [(время, лекарство)]
    first_day = now.date()
    for offset in range(horizon_days):
        day = first_day + dt.timedelta(days=offset)
        for tm, med in core.doses_for(data, day):
            if core.is_taken(data, day, med, tm):
                continue
            due = dt.datetime.combine(day, dt.time.fromisoformat(tm))
            if quiet and core.in_quiet(due):
                continue
            if due > now:
                grouped.setdefault((due, "dose"), []).append((tm, med))
            if due + MISSED_AFTER > now:
                grouped.setdefault((due + MISSED_AFTER, "missed"), []).append((tm, med))

    entries = []
    for (moment, kind), items in sorted(grouped.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        meds = [m for _tm, m in items]
        times = ", ".join(sorted({tm for tm, _m in items}))
        if kind == "dose":
            title, text = texts["rem_dose_title"], _join(meds)
        else:
            title = texts["rem_missed_title"]
            text = texts["rem_missed_text"].format(names=_join(meds), tm=times)
        if quiet and core.in_quiet(moment):
            continue
        entries.append({"at": _epoch_ms(moment), "id": "%s|%s" % (kind, moment.strftime("%Y%m%d%H%M")),
                        "kind": kind, "title": title, "text": text})

    if entries:
        end = dt.datetime.combine(first_day + dt.timedelta(days=horizon_days - 1), dt.time(9, 0))
        if end > now:
            entries.append({"at": _epoch_ms(end), "id": "refresh|" + end.strftime("%Y%m%d%H%M"),
                            "kind": "refresh", "title": texts["rem_refresh_title"],
                            "text": texts["rem_refresh_text"]})
        entries.sort(key=lambda e: e["at"])
    plan["alarms"] = entries[:MAX_ENTRIES]
    return plan


def write_plan(directory, plan):
    """Атомарно записывает план. Возвращает True/False."""
    path = os.path.join(directory, PLAN_FILE)
    try:
        os.makedirs(directory, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".alarms-", dir=directory)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        return True
    except Exception as exc:
        print("alarm plan write failed:", exc)
        return False


def beat(directory, foreground, now_ms):
    """Отметка «приложение открыто»: пока она свежая, Java не дублирует окно напоминания уведомлением."""
    try:
        with open(os.path.join(directory, BEAT_FILE), "w", encoding="utf-8") as f:
            f.write(str(int(now_ms) if foreground else 0))
    except OSError as exc:
        print("beat write failed:", exc)
