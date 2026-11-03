# -*- coding: utf-8 -*-
"""Safe Area для Android: отступы под строку состояния, вырез камеры и панель навигации.

Начиная с Android 15 (при targetSdk >= 35) приложения рисуются ПОД системными панелями
(edge-to-edge). Kivy/SDL про это не знает, поэтому верх экрана оказывался под статус-баром.
Здесь мы читаем реальные отступы у системы, а в screens.kv добавляем их как padding корня.
На старых версиях Android система сама оставляет место под панелями — отступы равны 0.
"""
from kivy.utils import platform


def get_insets():
    """(left, top, right, bottom) в пикселях. None — окно ещё не готово, повторите позже."""
    if platform != "android":
        return (0, 0, 0, 0)
    try:
        from jnius import autoclass
        activity = autoclass("org.kivy.android.PythonActivity").mActivity
        sdk = autoclass("android.os.Build$VERSION").SDK_INT
        target = activity.getApplicationInfo().targetSdkVersion
        if sdk < 35 or target < 35:
            return (0, 0, 0, 0)            # система сама не даёт заходить под панели
        root = activity.getWindow().getDecorView().getRootWindowInsets()
        if root is None:
            return None
        Type = autoclass("android.view.WindowInsets$Type")
        ins = root.getInsets(Type.systemBars() | Type.displayCutout())
        return (int(ins.left), int(ins.top), int(ins.right), int(ins.bottom))
    except Exception as exc:
        print("insets error:", exc)
        return (0, 0, 0, 0)


def set_light_bars(light):
    """Цвет значков строки состояния/навигации: тёмные на светлой теме, светлые на тёмной."""
    if platform != "android":
        return
    try:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass

        @run_on_ui_thread
        def apply():
            try:
                activity = autoclass("org.kivy.android.PythonActivity").mActivity
                if autoclass("android.os.Build$VERSION").SDK_INT < 30:
                    return
                controller = activity.getWindow().getInsetsController()
                if controller is None:
                    return
                mask = 8 | 16                     # LIGHT_STATUS_BARS | LIGHT_NAVIGATION_BARS
                controller.setSystemBarsAppearance(mask if light else 0, mask)
            except Exception as exc:
                print("system bars error:", exc)

        apply()
    except Exception as exc:
        print("system bars error:", exc)
