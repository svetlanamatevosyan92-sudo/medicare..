# -*- coding: utf-8 -*-
"""Хук python-for-android: прописывает приёмники напоминаний в AndroidManifest.xml.

Buildozer не умеет добавлять <receiver> внутрь <application>, поэтому перед сборкой
вставляем их в шаблон манифеста дистрибутива. Идемпотентно: повторный запуск ничего не дублирует.
Подключается строкой  p4a.hook = p4a_hook.py  в buildozer.spec.
"""
import glob
import os

MARKER = "org.medicare.reminder.ReminderReceiver"
RECEIVERS = """
        <receiver android:name="org.medicare.reminder.ReminderReceiver" android:exported="false" />
        <receiver android:name="org.medicare.reminder.BootReceiver" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.intent.action.TIMEZONE_CHANGED" />
                <action android:name="android.intent.action.TIME_SET" />
            </intent-filter>
        </receiver>
"""


def _patch(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if MARKER in text:
        return False
    if "</application>" not in text:
        raise RuntimeError("p4a_hook: в %s нет </application>, формат шаблона изменился" % path)
    text = text.replace("</application>", RECEIVERS + "    </application>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("p4a_hook: приёмники напоминаний добавлены в", path)
    return True


def _templates(toolchain):
    found = []
    try:
        found.append(os.path.join(toolchain._dist.dist_dir, "templates", "AndroidManifest.tmpl.xml"))
    except Exception:
        pass
    found += glob.glob(os.path.join(
        os.getcwd(), ".buildozer", "android", "platform", "build-*", "dists", "*",
        "templates", "AndroidManifest.tmpl.xml"))
    return [p for p in dict.fromkeys(found) if os.path.exists(p)]


def before_apk_build(toolchain):
    _run(toolchain)


def before_apk_assemble(toolchain):
    _run(toolchain)


def _run(toolchain):
    paths = _templates(toolchain)
    if not paths:
        raise RuntimeError("p4a_hook: не найден AndroidManifest.tmpl.xml — приёмники напоминаний не добавлены")
    for path in paths:
        _patch(path)
