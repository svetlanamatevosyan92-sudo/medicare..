# -*- coding: utf-8 -*-
"""Переводы (RU / EN / HY) и встроенная база лекарств."""

FORMS = ["tablet", "capsule", "syrup", "drops", "injection", "ointment", "powder"]
HOWS = ["after", "before", "during", "any", "sleep"]

T = {}

T["en"] = {
    "app_sub": "Your medication\nassistant",
    "start": "Start",
    "choose_lang": "Choose language",
    "choose_lang_sub": "Please choose a language that suits you",
    "next": "Next",
    "g_morning": "Good morning,", "g_day": "Good afternoon,",
    "g_evening": "Good evening,", "g_night": "Good night,",
    "dflt_name": "Friend",
    "today": "Today",
    "next_dose": "Next dose",
    "show_all": "Show all",
    "no_next": "No more doses today",
    "day_schedule": "Daily schedule",
    "my_meds": "My medicines",
    "add_med": "Add medicine",
    "notifications": "Notifications",
    "nav_home": "Home", "nav_cal": "Calendar", "nav_meds": "Medicines", "nav_profile": "Profile",
    "add_photo": "Add photo", "optional": "(optional)",
    "med_name": "Medicine name *", "dose": "Dosage (e.g. 500 mg) *",
    "form": "Form", "how": "How to take",
    "times": "Intake times", "add_time": "Add time",
    "course": "Course, days (empty = ongoing)",
    "note": "Purpose (optional)",
    "from_db": "Choose from database",
    "save": "Save",
    "fill_required": "Fill in name and dosage",
    "need_time": "Add at least one time",
    "saved": "Saved",
    "details": "Medicine details",
    "how_to": "How to take", "intake_time": "Intake time", "course_t": "Course",
    "purpose": "Purpose",
    "open_instr": "Open instructions",
    "instruction": "Instructions",
    "no_instr": "No built-in instructions for this medicine. Please follow the package leaflet and your doctor's advice.",
    "disclaimer": "This information is for reference only and does not replace the manufacturer's leaflet or a doctor's advice.",
    "close": "Close",
    "days_unit": "days", "ongoing": "Ongoing",
    "no_meds": "No medicines yet. Add your first one!",
    "nothing_today": "No doses on this day",
    "delete": "Delete", "deleted": "Deleted", "confirm_del": "Delete this medicine?",
    "n_enable": "Enable notifications",
    "n_methods": "Notification methods",
    "n_push": "Push notifications", "n_sound": "Sound", "n_vib": "Vibration",
    "n_extra": "Additional",
    "n_bg": "Remind even if the app is closed",
    "n_quiet": "Quiet mode (22:00 to 06:00)",
    "profile": "Profile", "personal": "Personal data",
    "app_lang": "App language", "theme": "Theme",
    "help": "Help & support", "about": "About the app",
    "th_title": "Appearance (themes)", "choose_theme": "Choose theme",
    "th_light": "Light", "th_dark": "Dark", "th_blue": "Blue",
    "language": "Language",
    "time_to_take": "Time to take your medicine!",
    "taken": "Taken", "snooze": "Snooze",
    "name": "Name", "email": "Email", "cancel": "Cancel", "ok": "OK",
    "svc_text": "Reminders are active",
    "help_text": "1. Add a medicine with the 'Add medicine' button.\n2. Set the intake times.\n3. Mark doses as taken in the daily schedule.\n\nFor reminders to work when the app is closed, allow notifications and disable battery optimization for MediCare.",
    "about_text": "MediCare helps you remember to take your medicines on time.\n\nThe app follows general recommendations on taking and storing medicines (WHO, FDA, EMA, GMP principles). It is not a medical device and does not replace a doctor.",
    "f_tablet": "Tablets", "f_capsule": "Capsules", "f_syrup": "Syrup", "f_drops": "Drops",
    "f_injection": "Injection", "f_ointment": "Ointment", "f_powder": "Powder",
    "h_after": "After meals", "h_before": "Before meals", "h_during": "During meals",
    "h_any": "Regardless of meals", "h_sleep": "Before sleep",
    "p_morning": "Morning", "p_day": "Day", "p_evening": "Evening", "p_night": "Night",
    "months": ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"],
    "wd_short": ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
    "wd_full": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}

T["ru"] = {
    "app_sub": "Твой помощник\nв приёме лекарств",
    "start": "Начать",
    "choose_lang": "Выберите язык",
    "choose_lang_sub": "Пожалуйста, выберите удобный для вас язык",
    "next": "Далее",
    "g_morning": "Доброе утро,", "g_day": "Добрый день,",
    "g_evening": "Добрый вечер,", "g_night": "Доброй ночи,",
    "dflt_name": "Друг",
    "today": "Сегодня",
    "next_dose": "Следующий приём",
    "show_all": "Показать все",
    "no_next": "На сегодня приёмов больше нет",
    "day_schedule": "Расписание дня",
    "my_meds": "Мои лекарства",
    "add_med": "Добавить лекарство",
    "notifications": "Уведомления",
    "nav_home": "Главная", "nav_cal": "Календарь", "nav_meds": "Лекарства", "nav_profile": "Профиль",
    "add_photo": "Добавить фото", "optional": "(по желанию)",
    "med_name": "Название лекарства *", "dose": "Дозировка (например: 500 мг) *",
    "form": "Форма выпуска", "how": "Как принимать",
    "times": "Время приёма", "add_time": "Добавить время",
    "course": "Курс, дней (пусто — постоянно)",
    "note": "Назначение (по желанию)",
    "from_db": "Выбрать из базы лекарств",
    "save": "Сохранить",
    "fill_required": "Заполните название и дозировку",
    "need_time": "Добавьте хотя бы одно время",
    "saved": "Сохранено",
    "details": "Детали лекарства",
    "how_to": "Как принимать", "intake_time": "Время приёма", "course_t": "Курс",
    "purpose": "Назначение",
    "open_instr": "Открыть инструкцию",
    "instruction": "Инструкция",
    "no_instr": "Для этого лекарства нет встроенной инструкции. Следуйте листку-вкладышу и назначению врача.",
    "disclaimer": "Информация носит справочный характер и не заменяет инструкцию производителя и консультацию врача.",
    "close": "Закрыть",
    "days_unit": "дн.", "ongoing": "Постоянно",
    "no_meds": "Лекарств пока нет. Добавьте первое!",
    "nothing_today": "На этот день приёмов нет",
    "delete": "Удалить", "deleted": "Удалено", "confirm_del": "Удалить это лекарство?",
    "n_enable": "Включить уведомления",
    "n_methods": "Способы уведомлений",
    "n_push": "Push-уведомления", "n_sound": "Звук", "n_vib": "Вибрация",
    "n_extra": "Дополнительно",
    "n_bg": "Напоминать, даже если приложение закрыто",
    "n_quiet": "Тихий режим (с 22:00 до 06:00)",
    "profile": "Профиль", "personal": "Личные данные",
    "app_lang": "Язык приложения", "theme": "Тема",
    "help": "Справка и поддержка", "about": "О приложении",
    "th_title": "Оформление (темы)", "choose_theme": "Выберите тему",
    "th_light": "Светлая", "th_dark": "Тёмная", "th_blue": "Синяя",
    "language": "Язык",
    "time_to_take": "Время принять лекарство!",
    "taken": "Принял(а)", "snooze": "Отложить",
    "name": "Имя", "email": "Email", "cancel": "Отмена", "ok": "OK",
    "svc_text": "Напоминания активны",
    "help_text": "1. Добавьте лекарство кнопкой «Добавить лекарство».\n2. Укажите время приёма.\n3. Отмечайте приёмы в расписании дня.\n\nЧтобы напоминания приходили при закрытом приложении, разрешите уведомления и отключите для MediCare экономию батареи.",
    "about_text": "MediCare помогает не забывать о приёме лекарств.\n\nПриложение ориентируется на общие рекомендации по приёму и хранению лекарств (принципы ВОЗ, FDA, EMA, GMP). Это не медицинское изделие и не заменяет врача.",
    "f_tablet": "Таблетки", "f_capsule": "Капсулы", "f_syrup": "Сироп", "f_drops": "Капли",
    "f_injection": "Инъекции", "f_ointment": "Мазь", "f_powder": "Порошок",
    "h_after": "После еды", "h_before": "Перед едой", "h_during": "Во время еды",
    "h_any": "Независимо от еды", "h_sleep": "Перед сном",
    "p_morning": "Утро", "p_day": "День", "p_evening": "Вечер", "p_night": "Ночь",
    "months": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля",
               "августа", "сентября", "октября", "ноября", "декабря"],
    "wd_short": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    "wd_full": ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"],
}

