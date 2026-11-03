# -*- coding: utf-8 -*-
"""Проверка расписания: предупреждения до того, как человек что-то перепутает.

Это НЕ диагностика и НЕ замена врача или фармацевта. Проверки намеренно простые и осторожные,
каждая — общеизвестное правило для небольшого набора препаратов из справочника drugs.py.
Любое правило перед выпуском нужно сверить с врачом/фармацевтом (см. README, раздел про
медицинскую безопасность). Незнакомые лекарства проверяются только на дубликаты и «тесноту».

Без Kivy: модуль тестируется отдельно (tests_app/test_schedule_check.py).
"""
import datetime as dt

import drugs as DR

# Обычный максимум суточной дозы (мг) для безрецептурного применения.
MAX_DAILY_MG = {
    "paracetamol": 4000, "ibuprofen": 1200, "aspirin": 3000,
    "melatonin": 5, "loratadine": 10, "cetirizine": 10, "magnesium": 350,
}

# Минимальный промежуток между приёмами (часы) — по текстам справочника drugs.py.
MIN_INTERVAL_H = {"paracetamol": 4, "ibuprofen": 6, "aspirin": 4}

# Группы препаратов одного действия: вместе обычно не принимают без назначения врача.
CLASS_GROUPS = (
    ("class_nsaid", frozenset({"ibuprofen", "aspirin"})),
    ("class_antihistamine", frozenset({"loratadine", "cetirizine"})),
)

CROWDED_AT_ONCE = 4          # столько лекарств в одну минуту — «тесно»

QUIET_START, QUIET_END = 22, 6   # как в core.in_quiet()

_MSG = {
    "ru": {
        "dup_drug": "«{names}» несколько раз в списке. Проверьте, не получится ли двойной приём.",
        "class_nsaid": "{names}: оба противовоспалительные. Вместе они повышают риск проблем с желудком. "
                       "Обсудите это с врачом или фармацевтом.",
        "class_antihistamine": "{names}: два средства от аллергии одного типа. Обычно их не принимают вместе. "
                               "Спросите врача или фармацевта.",
        "too_close": "{names}: приёмы слишком близко (до {hours} ч между ними). Обычно нужно не меньше {min} ч. "
                     "Сверьтесь с инструкцией или врачом.",
        "daily_limit": "{names}: за сутки выходит {tot} мг, обычный предел без назначения врача — {mx} мг. "
                       "Уточните у врача.",
        "crowded": "В {tm} назначено сразу {n} лекарств. Спросите фармацевта, можно ли разнести их по времени.",
        "quiet": "Приём «{names}» в {tm} попадает на тихие часы (22:00–06:00): напоминание не прозвучит. "
                 "Выключите тихий режим или перенесите время.",
        "ok": "Проблем в расписании не нашлось. Это простая проверка: вопросы о лекарствах всё равно "
              "обсуждайте с врачом или фармацевтом.",
    },
    "en": {
        "dup_drug": "“{names}” is in the list more than once. Check that you will not take a double dose.",
        "class_nsaid": "{names}: both are anti-inflammatory drugs. Together they raise the risk of stomach "
                       "problems. Please discuss it with a doctor or pharmacist.",
        "class_antihistamine": "{names}: two allergy medicines of the same type. They are usually not taken "
                               "together. Ask a doctor or pharmacist.",
        "too_close": "{names}: doses are too close together (as little as {hours} h apart). Usually at least "
                     "{min} h is needed. Check the leaflet or ask a doctor.",
        "daily_limit": "{names}: this adds up to {tot} mg a day; the usual limit without a prescription is "
                       "{mx} mg. Please check with a doctor.",
        "crowded": "{n} medicines are scheduled at {tm}. Ask a pharmacist whether they can be spread out.",
        "quiet": "The dose of “{names}” at {tm} falls in quiet hours (22:00–06:00): the reminder will not "
                 "sound. Turn quiet mode off or change the time.",
        "ok": "No problems found in the schedule. This is a simple check: still discuss any medicine "
              "questions with a doctor or pharmacist.",
    },
    "hy": {
        "dup_drug": "«{names}» դեղը ցանկում մի քանի անգամ է։ Ստուգեք՝ կրկնակի ընդունում չի՞ ստացվի։",
        "class_nsaid": "{names}՝ երկուսն էլ հակաբորբոքային դեղեր են։ Միասին մեծացնում են ստամոքսի խնդիրների "
                       "վտանգը։ Քննարկեք բժշկի կամ դեղագործի հետ։",
        "class_antihistamine": "{names}՝ ալերգիայի երկու նույն տիպի դեղ։ Սովորաբար դրանք միասին չեն "
                               "ընդունում։ Հարցրեք բժշկին կամ դեղագործին։",
        "too_close": "{names}՝ ընդունումները շատ մոտ են ({hours} ժ-ից պակաս)։ Սովորաբար պետք է առնվազն "
                     "{min} ժ։ Ստուգեք հրահանգը կամ հարցրեք բժշկին։",
        "daily_limit": "{names}՝ օրական ստացվում է {tot} մգ, առանց բժշկի նշանակման սովորական սահմանը {mx} մգ է։ "
                       "Հարցրեք բժշկին։",
        "crowded": "{tm}-ին միանգամից {n} դեղ է նշանակված։ Հարցրեք դեղագործին՝ կարելի՞ է դրանք բաժանել "
                   "տարբեր ժամերի։",
        "quiet": "«{names}» դեղի {tm}-ի ընդունումն ընկնում է լռության ժամերին (22:00–06:00)՝ հիշեցումը "
                 "չի հնչի։ Անջատեք լռության ռեժիմը կամ փոխեք ժամը։",
        "ok": "Ժամանակացույցում խնդիր չի գտնվել։ Սա պարզ ստուգում է. դեղերի հարցերը միևնույն է քննարկեք "
              "բժշկի կամ դեղագործի հետ։",
    },
}


