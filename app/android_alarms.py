# -*- coding: utf-8 -*-
"""Мост к нативным напоминаниям Android (android_src/org/medicare/reminder).

Работает только на телефоне. На компьютере все функции безопасно ничего не делают.
"""
import importlib

from kivy.utils import platform


def available():
    return platform == "android"


def _core():
    jnius = importlib.import_module("jnius")
    return jnius.autoclass("org.medicare.reminder.ReminderCore")


def _activity():
    jnius = importlib.import_module("jnius")
    return jnius.autoclass("org.kivy.android.PythonActivity").mActivity


def reschedule():
    """Поставить будильник на ближайшую запись нового плана. True — вызов выполнен."""
    if not available():
        return False
    try:
        _core().schedule(_activity())
        return True
    except Exception as exc:
        print("native reminders unavailable:", exc)
        return False


def cancel():
    if not available():
        return False
    try:
        _core().cancel(_activity())
        return True
    except Exception as exc:
        print("native cancel failed:", exc)
        return False


def notifications_allowed():
    """Разрешены ли уведомления в системных настройках. None — не удалось определить."""
    if not available():
        return None
    try:
        jnius = importlib.import_module("jnius")
        ctx = _activity()
        nm = ctx.getSystemService(jnius.autoclass("android.content.Context").NOTIFICATION_SERVICE)
        return bool(nm.areNotificationsEnabled())
    except Exception as exc:
        print("cannot read notification state:", exc)
        return None