# Армянский: недостающие ключи автоматически берутся из английского.
# Желательно показать перевод носителю языка.
T["hy"] = {
    "app_sub": "Քո օգնականը\nդեղերի ընդունման մեջ",
    "start": "Սկսել",
    "choose_lang": "Ընտրեք լեզուն",
    "choose_lang_sub": "Խնդրում ենք ընտրել ձեզ հարմար լեզուն",
    "next": "Հաջորդը",
    "g_morning": "Բարի լույս,", "g_day": "Բարի օր,",
    "g_evening": "Բարի երեկո,", "g_night": "Բարի գիշեր,",
    "dflt_name": "Ընկեր",
    "today": "Այսօր",
    "next_dose": "Հաջորդ ընդունումը",
    "show_all": "Ցույց տալ բոլորը",
    "no_next": "Այսօր ընդունումներ այլևս չկան",
    "day_schedule": "Օրվա ժամանակացույց",
    "my_meds": "Իմ դեղերը",
    "add_med": "Ավելացնել դեղ",
    "notifications": "Ծանուցումներ",
    "nav_home": "Գլխավոր", "nav_cal": "Օրացույց", "nav_meds": "Դեղեր", "nav_profile": "Պրոֆիլ",
    "add_photo": "Ավելացնել լուսանկար", "optional": "(ըստ ցանկության)",
    "med_name": "Դեղի անվանումը *", "dose": "Դոզավորում *",
    "form": "Թողարկման ձև", "how": "Ինչպես ընդունել",
    "times": "Ընդունման ժամը", "add_time": "Ավելացնել ժամ",
    "save": "Պահպանել",
    "saved": "Պահպանվեց",
    "details": "Դեղի մանրամասներ",
    "how_to": "Ինչպես ընդունել", "course_t": "Կուրս",
    "purpose": "Նշանակություն",
    "open_instr": "Բացել հրահանգը",
    "instruction": "Հրահանգ",
    "close": "Փակել",
    "days_unit": "օր", "ongoing": "Մշտապես",
    "delete": "Ջնջել",
    "n_enable": "Միացնել ծանուցումները",
    "n_push": "Push ծանուցումներ", "n_sound": "Ձայն", "n_vib": "Թրթռոց",
    "profile": "Պրոֆիլ", "personal": "Անձնական տվյալներ",
    "app_lang": "Հավելվածի լեզուն", "theme": "Թեմա",
    "th_title": "Ձևավորում (թեմաներ)", "choose_theme": "Ընտրեք թեման",
    "th_light": "Լուսավոր", "th_dark": "Մութ", "th_blue": "Կապույտ",
    "language": "Լեզու",
    "time_to_take": "Դեղ ընդունելու ժամանակն է!",
    "taken": "Ընդունեցի", "snooze": "Հետաձգել",
    "name": "Անուն", "cancel": "Չեղարկել",
    "f_tablet": "Հաբեր", "f_capsule": "Պարկուճներ", "f_syrup": "Օշարակ", "f_drops": "Կաթիլներ",
    "f_injection": "Ներարկում", "f_ointment": "Քսուք", "f_powder": "Փոշի",
    "h_after": "Ուտելուց հետո", "h_before": "Ուտելուց առաջ", "h_during": "Ուտելու ժամանակ",
    "h_any": "Անկախ սնունդից", "h_sleep": "Քնելուց առաջ",
    "p_morning": "Առավոտ", "p_day": "Օր", "p_evening": "Երեկո", "p_night": "Գիշեր",
    "months": ["հունվարի", "փետրվարի", "մարտի", "ապրիլի", "մայիսի", "հունիսի", "հուլիսի",
               "օգոստոսի", "սեպտեմբերի", "հոկտեմբերի", "նոյեմբերի", "դեկտեմբերի"],
    "wd_short": ["Երկ", "Երք", "Չրք", "Հնգ", "Ուր", "Շբթ", "Կիր"],
    "wd_full": ["Երկուշաբթի", "Երեքշաբթի", "Չորեքշաբթի", "Հինգշաբթի", "Ուրբաթ", "Շաբաթ", "Կիրակի"],
}

LANG_NAMES = {"ru": "Русский", "en": "English", "hy": "Հայերեն"}


def _m(key, ru, en, hy, dose_ru, dose_en, dose_hy, form, how, times, days,
       p_ru, p_en, i_ru, i_en):
    return {
        "key": key,
        "name": {"ru": ru, "en": en, "hy": hy},
        "dose": {"ru": dose_ru, "en": dose_en, "hy": dose_hy},
        "form": form, "how": how, "times": times, "days": days,
        "purpose": {"ru": p_ru, "en": p_en},
        "instr": {"ru": i_ru, "en": i_en},
    }


