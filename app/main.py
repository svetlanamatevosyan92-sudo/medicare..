# -*- coding: utf-8 -*-
"""MediCare — напоминания о приёме лекарств (Kivy + KivyMD 1.2.0)."""

import os
import sys
import uuid
import datetime as dt
import shutil
import importlib
import threading
import time

# Настройки окна и ввода — ДО импорта остальных модулей kivy
from kivy.config import Config
Config.set("graphics", "width", "390")
Config.set("graphics", "height", "720")
Config.set("graphics", "resizable", "1")
Config.set("input", "mouse", "mouse,disable_multitouch")

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.utils import platform, get_color_from_hex as hx
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    DictProperty, StringProperty, BooleanProperty, ColorProperty,
    ObjectProperty, NumericProperty, ListProperty
)
from kivy.factory import Factory
from kivy.graphics.texture import Texture
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.toast import toast as native_toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.scrollview import MDScrollView

import core
import data as D
import drugs as DR
import assistant as AS
import voice
import safety
import schedule_check as SC
import voice_commands as VC
import alarm_plan as AP
import insets
import android_alarms as AL
from reminders import ReminderScheduler


# ---- Шрифт с кириллицей и армянским -----------------------------------------

_F = os.path.join(BASE, "fonts", "DejaVuSans.ttf")
_FB = os.path.join(BASE, "fonts", "DejaVuSans-Bold.ttf")

if not os.path.exists(_F):
    from kivy.resources import resource_find
    _F = resource_find("data/fonts/DejaVuSans.ttf") or _F

if os.path.exists(_F):
    for _n in ("Roboto", "RobotoLight", "RobotoMedium", "RobotoThin", "RobotoBlack"):
        LabelBase.register(
            name=_n,
            fn_regular=_F,
            fn_bold=_FB if os.path.exists(_FB) else _F
        )


TABS = ("home", "schedule", "meds", "profile")

# Цвета подобраны так, чтобы основной текст имел контраст не ниже 4.5:1 (WCAG 2.x, AA)
THEMES = {
    # Один акцентный цвет (бирюзовый), остальное — спокойные нейтральные тона.
    # Контраст основного текста и текста на кнопках — не ниже 4.5:1 (WCAG AA).
    "light": dict(
        style="Light", bg="#F6F8F9", card="#FFFFFF",
        text="#12202B", sub="#566774", primary="#0E6F78",
        on_primary="#FFFFFF", accent="#0E6F78", soft="#E8F1F2", line="#E1E8EB",
        ok="#1B7F54", err="#C0392B",
        grad=("#F6F8F9", "#F6F8F9", "#F6F8F9")
    ),
    "dark": dict(
        style="Dark", bg="#0E1417", card="#162026",
        text="#E8EEF1", sub="#9FB0BB", primary="#5CC8D0",
        on_primary="#06262A", accent="#5CC8D0", soft="#1F2B32", line="#26333B",
        ok="#4CC38A", err="#F28B82",
        grad=("#0E1417", "#0E1417", "#0E1417")
    ),
}

CHIPS = {
    "morning": [1.00, 0.91, 0.80, 1],
    "day": [0.84, 0.91, 0.98, 1],
    "evening": [0.99, 0.87, 0.90, 1],
    "night": [0.88, 0.86, 0.98, 1],
}

CHIP_ICONS = {
    "morning": "white-balance-sunny",
    "day": "weather-partly-cloudy",
    "evening": "weather-sunset",
    "night": "weather-night",
}

# Обычный максимум суточной дозы (мг) для безрецептурного применения.
MAX_MG = SC.MAX_DAILY_MG

_UNITS = {
    "ru": (("mg", "мг"), ("mcg", "мкг"), ("IU", "МЕ"), ("sachet", "пакет")),
    "hy": (("mg", "մգ"), ("mcg", "մկգ"), ("IU", "ՄՄ"), ("sachet", "տոպրակ")),
}


def _tr_unit(text, lang):
    for a, b in _UNITS.get(lang, ()):
        text = text.replace(a, b)
    return text


def _adapt(d):
    """Приводит запись справочника к формату встроенной базы лекарств."""
    ds = d["dose_short"]
    return {
        "key": d["key"],
        "name": d["name"],
        "dose": {l: _tr_unit(ds, l) for l in ("ru", "en", "hy")},
        "form": d["form"], "how": d["how"],
        "times": list(d["times"]), "days": d["days"],
        "purpose": d["use"],
        # Всегда используем одинаковую структуру для всех языков.
        # В DRUGS сейчас нет полных армянских инструкций, поэтому для hy
        # оставляем английский fallback до добавления проверенного перевода.
        "instr": {
            lang: "\n".join(
                "• " + (d[key].get(lang) or d[key].get("en") or d[key].get("ru") or "")
                for key in ("dose", "max", "avoid", "inter")
                if d[key].get(lang) or d[key].get("en") or d[key].get("ru")
            )
            for lang in ("ru", "en", "hy")
        },
    }


for _d in DR.DRUGS:
    if _d["key"] not in D.MEDDB:
        _e = _adapt(_d)
        D.MEDDB[_e["key"]] = _e
        D.MEDLIST.append(_e)


def make_gradient(stops):
    """Вертикальный градиент: stops — цвета сверху вниз (hex)."""
    n = 96
    cols = [hx(s) for s in stops]
    seg = len(cols) - 1
    buf = bytearray()
    for i in range(n):                      # строка 0 — нижняя
        t = 1.0 - i / float(n - 1)          # 0 — верх, 1 — низ
        pos = t * seg
        k = min(int(pos), seg - 1)
        f = pos - k
        a, b = cols[k], cols[k + 1]
        for ch in range(3):
            buf.append(int(255 * (a[ch] + (b[ch] - a[ch]) * f)))
        buf.append(255)
    tex = Texture.create(size=(1, n), colorfmt="rgba")
    tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
    tex.mag_filter = "linear"
    tex.min_filter = "linear"
    return tex


# ---- Виджеты ---------------------------------------------------------------

class Row(MDCard):
    icon = StringProperty("pill")
    text = StringProperty("")
    sub = StringProperty("")
    value = StringProperty("")
    tint = ColorProperty([0.25, 0.4, 0.5, 1])


class DoseRow(MDBoxLayout):
    time = StringProperty("")
    chip_icon = StringProperty("white-balance-sunny")
    period = StringProperty("")
    title = StringProperty("")
    sub = StringProperty("")
    state = StringProperty("pending")   # pending / taken / missed
    chip = ColorProperty([1, 1, 1, 1])

    __events__ = ("on_open", "on_toggle")

    def on_open(self, *args):
        pass

    def on_toggle(self, *args):
        pass


class IconBadge(MDCard):
    """Круглая иконка. Не перехватывает нажатия: иначе строка списка не срабатывала
    при нажатии на иконку (MDCard сам обрабатывает касания)."""
    icon = StringProperty("pill")
    bg = ColorProperty([0.9, 0.94, 0.98, 1])
    fg = ColorProperty([0.2, 0.45, 0.85, 1])

    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False


class DayCell(ButtonBehavior, MDBoxLayout):
    wd = StringProperty("")
    num = StringProperty("")
    sel = BooleanProperty(False)
    mark = StringProperty("")      # "", done, missed, part, pending
    today = BooleanProperty(False)


class NavItem(ButtonBehavior, MDBoxLayout):
    icon = StringProperty("home")
    text = StringProperty("")
    target = StringProperty("home")


class TimeChip(MDCard):
    text = StringProperty("")


class DrugRow(MDCard):
    title = StringProperty("")
    sub = StringProperty("")
    who = BooleanProperty(False)


