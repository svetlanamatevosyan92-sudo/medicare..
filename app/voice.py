# -*- coding: utf-8 -*-
"""Голосовой ввод и озвучивание ответов.

Android: системное распознавание речи (RecognizerIntent) — без ключей и без
отправки аудио на наш сервер. Нужна установленная служба распознавания Google;
поддержка армянского зависит от устройства.
Компьютер: голосового ввода нет (используйте текстовое поле).
"""
import importlib

from kivy.utils import platform

_REQ_CODE = 7321
_LOCALES = {"ru": "ru-RU", "en": "en-US", "hy": "hy-AM"}
_pending = {"cb": None, "bound": False}


def available():
    return platform == "android"


def listen(lang, on_text, on_fail):
    """Запускает системное окно распознавания речи.

    on_text(str) / on_fail(str) вызываются в основном потоке Kivy.
    """
    if platform != "android":
        on_fail("unavailable")
        return
    try:
        activity_mod = importlib.import_module("android.activity")
        jnius = importlib.import_module("jnius")
        autoclass = jnius.autoclass
        Intent = autoclass("android.content.Intent")
        RecognizerIntent = autoclass("android.speech.RecognizerIntent")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        def on_result(request_code, result_code, intent):
            if request_code != _REQ_CODE:
                return
            from kivy.clock import Clock
            text = ""
            try:
                if result_code == -1 and intent is not None:  # RESULT_OK
                    items = intent.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                    if items is not None and items.size() > 0:
                        text = str(items.get(0))
            except Exception:
                text = ""
            cb = _pending["cb"]
            _pending["cb"] = None
            if cb:
                Clock.schedule_once(lambda *_: cb(text), 0)

        _pending["cb"] = lambda text: on_text(text) if text else on_fail("empty")
        if not _pending["bound"]:
            activity_mod.bind(on_activity_result=on_result)
            _pending["bound"] = True

        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                        RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, _LOCALES.get(lang, "ru-RU"))
        intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
        PythonActivity.mActivity.startActivityForResult(intent, _REQ_CODE)
    except Exception as exc:  # нет службы распознавания, нет jnius и т.п.
        print("voice error:", exc)
        _pending["cb"] = None
        on_fail("error")


def speak(text, lang=None):
    """Озвучивает ответ (если есть TTS). Ошибки не критичны.

    Язык озвучки определяется системным движком телефона (plyer не позволяет его задать);
    армянский голос есть не на всех телефонах — тогда текст просто остаётся на экране.
    """
    if not text:
        return
    try:
        from plyer import tts
        tts.speak(text)
    except Exception as exc:
        print("tts unavailable:", exc)
