[app]
title = MediCare
package.name = medicare
package.domain = org.medicare
source.dir = .
source.include_exts = py,png,kv,wav,ttf
source.exclude_dirs = tests_app,tools,bin,.buildozer,.github,android_src,__pycache__
source.exclude_patterns = p4a_hook.py,*.md,*.spec
version = 1.0.0
entry_point = main.py

# Версии привязаны к тем, под которые написан код (см. requirements.txt).
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,plyer,certifi,pyjnius,android

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
presplash.color = #F6F8F9

# INTERNET — связь с сервером помощника; POST_NOTIFICATIONS — уведомления (Android 13+);
# VIBRATE — вибрация напоминания; RECEIVE_BOOT_COMPLETED — вернуть напоминания после перезагрузки.
# RECORD_AUDIO не нужен: распознавание речи делает системная служба Google в своём окне.
android.permissions = INTERNET,POST_NOTIFICATIONS,VIBRATE,RECEIVE_BOOT_COMPLETED

android.api = 34
android.minapi = 26
android.ndk = 25b
# Только 64-бит: все современные телефоны, сборка вдвое быстрее и APK меньше.
# Для очень старых телефонов верните:  arm64-v8a, armeabi-v7a
android.archs = arm64-v8a
android.accept_sdk_license = True

# Данные не должны попадать в облачные и adb-копии (там расписание и медицинские сведения).
android.allow_backup = False
android.release_artifact = apk

# Нативные напоминания (Java) и регистрация их приёмников в манифесте.
android.add_src = android_src
p4a.hook = p4a_hook.py

[buildozer]
log_level = 2
warn_on_root = 1