# Самые распространённые обиходные и торговые названия. Без них «Аспирин» (так пишет почти
# каждый) не совпал бы с записью справочника «Ацетилсалициловая кислота».
ALIASES = {
    "aspirin": ("аспирин", "aspirin", "ասպիրին", "тромбо асс", "кардиомагнил"),
    "paracetamol": ("панадол", "panadol", "эффералган", "efferalgan", "тайленол", "tylenol"),
    "ibuprofen": ("нурофен", "nurofen", "advil", "адвил", "миг 200", "իբուպրոֆեն"),
    "loratadine": ("кларитин", "claritin", "лоратадин"),
    "cetirizine": ("зиртек", "zyrtec", "цетрин", "cetrin"),
    "metformin": ("глюкофаж", "glucophage", "сиофор", "siofor"),
    "omeprazole": ("омез", "omez", "losec", "prilosec"),
    "amlodipine": ("норваск", "norvasc", "нормодипин"),
    "salbutamol": ("вентолин", "ventolin"),
    "ors": ("регидрон", "regidron"),
    "melatonin": ("мелаксен", "melaxen"),
}


def _lookup():
    names = {}
    for d in DR.DRUGS:
        for n in d["name"].values():
            names[n.casefold()] = d["key"]
    for key, aliases in ALIASES.items():
        for a in aliases:
            names[a.casefold()] = key
    return names


_NAME_TO_KEY = _lookup()
_KEYS = {d["key"] for d in DR.DRUGS}


def drug_key(med):
    """Ключ справочника для лекарства или None, если оно незнакомо."""
    key = med.get("db")
    if isinstance(key, str) and key in _KEYS:
        return key
    return key_for_name(med.get("name", ""))


def key_for_name(name):
    """Ключ справочника по названию (на любом из трёх языков, с торговыми названиями) или None."""
    name = str(name or "").strip().casefold()
    if name in _NAME_TO_KEY:
        return _NAME_TO_KEY[name]
    # «Аспирин Кардио», «Нурофен Экспресс»: торговое название с добавкой
    for alias, key in _NAME_TO_KEY.items():
        if len(alias) >= 5 and name.startswith(alias + " "):
            return key
    return None


