# -*- coding: utf-8 -*-
"""Справочник лекарств: код ATC (ВОЗ), показания, дозы, ограничения, источники.

ВАЖНО: данные справочные и обобщённые. Они не заменяют инструкцию производителя
и назначение врача. Перед выпуском приложения сверьте каждую запись с актуальными
документами ВОЗ (EML), FDA (label) и EMA (SmPC) или проверьте у фармацевта.
Для армянского языка при отсутствии перевода показывается английский текст.
"""

# Источники: WHO = Model List of Essential Medicines, FDA = US label, EMA = SmPC
SRC_WHO, SRC_FDA, SRC_EMA = "WHO", "FDA", "EMA"


def _d(key, atc, ru, en, hy, cls_ru, cls_en, sources, who_eml,
       use_ru, use_en, dose_ru, dose_en, maxd_ru, maxd_en,
       avoid_ru, avoid_en, inter_ru, inter_en, store_ru, store_en,
       form="tablet", how="after", times=("08:00",), days=0, dose_short=""):
    return {
        "key": key, "atc": atc,
        "name": {"ru": ru, "en": en, "hy": hy},
        "cls": {"ru": cls_ru, "en": cls_en},
        "sources": list(sources), "who_eml": who_eml,
        "use": {"ru": use_ru, "en": use_en},
        "dose": {"ru": dose_ru, "en": dose_en},
        "max": {"ru": maxd_ru, "en": maxd_en},
        "avoid": {"ru": avoid_ru, "en": avoid_en},
        "inter": {"ru": inter_ru, "en": inter_en},
        "store": {"ru": store_ru, "en": store_en},
        "form": form, "how": how, "times": list(times), "days": days,
        "dose_short": dose_short,
    }


