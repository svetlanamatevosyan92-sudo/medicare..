# -*- coding: utf-8 -*-
"""Офлайн-страховка: распознаёт описание неотложного состояния БЕЗ интернета и без ИИ.

Список шаблонов должен совпадать с backend/app/logic.py (EMERGENCY_PATTERNS) — это проверяет
tests_app/test_safety.py. Шаблоны намеренно осторожные: лишнее предупреждение лучше пропущенного.
Армянские фразы нужно проверить носителем языка и врачом.
"""
import re

EMERGENCY_PATTERNS = [
    'бол[ьи]\\w* (в|за) груд',
    'давит\\w* (в|на) груд',
    'давлени\\w* в груд',
    '(не могу|трудно|тяжело|нечем) дыша',
    'задыха',
    'удушь',
    'теря\\w* сознани',
    'потерял\\w* сознани',
    'без сознани',
    'упал\\w* в обморок',
    'онем\\w* (рук|нога|ног|лиц|полов|сторон)',
    'перекос\\w* лиц',
    'лицо перекос',
    '(речь|язык) (наруш|заплета)',
    'не могу говорить',
    'сильн\\w* кровотечени',
    'кровь не останавлива',
    'припадок',
    'эпилептическ',
    'судорог\\w* (по всему|во всём|во всем|всего|тела)',
    'отёк\\w* (лиц|горл|язык|губ)',
    'отек\\w* (лиц|горл|язык|губ)',
    'язык распух',
    'передозиров',
    'выпил\\w* (слишком много|целую пачку|всю пачку)',
    'хочу умереть',
    'не хочу жить',
    'покончить с собой',
    'суицид',
    'причинить себе вред',
    'chest (pain|pressure|tightness)',
    'pain in (my )?chest',
    "(can'?t|cannot|can not|unable to) breathe",
    'hard to breathe',
    'difficulty breathing',
    '(fainted|passed out|lost consciousness|unconscious)',
    '\\bstroke\\b',
    '(face|arm|leg) (is )?(droop|numb)',
    'numb(ness)? (on|in) (one|my) (side|arm|leg|face)',
    'slurred speech',
    "can'?t speak",
    'seizure',
    'convulsion',
    '(severe|heavy) bleeding',
    "won'?t stop bleeding",
    'overdos',
    'swell\\w* (of|in) (my )?(face|throat|tongue|lips)',
    '(face|throat|tongue|lips) (is |are )?swell',
    'anaphyla',
    'want to die',
    'kill myself',
    'end my life',
    'suicid',
    'hurt myself',
    'կրծքավանդակ\\w* ցավ',
    'ցավ\\w* կրծք',
    'չեմ կարող շնչել',
    'շնչել դժվար',
    'ուշագնաց',
    'գիտակցությունս կորց',
    'ինքնասպան',
    'ուզում եմ մեռնել',
]

_RE = re.compile("|".join("(?:%s)" % p for p in EMERGENCY_PATTERNS), re.IGNORECASE | re.UNICODE)


def is_emergency(text):
    """True, если текст похож на описание неотложного состояния."""
    return isinstance(text, str) and _RE.search(text) is not None