_LIST = [
    _m("paracetamol", "Парацетамол", "Paracetamol", "Պարացետամոլ",
       "500 мг", "500 mg", "500 մգ", "tablet", "after", ["08:00", "16:00", "22:00"], 5,
       "Обезболивающее, жаропонижающее", "Pain reliever, fever reducer",
       "• Взрослым обычно по 1 таблетке (500 мг) до 3–4 раз в день, интервал не менее 4–6 часов.\n"
       "• Не превышайте суточную дозу из инструкции (для взрослых — не более 4 г в сутки).\n"
       "• Не принимайте вместе с другими препаратами с парацетамолом.\n"
       "• Осторожно при болезнях печени и при употреблении алкоголя.\n"
       "• Если температура держится более 3 дней или боль более 5 дней — к врачу.",
       "• Adults usually take 1 tablet (500 mg) up to 3–4 times a day, at least 4–6 hours apart.\n"
       "• Do not exceed the daily maximum on the leaflet (for adults, no more than 4 g per day).\n"
       "• Do not combine with other paracetamol-containing products.\n"
       "• Use caution with liver disease and alcohol.\n"
       "• See a doctor if fever lasts over 3 days or pain over 5 days."),
    _m("ibuprofen", "Ибупрофен", "Ibuprofen", "Իբուպրոֆեն",
       "200 мг", "200 mg", "200 մգ", "tablet", "after", ["09:00", "15:00"], 3,
       "Обезболивающее, противовоспалительное, жаропонижающее", "Pain reliever, anti-inflammatory, fever reducer",
       "• Принимайте во время или после еды, запивая водой.\n"
       "• Используйте минимальную эффективную дозу на самый короткий срок.\n"
       "• Не применяйте при язве желудка, тяжёлых болезнях почек и сердца, в 3 триместре беременности, при аллергии на НПВП.\n"
       "• Не сочетайте с другими НПВП (аспирин, диклофенак).\n"
       "• Если боль или температура не проходят 3 дня — к врачу.",
       "• Take with or after food, with water.\n"
       "• Use the lowest effective dose for the shortest time.\n"
       "• Avoid with stomach ulcers, severe kidney or heart disease, in the 3rd trimester, or with NSAID allergy.\n"
       "• Do not combine with other NSAIDs (aspirin, diclofenac).\n"
       "• See a doctor if pain or fever lasts more than 3 days."),
    _m("vitd3", "Витамин D3", "Vitamin D3", "Վիտամին D3",
       "1000 МЕ", "1000 IU", "1000 ՄՄ", "capsule", "after", ["10:00"], 0,
       "Поддержание уровня витамина D, здоровье костей", "Maintains vitamin D levels, bone health",
       "• Принимайте во время или после еды с жирами — так лучше усваивается.\n"
       "• Не превышайте рекомендуемую суточную дозу; высокие дозы — только по назначению врача.\n"
       "• Врач может назначить анализ на уровень витамина D.",
       "• Take with or after a meal containing fat for better absorption.\n"
       "• Do not exceed the recommended daily dose; high doses only as prescribed.\n"
       "• A doctor may order a vitamin D blood test."),
    _m("magnesium", "Магний", "Magnesium", "Մագնեզիում",
       "250 мг", "250 mg", "250 մգ", "tablet", "after", ["14:00"], 0,
       "Восполнение дефицита магния, поддержка нервной и мышечной систем", "Replenishes magnesium, supports nerves and muscles",
       "• Принимайте во время или после еды, запивая водой.\n"
       "• При болезнях почек — только по назначению врача.\n"
       "• Делайте интервал 2–3 часа с антибиотиками (тетрациклины, хинолоны) и препаратами железа.",
       "• Take with or after food, with water.\n"
       "• With kidney disease, only as prescribed.\n"
       "• Keep a 2–3 hour gap from antibiotics (tetracyclines, quinolones) and iron."),
    _m("omega3", "Омега-3", "Omega-3", "Օմեգա-3",
       "1000 мг", "1000 mg", "1000 մգ", "capsule", "after", ["18:00"], 0,
       "Поддержка сердца и сосудов, жирового обмена", "Supports heart, vessels and fat metabolism",
       "• Принимайте во время еды.\n"
       "• При приёме антикоагулянтов, перед операцией и при аллергии на рыбу — проконсультируйтесь с врачом.\n"
       "• Храните в прохладном месте, плотно закрыв.",
       "• Take with meals.\n"
       "• Consult a doctor if you take anticoagulants, before surgery, or if allergic to fish.\n"
       "• Store in a cool place, tightly closed."),
    _m("melatonin", "Мелатонин", "Melatonin", "Մելատոնին",
       "3 мг", "3 mg", "3 մգ", "tablet", "sleep", ["22:00"], 0,
       "Помощь при нарушениях сна и смене часовых поясов", "Helps with sleep problems and jet lag",
       "• Принимайте за 30–60 минут до сна.\n"
       "• Может вызывать сонливость — не садитесь за руль после приёма.\n"
       "• При беременности, кормлении и аутоиммунных болезнях — только после консультации врача.",
       "• Take 30–60 minutes before bed.\n"
       "• May cause drowsiness — do not drive afterwards.\n"
       "• In pregnancy, breastfeeding or autoimmune disease, consult a doctor first."),
    _m("vitc", "Витамин C", "Vitamin C", "Վիտամին C",
       "500 мг", "500 mg", "500 մգ", "tablet", "after", ["09:00"], 0,
       "Поддержка иммунитета, антиоксидант", "Immune support, antioxidant",
       "• Принимайте после еды.\n"
       "• Большие дозы могут раздражать желудок.\n"
       "• При мочекаменной болезни — только после консультации врача.",
       "• Take after food.\n"
       "• High doses may irritate the stomach.\n"
       "• With kidney stones, consult a doctor first."),
    _m("loratadine", "Лоратадин", "Loratadine", "Լորատադին",
       "10 мг", "10 mg", "10 մգ", "tablet", "any", ["09:00"], 0,
       "Противоаллергическое средство", "Antihistamine for allergies",
       "• 1 таблетка 1 раз в сутки независимо от еды.\n"
       "• У части людей может вызывать сонливость.\n"
       "• Детям, беременным и кормящим — только по назначению врача.",
       "• 1 tablet once a day, with or without food.\n"
       "• May cause drowsiness in some people.\n"
       "• Children, pregnant and breastfeeding women — only as prescribed."),
    _m("omeprazole", "Омепразол", "Omeprazole", "Օմեպրազոլ",
       "20 мг", "20 mg", "20 մգ", "capsule", "before", ["08:00"], 0,
       "Снижает кислотность желудка", "Reduces stomach acid",
       "• Принимайте утром за 30 минут до еды.\n"
       "• Глотайте целиком, не разжёвывая.\n"
       "• Длительный приём — только по назначению врача.",
       "• Take in the morning, 30 minutes before a meal.\n"
       "• Swallow whole, do not chew.\n"
       "• Long-term use only as prescribed."),
]