DRUGS = [
    _d("paracetamol", "N02BE01", "Парацетамол", "Paracetamol", "Պարացետամոլ",
       "Анальгетик, жаропонижающее", "Analgesic, antipyretic",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Боль слабой и умеренной интенсивности, повышенная температура.",
       "Mild to moderate pain, fever.",
       "Взрослым 500–1000 мг каждые 4–6 часов.",
       "Adults 500–1000 mg every 4–6 hours.",
       "Не более 4 г в сутки (при риске для печени — меньше).",
       "No more than 4 g per day (less if liver risk).",
       "Тяжёлые болезни печени, регулярный алкоголь, приём других препаратов с парацетамолом.",
       "Severe liver disease, regular alcohol use, other paracetamol-containing products.",
       "Варфарин (усиление эффекта при длительном приёме), алкоголь.",
       "Warfarin (effect may increase with long use), alcohol.",
       "При комнатной температуре, в сухом месте, вдали от детей.",
       "Room temperature, dry place, out of reach of children.",
       times=("08:00", "16:00", "22:00"), days=5, dose_short="500 mg"),

    _d("ibuprofen", "M01AE01", "Ибупрофен", "Ibuprofen", "Իբուպրոֆեն",
       "НПВП", "NSAID",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Боль, воспаление, повышенная температура.",
       "Pain, inflammation, fever.",
       "Взрослым 200–400 мг каждые 6–8 часов во время или после еды.",
       "Adults 200–400 mg every 6–8 hours with or after food.",
       "Безрецептурно — до 1200 мг в сутки; выше — только по назначению врача.",
       "Over the counter up to 1200 mg per day; higher only if prescribed.",
       "Язва желудка, тяжёлые болезни почек или сердца, аллергия на НПВП, 3 триместр беременности.",
       "Stomach ulcer, severe kidney or heart disease, NSAID allergy, 3rd trimester of pregnancy.",
       "Аспирин и другие НПВП, антикоагулянты, диуретики, ингибиторы АПФ.",
       "Aspirin and other NSAIDs, anticoagulants, diuretics, ACE inhibitors.",
       "До 25 °C, в сухом месте.", "Below 25 °C, dry place.",
       times=("09:00", "15:00"), days=3, dose_short="200 mg"),

    _d("aspirin", "N02BA01", "Ацетилсалициловая кислота", "Acetylsalicylic acid", "Ացետիլսալիցիլաթթու",
       "НПВП, антиагрегант", "NSAID, antiplatelet",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Боль, температура; в малых дозах — профилактика тромбозов по назначению врача.",
       "Pain, fever; low dose for clot prevention when prescribed.",
       "Обезболивание: 500–1000 мг до 3 раз в день после еды. Профилактика: 75–100 мг раз в день только по назначению.",
       "Pain: 500–1000 mg up to 3 times daily after food. Prevention: 75–100 mg once daily only if prescribed.",
       "Для обезболивания — не более 3 г в сутки.",
       "For pain relief no more than 3 g per day.",
       "Дети и подростки с вирусной инфекцией (риск синдрома Рея), язва, склонность к кровотечениям, астма на НПВП.",
       "Children and teens with viral infection (Reye's syndrome), ulcer, bleeding tendency, NSAID-induced asthma.",
       "Антикоагулянты, другие НПВП, метотрексат, алкоголь.",
       "Anticoagulants, other NSAIDs, methotrexate, alcohol.",
       "В сухом месте при комнатной температуре.", "Dry place at room temperature.",
       days=0, dose_short="500 mg"),

    _d("amoxicillin", "J01CA04", "Амоксициллин", "Amoxicillin", "Ամոքսիցիլին",
       "Антибиотик (пенициллины)", "Antibiotic (penicillins)",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Бактериальные инфекции дыхательных путей, ЛОР-органов, мочевыводящих путей — только по назначению врача.",
       "Bacterial infections of airways, ENT, urinary tract; prescription only.",
       "Взрослым обычно 500 мг каждые 8 часов или 1 г каждые 12 часов, курс определяет врач.",
       "Adults usually 500 mg every 8 hours or 1 g every 12 hours; course set by a doctor.",
       "Не превышайте дозу, назначенную врачом. Курс нужно закончить.",
       "Do not exceed the prescribed dose. Finish the full course.",
       "Аллергия на пенициллины и цефалоспорины, инфекционный мононуклеоз.",
       "Allergy to penicillins or cephalosporins, infectious mononucleosis.",
       "Метотрексат, варфарин, пробенецид; может снижать действие гормональных контрацептивов.",
       "Methotrexate, warfarin, probenecid; may reduce hormonal contraceptives.",
       "До 25 °C; суспензию хранить по инструкции.", "Below 25 °C; store suspension as directed.",
       form="capsule", how="any", times=("08:00", "16:00", "00:00"), days=7, dose_short="500 mg"),

    _d("metformin", "A10BA02", "Метформин", "Metformin", "Մետֆորմին",
       "Сахароснижающее", "Antidiabetic",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Сахарный диабет 2 типа — по назначению врача.",
       "Type 2 diabetes; prescription only.",
       "Начинают с 500 мг 1–2 раза в день во время еды, дозу повышает врач.",
       "Usually start at 500 mg once or twice daily with meals; dose adjusted by a doctor.",
       "Обычно до 2000–3000 мг в сутки по назначению.",
       "Usually up to 2000–3000 mg per day as prescribed.",
       "Тяжёлая почечная недостаточность, острые состояния с риском лактоацидоза, злоупотребление алкоголем.",
       "Severe kidney failure, acute conditions with lactic acidosis risk, heavy alcohol use.",
       "Йодсодержащие контрастные вещества (приём приостанавливают), алкоголь.",
       "Iodinated contrast agents (therapy is paused), alcohol.",
       "При комнатной температуре.", "Room temperature.",
       how="during", times=("08:00", "20:00"), dose_short="500 mg"),

    _d("omeprazole", "A02BC01", "Омепразол", "Omeprazole", "Օմեպրազոլ",
       "Ингибитор протонной помпы", "Proton pump inhibitor",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Изжога, ГЭРБ, язва желудка по назначению.",
       "Heartburn, GERD, stomach ulcer when prescribed.",
       "Взрослым 20 мг один раз в день за 30–60 минут до завтрака.",
       "Adults 20 mg once daily 30–60 minutes before breakfast.",
       "Обычно 20–40 мг в сутки; без врача — курс не более 2 недель.",
       "Usually 20–40 mg per day; self-treatment no longer than 2 weeks.",
       "Аллергия на компоненты; при длительном приёме нужен контроль врача.",
       "Allergy to ingredients; long-term use needs medical supervision.",
       "Клопидогрел, метотрексат, некоторые противогрибковые средства.",
       "Clopidogrel, methotrexate, some antifungals.",
       "До 25 °C, в сухом месте.", "Below 25 °C, dry place.",
       form="capsule", how="before", times=("07:30",), days=14, dose_short="20 mg"),

    _d("loratadine", "R06AX13", "Лоратадин", "Loratadine", "Լորատադին",
       "Антигистаминное", "Antihistamine",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Аллергический ринит, крапивница.", "Allergic rhinitis, urticaria.",
       "Взрослым и детям старше 12 лет 10 мг один раз в день.",
       "Adults and children over 12: 10 mg once daily.",
       "10 мг в сутки.", "10 mg per day.",
       "Аллергия на компоненты; при болезнях печени дозу снижает врач.",
       "Allergy to ingredients; liver disease needs dose adjustment.",
       "Кетоконазол, эритромицин, циметидин могут повышать концентрацию.",
       "Ketoconazole, erythromycin, cimetidine may raise levels.",
       "До 25 °C.", "Below 25 °C.",
       how="any", times=("09:00",), days=10, dose_short="10 mg"),

    _d("cetirizine", "R06AE07", "Цетиризин", "Cetirizine", "Ցետիրիզին",
       "Антигистаминное", "Antihistamine",
       (SRC_FDA, SRC_EMA), False,
       "Аллергический ринит, крапивница.", "Allergic rhinitis, urticaria.",
       "Взрослым 10 мг один раз в день, вечером при сонливости.",
       "Adults 10 mg once daily; take in the evening if drowsy.",
       "10 мг в сутки.", "10 mg per day.",
       "Тяжёлая почечная недостаточность; осторожно за рулём.",
       "Severe kidney failure; use caution when driving.",
       "Алкоголь и седативные средства усиливают сонливость.",
       "Alcohol and sedatives increase drowsiness.",
       "До 25 °C.", "Below 25 °C.",
       how="any", times=("21:00",), days=10, dose_short="10 mg"),

    _d("vitd3", "A11CC05", "Витамин D3 (колекальциферол)", "Vitamin D3 (cholecalciferol)", "Վիտամին D3",
       "Витамин", "Vitamin",
       (SRC_WHO, SRC_EMA), True,
       "Профилактика и лечение дефицита витамина D, здоровье костей.",
       "Prevention and treatment of vitamin D deficiency, bone health.",
       "Профилактика у взрослых обычно 600–2000 МЕ в день; лечебные дозы — по назначению.",
       "Adult prevention usually 600–2000 IU daily; treatment doses as prescribed.",
       "Без наблюдения врача обычно не более 4000 МЕ в сутки.",
       "Without medical supervision usually no more than 4000 IU per day.",
       "Гиперкальциемия, камни в почках, саркоидоз.",
       "Hypercalcemia, kidney stones, sarcoidosis.",
       "Тиазидные диуретики, препараты кальция (контроль уровня кальция).",
       "Thiazide diuretics, calcium supplements (calcium monitoring).",
       "В защищённом от света месте.", "Protect from light.",
       form="capsule", how="after", times=("10:00",), dose_short="1000 IU"),

    _d("magnesium", "A12CC", "Магний", "Magnesium", "Մագնեզիում",
       "Минеральная добавка", "Mineral supplement",
       (SRC_EMA,), False,
       "Восполнение дефицита магния, поддержка нервной и мышечной систем.",
       "Magnesium deficiency, support of nerves and muscles.",
       "Взрослым обычно 250–400 мг элементарного магния в сутки.",
       "Adults usually 250–400 mg elemental magnesium per day.",
       "Для добавок — как правило, не более 350 мг в сутки без врача.",
       "For supplements generally no more than 350 mg per day without medical advice.",
       "Тяжёлая почечная недостаточность.", "Severe kidney failure.",
       "Разделяйте на 2–3 часа с тетрациклинами, хинолонами и препаратами железа.",
       "Separate by 2–3 hours from tetracyclines, quinolones and iron.",
       "При комнатной температуре.", "Room temperature.",
       how="after", times=("14:00",), dose_short="250 mg"),

    _d("omega3", "C10AX06", "Омега-3", "Omega-3", "Օմեգա-3",
       "Жирные кислоты", "Fatty acids",
       (SRC_EMA, SRC_FDA), False,
       "Поддержка сердечно-сосудистой системы по рекомендации врача.",
       "Cardiovascular support as advised by a doctor.",
       "Обычно 250–500 мг ЭПК+ДГК в сутки с едой.",
       "Usually 250–500 mg EPA+DHA daily with food.",
       "Более 3 г в сутки — только под наблюдением врача.",
       "More than 3 g per day only under medical supervision.",
       "Аллергия на рыбу, нарушения свёртывания, предстоящая операция.",
       "Fish allergy, bleeding disorders, upcoming surgery.",
       "Антикоагулянты и антиагреганты.", "Anticoagulants and antiplatelets.",
       "В прохладном месте.", "Cool place.",
       form="capsule", how="after", times=("18:00",), dose_short="1000 mg"),

    _d("melatonin", "N05CH01", "Мелатонин", "Melatonin", "Մելատոնին",
       "Регулятор сна", "Sleep regulator",
       (SRC_EMA,), False,
       "Кратковременные нарушения сна, смена часовых поясов.",
       "Short-term sleep problems, jet lag.",
       "Обычно 1–3 мг за 30–60 минут до сна.",
       "Usually 1–3 mg 30–60 minutes before bedtime.",
       "Как правило, не более 5 мг в сутки без врача.",
       "Generally no more than 5 mg per day without a doctor.",
       "Беременность и кормление, аутоиммунные заболевания — только после консультации.",
       "Pregnancy, breastfeeding, autoimmune disease: consult a doctor first.",
       "Алкоголь, седативные препараты, флувоксамин.",
       "Alcohol, sedatives, fluvoxamine.",
       "В защищённом от света месте.", "Protect from light.",
       how="sleep", times=("22:00",), dose_short="3 mg"),

    _d("amlodipine", "C08CA01", "Амлодипин", "Amlodipine", "Ամլոդիպին",
       "Антигипертензивное", "Antihypertensive",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Артериальная гипертензия, стенокардия — по назначению врача.",
       "Hypertension, angina; prescription only.",
       "Начальная доза обычно 5 мг один раз в день.",
       "Starting dose usually 5 mg once daily.",
       "Обычно до 10 мг в сутки.", "Usually up to 10 mg per day.",
       "Выраженная гипотония, тяжёлый аортальный стеноз, аллергия.",
       "Marked hypotension, severe aortic stenosis, allergy.",
       "Симвастатин (ограничение дозы), грейпфрутовый сок, кларитромицин.",
       "Simvastatin (dose limit), grapefruit juice, clarithromycin.",
       "До 25 °C.", "Below 25 °C.",
       how="any", times=("08:00",), dose_short="5 mg"),

    _d("atorvastatin", "C10AA05", "Аторвастатин", "Atorvastatin", "Ատորվաստատին",
       "Статин", "Statin",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Снижение холестерина и сердечно-сосудистого риска — по назначению.",
       "Lowering cholesterol and cardiovascular risk; prescription only.",
       "Обычно 10–40 мг один раз в день в одно и то же время.",
       "Usually 10–40 mg once daily at the same time.",
       "Обычно до 80 мг в сутки по назначению.",
       "Usually up to 80 mg per day as prescribed.",
       "Активные болезни печени, беременность и кормление.",
       "Active liver disease, pregnancy and breastfeeding.",
       "Кларитромицин, противогрибковые средства, грейпфрутовый сок, фибраты.",
       "Clarithromycin, antifungals, grapefruit juice, fibrates.",
       "До 25 °C.", "Below 25 °C.",
       how="any", times=("21:00",), dose_short="20 mg"),

    _d("salbutamol", "R03AC02", "Сальбутамол", "Salbutamol", "Սալբուտամոլ",
       "Бронхолитик", "Bronchodilator",
       (SRC_WHO, SRC_FDA, SRC_EMA), True,
       "Приступы бронхиальной астмы — быстрое облегчение.",
       "Asthma attacks; quick relief.",
       "Обычно 1–2 ингаляции (100 мкг на вдох) при приступе, по назначению врача.",
       "Usually 1–2 puffs (100 mcg each) for symptoms, as prescribed.",
       "Если нужен чаще, чем обычно, обратитесь к врачу.",
       "If you need it more often than usual, see a doctor.",
       "Аллергия на компоненты; осторожно при болезнях сердца и тиреотоксикозе.",
       "Allergy to ingredients; caution with heart disease or thyrotoxicosis.",
       "Бета-блокаторы снижают эффект.", "Beta-blockers reduce the effect.",
       "Не нагревать баллон, защищать от прямого солнца.",
       "Do not heat the canister; protect from direct sun.",
       form="drops", how="any", times=("08:00",), dose_short="100 mcg"),

    _d("ors", "A07CA", "Регидратационные соли", "Oral rehydration salts", "Ռեհիդրատացիոն աղեր",
       "Регидратация", "Rehydration",
       (SRC_WHO,), True,
       "Потеря жидкости при диарее и рвоте.", "Fluid loss from diarrhea and vomiting.",
       "Пакет растворяют в указанном на упаковке объёме воды; пить небольшими глотками.",
       "Dissolve a sachet in the water volume stated on the pack; sip slowly.",
       "По инструкции; при тяжёлом обезвоживании нужна помощь врача.",
       "As directed; severe dehydration needs medical care.",
       "Кишечная непроходимость, тяжёлая рвота без возможности пить.",
       "Intestinal obstruction, persistent vomiting with inability to drink.",
       "Нет значимых.", "No significant interactions.",
       "Готовый раствор хранить в холодильнике до 24 часов.",
       "Keep prepared solution refrigerated up to 24 hours.",
       form="powder", how="any", times=("09:00", "15:00"), days=2, dose_short="1 sachet"),
]