class Flag(Widget):
    kind = StringProperty("ru")


class Bar(Widget):
    pct = NumericProperty(0)


class Badge(MDCard):
    text = StringProperty("")
    bg = ColorProperty([0.9, 0.94, 0.98, 1])
    fg = ColorProperty([0.1, 0.2, 0.3, 1])


class Bubble(MDCard):
    """Сообщение в чате с помощником."""
    text = StringProperty("")
    mine = BooleanProperty(False)
    alert = BooleanProperty(False)


class DosePopup(ModalView):
    title = StringProperty("")
    med = StringProperty("")
    sub = StringProperty("")
    cb_take = ObjectProperty(None, allownone=True)
    cb_snooze = ObjectProperty(None, allownone=True)


class EarlyNotice(ModalView):
    """Ненавязчивое уведомление внизу экрана вместо системного toast."""
    message = StringProperty("")

    def __init__(self, message="", warning=True, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.size_hint = (0.92, None)
        self.height = dp(66)
        self.auto_dismiss = True
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0)
        self.pos_hint = {"center_x": 0.5, "y": 0.035}

        card = MDCard(
            orientation="horizontal",
            size_hint=(1, 1),
            padding=(dp(14), dp(8)),
            spacing=dp(10),
            radius=[dp(18)],
            md_bg_color=MDApp.get_running_app().c_card,
            line_color=MDApp.get_running_app().c_err if warning else MDApp.get_running_app().c_line,
            line_width=1,
            elevation=0,
        )
        icon = MDLabel(
            text="clock-alert-outline",
            font_name="Roboto",
            size_hint=(None, 1),
            width=dp(28),
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().c_err if warning else MDApp.get_running_app().c_accent,
        )
        # Use a standard text label for consistent rendering across KivyMD versions.
        icon.text = "!" if warning else "i"
        icon.bold = True
        icon.font_size = "22sp"
        label = MDLabel(
            text=message,
            size_hint=(1, 1),
            halign="left",
            valign="middle",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().c_text,
        )
        label.bind(size=lambda w, *_: setattr(w, "text_size", (w.width, None)))
        label.bind(texture_size=lambda _w, size: setattr(self, "height", max(dp(66), size[1] + dp(24))))
        card.add_widget(icon)
        card.add_widget(label)
        self.add_widget(card)
        Clock.schedule_once(lambda *_: self.dismiss() if self.parent else None, 2.8)


def toast(message):
    """Wrapped in-app feedback; long error strings must not leave the window."""
    app = MDApp.get_running_app()
    if app and getattr(app, "w", None) is not None:
        app.show_notice(str(message), warning=False)
    else:
        native_toast(str(message))


# ---- Приложение -------------------------------------------------------------