MEDDB = {e["key"]: e for e in _LIST}
MEDLIST = _LIST


# ---- Дополнения v2: редактирование, история, ошибки, безопасность ----------
T["en"].update({
    "edit": "Edit", "edit_med": "Edit medicine",
    "missed": "Missed",
    "today_reminders": "Today's reminders",
    "stat": "Taken: {a} of {b}",
    "err_save": "Could not save data. Check free storage space.",
    "perm_denied": "Notifications are blocked. Enable them in system settings, otherwise reminders will not appear.",
    "err_name_long": "Name is too long (max 60 characters)",
    "err_dose": "Enter the dosage with a number, e.g. 500 mg",
    "err_course": "Course must be from 1 to 365 days",
    "err_email": "Enter a valid email",
    "important": "Important",
    "disc_text": "MediCare helps you follow treatment already prescribed by your doctor. It does not diagnose, prescribe or select medicines and does not replace medical advice. Never change a dose without your doctor's approval.",
    "about_text": "MediCare helps you follow treatment already prescribed by your doctor and not forget to take your medicines.\n\nThe app does not diagnose, prescribe or select medicines and does not replace a doctor. Never change a dose without your doctor's approval.\n\nThe app itself does not send your data to the internet; it is stored on this device.\n\nThe app follows general recommendations on taking and storing medicines. No compliance with standards and no certification is claimed.",
})

T["ru"].update({
    "edit": "Редактировать", "edit_med": "Редактировать лекарство",
    "missed": "Пропущено",
    "today_reminders": "Напоминания на сегодня",
    "stat": "Принято: {a} из {b}",
    "err_save": "Не удалось сохранить данные. Проверьте свободное место на устройстве.",
    "perm_denied": "Уведомления отключены. Включите их в настройках системы, иначе напоминания не появятся.",
    "err_name_long": "Слишком длинное название (максимум 60 символов)",
    "err_dose": "Укажите дозировку с числом, например: 500 мг",
    "err_course": "Курс должен быть от 1 до 365 дней",
    "err_email": "Введите корректный email",
    "important": "Важно",
    "disc_text": "MediCare помогает соблюдать лечение, уже назначенное врачом. Приложение не ставит диагнозы, не назначает и не подбирает лекарства и не заменяет консультацию врача. Не меняйте дозировку без согласования с врачом.",
    "about_text": "MediCare помогает соблюдать лечение, уже назначенное врачом, и не забывать о приёме лекарств.\n\nПриложение не ставит диагнозы, не назначает и не подбирает лекарства и не заменяет врача. Не меняйте дозировку без согласования с врачом.\n\nПриложение само не отправляет ваши данные в интернет: они хранятся на этом устройстве.\n\nПриложение ориентируется на общие рекомендации по приёму и хранению лекарств. Соответствие стандартам и сертификация не заявляются.",
})

T["hy"].update({
    "edit": "Խմբագրել", "edit_med": "Խմբագրել դեղը",
    "missed": "Բաց թողնված",
    "today_reminders": "Այսօրվա հիշեցումները",
    "stat": "Ընդունված՝ {a} / {b}",
    "important": "Կարևոր",
})

# ---- Дополнения v3: справочник и международные стандарты -------------------
T["en"].update({
    "reference": "Drug reference",
    "reference_sub": "International usage guidance",
    "search_hint": "Search by name or ATC code",
    "no_results": "Nothing found",
    "atc": "ATC code",
    "indications": "Indications",
    "std_dose": "Standard adult dose",
    "max_dose": "Maximum daily dose",
    "avoid": "Do not use if",
    "interactions": "Interactions",
    "storage": "Storage",
    "sources": "Based on",
    "who_eml": "WHO Essential Medicines",
    "add_to_schedule": "Add to schedule",
    "standards": "International standards",
    "ref_disclaimer": "Reference information compiled from public WHO, FDA and EMA guidance. It does not replace the manufacturer's leaflet or your doctor's advice.",
    "limit_warn": "The daily total ({tot} mg) is above the usual maximum ({mx} mg). Check this with your doctor or pharmacist.",
    "save_anyway": "Save anyway",
    "review": "Review",
    "progress": "Today's progress",
    "per_day": "per day",
    "ph_name": "e.g. Paracetamol", "ph_dose": "e.g. 500 mg",
    "lbl_name": "Medicine name *", "lbl_dose": "Dosage *",
    "lbl_form": "Form", "lbl_how": "How to take",
    "sleep_snooze": "Snoozed for 10 minutes",
})
T["ru"].update({
    "reference": "Справочник лекарств",
    "reference_sub": "Международные стандарты применения",
    "search_hint": "Поиск по названию или коду ATC",
    "no_results": "Ничего не найдено",
    "atc": "Код ATC",
    "indications": "Показания",
    "std_dose": "Стандартная доза для взрослых",
    "max_dose": "Максимальная суточная доза",
    "avoid": "Не применять при",
    "interactions": "Взаимодействия",
    "storage": "Хранение",
    "sources": "Основано на",
    "who_eml": "Основные лекарства ВОЗ",
    "add_to_schedule": "Добавить в расписание",
    "standards": "Международные стандарты",
    "ref_disclaimer": "Справочная информация составлена по открытым рекомендациям ВОЗ, FDA и EMA. Она не заменяет инструкцию производителя и совет врача.",
    "limit_warn": "Суточная сумма ({tot} мг) выше обычного максимума ({mx} мг). Уточните у врача или фармацевта.",
    "save_anyway": "Всё равно сохранить",
    "review": "Проверить",
    "progress": "Прогресс за сегодня",
    "per_day": "в сутки",
    "ph_name": "Например: Парацетамол", "ph_dose": "Например: 500 мг",
    "lbl_name": "Название лекарства *", "lbl_dose": "Дозировка *",
    "lbl_form": "Форма выпуска", "lbl_how": "Как принимать",
    "sleep_snooze": "Отложено на 10 минут",
})
T["hy"].update({
    "reference": "Դեղերի տեղեկատու",
    "reference_sub": "Միջազգային ստանդարտներ",
    "standards": "Միջազգային ստանդարտներ",
    "add_to_schedule": "Ավելացնել ժամանակացույցին",
    "search_hint": "Որոնել անունով կամ ATC կոդով",
})


