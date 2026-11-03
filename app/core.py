# -*- coding: utf-8 -*-
"""Хранилище и логика расписания MediCare.

Используется приложением и фоновой службой. Формат medicare.json сохраняется
совместимым с предыдущими версиями приложения.
"""
import os
import json
import datetime as dt
import tempfile
import copy
import shutil


def _store_dir():
    # На Android ANDROID_PRIVATE должен указывать на общий каталог данных
    # приложения и фоновой службы. На компьютере используем ~/.medicare.
    return (
        os.environ.get("MEDICARE_DATA_DIR")
        or
        os.environ.get("ANDROID_PRIVATE")
        or os.path.join(os.path.expanduser("~"), ".medicare")
    )


STORE = os.path.join(_store_dir(), "medicare.json")

DEFAULT = {
    "onboarded": False,
    "lang": "ru",
    "theme": "light",
    "name": "",
    "email": "",
    "notif": {
        "all": True,
        "push": True,
        "sound": True,
        "vib": True,
        "bg": True,
        "quiet": False,
    },
    "meds": [],
    "log": {},  # "YYYY-MM-DD": {"medid|HH:MM": "taken"}
}


def _default_data():
    """Возвращает независимую копию значений по умолчанию."""
    return json.loads(json.dumps(DEFAULT))


def _valid_time(value):
    """True, если время имеет корректный формат HH:MM."""
    if not isinstance(value, str):
        return False
    try:
        dt.time.fromisoformat(value)
        # В расписании поддерживаем именно HH:MM, без секунд и часового пояса.
        return len(value) == 5 and value[2] == ":"
    except (TypeError, ValueError):
        return False


def normalize_med(med):
    """Reject broken identity/schedules and repair optional display fields."""
    if not isinstance(med, dict):
        return None
    med = copy.deepcopy(med)
    if not isinstance(med.get("id"), str) or not med["id"] or "|" in med["id"]:
        return None
    if not isinstance(med.get("name"), str) or not med["name"].strip():
        return None
    try:
        dt.date.fromisoformat(med.get("start"))
    except (TypeError, ValueError):
        return None
    times = med.get("times", [])
    med["times"] = sorted({t for t in times if _valid_time(t)}) if isinstance(times, (list, tuple)) else []
    if not med["times"]:
        return None
    for key in ("dose", "note", "photo"):
        if not isinstance(med.get(key), str):
            med[key] = ""
    if med.get("form") not in ("tablet", "capsule", "syrup", "drops", "injection", "ointment", "powder"):
        med["form"] = "tablet"
    if med.get("how") not in ("after", "before", "during", "any", "sleep"):
        med["how"] = "any"
    try:
        med["days"] = max(0, min(365, int(med.get("days") or 0)))
    except (ValueError, TypeError, OverflowError):
        med["days"] = 0
    if not isinstance(med.get("db"), str):
        med["db"] = None
    return med


def load():
    """Загружает данные; повреждённый JSON сохраняется рядом как .bak."""
    try:
        with open(STORE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if not isinstance(loaded, dict):
            raise ValueError("bad data format")
        data = loaded
    except FileNotFoundError:
        data = {}
    except Exception as exc:
        print("load error:", exc)
        data = {}
        try:
            if os.path.exists(STORE):
                backup = STORE + ".bak"
                # Не перезаписываем предыдущую резервную копию.
                if os.path.exists(backup):
                    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
                    backup = STORE + "." + stamp + ".bak"
                os.replace(STORE, backup)
        except Exception as backup_exc:
            print("backup error:", backup_exc)

    result = _default_data()

    # Сначала применяем известные верхнеуровневые значения из сохранённого файла.
    result.update(data)

    # Настройки уведомлений дополняются новыми значениями по умолчанию.
    notif = dict(DEFAULT["notif"])
    saved_notif = data.get("notif")
    if isinstance(saved_notif, dict):
        notif.update(saved_notif)
    result["notif"] = notif

    # Не позволяем повреждённым разделам ломать интерфейс.
    if not isinstance(result.get("meds"), list):
        result["meds"] = []
    else:
        repaired = []
        seen = set()
        for item in result["meds"]:
            med = normalize_med(item)
            if med and med["id"] not in seen:
                repaired.append(med)
                seen.add(med["id"])
        if repaired != result["meds"] and os.path.isfile(STORE):
            # Preserve the first pre-repair document before a later UI save.
            backup = STORE + ".recovery.bak"
            if not os.path.exists(backup):
                try:
                    shutil.copy2(STORE, backup)
                except OSError as exc:
                    print("recovery backup error:", exc)
        result["meds"] = repaired

    if not isinstance(result.get("log"), dict):
        result["log"] = {}
    else:
        # Оставляем только даты с объектами записей.
        result["log"] = {
            day: entries
            for day, entries in result["log"].items()
            if isinstance(day, str) and isinstance(entries, dict)
        }

    if not isinstance(result.get("lang"), str) or not result["lang"]:
        result["lang"] = DEFAULT["lang"]
    if not isinstance(result.get("theme"), str) or not result["theme"]:
        result["theme"] = DEFAULT["theme"]
    if not isinstance(result.get("name"), str):
        result["name"] = ""
    if not isinstance(result.get("email"), str):
        result["email"] = ""
    result["onboarded"] = bool(result.get("onboarded", False))
    for key, default in DEFAULT["notif"].items():
        value = result["notif"].get(key)
        result["notif"][key] = value if isinstance(value, bool) else default

    return result


def save(data):
    """Атомарно сохраняет данные и возвращает True/False."""
    if not isinstance(data, dict):
        print("save error: data must be a dictionary")
        return False

    directory = os.path.dirname(STORE) or "."
    temp_path = None
    try:
        os.makedirs(directory, exist_ok=True)

        # Временный файл создаётся в том же каталоге, чтобы os.replace()
        # оставался атомарным на файловой системе назначения.
        fd, temp_path = tempfile.mkstemp(
            prefix=".medicare-",
            suffix=".tmp",
            dir=directory,
        )
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, STORE)
        temp_path = None
        return True
    except Exception as exc:
        print("save error:", exc)
        return False
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass


def doses_for(data, day):
    """Возвращает список (время, лекарство) на дату, отсортированный по времени."""
    out = []
    if not isinstance(data, dict) or not isinstance(day, dt.date):
        return out

    meds = data.get("meds", [])
    if not isinstance(meds, list):
        return out

    for med in meds:
        if not isinstance(med, dict):
            continue

        try:
            start_value = med.get("start")
            start = dt.date.fromisoformat(start_value)
        except (TypeError, ValueError):
            continue

        if day < start:
            continue

        try:
            days = int(med.get("days") or 0)
        except (TypeError, ValueError, OverflowError):
            days = 0

        if days > 0 and day >= start + dt.timedelta(days=days):
            continue

        times = med.get("times", [])
        if not isinstance(times, (list, tuple)):
            continue

        for tm in dict.fromkeys(t for t in times if isinstance(t, str)):
            if _valid_time(tm):
                out.append((tm, med))

    out.sort(key=lambda item: item[0])
    return out


def key_of(m, tm):
    """Создаёт стабильный ключ для лекарства и времени приёма."""
    med_id = m.get("id", "") if isinstance(m, dict) else ""
    return "%s|%s" % (med_id, tm)


def is_taken(data, day, m, tm):
    """Проверяет, отмечена ли доза как принятая."""
    if not isinstance(data, dict):
        return False
    log = data.get("log", {})
    if not isinstance(log, dict):
        return False
    day_log = log.get(day.isoformat(), {})
    if not isinstance(day_log, dict):
        return False
    return day_log.get(key_of(m, tm)) == "taken"


def status(data, day, m, tm, now):
    """Возвращает 'taken', 'missed' (прошёл час) или 'pending'."""
    if is_taken(data, day, m, tm):
        return "taken"

    if not _valid_time(tm):
        return "pending"

    try:
        hour, minute = int(tm[:2]), int(tm[3:5])
        due = dt.datetime.combine(day, dt.time(hour, minute))

        # Если одно из значений timezone-aware, приводим due к часовому поясу now.
        if now.tzinfo is not None and now.utcoffset() is not None:
            due = due.replace(tzinfo=now.tzinfo)
        elif due.tzinfo is not None:
            now = now.replace(tzinfo=due.tzinfo)
    except (TypeError, ValueError, AttributeError):
        return "pending"

    try:
        return "missed" if now > due + dt.timedelta(hours=1) else "pending"
    except TypeError:
        # Например, если передали несовместимые naive/aware даты.
        return "pending"


# Пожилые люди часто принимают лекарство чуть раньше. Если не дать отметить
# такой приём, в назначенное время придёт напоминание и человек может выпить
# дозу второй раз. Поэтому отметка доступна за EARLY_MINUTES до времени приёма.
EARLY_MINUTES = 60