# Հայերեն թարգմանություններ։ Դեղաչափերը տեղեկատու են և չեն փոխարինում բժշկի նշանակմանը։
HY_TRANSLATIONS = {
    "paracetamol": {
        "cls": "Ցավազրկող, ջերմիջեցնող",
        "use": "Թեթև և միջին ուժգնության ցավ, բարձր ջերմություն։",
        "dose": "Մեծահասակներին՝ 500–1000 մգ յուրաքանչյուր 4–6 ժամը մեկ։",
        "max": "Օրական առավելագույնը՝ 4 գ․ լյարդի խնդիրների դեպքում՝ ավելի քիչ։",
        "avoid": "Լյարդի ծանր հիվանդություն, ալկոհոլի կանոնավոր օգտագործում կամ պարացետամոլ պարունակող այլ դեղեր ընդունել։",
        "inter": "Վարֆարին (երկարատև օգտագործման դեպքում ազդեցությունը կարող է ուժեղանալ), ալկոհոլ։",
        "store": "Պահել սենյակային ջերմաստիճանում, չոր վայրում և երեխաներից հեռու։",
    },
    "ibuprofen": {
        "cls": "Ոչ ստերոիդային հակաբորբոքային դեղ (ՈՍՀԲԴ)",
        "use": "Ցավ, բորբոքում, բարձր ջերմություն։",
        "dose": "Մեծահասակներին՝ 200–400 մգ յուրաքանչյուր 6–8 ժամը մեկ՝ սննդի հետ կամ դրանից հետո։",
        "max": "Առանց դեղատոմսի՝ օրական մինչև 1200 մգ․ ավելի բարձր դեղաչափը՝ միայն բժշկի նշանակմամբ։",
        "avoid": "Ստամոքսի խոց, երիկամների կամ սրտի ծանր հիվանդություն, ՈՍՀԲԴ-ի նկատմամբ ալերգիա, հղիության երրորդ եռամսյակ։",
        "inter": "Ասպիրին և այլ ՈՍՀԲԴ-ներ, հակամակարդիչներ, միզամուղներ, ԱՓՖ ինհիբիտորներ։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում, չոր վայրում։",
    },
    "aspirin": {
        "cls": "ՈՍՀԲԴ, հակաթրոմբոցիտային միջոց",
        "use": "Ցավ և ջերմություն․ փոքր դեղաչափերով՝ թրոմբների կանխարգելման համար միայն բժշկի նշանակմամբ։",
        "dose": "Ցավի դեպքում՝ 500–1000 մգ օրական մինչև 3 անգամ՝ ուտելուց հետո։ Կանխարգելման համար՝ 75–100 մգ օրական մեկ անգամ՝ միայն բժշկի նշանակմամբ։",
        "max": "Ցավազրկման համար՝ օրական առավելագույնը 3 գ։",
        "avoid": "Երեխաներ և դեռահասներ՝ վիրուսային վարակի դեպքում (Ռեյի համախտանիշի վտանգ), խոց, արյունահոսության հակում, ՈՍՀԲԴ-ով պայմանավորված ասթմա։",
        "inter": "Հակամակարդիչներ, այլ ՈՍՀԲԴ-ներ, մեթոտրեքսատ, ալկոհոլ։",
        "store": "Պահել չոր վայրում՝ սենյակային ջերմաստիճանում։",
    },
    "amoxicillin": {
        "cls": "Հակաբիոտիկ (պենիցիլինների խումբ)",
        "use": "Շնչուղիների, ԼՕՌ օրգանների և միզուղիների բակտերիալ վարակներ՝ միայն բժշկի նշանակմամբ։",
        "dose": "Մեծահասակներին սովորաբար՝ 500 մգ յուրաքանչյուր 8 ժամը մեկ կամ 1 գ յուրաքանչյուր 12 ժամը մեկ․ բուժման տևողությունը որոշում է բժիշկը։",
        "max": "Մի գերազանցեք բժշկի նշանակած դեղաչափը։ Ավարտեք նշանակված բուժման կուրսը։",
        "avoid": "Ալերգիա պենիցիլինների կամ ցեֆալոսպորինների նկատմամբ, վարակիչ մոնոնուկլեոզ։",
        "inter": "Մեթոտրեքսատ, վարֆարին, պրոբենեցիդ․ կարող է նվազեցնել հորմոնալ հակաբեղմնավորիչների արդյունավետությունը։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում․ կախույթը պահել ըստ հրահանգի։",
    },
    "metformin": {
        "cls": "Արյան շաքարը նվազեցնող դեղ",
        "use": "2-րդ տիպի շաքարային դիաբետ՝ բժշկի նշանակմամբ։",
        "dose": "Սովորաբար սկսում են 500 մգ-ից՝ օրական 1–2 անգամ, սննդի հետ․ դեղաչափը կարգավորում է բժիշկը։",
        "max": "Սովորաբար օրական մինչև 2000–3000 մգ՝ բժշկի նշանակմամբ։",
        "avoid": "Երիկամային ծանր անբավարարություն, լակտացիդոզի վտանգով սուր վիճակներ, ալկոհոլի չարաշահում։",
        "inter": "Յոդ պարունակող կոնտրաստային նյութեր (դեղի ընդունումը կարող է ժամանակավորապես դադարեցվել), ալկոհոլ։",
        "store": "Պահել սենյակային ջերմաստիճանում։",
    },
    "omeprazole": {
        "cls": "Պրոտոնային պոմպի ինհիբիտոր",
        "use": "Այրոց, գաստրոէզոֆագեալ ռեֆլյուքսային հիվանդություն, ստամոքսի խոց՝ բժշկի ցուցումով։",
        "dose": "Մեծահասակներին՝ 20 մգ օրական մեկ անգամ՝ նախաճաշից 30–60 րոպե առաջ։",
        "max": "Սովորաբար օրական 20–40 մգ․ առանց բժշկի խորհրդի ինքնուրույն բուժումը՝ առավելագույնը 2 շաբաթ։",
        "avoid": "Բաղադրիչների նկատմամբ ալերգիա․ երկարատև ընդունման դեպքում անհրաժեշտ է բժշկական վերահսկողություն։",
        "inter": "Կլոպիդոգրել, մեթոտրեքսատ, որոշ հակասնկային դեղեր։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում, չոր վայրում։",
    },
    "loratadine": {
        "cls": "Հակահիստամինային դեղ",
        "use": "Ալերգիկ ռինիտ, եղնջացան։",
        "dose": "Մեծահասակներին և 12 տարեկանից բարձր երեխաներին՝ 10 մգ օրական մեկ անգամ։",
        "max": "Օրական 10 մգ։",
        "avoid": "Բաղադրիչների նկատմամբ ալերգիա․ լյարդի հիվանդության դեպքում դեղաչափը որոշում է բժիշկը։",
        "inter": "Կետոկոնազոլը, էրիթրոմիցինը և ցիմետիդինը կարող են բարձրացնել դեղի խտությունը։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում։",
    },
    "cetirizine": {
        "cls": "Հակահիստամինային դեղ",
        "use": "Ալերգիկ ռինիտ, եղնջացան։",
        "dose": "Մեծահասակներին՝ 10 մգ օրական մեկ անգամ․ քնկոտության դեպքում ընդունել երեկոյան։",
        "max": "Օրական 10 մգ։",
        "avoid": "Երիկամային ծանր անբավարարություն․ զգուշություն՝ մեքենա վարելիս։",
        "inter": "Ալկոհոլը և հանգստացնող դեղերը կարող են ուժեղացնել քնկոտությունը։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում։",
    },
    "vitd3": {
        "cls": "Վիտամին",
        "use": "Վիտամին D-ի պակասի կանխարգելում և բուժում, ոսկրերի առողջություն։",
        "dose": "Մեծահասակների կանխարգելիչ դեղաչափը սովորաբար օրական 600–2000 ՄՄ է․ բուժական դեղաչափերը՝ բժշկի նշանակմամբ։",
        "max": "Առանց բժշկական հսկողության սովորաբար՝ օրական ոչ ավելի, քան 4000 ՄՄ։",
        "avoid": "Հիպերկալցեմիա, երիկամների քարեր, սարկոիդոզ։",
        "inter": "Թիազիդային միզամուղներ, կալցիումի հավելումներ (անհրաժեշտ է վերահսկել կալցիումի մակարդակը)։",
        "store": "Պահել լույսից պաշտպանված վայրում։",
    },
    "magnesium": {
        "cls": "Հանքային հավելում",
        "use": "Մագնեզիումի պակասի լրացում, նյարդային և մկանային համակարգերի աջակցություն։",
        "dose": "Մեծահասակներին սովորաբար՝ օրական 250–400 մգ տարրական մագնեզիում։",
        "max": "Հավելումների համար սովորաբար՝ օրական առավելագույնը 350 մգ առանց բժշկի խորհրդի։",
        "avoid": "Երիկամային ծանր անբավարարություն։",
        "inter": "Տետրացիկլիններից, քինոլոններից և երկաթի պատրաստուկներից ընդունել 2–3 ժամ տարբերությամբ։",
        "store": "Պահել սենյակային ջերմաստիճանում։",
    },
    "omega3": {
        "cls": "Ճարպաթթուներ",
        "use": "Սրտանոթային համակարգի աջակցություն՝ բժշկի խորհրդով։",
        "dose": "Սովորաբար օրական 250–500 մգ EPA+DHA՝ սննդի հետ։",
        "max": "Օրական 3 գ-ից ավելի՝ միայն բժշկական հսկողությամբ։",
        "avoid": "Ձկան նկատմամբ ալերգիա, արյան մակարդելիության խանգարումներ, նախատեսվող վիրահատություն։",
        "inter": "Հակամակարդիչներ և հակաթրոմբոցիտային դեղեր։",
        "store": "Պահել զով վայրում։",
    },
    "melatonin": {
        "cls": "Քունը կարգավորող միջոց",
        "use": "Քնի կարճատև խանգարումներ, ժամային գոտիների փոփոխություն։",
        "dose": "Սովորաբար 1–3 մգ՝ քնելուց 30–60 րոպե առաջ։",
        "max": "Առանց բժշկի խորհրդի սովորաբար՝ օրական առավելագույնը 5 մգ։",
        "avoid": "Հղիություն, կրծքով կերակրում կամ աուտոիմուն հիվանդություններ՝ նախապես բժշկի հետ խորհրդակցել։",
        "inter": "Ալկոհոլ, հանգստացնող դեղեր, ֆլուվոքսամին։",
        "store": "Պահել լույսից պաշտպանված վայրում։",
    },
    "amlodipine": {
        "cls": "Արյան ճնշումը նվազեցնող դեղ",
        "use": "Զարկերակային գերճնշում, ստենոկարդիա՝ բժշկի նշանակմամբ։",
        "dose": "Սկզբնական դեղաչափը սովորաբար 5 մգ օրական մեկ անգամ է։",
        "max": "Սովորաբար օրական մինչև 10 մգ։",
        "avoid": "Արտահայտված հիպոտոնիա, աորտայի ծանր ստենոզ, ալերգիա։",
        "inter": "Սիմվաստատին (դեղաչափի սահմանափակում), գրեյպֆրուտի հյութ, կլարիթրոմիցին։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում։",
    },
    "atorvastatin": {
        "cls": "Ստատին",
        "use": "Խոլեստերինի և սրտանոթային ռիսկի նվազեցում՝ բժշկի նշանակմամբ։",
        "dose": "Սովորաբար 10–40 մգ օրական մեկ անգամ՝ ամեն օր նույն ժամին։",
        "max": "Սովորաբար օրական մինչև 80 մգ՝ բժշկի նշանակմամբ։",
        "avoid": "Լյարդի ակտիվ հիվանդություն, հղիություն և կրծքով կերակրում։",
        "inter": "Կլարիթրոմիցին, հակասնկային դեղեր, գրեյպֆրուտի հյութ, ֆիբրատներ։",
        "store": "Պահել 25 °C-ից ցածր ջերմաստիճանում։",
    },
    "salbutamol": {
        "cls": "Բրոնխալայնիչ",
        "use": "Բրոնխային ասթմայի նոպաների արագ թեթևացում։",
        "dose": "Սովորաբար՝ 1–2 ներշնչում (յուրաքանչյուրը՝ 100 մկգ) ախտանշանների դեպքում՝ բժշկի ցուցումով։",
        "max": "Եթե դեղը սովորականից հաճախ է անհրաժեշտ, դիմեք բժշկի։",
        "avoid": "Բաղադրիչների նկատմամբ ալերգիա․ զգուշություն՝ սրտային հիվանդությունների և թիրեոտոքսիկոզի դեպքում։",
        "inter": "Բետա-պաշարիչները կարող են նվազեցնել ազդեցությունը։",
        "store": "Բալոնը չտաքացնել, պաշտպանել արևի ուղիղ ճառագայթներից։",
    },
    "ors": {
        "cls": "Բերանային ռեհիդրատացիոն միջոց",
        "use": "Փորլուծության կամ փսխման հետևանքով հեղուկի կորուստ։",
        "dose": "Փաթեթի պարունակությունը լուծել փաթեթի վրա նշված ջրի ծավալում և խմել փոքր կումերով։",
        "max": "Օգտագործել ըստ հրահանգի․ ծանր ջրազրկման դեպքում անհրաժեշտ է բժշկական օգնություն։",
        "avoid": "Աղիքային անանցանելիություն, շարունակական փսխում՝ հեղուկ խմելու անհնարինությամբ։",
        "inter": "Էական փոխազդեցություններ հայտնի չեն։",
        "store": "Պատրաստված լուծույթը պահել սառնարանում՝ մինչև 24 ժամ։",
    },
}