# ---- Завершение армянской локализации ------------------------------------
# Все ключи интерфейса должны существовать для каждого языка. Английский
# остаётся техническим резервом только для ключей, которым ещё не задан перевод.
_HY_EXTRA = {
    "optional": "(ըստ ցանկության)",
    "course": "Կուրսի տևողությունը՝ օրերով (դատարկ՝ շարունակական)",
    "note": "Նպատակ (ըստ ցանկության)",
    "from_db": "Ընտրել դեղերի ցանկից",
    "fill_required": "Լրացրեք դեղի անվանումը և դեղաչափը",
    "need_time": "Ավելացրեք առնվազն մեկ ընդունման ժամ",
    "no_instr": "Այս դեղի համար ներկառուցված հրահանգ չկա։ Հետևեք փաթեթի ներդիրին և բժշկի խորհրդին։",
    "disclaimer": "Տեղեկությունը միայն տեղեկատու է և չի փոխարինում արտադրողի հրահանգին կամ բժշկի խորհրդին։",
    "no_meds": "Դեռ դեղեր չկան։ Ավելացրեք առաջին դեղը։",
    "nothing_today": "Այս օրը ընդունումներ չկան",
    "deleted": "Ջնջված է",
    "confirm_del": "Ջնջե՞լ այս դեղը։",
    "n_methods": "Ծանուցման եղանակներ",
    "n_extra": "Լրացուցիչ",
    "n_bg": "Հիշեցնել նաև հավելվածը փակ լինելու դեպքում",
    "n_quiet": "Լուռ ռեժիմ (22:00–06:00)",
    "help": "Օգնություն և աջակցություն",
    "about": "Հավելվածի մասին",
    "help_text": "1. Ավելացրեք դեղը՝ սեղմելով «Ավելացնել դեղ»։\n2. Նշեք ընդունման ժամերը։\n3. Օրվա ժամանակացույցում նշեք ընդունված դեղաչափերը։\n\nՓակ հավելվածի դեպքում հիշեցումներ ստանալու համար թույլատրեք ծանուցումները և անջատեք MediCare-ի մարտկոցի խնայողությունը։",
    "about_text": "MediCare-ն օգնում է չմոռանալ բժշկի նշանակած դեղերի ընդունման մասին։ Հավելվածը չի ախտորոշում, դեղեր չի նշանակում և չի փոխարինում բժշկի խորհրդին։ Մի փոխեք դեղաչափը առանց բժշկի հետ համաձայնեցնելու։",
    "email": "Էլեկտրոնային փոստ",
    "ok": "Լավ",
    "svc_text": "Հիշեցումները միացված են",
    "err_save": "Չհաջողվեց պահպանել տվյալները։ Ստուգեք սարքի ազատ հիշողությունը։",
    "perm_denied": "Ծանուցումներն արգելափակված են։ Միացրեք դրանք համակարգի կարգավորումներում, հակառակ դեպքում հիշեցումները չեն ցուցադրվի։",
    "err_name_long": "Անվանումը չափազանց երկար է (առավելագույնը՝ 60 նիշ)",
    "err_dose": "Մուտքագրեք դեղաչափը թվով, օրինակ՝ 500 մգ",
    "err_course": "Կուրսը պետք է լինի 1-ից 365 օր",
    "err_email": "Մուտքագրեք ճիշտ էլեկտրոնային փոստի հասցե",
    "disc_text": "MediCare-ն օգնում է հետևել բժշկի կողմից արդեն նշանակված բուժմանը։ Հավելվածը չի ախտորոշում, դեղեր չի նշանակում կամ ընտրում և չի փոխարինում բժշկական խորհրդատվությանը։ Երբեք մի փոխեք դեղաչափը առանց բժշկի համաձայնության։",
    "reference_sub": "Դեղերի օգտագործման վերաբերյալ միջազգային ուղեցույցներ",
    "no_results": "Արդյունքներ չեն գտնվել",
    "atc": "ATC կոդ",
    "indications": "Ցուցումներ",
    "std_dose": "Մեծահասակների սովորական դեղաչափ",
    "max_dose": "Օրական առավելագույն դեղաչափ",
    "avoid": "Չօգտագործել հետևյալ դեպքերում",
    "interactions": "Փոխազդեցություններ",
    "storage": "Պահպանում",
    "sources": "Հիմնված է",
    "who_eml": "ԱՀԿ-ի հիմնական դեղերի ցանկ",
    "ref_disclaimer": "Տեղեկությունը կազմված է ԱՀԿ-ի, FDA-ի և EMA-ի հանրային ուղեցույցների հիման վրա։ Այն չի փոխարինում արտադրողի հրահանգին կամ բժշկի խորհրդին։",
    "limit_warn": "Օրական ընդհանուր դեղաչափը ({tot} մգ) գերազանցում է սովորական առավելագույնը ({mx} մգ)։ Խորհրդակցեք բժշկի կամ դեղագետի հետ։",
    "save_anyway": "Միևնույն է պահպանել",
    "review": "Ստուգել",
    "per_day": "օրական",
    "ph_name": "օրինակ՝ Պարացետամոլ",
    "ph_dose": "օրինակ՝ 500 մգ",
    "lbl_name": "Դեղի անվանումը *",
    "lbl_dose": "Դեղաչափ *",
    "lbl_form": "Դեղաձև",
    "lbl_how": "Ինչպես ընդունել",
    "sleep_snooze": "Հետաձգվել է 10 րոպեով",
    "edit": "Խմբագրել",
    "edit_med": "Խմբագրել դեղը",
    "missed": "Բաց է թողնվել",
    "today_reminders": "Այսօրվա հիշեցումները",
    "stat": "Ընդունված է՝ {a}՝ {b}-ից",
}
T["hy"].update(_HY_EXTRA)