def _active(med, today):
    try:
        start = dt.date.fromisoformat(med.get("start"))
        days = int(med.get("days") or 0)
    except (TypeError, ValueError):
        return False
    if today < start:
        return True            # курс ещё не начался, но уже запланирован — проверять нужно
    return not (days > 0 and today >= start + dt.timedelta(days=days))


def _minutes(tm):
    return int(tm[:2]) * 60 + int(tm[3:5])


def _min_gap_hours(times):
    """Наименьший промежуток (часы) между соседними приёмами за сутки, с переходом через полночь."""
    mins = sorted({_minutes(t) for t in times})
    if len(mins) < 2:
        return None
    gaps = [b - a for a, b in zip(mins, mins[1:])] + [mins[0] + 1440 - mins[-1]]
    return min(gaps) / 60.0


def _fmt_hours(value):
    value = round(value * 2) / 2.0
    return str(int(value)) if value == int(value) else str(value)


def _finding(code, severity, meds, **extra):
    return {"code": code, "severity": severity, "ids": sorted({m["id"] for m in meds}),
            "names": sorted({m["name"] for m in meds}, key=str.casefold), **extra}


def analyze(meds, today=None, quiet=False):
    """Возвращает список находок (словари). Сначала самые важные (severity 'warn')."""
    today = today or dt.date.today()
    meds = [m for m in meds if isinstance(m, dict) and m.get("id") and m.get("name")
            and isinstance(m.get("times"), list) and _active(m, today)]
    out = []

    groups = {}
    for m in meds:
        groups.setdefault(drug_key(m) or "name:" + m["name"].strip().casefold(), []).append(m)

    for key, items in groups.items():
        if len(items) > 1:
            out.append(_finding("dup_drug", "warn", items))
        gap_limit = MIN_INTERVAL_H.get(key)
        if gap_limit:
            times = [t for m in items for t in m["times"] if isinstance(t, str) and len(t) == 5]
            gap = _min_gap_hours(times)
            if gap is not None and gap < gap_limit:
                out.append(_finding("too_close", "warn", items, hours=_fmt_hours(gap), min=gap_limit))

    present = {k for k in groups if not k.startswith("name:")}
    for code, members in CLASS_GROUPS:
        hit = sorted(present & members)
        if len(hit) > 1:
            out.append(_finding(code, "warn", [m for k in hit for m in groups[k]]))

    for key, items in groups.items():
        limit = MAX_DAILY_MG.get(key)
        if not limit:
            continue
        total = 0.0
        for m in items:
            part = DR.daily_total_mg({"dose": m.get("dose", ""), "times": m["times"]})
            total += part or 0
        if total > limit:
            out.append(_finding("daily_limit", "warn", items, tot=int(total), mx=int(limit)))

    by_time = {}
    for m in meds:
        for t in {t for t in m["times"] if isinstance(t, str) and len(t) == 5 and t[2] == ":"}:
            by_time.setdefault(t, []).append(m)
    for t, items in sorted(by_time.items()):
        if len(items) >= CROWDED_AT_ONCE:
            out.append(_finding("crowded", "info", items, tm=t, n=len(items)))
        if quiet and (int(t[:2]) >= QUIET_START or int(t[:2]) < QUIET_END):
            out.append(_finding("quiet", "warn", items, tm=t))

    out.sort(key=lambda f: (f["severity"] != "warn", f["code"], f["names"]))
    return out


def for_medication(findings, med_id):
    """Только находки, в которых участвует конкретное лекарство (например, только что добавленное)."""
    return [f for f in findings if med_id in f["ids"]]


def render(finding, lang="ru"):
    table = _MSG.get(lang) or _MSG["en"]
    template = table.get(finding["code"]) or _MSG["en"][finding["code"]]
    params = {k: v for k, v in finding.items() if k not in ("code", "severity", "ids", "names")}
    params["names"] = ", ".join(finding["names"])
    return template.format(**params)


def render_all(findings, lang="ru"):
    """Текст для чата или озвучивания: нумерованные пункты или сообщение «всё в порядке»."""
    if not findings:
        return (_MSG.get(lang) or _MSG["en"])["ok"]
    return "\n".join("%d. %s" % (i, render(f, lang)) for i, f in enumerate(findings, 1))