for _drug in DRUGS:
    _hy = HY_TRANSLATIONS.get(_drug["key"], {})
    for _field, _translation in _hy.items():
        _drug[_field]["hy"] = _translation


DRUGDB = {d["key"]: d for d in DRUGS}
DRUG_LIST = DRUGS

SOURCE_INFO = {
    "WHO": {"ru": "Модельный список основных лекарств ВОЗ", "en": "WHO Model List of Essential Medicines", "hy": "ԱՀԿ-ի հիմնական դեղերի մոդելային ցանկ"},
    "FDA": {"ru": "Инструкция (label) Управления по санитарному надзору США", "en": "US FDA drug label", "hy": "ԱՄՆ FDA-ի դեղի պաշտոնական հրահանգ"},
    "EMA": {"ru": "Характеристика препарата (SmPC) Европейского агентства по лекарствам",
            "en": "EMA Summary of Product Characteristics (SmPC)",
            "hy": "Եվրոպական դեղերի գործակալության դեղի բնութագիր (SmPC)"},
}


def search(query, lang="ru"):
    """Поиск по названию (любой язык), коду ATC и классу."""
    q = (query or "").strip().lower()
    if not q:
        return list(DRUGS)
    out = []
    for d in DRUGS:
        hay = [v.lower() for v in d["name"].values()]
        hay.append(d["atc"].lower())
        hay += [v.lower() for v in d["cls"].values()]
        if any(q in h for h in hay):
            out.append(d)
    return out


def daily_total_mg(med):
    """Оценивает суточную дозу, только если поле dose — одно однозначное число
    в мг или граммах («500 мг», «1 г», «0,5 g»).

    Диапазоны («500–1000 мг»), «2 таблетки», мкг/МЕ/мл намеренно не считаются,
    чтобы не создавать ложных предупреждений.
    """
    import re

    dose = med.get("dose", "")
    if isinstance(dose, dict):
        # Callers should pass the already-selected localized string.
        return None
    dose = str(dose or "").strip()
    match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*(мг|mg|մգ|г|гр|g|գ)\.?", dose, re.I)
    if not match:
        return None
    unit = match.group(2).lower()
    factor = 1.0 if unit in ("мг", "mg", "մգ") else 1000.0

    times = med.get("times", [])
    if not isinstance(times, (list, tuple)) or not times:
        return None
    return float(match.group(1).replace(",", ".")) * factor * len(times)