# Add Armenian translations for the built-in medicine descriptions and instructions.
_HY_MED_TEXT = {
    "paracetamol": (
        "Ցավազրկող և ջերմիջեցնող միջոց",
        "• Մեծահասակների դեղաչափը ճշտեք փաթեթի ներդիրով կամ բժշկի/դեղագետի հետ։\n"
        "• Մի համատեղեք պարացետամոլ պարունակող այլ դեղերի հետ։\n"
        "• Լյարդի հիվանդության կամ ալկոհոլի օգտագործման դեպքում խորհրդակցեք բժշկի հետ։\n"
        "• Երկարատև ցավի կամ ջերմության դեպքում դիմեք բժշկի։"
    ),
    "ibuprofen": (
        "Ցավազրկող և հակաբորբոքային միջոց",
        "• Ընդունեք սննդի հետ կամ դրանից հետո՝ ջրով։\n"
        "• Օգտագործեք նվազագույն արդյունավետ դեղաչափը՝ հնարավորինս կարճ ժամանակով։\n"
        "• Ստամոքսի խոցի, երիկամների կամ սրտի ծանր հիվանդության, հղիության երրորդ եռամսյակի կամ ՈՍՀԲԴ-ի ալերգիայի դեպքում մի օգտագործեք առանց բժշկի ցուցման։\n"
        "• Մի համատեղեք այլ ՈՍՀԲԴ-ների հետ առանց բժշկի խորհրդի։"
    ),
    "vitd3": (
        "Օգնում է պահպանել վիտամին D-ի մակարդակը և ոսկրերի առողջությունը",
        "• Ընդունեք սննդի հետ կամ դրանից հետո՝ ըստ փաթեթի հրահանգի։\n"
        "• Մի գերազանցեք առաջարկվող օրական դեղաչափը։ Բարձր դեղաչափերն ընդունեք միայն բժշկի նշանակմամբ։"
    ),
    "magnesium": (
        "Մագնեզիումի լրացում և նյարդամկանային համակարգի աջակցություն",
        "• Ընդունեք սննդի հետ կամ դրանից հետո՝ ջրով։\n"
        "• Երիկամների հիվանդության դեպքում ընդունեք միայն բժշկի ցուցումով։\n"
        "• Հակաբիոտիկներից և երկաթի պատրաստուկներից պահեք 2–3 ժամ ընդմիջում։"
    ),
    "omega3": (
        "Աջակցում է սրտի և անոթների առողջությանը",
        "• Ընդունեք սննդի հետ՝ ըստ փաթեթի հրահանգի։\n"
        "• Հակամակարդիչներ ընդունելու, վիրահատությունից առաջ կամ ձկան նկատմամբ ալերգիայի դեպքում խորհրդակցեք բժշկի հետ։"
    ),
    "melatonin": (
        "Օգնում է քնի կարճատև խանգարումների դեպքում",
        "• Սովորաբար ընդունվում է քնելուց 30–60 րոպե առաջ՝ ըստ բժշկի կամ փաթեթի հրահանգի։\n"
        "• Կարող է առաջացնել քնկոտություն․ ընդունելուց հետո մի վարեք մեքենա։\n"
        "• Հղիության, կրծքով կերակրման կամ աուտոիմուն հիվանդությունների դեպքում նախ խորհրդակցեք բժշկի հետ։"
    ),
    "vitc": (
        "Վիտամին C-ի աղբյուր և հակաօքսիդանտ",
        "• Ընդունեք ըստ փաթեթի հրահանգի։\n"
        "• Բարձր դեղաչափերը կարող են գրգռել ստամոքսը։\n"
        "• Երիկամային քարերի դեպքում նախ խորհրդակցեք բժշկի հետ։"
    ),
    "loratadine": (
        "Հակահիստամինային միջոց ալերգիայի դեպքում",
        "• Օգտագործեք միայն փաթեթի հրահանգին կամ բժշկի ցուցմանը համապատասխան։\n"
        "• Որոշ մարդկանց մոտ կարող է առաջացնել քնկոտություն։\n"
        "• Երեխաների, հղիների և կրծքով կերակրողների համար անհրաժեշտ է բժշկի խորհրդատվություն։"
    ),
    "omeprazole": (
        "Նվազեցնում է ստամոքսի թթվայնությունը",
        "• Ընդունեք առավոտյան՝ սնունդից առաջ, ըստ բժշկի կամ փաթեթի հրահանգի։\n"
        "• Պարկուճը կուլ տվեք ամբողջությամբ, եթե փաթեթի հրահանգը այլ բան չի նշում։\n"
        "• Երկարատև օգտագործումը պետք է համաձայնեցնել բժշկի հետ։"
    ),
}
for _med in MEDLIST:
    _hy_text = _HY_MED_TEXT.get(_med["key"])
    if _hy_text:
        _med["purpose"]["hy"] = _hy_text[0]
        _med["instr"]["hy"] = _hy_text[1]

# Complete the interface dictionaries consistently; English is only the last-resort
# fallback for future keys not yet translated.
for _lang in ("ru", "hy"):
    for _key, _value in T["en"].items():
        T[_lang].setdefault(_key, _HY_EXTRA.get(_key, _value) if _lang == "hy" else _value)

# Improvements to the existing app, with all three interface languages.
T["en"].update({
    "streak_stat": "Completed days: {current} · Best streak: {best}",
    "undo_dose": "Undo this check-off?", "undo": "Undo", "undone": "Check-off undone",
    "search_meds": "Search medicines", "today_short": "Today",
    "foreground_only": "Reminders work while this app is open. Closed-app reminders are not included in this source package.",
    "photo_unavailable": "Photo unavailable. Choose a readable PNG or JPEG file.",
    "ref_disclaimer": "This supplied reference content has not been individually verified against current labels. Source badges are not approvals. Follow your prescription and package leaflet; consult your pharmacist.",
    "sources": "Reference organizations (not product approvals)",
})
T["ru"].update({
    "streak_stat": "Дней подряд: {current} · Лучшая серия: {best}",
    "undo_dose": "Отменить отметку о приёме?", "undo": "Отменить отметку", "undone": "Отметка отменена",
    "search_meds": "Поиск лекарств", "today_short": "Сегодня",
    "foreground_only": "Напоминания работают, пока приложение открыто. Напоминания при закрытом приложении не включены в этот пакет исходников.",
    "photo_unavailable": "Фото недоступно. Выберите доступный файл PNG или JPEG.",
    "ref_disclaimer": "Данные справочника не сверены с актуальными инструкциями для каждого препарата. Значки источников не означают одобрение. Следуйте назначению и инструкции; уточняйте у фармацевта.",
    "sources": "Справочные организации (не одобрения препарата)",
})
T["hy"].update({
    "streak_stat": "Անընդմեջ օրեր՝ {current} · Լավագույնը՝ {best}",
    "undo_dose": "Չեղարկե՞լ ընդունման նշումը։", "undo": "Չեղարկել նշումը", "undone": "Նշումը չեղարկված է",
    "search_meds": "Փնտրել դեղեր", "today_short": "Այսօր",
    "foreground_only": "Հիշեցումները գործում են, երբ հավելվածը բաց է։ Փակ հավելվածի հիշեցումները ներառված չեն այս փաթեթում։",
    "photo_unavailable": "Լուսանկարը հասանելի չէ։ Ընտրեք ընթեռնելի PNG կամ JPEG ֆայլ։",
    "ref_disclaimer": "Տրամադրված տեղեկությունը չի ստուգվել յուրաքանչյուր դեղի արդի հրահանգի հետ։ Աղբյուրների նշանները հաստատումներ չեն։ Հետևեք նշանակմանը և ներդիրին, խորհրդակցեք դեղագետի հետ։",
    "sources": "Տեղեկատու կազմակերպություններ (ոչ հաստատումներ)",
})