class MediCareApp(MDApp):
    t = DictProperty({})
    lang = StringProperty("ru")
    theme = StringProperty("light")

    c_bg = ColorProperty([1, 1, 1, 1])
    c_card = ColorProperty([1, 1, 1, 1])
    c_text = ColorProperty([0, 0, 0, 1])
    c_sub = ColorProperty([0.4, 0.4, 0.4, 1])
    c_primary = ColorProperty([0.2, 0.3, 0.4, 1])
    c_accent = ColorProperty([0.2, 0.5, 0.9, 1])
    c_soft = ColorProperty([0.9, 0.94, 0.98, 1])
    c_line = ColorProperty([0.9, 0.9, 0.9, 1])
    grad_tex = ObjectProperty(None, allownone=True)
    c_ok = ColorProperty([0.11, 0.50, 0.33, 1])
    c_err = ColorProperty([0.75, 0.22, 0.17, 1])
    c_on_primary = ColorProperty([1, 1, 1, 1])

    tab = StringProperty("home")
    show_nav = BooleanProperty(False)
    pills = StringProperty("")

    greet = StringProperty("")
    uname = StringProperty("")
    avatar_letter = StringProperty("")
    email_text = StringProperty("")
    date_text = StringProperty("")
    home_stat = StringProperty("")
    streak_text = StringProperty("")
    next_title = StringProperty("")
    next_sub = StringProperty("")
    lang_name = StringProperty("")
    theme_name = StringProperty("")
    sel_text = StringProperty("")
    sel_stat = StringProperty("")
    perm_warn = StringProperty("")
    home_pct = NumericProperty(0)
    has_std = BooleanProperty(False)

    # справочник
    dr_key = StringProperty("")
    dr_title = StringProperty("")
    dr_sub = StringProperty("")
    dr_atc = StringProperty("")
    dr_who = BooleanProperty(False)
    dr_fda = BooleanProperty(False)
    dr_ema = BooleanProperty(False)
    dr_use = StringProperty("")
    dr_dose = StringProperty("")
    dr_max = StringProperty("")
    dr_avoid = StringProperty("")
    dr_inter = StringProperty("")
    dr_store = StringProperty("")
    dr_src = StringProperty("")
    lib_back = StringProperty("home")

    add_title = StringProperty("")
    add_back = StringProperty("home")
    add_form_text = StringProperty("")
    add_how_text = StringProperty("")
    add_photo = StringProperty("")

    d_title = StringProperty("")
    d_sub = StringProperty("")
    d_how = StringProperty("")
    d_times = StringProperty("")
    d_course = StringProperty("")
    d_purpose = StringProperty("")
    d_img = StringProperty("")
    detail_back = StringProperty("meds")

    asst_status = StringProperty("")

    n_all = BooleanProperty(True)
    n_push = BooleanProperty(True)
    n_sound = BooleanProperty(True)
    n_vib = BooleanProperty(True)
    n_bg = BooleanProperty(True)
    n_quiet = BooleanProperty(False)
    background_supported = BooleanProperty(False)

    # Safe Area (пиксели): отступы под строку состояния, вырез и панель навигации
    inset_left = NumericProperty(0)
    inset_top = NumericProperty(0)
    inset_right = NumericProperty(0)
    inset_bottom = NumericProperty(0)

    w = None

    # ---------------------------------------------------------------- build

    def build(self):
        self.title = "MediCare"
        self.theme_cls.primary_palette = "Blue"
        from kivy.core.window import Window
        Window.softinput_mode = "below_target"   # клавиатура не закрывает поле ввода

        self.data = core.load()
        self.pills = os.path.join(BASE, "pills.png")
        self.d_img = self.pills

        self.lang = self.data["lang"] if self.data["lang"] in D.T else "ru"
        self.load_texts()
        self.set_theme(
            self.data["theme"] if self.data["theme"] in THEMES else "light",
            persist=False
        )
        self.add_title = self.t["add_med"]

        for key, value in self.data["notif"].items():
            if hasattr(self, "n_" + key):
                setattr(self, "n_" + key, bool(value))

        self.sel_date = dt.date.today()
        self.scheduler = ReminderScheduler()
        self.reminder_sound = SoundLoader.load(os.path.join(BASE, "reminder.wav"))
        self.queue = []
        self.dialog = None
        self.menu = None
        self.cur = None
        self.edit_id = None

        self.form_key = "tablet"
        self.how_key = "after"
        self.new_times = ["08:00"]
        self.new_db = None

        self.assistant = AS.AssistantClient(self.data)
        if self.assistant.migrate_legacy():     # токен и install_id уходят из medicare.json в защищённое хранилище
            core.save(self.data)
        self.background_supported = AL.available()
        self.chat_hist = []        # только в памяти: переписка не сохраняется на диск
        self.chat_busy = False
        self._pending_props = []

        root = Builder.load_file(os.path.join(BASE, "screens.kv"))

        self.w = root.ids
        self.sm = root.ids.sm

        # Returning users go straight to the daily dashboard.
        self.go("home" if self.data.get("onboarded") else "splash")

        self.sync_reminders()
        Clock.schedule_once(lambda *_: self._poll_insets(), 0.3)
        self._tick_event = Clock.schedule_interval(self.tick, 15)
        Clock.schedule_once(lambda *_: self.android_setup(), 1)

        return root

    def on_pause(self):
        self._beat(False)
        self.sync_reminders()
        return True

    def on_resume(self):
        self._poll_insets()
        self._beat(True)
        self.sync_reminders()      # время/часовой пояс могли измениться, пока приложение было свёрнуто
        self.refresh(self.sm.current)
        self.tick()

    def on_stop(self):
        self._beat(False)
        if hasattr(self, "_tick_event"):
            self._tick_event.cancel()

    def _poll_insets(self, tries=8):
        """Окно Android готово не сразу, поэтому несколько раз пробуем прочитать отступы."""
        vals = insets.get_insets()
        if vals is None:
            if tries > 0:
                Clock.schedule_once(lambda *_: self._poll_insets(tries - 1), 0.4)
            return
        self.inset_left, self.inset_top, self.inset_right, self.inset_bottom = vals

    def _beat(self, foreground):
        """Отметка «приложение открыто»: пока она свежая, нативные уведомления не дублируют наше окно."""
        if platform == "android":
            AP.beat(os.path.dirname(core.STORE), foreground, int(time.time() * 1000))

    # ------------------------------------------------------ Фоновые напоминания

    def reminder_texts(self):
        keys = ("rem_dose_title", "rem_missed_title", "rem_missed_text",
                "rem_refresh_title", "rem_refresh_text", "rem_channel_name")
        return {k: self.t[k] for k in keys}

    def sync_reminders(self):
        """Пересчитывает план напоминаний и передаёт его системе (будильник Android).

        Вызывается после любого изменения данных, при запуске и при возврате в приложение.
        Ошибки не должны ломать приложение: тогда работают напоминания при открытом приложении.
        """
        try:
            plan = AP.build_plan(self.data, dt.datetime.now(), self.reminder_texts())
            if not AP.write_plan(os.path.dirname(core.STORE), plan) or not AL.available():
                return False
            return AL.reschedule() if plan["alarms"] else AL.cancel()
        except Exception as exc:
            print("reminder sync failed:", exc)
            return False

    # ------------------------------------------------------ Хранение

    def persist(self):
        """Сохраняет данные; при ошибке показывает сообщение."""
        ok = core.save(self.data)
        if not ok:
            toast(self.t["err_save"])
        else:
            self.sync_reminders()
        return ok

    # ------------------------------------------------------ Тексты и тема

    def load_texts(self):
        # English is the final fallback for keys not yet translated.
        # Copy the dictionary so updates never mutate the source translations.
        base = dict(D.T.get("en", {}))
        selected = D.T.get(self.lang, {})
        if isinstance(selected, dict):
            base.update(selected)

        self.t = base
        self.lang_name = D.LANG_NAMES.get(self.lang, self.lang)
        self.theme_name = base.get("th_" + self.theme, "")

    def set_lang(self, code):
        # Ignore unsupported language codes instead of leaving the app in a
        # partially translated state.
        if code not in D.T:
            return

        old = self.lang
        self.lang = code
        self.data["lang"] = code
        self.load_texts()
        self.theme_name = self.t.get("th_" + self.theme, self.theme_name)
        if not self.persist():
            self.lang = old
            self.data["lang"] = old
            self.load_texts()
            return

        if self.w is not None:
            # Rebuild dynamic lists as well as refreshing labels bound in KV.
            self.refresh(self.sm.current)

    def set_theme(self, name, persist=True):
        if name not in THEMES:
            return
        cfg = THEMES[name]
        old = self.theme

        self.theme = name
        self.theme_cls.theme_style = cfg["style"]

        self.c_bg = hx(cfg["bg"])
        self.c_card = hx(cfg["card"])
        self.c_text = hx(cfg["text"])
        self.c_sub = hx(cfg["sub"])
        self.c_primary = hx(cfg["primary"])
        self.c_accent = hx(cfg["accent"])
        self.c_soft = hx(cfg["soft"])
        self.c_line = hx(cfg["line"])
        self.c_on_primary = hx(cfg["on_primary"])
        self.c_ok = hx(cfg["ok"])
        self.c_err = hx(cfg["err"])
        self.grad_tex = make_gradient(cfg["grad"])

        self.theme_name = self.t.get("th_" + name, "")
        insets.set_light_bars(name == "light")

        if persist:
            self.data["theme"] = name
            if not self.persist():
                self.data["theme"] = old
                self.set_theme(old, persist=False)

    # ------------------------------------------------------ Навигация

    def go(self, name):
        if not self.sm.has_screen(name):
            return
        self.show_nav = name in TABS

        if name in TABS:
            self.tab = name

        # Size the target before on_pre_enter builds adaptive lists. Otherwise
        # first visits can render at the default 100x100 or old nav height.
        if self.sm.parent:
            self.sm.parent.do_layout()
        target = self.sm.get_screen(name)
        target.pos = self.sm.pos
        target.size = self.sm.size
        self.sm.current = name

    def continue_from_splash(self):
        if self.data.get("onboarded", False):
            self.go("home")
            self.refresh("home")
        else:
            self.go("lang")

    def finish_onboarding(self):
        self.data["onboarded"] = True
        if not self.persist():
            self.data["onboarded"] = False
            return
        self.go("home")
        self._dialog(
            self.t["important"], text=self.t["disc_text"],
            buttons=[("ok", None)]
        )

    def refresh(self, name):
        if self.w is None:
            return

        fn = getattr(self, "_r_" + name, None)

        if fn:
            fn()

    # ------------------------------------------------------ Помощники

    def loc(self, d):
        return d.get(self.lang) or d.get("en") or ""

    def period(self, tm):
        hour = int(tm[:2])

        if 5 <= hour < 12:
            return "morning"
        if 12 <= hour < 17:
            return "day"
        if 17 <= hour < 22:
            return "evening"

        return "night"

    def med_title(self, med):
        return "%s %s" % (med["name"], med["dose"])

    def med_sub(self, med):
        return "%s • %s" % (
            self.t["f_" + med["form"]],
            self.t["h_" + med["how"]]
        )

    def db_text(self, med, field):
        entry = D.MEDDB.get(med.get("db"))
        return self.loc(entry[field]) if entry else ""

    def date_str(self, date, with_wd=False):
        result = "%d %s" % (date.day, self.t["months"][date.month - 1])

        if with_wd:
            result += ", " + self.t["wd_full"][date.weekday()]

        return result

    def day_stat(self, day):
        items = core.doses_for(self.data, day)
        done = sum(1 for tm, m in items if core.is_taken(self.data, day, m, tm))
        return self.t["stat"].format(a=done, b=len(items))

    # ------------------------------------------------------ Обновление экранов

    def _user(self):
        self.uname = self.data["name"] or self.t["dflt_name"]
        self.avatar_letter = self.uname[:1].upper()
        self.email_text = self.data["email"] or ""
        self.lang_name = D.LANG_NAMES.get(self.lang, "")
        self.theme_name = self.t.get("th_" + self.theme, "")

    def _r_home(self):
        self._user()

        now = dt.datetime.now()
        hour = now.hour

        greeting = (
            "g_morning" if 5 <= hour < 12
            else "g_day" if 12 <= hour < 17
            else "g_evening" if 17 <= hour < 23
            else "g_night"
        )

        self.greet = self.t[greeting]
        today = now.date()

        self.date_text = "%s, %s" % (self.t["today"], self.date_str(today))
        self.home_stat = self.day_stat(today)
        stats = core.adherence(self.data, today)
        self.streak_text = self.t["streak_stat"].format(current=stats["current"], best=stats["best"])

        items_today = core.doses_for(self.data, today)
        done_today = sum(
            1 for tm, m in items_today if core.is_taken(self.data, today, m, tm)
        )
        self.home_pct = (done_today / len(items_today)) if items_today else 0

        current_time = now.strftime("%H:%M")

        todo = [
            (tm, med)
            for tm, med in core.doses_for(self.data, today)
            if not core.is_taken(self.data, today, med, tm)
        ]

        upcoming = [item for item in todo if item[0] >= current_time]
        next_items = upcoming or todo

        if next_items:
            tm, med = next_items[0]
            self.next_title = self.med_title(med)
            self.next_sub = "%s • %s" % (tm, self.t["h_" + med["how"]])
        else:
            self.next_title = self.t["no_next"]
            self.next_sub = ""

    def _r_profile(self):
        self._user()

    def _r_theme(self):
        self._user()

    def _empty_label(self, key):
        return MDLabel(
            text=self.t[key],
            halign="center",
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=self.c_sub
        )

    def _dose_row(self, day, tm, med, now):
        period = self.period(tm)
        state = core.status(self.data, day, med, tm, now)
        sub = self.t["h_" + med["how"]]

        if state == "missed":
            sub = "%s • %s" % (self.t["missed"], sub)

        row = DoseRow(
            time=tm,
            chip_icon=CHIP_ICONS[period],
            period=self.t["p_" + period],
            title=self.med_title(med),
            sub=sub,
            state=state,
            chip=CHIPS[period]
        )

        row.bind(
            on_open=lambda _w, m=med: self.open_detail(m, self.sm.current),
            on_toggle=lambda _w, m=med, t=tm, d=day: self.toggle_dose(m, t, d)
        )

        return row

    def show_notice(self, message, warning=True):
        # Закрываем предыдущее уведомление, чтобы сообщения не наслаивались.
        old = getattr(self, "_notice", None)
        if old is not None and old.parent:
            old.dismiss()
        self._notice = EarlyNotice(message=message, warning=warning)
        self._notice.open()

    def early_dose_message(self):
        return {
            "ru": "Пока рано — отметить приём можно не раньше чем за час до назначенного времени.",
            "en": "Too early — you can mark this dose no sooner than one hour before its time.",
            "hy": "Դեռ վաղ է․ ընդունումը կարելի է նշել նշանակված ժամից առնվազն մեկ ժամ առաջ։",
        }.get(self.lang, "Пока рано — отметить приём можно не раньше чем за час до назначенного времени.")

    def toggle_dose(self, med, tm, day):
        was_taken = core.is_taken(self.data, day, med, tm)
        if not was_taken and not core.can_mark_taken(day, tm):
            self.show_notice(self.early_dose_message())
            return
        if was_taken:
            self._dialog(self.t["undo_dose"], text=self.med_title(med),
                         buttons=[("cancel", None), ("undo", lambda: self._commit_dose(med, tm, day, False))])
            return
        self._commit_dose(med, tm, day, True)

    def _commit_dose(self, med, tm, day, taken):
        result = core.change_taken(self.data, day, med, tm, taken=taken)
        if result == "error":
            toast(self.t["err_save"])
        elif result == "blocked":
            self.show_notice(self.early_dose_message())
        elif result == "saved":
            toast(self.t["taken"] if taken else self.t["undone"])
            self.sync_reminders()
        self.refresh(self.sm.current)

    # -- расписание и история
    def _r_schedule(self):
        self._build_week()
        self._build_doses()

    def _build_week(self):
        box = self.w.week
        box.clear_widgets()

        monday = self.sel_date - dt.timedelta(days=self.sel_date.weekday())

        for i in range(7):
            date = monday + dt.timedelta(days=i)

            cell = DayCell(
                wd=self.t["wd_short"][i],
                num=str(date.day),
                sel=(date == self.sel_date),
                mark=core.day_mark(self.data, date),
                today=(date == dt.date.today())
            )

            cell.bind(on_release=lambda _widget, d=date: self.pick_date(d))

            box.add_widget(cell)

        self.sel_text = self.date_str(self.sel_date, True)

    def pick_date(self, date):
        self.sel_date = date
        self._r_schedule()

    def shift_week(self, amount):
        self.pick_date(self.sel_date + dt.timedelta(days=7 * amount))

    def today_schedule(self):
        self.pick_date(dt.date.today())

    def _build_doses(self):
        box = self.w.dose_list
        box.clear_widgets()

        items = core.doses_for(self.data, self.sel_date)
        now = dt.datetime.now()

        if not items:
            box.add_widget(self._empty_label("nothing_today"))

        for tm, med in items:
            box.add_widget(self._dose_row(self.sel_date, tm, med, now))

        self.sel_stat = self.day_stat(self.sel_date)

    # -- уведомления: список напоминаний на сегодня
    def _r_notif(self):
        box = self.w.notif_list
        box.clear_widgets()

        now = dt.datetime.now()
        today = now.date()
        items = core.doses_for(self.data, today)

        if not items:
            box.add_widget(self._empty_label("nothing_today"))

        for tm, med in items:
            box.add_widget(self._dose_row(today, tm, med, now))

    # -- список лекарств
    def _r_meds(self):
        box = self.w.med_list
        box.clear_widgets()

        query = self.w.med_search.text.strip().casefold()
        matches = [med for med in self.data["meds"]
                   if query in (med["name"] + " " + med["dose"]).casefold()]
        if not matches:
            box.add_widget(self._empty_label("no_results" if query else "no_meds"))

        for med in matches:
            row = Row(
                icon="pill",
                text=self.med_title(med),
                sub=self.med_sub(med),
                tint=self.c_accent
            )

            row.bind(on_release=lambda _w, m=med: self.open_detail(m, "meds"))

            box.add_widget(row)

    # ------------------------------------------------------ Детали лекарства

    def open_detail(self, med, back):
        self.cur = med
        self.detail_back = back

        self.d_title = med["name"]
        self.d_sub = "%s • %s" % (med["dose"], self.t["f_" + med["form"]])
        self.d_how = self.t["h_" + med["how"]]
        self.d_times = ", ".join(med["times"])

        days = int(med.get("days") or 0)

        self.d_course = (
            "%d %s" % (days, self.t["days_unit"]) if days else self.t["ongoing"]
        )

        self.d_purpose = (
            med.get("note") or self.db_text(med, "purpose") or "—"
        )

        self.has_std = med.get("db") in DR.DRUGDB

        photo = med.get("photo") or ""
        self.d_img = photo if photo and os.path.exists(photo) else self.pills
        self.go("detail")

    def show_instruction(self):
        if not self.cur:
            return

        text = self.db_text(self.cur, "instr") or self.t["no_instr"]
        text += "\n\n" + self.t["disclaimer"] + "\n\n" + self.t["ref_disclaimer"]

        scroll = MDScrollView(size_hint_y=None, height=dp(320))

        label = MDLabel(
            text=text,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=self.c_text
        )

        scroll.add_widget(label)

        self._dialog(
            self.t["instruction"] + ": " + self.cur["name"],
            content=scroll,
            buttons=[("close", None)]
        )

    def delete_med(self):
        def yes(*_):
            backup = list(self.data["meds"])
            self.data["meds"] = [
                med for med in self.data["meds"]
                if med["id"] != self.cur["id"]
            ]

            if not self.persist():
                self.data["meds"] = backup
                return

            toast(self.t["deleted"])
            self.go("meds")
            self.refresh("meds")

        self._dialog(
            self.t["confirm_del"],
            text=self.med_title(self.cur),
            buttons=[("cancel", None), ("delete", yes)]
        )

    # ------------------------------------------------------ Справочник

    def _r_lib(self):
        self.show_lib(self.w.lib_search.text if "lib_search" in self.w else "")

    def show_lib(self, query=""):
        box = self.w.lib_list
        box.clear_widgets()

        found = DR.search(query)

        if not found:
            box.add_widget(self._empty_label("no_results"))

        for d in found:
            row = DrugRow(
                title=self.loc(d["name"]),
                sub="%s • %s" % (d["atc"], self.loc(d["cls"])),
                who=d["who_eml"]
            )
            row.bind(on_release=lambda _w, k=d["key"]: self.open_drug(k, "lib"))
            box.add_widget(row)

    def open_drug(self, key, back="lib"):
        d = DR.DRUGDB.get(key)

        if not d:
            return

        self.dr_key = key
        self.lib_back = back
        self.dr_title = self.loc(d["name"])
        self.dr_sub = self.loc(d["cls"])
        self.dr_atc = d["atc"]
        self.dr_who = d["who_eml"]
        self.dr_fda = "FDA" in d["sources"]
        self.dr_ema = "EMA" in d["sources"]
        self.dr_use = self.loc(d["use"])
        self.dr_dose = self.loc(d["dose"])
        self.dr_max = self.loc(d["max"])
        self.dr_avoid = self.loc(d["avoid"])
        self.dr_inter = self.loc(d["inter"])
        self.dr_store = self.loc(d["store"])
        self.dr_src = "\n".join(
            "• " + self.loc(DR.SOURCE_INFO[s]) for s in d["sources"]
        )

        badges = self.w.dr_badges
        badges.clear_widgets()
        specs = [(d["atc"], self.c_soft, self.c_text)]
        if d["who_eml"]:
            specs.append(("WHO EML", [0.84, 0.91, 0.98, 1], [0.10, 0.30, 0.60, 1]))
        if "FDA" in d["sources"]:
            specs.append(("FDA", [0.82, 0.94, 0.88, 1], [0.08, 0.40, 0.25, 1]))
        if "EMA" in d["sources"]:
            specs.append(("EMA", [0.90, 0.86, 0.98, 1], [0.32, 0.20, 0.60, 1]))
        for text, bg, fg in specs:
            badges.add_widget(Factory.Badge(text=text, bg=bg, fg=fg))

        self.go("drug")

    def drug_to_schedule(self):
        entry = D.MEDDB.get(self.dr_key)

        if not entry:
            return

        self.new_med()
        self._use_db(entry)
        self.add_back = "drug"

    def open_standards(self):
        if self.cur and self.cur.get("db") in DR.DRUGDB:
            self.open_drug(self.cur["db"], "detail")

    def _limit_exceeded(self, db, dose, times):
        mx = MAX_MG.get(db)
        total = DR.daily_total_mg({"dose": dose, "times": times})

        if mx and total and total > mx:
            return total, mx

        return None

    # ------------------------------------------------------ Добавление и редактирование

    def new_med(self):
        widgets = self.w

        widgets.name_f.text = ""
        widgets.dose_f.text = ""
        widgets.course_f.text = ""
        widgets.note_f.text = ""

        self.edit_id = None
        self.add_title = self.t["add_med"]
        self.add_back = "home"
        self.form_key = "tablet"
        self.how_key = "after"
        self.new_times = ["08:00"]
        self.new_db = None
        self.add_photo = ""

        self._sync_add()
        self.go("add")

    def edit_med(self):
        med = self.cur

        if not med:
            return

        widgets = self.w

        widgets.name_f.text = med["name"]
        widgets.dose_f.text = med["dose"]
        days = int(med.get("days") or 0)
        widgets.course_f.text = str(days) if days else ""
        widgets.note_f.text = med.get("note", "")

        self.edit_id = med["id"]
        self.add_title = self.t["edit_med"]
        self.add_back = "detail"
        self.form_key = med["form"]
        self.how_key = med["how"]
        self.new_times = list(med["times"])
        self.new_db = med.get("db")
        self.add_photo = med.get("photo") or ""

        self._sync_add()
        self.go("add")

    def _sync_add(self):
        self.add_form_text = self.t["f_" + self.form_key]
        self.add_how_text = self.t["h_" + self.how_key]

        box = self.w.times_box
        box.clear_widgets()

        for tm in self.new_times:
            chip = TimeChip(text=tm + "  ✕")
            chip.bind(on_release=lambda _w, t=tm: self._del_time(t))
            box.add_widget(chip)

    def _del_time(self, tm):
        if tm in self.new_times:
            self.new_times.remove(tm)

        self._sync_add()

    def add_time(self):
        picker = MDTimePicker()
        picker.bind(on_save=self._time_saved)
        picker.open()

    def _time_saved(self, instance, value):
        if not isinstance(value, dt.time):
            toast(self.t["need_time"])
            return
        tm = value.strftime("%H:%M")

        if tm not in self.new_times:
            self.new_times.append(tm)
            self.new_times.sort()

        self._sync_add()
        instance.dismiss()

    def _menu(self, caller, items):
        if self.menu:
            self.menu.dismiss()

        self.menu = MDDropdownMenu(caller=caller, items=items, width_mult=4)
        self.menu.open()

    def pick_form(self, caller):
        items = [
            {
                "text": self.t["f_" + key],
                "viewclass": "OneLineListItem",
                "on_release": lambda k=key: self._set_form(k)
            }
            for key in D.FORMS
        ]

        self._menu(caller, items)

    def _set_form(self, key):
        self.form_key = key
        self._sync_add()

        if self.menu:
            self.menu.dismiss()

    def pick_how(self, caller):
        items = [
            {
                "text": self.t["h_" + key],
                "viewclass": "OneLineListItem",
                "on_release": lambda k=key: self._set_how(k)
            }
            for key in D.HOWS
        ]

        self._menu(caller, items)

    def _set_how(self, key):
        self.how_key = key
        self._sync_add()

        if self.menu:
            self.menu.dismiss()

    def pick_db(self, caller):
        content = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None, height=dp(360))
        search = Factory.F(hint_text=self.t["search_meds"])
        scroll = MDScrollView()
        rows = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(6))
        scroll.add_widget(rows)
        content.add_widget(search)
        content.add_widget(scroll)

        def select(entry):
            if self.dialog:
                self.dialog.dismiss()
            self._use_db(entry)

        def update(_field=None, query=""):
            rows.clear_widgets()
            matches = [entry for entry in D.MEDLIST
                       if any(query.strip().casefold() in name.casefold() for name in entry["name"].values())]
            if not matches:
                rows.add_widget(self._empty_label("no_results"))
            for entry in matches:
                row = Row(icon="pill", text=self.loc(entry["name"]), sub=self.loc(entry["dose"]), tint=self.c_ok)
                row.bind(on_release=lambda _w, e=entry: select(e))
                rows.add_widget(row)
        search.bind(text=update)
        update()
        self._dialog(self.t["from_db"], content=content, buttons=[("cancel", None)])

    def _use_db(self, entry):
        widgets = self.w

        widgets.name_f.text = self.loc(entry["name"])
        widgets.dose_f.text = self.loc(entry["dose"])
        widgets.course_f.text = str(entry["days"]) if entry["days"] else ""

        self.form_key = entry["form"]
        self.how_key = entry["how"]
        self.new_times = list(entry["times"])
        self.new_db = entry["key"]

        self._sync_add()

        if self.menu:
            self.menu.dismiss()

    def pick_photo(self):
        try:
            from plyer import filechooser

            filechooser.open_file(
                on_selection=self._photo_sel,
                filters=[["Images", "*.png", "*.jpg", "*.jpeg"]]
            )

        except Exception:
            toast(self.t["photo_unavailable"])

    def _photo_sel(self, selection):
        def apply(*_):
            if not selection:
                return
            source = selection[0]
            ext = os.path.splitext(source)[1].lower()
            if ext not in (".png", ".jpg", ".jpeg") or not os.path.isfile(source):
                toast(self.t["photo_unavailable"])
                return
            try:
                directory = os.path.join(os.path.dirname(core.STORE), "photos")
                os.makedirs(directory, exist_ok=True)
                target = os.path.join(directory, uuid.uuid4().hex + ext)
                shutil.copy2(source, target)
                self.add_photo = target
            except OSError:
                toast(self.t["photo_unavailable"])
        Clock.schedule_once(apply, 0)

    def save_med(self, force=False):
        widgets = self.w

        name = widgets.name_f.text.strip()
        dose = widgets.dose_f.text.strip()
        course = widgets.course_f.text.strip()

        # --- проверка ввода
        if not name or not dose:
            toast(self.t["fill_required"])
            return

        if len(name) > 60:
            toast(self.t["err_name_long"])
            return

        if len(dose) > 30 or not any(ch.isdigit() for ch in dose):
            toast(self.t["err_dose"])
            return

        if course and (not course.isdigit() or not 1 <= int(course) <= 365):
            toast(self.t["err_course"])
            return

        if not self.new_times or not all(core._valid_time(t) for t in self.new_times):
            toast(self.t["need_time"])
            return

        # Editing a catalogue-derived name must not retain an unrelated leaflet.
        db = self.new_db
        if db and name.casefold() not in [v.casefold() for v in D.MEDDB.get(db, {}).get("name", {}).values()]:
            db = None

        if not db:
            low = name.lower()

            for entry in D.MEDLIST:
                if low in [v.lower() for v in entry["name"].values()]:
                    db = entry["key"]
                    break

        if not db:
            db = SC.key_for_name(name)

        if not force:
            over = self._limit_exceeded(db, dose, self.new_times)

            if over:
                self._dialog(
                    self.t["important"],
                    text=self.t["limit_warn"].format(
                        tot=int(over[0]), mx=int(over[1])
                    ),
                    buttons=[
                        ("review", None),
                        ("save_anyway", lambda: self.save_med(force=True)),
                    ]
                )
                return

        fields = {
            "name": name,
            "dose": dose,
            "form": self.form_key,
            "how": self.how_key,
            "times": sorted(set(self.new_times)),
            "days": int(course) if course else 0,
            "note": widgets.note_f.text.strip()[:200],
            "db": db,
            "photo": self.add_photo
        }

        if self.edit_id:
            med = next(
                (m for m in self.data["meds"] if m["id"] == self.edit_id), None
            )

            if med is None:
                return

            old = dict(med)
            med.update(fields)

            if not self.persist():
                med.clear()
                med.update(old)
                return

            toast(self.t["saved"])
            self.open_detail(med, self.detail_back)
            self._schedule_warnings(med["id"])
            return

        med = {
            "id": uuid.uuid4().hex,
            "start": dt.date.today().isoformat(),
        }
        med.update(fields)

        self.data["meds"].append(med)

        if not self.persist():
            self.data["meds"].pop()
            return

        toast(self.t["saved"])
        self.go("meds")
        self.refresh("meds")
        self._schedule_warnings(med["id"])

    # ------------------------------------------------------ Уведомления

    def set_n(self, key, val):
        if key not in core.DEFAULT["notif"]:
            return
        if key == "bg" and val and not self.background_supported:
            val = False
        old = self.data["notif"].get(key)
        if old == bool(val) and getattr(self, "n_" + key) == bool(val):
            return
        self.data["notif"][key] = bool(val)
        setattr(self, "n_" + key, bool(val))
        if not self.persist():
            self.data["notif"][key] = old
            setattr(self, "n_" + key, old)
            return
        if not self.n_all or (self.n_quiet and core.in_quiet(dt.datetime.now())):
            self.queue.clear()

        if key in ("bg", "all"):
            self._service(self.n_all and self.n_bg)

    def android_setup(self):
        # Android-specific notification permission setup.
        # Windows and other desktop platforms do not import Android modules.
        self.background_supported = AL.available()
        if not self.background_supported:
            self.n_bg = False
            self.data["notif"]["bg"] = False
            self.perm_warn = self.t["foreground_only"]
            return
        self.n_bg = bool(self.data["notif"].get("bg", True))
        self.perm_warn = self.t["bg_info"]
        if AL.notifications_allowed() is False:
            self.perm_warn = self.t["perm_denied"]

        try:
            # Load Android-only modules dynamically so Pylance on Windows
            # does not report them as missing Python packages.
            android_permissions = importlib.import_module("android.permissions")
            jnius = importlib.import_module("jnius")
            request_permissions = android_permissions.request_permissions
            autoclass = jnius.autoclass

            sdk = autoclass("android.os.Build$VERSION").SDK_INT

            if sdk >= 33:
                request_permissions(
                    ["android.permission.POST_NOTIFICATIONS"],
                    self._perm_result,
                )

        except Exception as error:
            print("Permission error:", error)

        self._service(self.n_all and self.n_bg)

    def _perm_result(self, permissions, results):
        # Permission callback may run from another thread.
        # Update the interface through Kivy Clock.
        def apply(*_):
            for perm, ok in zip(permissions, results):
                if perm.endswith("POST_NOTIFICATIONS"):
                    self.perm_warn = self.t["bg_info"] if ok else self.t["perm_denied"]
                    if ok:
                        self.sync_reminders()

                    if not ok:
                        toast(self.t["perm_denied"])

        Clock.schedule_once(apply, 0)

    def _service(self, start):
        # Фоновые напоминания: пересчитать план и поставить/снять системный будильник.
        return self.sync_reminders()

    def tick(self, *_):
        """Проверяет время приёма каждые 15 секунд, пока приложение открыто."""
        if self.w is None:
            return
        self._beat(True)
        now = dt.datetime.now()
        # Списки пересобираются раз в минуту: частая перерисовка сбрасывала
        # прокрутку и могла «съесть» нажатие в момент пересборки.
        minute = now.strftime("%Y%m%d%H%M")
        if minute != getattr(self, "_last_refresh", None):
            self._last_refresh = minute
            self.refresh(self.sm.current)
        if not self.n_all:
            self.queue.clear()
            return

        if self.n_quiet and core.in_quiet(now):
            self.queue.clear()
            return
        self.queue.extend(self.scheduler.due(self.data, now))

        self._show_next()

    def _show_next(self):
        if not self.n_all or (self.n_quiet and core.in_quiet(dt.datetime.now())):
            self.queue.clear()
            return
        if self.dialog or not self.queue or not self.data.get("onboarded"):
            return

        day, med, tm, fk = self.queue.pop(0)
        current = next((m for m in self.data["meds"] if m["id"] == med["id"]), None)
        if day != dt.date.today() or current is None or tm not in current["times"] or core.is_taken(self.data, day, med, tm):
            Clock.schedule_once(lambda *_: self._show_next(), 0)
            return
        med = current
        if self.n_sound and self.reminder_sound:
            self.reminder_sound.play()

        if self.n_vib and platform == "android":
            try:
                from plyer import vibrator
                vibrator.vibrate(0.6)
            except Exception:
                pass

        if self.n_push and platform != "ios":
            try:
                from plyer import notification

                notification.notify(
                    title="MediCare",
                    message=self.med_title(med),
                    app_name="MediCare",
                    timeout=8
                )
            except Exception as error:
                print("System notification unavailable:", error)

        def taken(*_):
            if not core.can_mark_taken(day, tm):
                self.show_notice(self.early_dose_message())
                return
            self._commit_dose(med, tm, day, True)

        def snooze(*_):
            self.scheduler.snooze(fk, dt.datetime.now())
            toast(self.t["sleep_snooze"])

        popup = DosePopup(
            title=self.t["time_to_take"],
            med=self.med_title(med),
            sub=self.t["h_" + med["how"]],
            cb_take=taken,
            cb_snooze=snooze
        )
        popup.bind(on_dismiss=self._dlg_closed)
        self.dialog = popup
        popup.open()

    def popup_action(self, popup, which):
        cb = popup.cb_take if which == "take" else popup.cb_snooze
        popup.dismiss()

        if cb:
            cb()

    # ------------------------------------------------------ AI-помощник

    def _r_assistant(self):
        # Экран пересобирается раз в минуту, поэтому чат здесь не трогаем:
        # только показываем приветствие, если переписка ещё не началась.
        if not self.w.chat_list.children:
            self.add_bubble(self.t["asst_intro"])

    def add_bubble(self, text, mine=False, alert=False):
        bubble = Bubble(text=text, mine=mine, alert=alert)
        self.w.chat_list.add_widget(bubble)
        Clock.schedule_once(lambda *_: setattr(self.w.chat_scroll, "scroll_y", 0), 0.1)

    def _assistant_cfg(self):
        cfg = self.data.get("assistant")
        if not isinstance(cfg, dict):
            cfg = {}
            self.data["assistant"] = cfg
        return cfg

    def send_chat(self, text=None, spoken=False):
        if self.chat_busy:
            return
        field = self.w.chat_input
        text = (text if text is not None else field.text).strip()
        if not text:
            return
        field.text = ""
        text = text[:1000]
        self.add_bubble(text, mine=True)

        # 1. Неотложные симптомы: подсказка звонить 112 появляется сразу и без интернета.
        self._emerg_shown = safety.is_emergency(text)
        if self._emerg_shown:
            self.add_bubble(self.t["asst_emergency"], alert=True)
            voice.speak(self.t["asst_emergency"], self.lang)
        else:
            # 2. Простые команды выполняются на телефоне, без сервера (см. voice_commands.py).
            intent = VC.parse(text)
            if intent:
                self._run_command(intent, spoken)
                return

        # 3. Всё остальное — помощнику на сервере, но только с согласия человека.
        if not self._assistant_cfg().get("consent"):
            self._ask_consent(text, spoken)
            return
        self._send_to_ai(text, spoken)

    def _ask_consent(self, text, spoken):
        def yes():
            self._assistant_cfg()["consent"] = True
            if not self.persist():
                self._assistant_cfg().pop("consent", None)
                return
            self._send_to_ai(text, spoken)
        self._dialog(self.t["asst_consent_title"], text=self.t["asst_consent_text"],
                     buttons=[("asst_consent_no", None), ("asst_consent_yes", yes)])

    def _send_to_ai(self, text, spoken):
        self.chat_hist.append({"role": "user", "content": text})
        if not self.assistant.configured():
            self.add_bubble(self.t["asst_not_configured"], alert=True)
            self.chat_hist.pop()
            return
        self.chat_busy = True
        self.asst_status = self.t["asst_thinking"]
        history = list(self.chat_hist)
        meds = [dict(m) for m in self.data["meds"]]
        lang = self.lang

        def work():
            try:
                result = self.assistant.chat(history, meds, lang)
                error = None
            except AS.AssistantError as exc:
                result, error = None, exc.kind
            except Exception as exc:       # не даём потоку молча упасть
                print("assistant error:", exc)
                result, error = None, "server"
            Clock.schedule_once(lambda *_: self._chat_done(result, error, spoken), 0)

        threading.Thread(target=work, daemon=True).start()

    # -- команды, которые приложение выполняет само

    def _local_answer(self, text, spoken):
        self.add_bubble(text)
        if spoken:
            voice.speak(text, self.lang)

    def _run_command(self, intent, spoken):
        now = dt.datetime.now()
        if intent.kind == "next":
            self._local_answer(VC.describe_next(self.data, now, self.lang), spoken)
        elif intent.kind == "today":
            self._local_answer(VC.describe_today(self.data, now, self.lang), spoken)
        elif intent.kind == "check":
            found = SC.analyze(self.data["meds"], now.date(), quiet=self.n_quiet)
            self._local_answer(SC.render_all(found, self.lang), spoken)
        elif intent.kind == "taken":
            self._voice_taken(intent.query, now, spoken)

    def _voice_taken(self, query, now, spoken):
        """«Я принял…»: меняем данные только после явного подтверждения кнопкой."""
        doses = VC.eligible_doses(self.data, now, query)
        if not doses:
            self._local_answer(self.t["vc_none_to_mark"], spoken)
            return
        items = "\n".join("%s — %s" % (tm, self.med_title(m)) for _day, tm, m in doses)
        question = self.t["vc_confirm_taken"].format(items=items)
        if spoken:
            voice.speak(question, self.lang)
        self._dialog(self.t["vc_confirm_title"], text=question,
                     buttons=[("asst_no", None), ("asst_yes", lambda: self._apply_taken(doses))])

    def _apply_taken(self, doses):
        done = []
        for day, tm, med in doses:
            if core.change_taken(self.data, day, med, tm, taken=True) == "saved":
                done.append("%s %s ✓" % (tm, self.med_title(med)))
        if done:
            self.sync_reminders()
            self.add_bubble("\n".join(done))
            toast(self.t["taken"])
        else:
            toast(self.t["err_save"])
        self.refresh(self.sm.current)

    def _chat_done(self, result, error, spoken):
        self.chat_busy = False
        self.asst_status = ""
        # токен/идентификатор установки могли обновиться
        core.save(self.data)
        if error:
            key = {"not_configured": "asst_not_configured", "network": "asst_err_network",
                   "rate": "asst_err_rate", "auth": "asst_err_auth"}.get(error, "asst_err_server")
            self.add_bubble(self.t[key], alert=True)
            return
        reply = (result.get("reply") or "").strip()
        urgency = result.get("urgency")
        if urgency == "emergency":
            if not getattr(self, "_emerg_shown", False):
                self.add_bubble(self.t["asst_emergency"], alert=True)
                voice.speak(self.t["asst_emergency"], self.lang)
        elif urgency == "doctor":
            reply = (reply + "\n\n" + self.t["asst_doctor"]).strip()
        if reply:
            self.add_bubble(reply)
            self.chat_hist.append({"role": "assistant", "content": reply})
            if spoken and urgency != "emergency":
                voice.speak(reply, self.lang)
        self._pending_props = [p for p in result.get("proposals", []) if isinstance(p, dict)][:5]
        self._next_proposal()

    def start_voice(self):
        if self.chat_busy:
            return
        if not voice.available():
            toast(self.t["asst_no_voice"])
            return
        self.asst_status = self.t["asst_listening"]

        def got(text):
            self.asst_status = ""
            self.send_chat(text, spoken=True)

        def failed(_reason):
            self.asst_status = ""
            toast(self.t["asst_voice_fail"])

        voice.listen(self.lang, got, failed)

    # -- добавление лекарства по предложению помощника (только с подтверждением)

    def _next_proposal(self):
        if self.dialog:
            Clock.schedule_once(lambda *_: self._next_proposal(), 0.5)
            return
        if not self._pending_props:
            return
        prop = self._pending_props.pop(0)
        med = self._med_from_proposal(prop)
        if med is None:
            toast(self.t["asst_invalid"])
            self._next_proposal()
            return
        lines = [self.med_title(med),
                 "%s: %s" % (self.t["asst_confirm_times"], ", ".join(med["times"])),
                 "%s: %s" % (self.t["asst_confirm_course"],
                             "%d %s" % (med["days"], self.t["days_unit"]) if med["days"] else self.t["ongoing"]),
                 "", self.t["asst_confirm_check"]]
        self._dialog(
            self.t["asst_confirm_title"], text="\n".join(lines),
            buttons=[("asst_no", lambda: self._next_proposal()),
                     ("asst_yes", lambda: self._confirm_proposal(med))]
        )

    def _med_from_proposal(self, prop):
        """Проверяет предложение помощника теми же правилами, что и ручной ввод."""
        name = str(prop.get("name") or "").strip()
        dose = str(prop.get("dose") or "").strip()
        if not name or len(name) > 60 or not dose or len(dose) > 30 \
                or not any(ch.isdigit() for ch in dose):
            return None
        db = None
        for entry in D.MEDLIST:
            if name.casefold() in [v.casefold() for v in entry["name"].values()]:
                db = entry["key"]
                break
        db = db or SC.key_for_name(name)
        raw = {
            "id": uuid.uuid4().hex,
            "start": dt.date.today().isoformat(),
            "name": name, "dose": dose,
            "form": prop.get("form"), "how": prop.get("how"),
            "times": prop.get("times"), "days": prop.get("days"),
            "note": str(prop.get("note") or "")[:200],
            "db": db, "photo": "",
        }
        return core.normalize_med(raw)

    def _confirm_proposal(self, med, force=False):
        if not force:
            over = self._limit_exceeded(med.get("db"), med["dose"], med["times"])
            if over:
                self._dialog(
                    self.t["important"],
                    text=self.t["limit_warn"].format(tot=int(over[0]), mx=int(over[1])),
                    buttons=[("asst_no", lambda: self._next_proposal()),
                             ("save_anyway", lambda: self._confirm_proposal(med, force=True))]
                )
                return
        same = any(
            m["name"].casefold() == med["name"].casefold()
            and m["dose"].casefold() == med["dose"].casefold()
            and m["times"] == med["times"]
            for m in self.data["meds"]
        )
        if same:
            toast(self.t["asst_duplicate"])
            self._next_proposal()
            return
        self.data["meds"].append(med)
        if not self.persist():
            self.data["meds"].pop()
            return
        toast(self.t["asst_added"])
        self.add_bubble("%s ✓" % self.med_title(med))
        self.refresh(self.sm.current)
        self._schedule_warnings(med["id"])
        self._next_proposal()

    # ------------------------------------------------------ Удаление данных

    def confirm_wipe(self):
        """«Удалить мои данные»: лекарства, отметки, фото, согласие помощника и токен сервера."""
        self._dialog(
            self.t["wipe_title"], text=self.t["wipe_text"],
            buttons=[("cancel", None), ("delete", self._wipe_all)]
        )

    def _wipe_all(self):
        try:
            self.assistant.forget()                  # токен и install_id из защищённого хранилища
        except Exception as exc:
            print("forget failed:", exc)
        try:
            shutil.rmtree(os.path.join(os.path.dirname(core.STORE), "photos"), ignore_errors=True)
        except Exception as exc:
            print("photos cleanup failed:", exc)
        keep = {"lang": self.data.get("lang", "ru"), "theme": self.data.get("theme", "light")}
        fresh = core._default_data()
        fresh.update(keep)
        fresh["onboarded"] = True
        # словарь меняем «на месте»: на него ссылаются помощник и другие части приложения
        self.data.clear()
        self.data.update(fresh)
        self.chat_hist = []
        self._pending_props = []
        self.queue.clear()
        if "chat_list" in self.w:
            self.w.chat_list.clear_widgets()
        if not self.persist():
            return
        toast(self.t["wipe_done"])
        self.go("home")
        self.refresh("home")

    # ------------------------------------------------------ Диалоги

    def _schedule_warnings(self, med_id):
        """После добавления лекарства показывает предупреждения расписания, где оно участвует.

        Суточный лимит не повторяем: о нём уже спрашивали до сохранения.
        """
        found = SC.for_medication(
            SC.analyze(self.data["meds"], dt.date.today(), quiet=self.n_quiet), med_id)
        found = [f for f in found if f["severity"] == "warn" and f["code"] != "daily_limit"]
        if not found:
            return
        scroll = MDScrollView(size_hint_y=None, height=dp(260))
        scroll.add_widget(MDLabel(
            text="\n\n".join(SC.render(f, self.lang) for f in found),
            adaptive_height=True, theme_text_color="Custom", text_color=self.c_text))
        Clock.schedule_once(lambda *_: self._dialog(
            self.t["sched_warn_title"], content=scroll, buttons=[("ok", None)]), 0.4)

    def _dialog(self, title, text=None, content=None, buttons=()):
        def make_button(key, callback):
            def press(*_):
                if self.dialog:
                    self.dialog.dismiss()

                if callback:
                    callback()

            return MDFlatButton(
                text=self.t[key],
                theme_text_color="Custom",
                text_color=self.c_accent,
                on_release=press
            )

        kwargs = {
            "title": title,
            "buttons": [make_button(k, cb) for k, cb in buttons],
            "md_bg_color": self.c_card
        }

        if content is not None:
            kwargs.update(type="custom", content_cls=content)
        else:
            kwargs["text"] = text or ""

        dialog = MDDialog(**kwargs)
        dialog.bind(on_dismiss=self._dlg_closed)

        self.dialog = dialog
        dialog.open()

    def _dlg_closed(self, *_):
        if not _ or self.dialog is _[0]:
            self.dialog = None
        Clock.schedule_once(lambda *_: self._show_next(), 0.3)

    def edit_profile(self):
        box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(150)
        )

        field1 = Factory.F(hint_text=self.t["name"], text=self.data["name"])
        field2 = Factory.F(hint_text=self.t["email"], text=self.data["email"])

        box.add_widget(field1)
        box.add_widget(field2)

        def save_profile():
            email = field2.text.strip()

            if email and ("@" not in email or "." not in email.split("@")[-1]):
                toast(self.t["err_email"])
                return

            old = (self.data["name"], self.data["email"])
            self.data["name"] = field1.text.strip()[:40]
            self.data["email"] = email[:80]

            if not self.persist():
                self.data["name"], self.data["email"] = old
            self.refresh(self.sm.current)

        self._dialog(
            self.t["personal"],
            content=box,
            buttons=[("cancel", None), ("save", save_profile)]
        )

    def show_text(self, key):
        scroll = MDScrollView(size_hint_y=None, height=dp(280))

        scroll.add_widget(
            MDLabel(
                text=self.t[key],
                adaptive_height=True,
                theme_text_color="Custom",
                text_color=self.c_text
            )
        )

        self._dialog(
            self.t["help" if key == "help_text" else "about"],
            content=scroll,
            buttons=[("close", None)]
        )


if __name__ == "__main__":
    MediCareApp().run()