def can_mark_taken(day, tm, now=None):
    """Разрешает отметить дозу не раньше чем за EARLY_MINUTES до её времени.

    Прошлые дозы можно отметить задним числом; будущую дату — нельзя.
    """
    if not isinstance(day, dt.date) or not _valid_time(tm):
        return False
    now = now or dt.datetime.now()
    if day < now.date():
        return True
    if day > now.date():
        return False
    try:
        hour, minute = int(tm[:2]), int(tm[3:5])
        due = dt.datetime.combine(day, dt.time(hour, minute))
        if now.tzinfo is not None and now.utcoffset() is not None:
            due = due.replace(tzinfo=now.tzinfo)
        return now >= due - dt.timedelta(minutes=EARLY_MINUTES)
    except (TypeError, ValueError, AttributeError):
        return False


def toggle(data, day, m, tm, now=None):
    """Переключает отметку; новую отметку блокирует до времени приёма."""
    if not isinstance(data, dict) or not isinstance(day, dt.date) or not _valid_time(tm):
        return False
    if not is_taken(data, day, m, tm) and not can_mark_taken(day, tm, now):
        return False

    log = data.setdefault("log", {})
    if not isinstance(log, dict):
        log = {}
        data["log"] = log

    day_key = day.isoformat()
    day_log = log.setdefault(day_key, {})
    if not isinstance(day_log, dict):
        day_log = {}
        log[day_key] = day_log

    key = key_of(m, tm)
    if day_log.get(key) == "taken":
        day_log.pop(key, None)
        if not day_log:
            log.pop(day_key, None)
        return False

    if not can_mark_taken(day, tm, now):
        return False

    day_log[key] = "taken"
    return True


def set_taken(data, day, m, tm, now=None):
    """Отмечает дозу принятой только после наступления её времени."""
    if not isinstance(data, dict) or not can_mark_taken(day, tm, now):
        return False
    log = data.setdefault("log", {})
    if not isinstance(log, dict):
        log = {}
        data["log"] = log
    day_log = log.setdefault(day.isoformat(), {})
    if not isinstance(day_log, dict):
        day_log = {}
        log[day.isoformat()] = day_log
    day_log[key_of(m, tm)] = "taken"
    return True


def in_quiet(now):
    """Тихие часы: с 22:00 до 06:00."""
    return now.hour >= 22 or now.hour < 6


def change_taken(data, day, med, tm, taken=None, now=None):
    """Commit a check-off transaction; never display unsaved success.

    taken=None toggles, True is idempotent, False undoes an existing entry.
    Return 'saved', 'blocked', 'unchanged', or 'error'.
    """
    now = now or dt.datetime.now()
    if not any(t == tm and m.get("id") == med.get("id") for t, m in doses_for(data, day)):
        return "blocked"
    before = is_taken(data, day, med, tm)
    target = not before if taken is None else bool(taken)
    if target == before:
        return "unchanged"
    if target and not can_mark_taken(day, tm, now):
        return "blocked"
    old_log = copy.deepcopy(data.get("log", {}))
    toggle(data, day, med, tm, now)
    if save(data):
        return "saved"
    data["log"] = old_log
    return "error"


def day_mark(data, day, today=None, now=None):
    """Метка дня для календаря: '' (нет приёмов), 'done', 'missed', 'part', 'pending'."""
    today = today or dt.date.today()
    items = doses_for(data, day)
    if not items:
        return ""
    taken = sum(1 for tm, m in items if is_taken(data, day, m, tm))
    if taken == len(items):
        return "done"
    if day < today:
        return "missed"
    if day > today:
        return "pending"
    now = now or dt.datetime.now()
    if any(status(data, day, m, tm, now) == "missed"
           for tm, m in items if not is_taken(data, day, m, tm)):
        return "missed"
    return "part" if taken else "pending"


def adherence(data, today=None):
    """Completed scheduled-day streak; an unfinished today isn't a break yet.

    Unscheduled days don't count or break a streak. Statistics use the current
    medication schedules, not an immutable prescription history.
    """
    today = today or dt.date.today()
    starts = []
    for med in data.get("meds", []):
        try:
            starts.append(dt.date.fromisoformat(med.get("start")))
        except (ValueError, TypeError, AttributeError):
            pass
    if not starts:
        return {"current": 0, "best": 0, "taken": 0, "total": 0}
    # Bound historical work for corrupted or extremely old imported dates.
    day = max(min(starts), today - dt.timedelta(days=3650))
    current = best = taken = total = 0
    while day <= today:
        items = doses_for(data, day)
        count = sum(is_taken(data, day, med, tm) for tm, med in items)
        taken += count
        total += len(items)
        if items and count == len(items):
            current += 1
            best = max(best, current)
        elif items and day < today:
            current = 0
        day += dt.timedelta(days=1)
    return {"current": current, "best": best, "taken": taken, "total": total}