# ---- AI-помощник: тексты интерфейса -------------------------------------------
_AI_T = {
    "ru": {
        "ai_assistant": "AI-помощник",
        "ai_assistant_sub": "Расскажите о самочувствии или добавьте лекарство голосом",
        "asst_intro": ("Здравствуйте! Я помощник MediCare. Можете рассказать, как вы себя "
                       "чувствуете, или продиктовать лекарство: название, дозу и время приёма. "
                       "Я не врач и не ставлю диагнозы."),
        "asst_disclaimer": "Помощник не заменяет врача. При тяжёлом состоянии звоните 112.",
        "asst_hint": "Напишите сообщение",
        "asst_speak": "Говорить",
        "asst_thinking": "Помощник думает…",
        "asst_listening": "Слушаю… говорите",
        "asst_no_voice": "Голосовой ввод доступен на телефоне. Напишите сообщение.",
        "asst_voice_fail": "Не удалось распознать речь. Попробуйте ещё раз.",
        "asst_not_configured": "Помощник не подключён: не указан адрес сервера.",
        "asst_err_network": "Нет связи с сервером. Проверьте интернет.",
        "asst_err_rate": "Слишком много запросов. Подождите немного.",
        "asst_err_auth": "Сервер отклонил запрос. Обновите приложение.",
        "asst_err_server": "Сервер временно недоступен. Попробуйте позже.",
        "asst_confirm_title": "Добавить это лекарство?",
        "asst_confirm_times": "Время",
        "asst_confirm_course": "Курс",
        "asst_confirm_check": "Проверьте название, дозу и время. Ошибки распознавания возможны.",
        "asst_yes": "Да, добавить",
        "asst_no": "Нет",
        "asst_added": "Лекарство добавлено",
        "asst_duplicate": "Такое лекарство уже есть в списке",
        "asst_invalid": "Не удалось добавить: данные неполные",
        "asst_emergency": "Это может быть срочно. Позвоните 112 или попросите помощи рядом.",
        "asst_doctor": "Лучше показаться врачу.",
    },
    "en": {
        "ai_assistant": "AI assistant",
        "ai_assistant_sub": "Talk about how you feel or add a medicine by voice",
        "asst_intro": ("Hello! I'm the MediCare assistant. You can tell me how you feel, or "
                       "dictate a medicine: its name, dose and times. I'm not a doctor and "
                       "I don't diagnose."),
        "asst_disclaimer": "The assistant does not replace a doctor. In a severe condition call 112.",
        "asst_hint": "Type a message",
        "asst_speak": "Speak",
        "asst_thinking": "The assistant is thinking…",
        "asst_listening": "Listening… please speak",
        "asst_no_voice": "Voice input is available on the phone. Please type a message.",
        "asst_voice_fail": "Could not recognise speech. Please try again.",
        "asst_not_configured": "Assistant is not connected: server address is not set.",
        "asst_err_network": "No connection to the server. Check your internet.",
        "asst_err_rate": "Too many requests. Please wait a little.",
        "asst_err_auth": "The server rejected the request. Please update the app.",
        "asst_err_server": "Server is temporarily unavailable. Try again later.",
        "asst_confirm_title": "Add this medicine?",
        "asst_confirm_times": "Times",
        "asst_confirm_course": "Course",
        "asst_confirm_check": "Check the name, dose and times. Recognition mistakes are possible.",
        "asst_yes": "Yes, add",
        "asst_no": "No",
        "asst_added": "Medicine added",
        "asst_duplicate": "This medicine is already in your list",
        "asst_invalid": "Could not add: the data is incomplete",
        "asst_emergency": "This may be urgent. Call 112 or ask someone nearby for help.",
        "asst_doctor": "It is better to see a doctor.",
    },
    "hy": {
        "ai_assistant": "AI օգնական",
        "ai_assistant_sub": "Պատմեք ինքնազգացողության մասին կամ ավելացրեք դեղը ձայնով",
        "asst_intro": ("Բարև ձեզ։ Ես MediCare-ի օգնականն եմ։ Կարող եք պատմել, թե ինչպես եք "
                       "զգում, կամ թելադրել դեղը՝ անունը, դեղաչափը և ընդունման ժամերը։ "
                       "Ես բժիշկ չեմ և ախտորոշում չեմ դնում։"),
        "asst_disclaimer": "Օգնականը չի փոխարինում բժշկին։ Ծանր վիճակում զանգահարեք 112։",
        "asst_hint": "Գրեք հաղորդագրություն",
        "asst_speak": "Խոսել",
        "asst_thinking": "Օգնականը մտածում է…",
        "asst_listening": "Լսում եմ… խոսեք",
        "asst_no_voice": "Ձայնային մուտքը հասանելի է հեռախոսում։ Գրեք հաղորդագրություն։",
        "asst_voice_fail": "Չհաջողվեց ճանաչել խոսքը։ Փորձեք կրկին։",
        "asst_not_configured": "Օգնականը միացված չէ՝ սերվերի հասցեն նշված չէ։",
        "asst_err_network": "Սերվերի հետ կապ չկա։ Ստուգեք ինտերնետը։",
        "asst_err_rate": "Չափազանց շատ հարցումներ։ Մի փոքր սպասեք։",
        "asst_err_auth": "Սերվերը մերժեց հարցումը։ Թարմացրեք հավելվածը։",
        "asst_err_server": "Սերվերը ժամանակավորապես անհասանելի է։ Փորձեք ավելի ուշ։",
        "asst_confirm_title": "Ավելացնե՞լ այս դեղը",
        "asst_confirm_times": "Ժամեր",
        "asst_confirm_course": "Կուրս",
        "asst_confirm_check": "Ստուգեք անունը, դեղաչափը և ժամերը։ Ճանաչման սխալներ հնարավոր են։",
        "asst_yes": "Այո, ավելացնել",
        "asst_no": "Ոչ",
        "asst_added": "Դեղն ավելացվեց",
        "asst_duplicate": "Այս դեղն արդեն ցանկում է",
        "asst_invalid": "Չհաջողվեց ավելացնել՝ տվյալները թերի են",
        "asst_emergency": "Սա կարող է շտապ լինել։ Զանգահարեք 112 կամ օգնություն խնդրեք մոտակայքում գտնվողից։",
        "asst_doctor": "Ավելի լավ է դիմել բժշկի։",
    },
}
for _lang, _tx in _AI_T.items():
    T[_lang].update(_tx)


# ---- Напоминания в фоне, голосовые команды, проверка расписания, согласие ----------
# Армянские тексты нужно проверить носителем языка.
_V2_T = {
    "ru": {
        "rem_dose_title": "Пора принять лекарство",
        "rem_missed_title": "Приём не отмечен",
        "rem_missed_text": "Не отмечено: {names} ({tm}). Если не уверены, принимали ли вы, не принимайте двойную дозу — спросите врача или фармацевта.",
        "rem_refresh_title": "Откройте MediCare",
        "rem_refresh_text": "Откройте приложение, чтобы напоминания на следующие дни продолжили приходить.",
        "rem_channel_name": "Напоминания о лекарствах",
        "bg_info": "Напоминания приходят, даже если приложение закрыто. На некоторых телефонах (Xiaomi, Huawei, Samsung) разрешите MediCare работать в фоне в настройках батареи.",
        "asst_check": "Проверить расписание",
        "asst_check_cmd": "проверь расписание",
        "vc_confirm_title": "Отметить как принятое?",
        "vc_confirm_taken": "Вы подтверждаете, что приняли:\n{items}",
        "vc_none_to_mark": "Не нашёл приёма, который можно отметить сейчас. Посмотрите расписание на главном экране.",
        "sched_warn_title": "Проверьте расписание",
        "asst_consent_title": "Отправить сообщение помощнику?",
        "asst_consent_text": "Чтобы ответить, помощник отправляет ваше сообщение и список ваших лекарств (названия, дозы, время) на сервер MediCare, а оттуда — в сервис ИИ Anthropic. Наш сервер переписку не сохраняет. Не пишите лишних личных данных: фамилию, адрес, номера документов. Помощник не заменяет врача. Согласны?",
        "asst_consent_yes": "Согласен",
        "asst_consent_no": "Не сейчас",
    },
    "en": {
        "rem_dose_title": "Time to take your medicine",
        "rem_missed_title": "Dose not marked",
        "rem_missed_text": "Not marked: {names} ({tm}). If you are not sure whether you took it, do not take a double dose — ask a doctor or pharmacist.",
        "rem_refresh_title": "Open MediCare",
        "rem_refresh_text": "Open the app so reminders for the coming days keep arriving.",
        "rem_channel_name": "Medicine reminders",
        "bg_info": "Reminders arrive even when the app is closed. On some phones (Xiaomi, Huawei, Samsung) allow MediCare to run in the background in the battery settings.",
        "asst_check": "Check schedule",
        "asst_check_cmd": "check my schedule",
        "vc_confirm_title": "Mark as taken?",
        "vc_confirm_taken": "Do you confirm you took:\n{items}",
        "vc_none_to_mark": "I could not find a dose that can be marked now. Please look at the schedule on the home screen.",
        "sched_warn_title": "Check your schedule",
        "asst_consent_title": "Send the message to the assistant?",
        "asst_consent_text": "To reply, the assistant sends your message and your medicine list (names, doses, times) to the MediCare server, and from there to the Anthropic AI service. Our server does not store the conversation. Do not write unnecessary personal data: surname, address, document numbers. The assistant does not replace a doctor. Do you agree?",
        "asst_consent_yes": "I agree",
        "asst_consent_no": "Not now",
    },
    "hy": {
        "rem_dose_title": "Դեղ ընդունելու ժամն է",
        "rem_missed_title": "Ընդունումը չի նշված",
        "rem_missed_text": "Չի նշված՝ {names} ({tm})։ Եթե վստահ չեք՝ ընդունե՞լ եք, կրկնակի չափաբաժին մի ընդունեք. հարցրեք բժշկին կամ դեղագործին։",
        "rem_refresh_title": "Բացեք MediCare-ը",
        "rem_refresh_text": "Բացեք հավելվածը, որպեսզի հաջորդ օրերի հիշեցումները շարունակեն գալ։",
        "rem_channel_name": "Դեղերի հիշեցումներ",
        "bg_info": "Հիշեցումները գալիս են նաև հավելվածը փակ լինելու դեպքում։ Որոշ հեռախոսներում (Xiaomi, Huawei, Samsung) մարտկոցի կարգավորումներում թույլատրեք MediCare-ի աշխատանքը ֆոնում։",
        "asst_check": "Ստուգել ժամանակացույցը",
        "asst_check_cmd": "ստուգիր ժամանակացույցը",
        "vc_confirm_title": "Նշե՞լ որպես ընդունված",
        "vc_confirm_taken": "Հաստատո՞ւմ եք, որ ընդունել եք՝\n{items}",
        "vc_none_to_mark": "Չգտա ընդունում, որը հիմա կարելի է նշել։ Տեսեք ժամանակացույցը գլխավոր էկրանին։",
        "sched_warn_title": "Ստուգեք ժամանակացույցը",
        "asst_consent_title": "Ուղարկե՞լ հաղորդագրությունը օգնականին",
        "asst_consent_text": "Պատասխանելու համար օգնականը ձեր հաղորդագրությունը և դեղերի ցանկը (անուններ, դեղաչափեր, ժամեր) ուղարկում է MediCare-ի սերվերին, այնտեղից՝ Anthropic-ի արհեստական բանականության ծառայությանը։ Մեր սերվերը գրագրությունը չի պահում։ Մի գրեք ավելորդ անձնական տվյալներ՝ ազգանուն, հասցե, փաստաթղթերի համարներ։ Օգնականը չի փոխարինում բժշկին։ Համա՞ձայն եք։",
        "asst_consent_yes": "Համաձայն եմ",
        "asst_consent_no": "Ոչ հիմա",
    },
}
for _lang, _tx in _V2_T.items():
    T[_lang].update(_tx)


# --- удаление данных (приватность) -------------------------------------------------------
# Армянские тексты нужно проверить носителем языка (как и остальные).
_V3_T = {
    "ru": {
        "wipe_row": "Удалить мои данные",
        "wipe_title": "Удалить все данные?",
        "wipe_text": "Все лекарства, отметки о приёме, фото и согласие на работу помощника будут "
                     "удалены с этого телефона. Это нельзя отменить.",
        "wipe_done": "Данные удалены",
    },
    "en": {
        "wipe_row": "Delete my data",
        "wipe_title": "Delete all data?",
        "wipe_text": "All medicines, intake marks, photos and the assistant consent will be removed "
                     "from this phone. This cannot be undone.",
        "wipe_done": "Data deleted",
    },
    "hy": {
        "wipe_row": "Ջնջել իմ տվյալները",
        "wipe_title": "Ջնջե՞լ բոլոր տվյալները",
        "wipe_text": "Բոլոր դեղերը, ընդունման նշումները, լուսանկարները և օգնականի համաձայնությունը "
                     "կջնջվեն այս հեռախոսից։ Սա հնարավոր չէ չեղարկել։",
        "wipe_done": "Տվյալները ջնջված են",
    },
}
for _lang, _tx in _V3_T.items():
    T[_lang].update(_tx)
