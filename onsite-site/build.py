#!/usr/bin/env python3
"""Static site generator for onsite.uz (RU / UZ / EN).

Run:  python3 build.py
Output: ./site/  (upload the contents of this folder to the web server root)

All texts live in CONTENT below. Contacts live in CONFIG.
"""
import html
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")

# --------------------------------------------------------------------------
# CONFIG — replace with company contacts if they differ
# --------------------------------------------------------------------------
CONFIG = {
    "base": "https://onsite.uz",
    "company": "ONSITE",
    "phone": "+998901888557",
    "phone_display": "+998 90 188 85 57",
    "email": "info@onsite.uz",
    "telegram": "https://t.me/sdalimov",
    "linkedin": "https://www.linkedin.com/in/sherozbek-dalimov-16016221/",
    "og_image": "/images/sherozbek-dalimov.jpg",
    "lastmod": date.today().isoformat(),
}

LANGS = ["ru", "uz", "en"]
OG_LOCALE = {"ru": "ru_RU", "uz": "uz_UZ", "en": "en_US"}

PATHS = {
    "home": {"ru": "/", "uz": "/uz/", "en": "/en/"},
    "product": {"ru": "/antiscalant-clean-ro.html", "uz": "/uz/antiskalant-clean-ro.html", "en": "/en/antiscalant-clean-ro.html"},
    "industries": {"ru": "/industries.html", "uz": "/uz/tarmoqlar.html", "en": "/en/industries.html"},
    "service": {"ru": "/dosing-service.html", "uz": "/uz/dozalash-xizmati.html", "en": "/en/dosing-service.html"},
    "cases": {"ru": "/projects-cases.html", "uz": "/uz/loyihalar-keyslar.html", "en": "/en/projects-cases.html"},
    "about": {"ru": "/about.html", "uz": "/uz/biz-haqimizda.html", "en": "/en/about.html"},
    "news": {"ru": "/news.html", "uz": "/uz/yangiliklar.html", "en": "/en/news.html"},
}
NAV_ORDER = ["home", "product", "industries", "service", "cases", "about"]

# --------------------------------------------------------------------------
# CONTENT
# --------------------------------------------------------------------------
CONTENT = {
# ============================== RU ==============================
"ru": {
    "nav": {"home": "Главная", "product": "CLEAN RO", "industries": "Отрасли", "service": "Сервис",
            "cases": "Кейсы", "about": "О компании", "news": "Новости"},
    "nav_cta": "Запросить расчёт",
    "contact_note": "Из Узбекистана удобнее позвонить. Из-за рубежа — email или Telegram.",
    "btn_call": "Позвонить", "btn_email": "Email", "btn_tg": "Telegram",
    "footer_about": "Производитель антискалантов CLEAN RO для систем обратного осмоса. Ташкент, Узбекистан.",
    "footer_more": "О компании",
    "footer_products": "Продукция", "footer_company": "Компания", "footer_contacts": "Контакты",
    "footer_dosing": "Расчёт дозировки",
    "footer_rights": "© 2026 ONSITE. Все права защищены.",
    "footer_city": "г. Ташкент, Алмазарский р-н, ул. Генерала Гафурова, тупик 2, д. 16",
    "cs_labels": ["Задача", "Решение", "Результат"],
    "pages": {
        "home": {
            "title": "ONSITE — производитель антискалантов CLEAN RO в Узбекистане",
            "desc": "Антискаланты CLEAN RO и CLEAN RO-1 для обратного осмоса от производителя в Ташкенте. Бесплатный расчёт дозировки, поставка со склада, оплата в сумах.",
            "eyebrow": "Производство антискалантов в Узбекистане",
            "h1": "Антискаланты CLEAN RO — защита мембран обратного осмоса от накипи",
            "lead": "Производим фосфонатные антискаланты в Ташкенте и рассчитываем дозировку по анализу вашей воды. Поставка со склада, оплата в сумах, поддержка инженера.",
            "cta1": "Запросить расчёт дозировки", "cta2": "Продукция",
            "tiles_badge": "Продукция и сервис",
            "tiles_h2": "Антискалант и инженерная поддержка — от одного поставщика",
            "tiles_p": "Мы не просто продаём реагент: подбираем продукт и дозировку под вашу воду и сопровождаем установку после запуска.",
            "tiles": [
                ["Продукт", "CLEAN RO", "Щелочной антискалант (pH 10,0–11,5) для обратного осмоса, нано- и ультрафильтрации. Ингибирует отложения карбонатов и сульфатов, дозировка 3–10 мг/л.", "Подробнее о CLEAN RO", "product", "#clean-ro"],
                ["Продукт", "CLEAN RO-1", "Кислотный антискалант (pH 1,5–1,7) для тех же систем. Для питьевой воды допускается до 7 г/т — применяется на производстве бутилированной воды.", "Подробнее о CLEAN RO-1", "product", "#clean-ro-1"],
                ["Сервис", "Расчёт дозировки и поддержка", "Бесплатный расчёт дозировки по анализу исходной воды, помощь с пуском и мониторинг работы установки инженером ONSITE.", "Подробнее о сервисе", "service", ""],
            ],
            "why_badge": "Почему ONSITE",
            "why_h2": "Местное производство с инженерной экспертизой международного уровня",
            "why": [
                ["Собственное производство", "Антискаланты производятся в Ташкенте, продукция всегда есть на складе."],
                ["Быстрая поставка и оплата в сумах", "Без импорта, таможни и валютного риска. Доставка по всему Узбекистану."],
                ["Инженерная поддержка", "Техническая экспертиза команды — 8 лет в Nalco Water (An Ecolab Company): расчёт дозировки, пуск, мониторинг."],
                ["Документы на продукт", "TDS и SDS на каждый продукт — для технических служб и отделов закупок."],
            ],
            "stats": [["40 т", "мощность производства в месяц"], ["−15%", "затраты на водоподготовку, АО «НГМК», ГМЗ-3"]],
            "ind_badge": "Отрасли", "ind_h2": "Где применяются антискаланты CLEAN RO", "ind_link": "Все отрасли",
            "ind": [
                ["Горнодобыча и металлургия", "Обратный осмос для технической, питьевой и обессоленной воды на ГОК и ГМЗ."],
                ["Пищевая промышленность и напитки", "Бутилированная вода, напитки, пивоварение, молочные производства."],
                ["Автомобилестроение", "Технологическая вода для окрасочных цехов и производственных линий."],
                ["Строительство и здания", "Установки обратного осмоса в жилых комплексах, отелях и бизнес-центрах."],
            ],
            "cases_badge": "Подтверждённые результаты", "cases_h2": "Кейсы наших клиентов", "cases_link": "Все кейсы",
            "news_badge": "Новости", "news_h2": "Последние обновления", "news_link": "Все новости",
            "faq_badge": "Вопросы", "faq_h2": "Частые вопросы",
            "faq": [
                ["Что такое антискалант и зачем он нужен?", "Антискалант — реагент, который дозируется в исходную воду перед обратным осмосом и не даёт солям жёсткости выпадать в осадок на мембранах. Без него мембраны быстрее зарастают, падает производительность, растут расходы на промывки и замену мембран."],
                ["Чем отличаются CLEAN RO и CLEAN RO-1?", "CLEAN RO — щелочной продукт (pH 10,0–11,5, плотность 1,20 г/см³), CLEAN RO-1 — кислотный (pH 1%-го раствора 1,5–1,7, плотность 1,10 г/см³). Оба ингибируют отложения карбонатов и сульфатов. Для питьевой воды CLEAN RO дозируют не более 5 г/т, CLEAN RO-1 — не более 7 г/т. Какой продукт подходит вашей установке, определяем по анализу воды."],
                ["Как рассчитывается дозировка?", "Типичная дозировка — 3–10 мг/л, стандартно 5 г на тонну подпиточной воды. Точная доза зависит от анализа исходной воды (жёсткость, щёлочность, сульфаты, кремний, железо, pH, солесодержание) и параметров установки (производительность, выход пермеата, тип мембран). Расчёт бесплатный."],
                ["В какой таре поставляется и сколько хранится?", "Канистра 25 кг, бочка 240 кг или IBC 1300 кг. Срок хранения — не менее 36 месяцев в закрытой заводской таре при +5…+25 °C. Температура замерзания −3 °C, зимой продукт нужно беречь от мороза."],
                ["Есть ли технические документы на продукт?", "Да, на каждый продукт есть TDS (техническое описание) и SDS (паспорт безопасности). Отправим по запросу."],
                ["Как происходит оплата и доставка?", "Работаем по договору, оплата в сумах. Поставляем со склада в Ташкенте с доставкой по всему Узбекистану."],
            ],
            "cta_h2": "Пришлите анализ воды — рассчитаем дозировку",
            "cta_p": "Опишите установку обратного осмоса и приложите анализ исходной воды — подберём продукт и дозировку бесплатно.",
        },
        "product": {
            "title": "Антискаланты CLEAN RO и CLEAN RO-1 для обратного осмоса — ONSITE",
            "desc": "Фосфонатные антискаланты CLEAN RO и CLEAN RO-1 для мембран обратного осмоса и нанофильтрации. Производство в Ташкенте, TDS и SDS, бесплатный расчёт дозировки.",
            "tag": "Продукция · Антискаланты",
            "h1": "Антискаланты CLEAN RO и CLEAN RO-1",
            "lead": "Фосфонатные ингибиторы накипеобразования для систем обратного осмоса и нанофильтрации. Производитель — ONSITE, Ташкент.",
            "summary": "CLEAN RO и CLEAN RO-1 — антискаланты производства ONSITE (Ташкент, Узбекистан) на основе органических комплексонов для обратного осмоса, нано- и ультрафильтрации. Ингибируют отложения карбонатов и сульфатов; дозировка 3–10 мг/л (стандартно 5 г/т). Фасовка 25 кг, 240 кг и 1300 кг; срок хранения 36 месяцев.",
            "line_badge": "Линейка продуктов", "line_h2": "Два продукта — одна задача: чистые мембраны",
            "spec_labels": ["Вид", "Цвет", "pH", "Плотность", "Основа", "Дозировка", "Питьевая вода", "Мембраны", "Фасовка", "Срок хранения"],
            "spec_ro": ["Жидкость", "От бесцветного до слегка жёлтого", "10,0–11,5", "1,20 г/см³", "Органические комплексоны", "3–10 мг/л, стандартно 5 г/т", "Не более 5 г/т подпиточной воды", "Все полиамидные", "Канистра 25 кг, бочка 240 кг, IBC 1300 кг", "36 месяцев при +5…+25 °C"],
            "spec_ro1": ["Жидкость", "От бесцветного до слегка жёлтого", "1,5–1,7 (1% раствор)", "1,10 ± 0,02 г/см³", "Органические комплексоны", "3–10 мг/л, стандартно 5 г/т", "Не более 7 г/т подпиточной воды", "Все полиамидные", "Канистра 25 кг, бочка 240 кг, IBC 1300 кг", "36 месяцев при +5…+25 °C"],
            "tag_ro": "Щелочной антискалант · pH 10,0–11,5",
            "tag_ro1": "Кислотный антискалант · pH 1,5–1,7 (1%)",
            "p_clean_ro": "Антискалант для обратного осмоса, нано- и ультрафильтрации. Стабилизирует пересыщенные солевые растворы, ингибирует отложения карбонатов и сульфатов металлов и содержит компоненты для удаления уже имеющихся солей с поверхности мембран.",
            "p_clean_ro_1": "Кислотный антискалант для обратного осмоса, нано- и ультрафильтрации с теми же функциями. Для питьевой воды допускает дозировку до 7 г/т — применяется на производстве бутилированной воды (Refresh Water).",
            "how_badge": "Преимущества", "how_h2": "Что дают CLEAN RO и CLEAN RO-1",
            "how": [
                "Ингибируют отложения карбонатов и сульфатов металлов",
                "Работают на широком спектре качества воды",
                "Во многих программах обработки не требуют дозирования соляной или другой кислоты",
                "Содержат компоненты для удаления уже имеющихся солей с поверхности мембран",
                "Совместимы со всеми мембранами на основе полиамидов",
                "Продлевают интервал между химическими промывками и срок службы мембран",
            ],
            "hand_badge": "Дозирование и хранение", "hand_h2": "Как применять и хранить",
            "hand": [
                "Подавайте продукт постоянно, из закрытой ёмкости, без контакта с атмосферой",
                "Настройте дозирующий насос на максимальную частоту и корректируйте дозировку",
                "Насосы, линии и ёмкости — из ПВХ, полиэтилена, тефлона или нержавеющей стали",
                "Не допускайте контакта неразбавленного продукта с алюминием, латунью и углеродистой сталью",
                "Хранение: не менее 36 месяцев в закрытой заводской таре при +5…+25 °C; температура замерзания −3 °C",
                "Средства защиты при работе: очки и резиновые перчатки",
            ],
            "steps_badge": "Как начать", "steps_h2": "Начало работы — 4 шага",
            "steps": [
                ["Анализ воды", "Вы присылаете анализ исходной воды и данные установки"],
                ["Расчёт", "Подбираем продукт и дозировку — бесплатно"],
                ["Поставка и пуск", "Поставляем со склада и помогаем настроить дозирование"],
                ["Мониторинг", "Следим за показателями установки и корректируем дозировку"],
            ],
            "price_amount": "40", "price_unit": "тонн в месяц — мощность производства",
            "price_note": "Склад в Ташкенте, поставка по всему Узбекистану",
            "price_h4": "Условия поставки",
            "price_list": [
                "Фасовка: канистра 25 кг, бочка 240 кг, IBC 1300 кг",
                "Цена — по запросу, зависит от объёма и формата поставки",
                "Оплата в сумах по договору",
                "TDS и SDS предоставляются с поставкой",
                "Бесплатный расчёт дозировки перед первой поставкой",
            ],
            "cta_h2": "Запросите TDS, SDS и расчёт дозировки",
            "cta_p": "Напишите, для какой установки нужен антискалант, — отправим документы и предложение.",
        },
        "industries": {
            "title": "Антискаланты для горнодобычи, пищевой промышленности и других отраслей — ONSITE",
            "desc": "Антискаланты CLEAN RO для установок обратного осмоса в горнодобыче, пищевой промышленности, автомобилестроении, строительстве и энергетике Узбекистана.",
            "tag": "Отрасли",
            "h1": "Антискаланты для вашей отрасли",
            "lead": "Установки обратного осмоса работают на воде разного состава и в разных режимах. Подбираем продукт и дозировку под задачу конкретного производства.",
            "grid_badge": "Области применения", "grid_h2": "С какими предприятиями работаем",
            "cards": [
                ["Горнодобыча и металлургия", "Обратный осмос для технической, питьевой и обессоленной воды на горно-обогатительных комбинатах и гидрометаллургических заводах. Высокая жёсткость и сульфаты требуют точного расчёта дозировки.", "Кейс: АО «НГМК», ГМЗ-3 — −15% затрат на водоподготовку"],
                ["Пищевая промышленность и напитки", "Бутилированная вода, безалкогольные напитки, пивоварение, молочные и соковые производства. Стабильное качество пермеата и предсказуемые промывки.", "Кейс: Refresh Water — CLEAN RO-1"],
                ["Автомобилестроение", "Обессоленная вода для окрасочных цехов, мойки и технологических линий.", "Кейс: SamAvto — подбор антискаланта"],
                ["Строительство и здания", "Установки обратного осмоса в жилых комплексах, гостиницах, бизнес-центрах и на объектах инфраструктуры.", ""],
                ["Энергетика и котельные", "Подготовка подпиточной воды для паровых и водогрейных котлов, где обратный осмос стоит перед ионным обменом или EDI.", ""],
                ["Другие отрасли", "Фармацевтика, химическая промышленность, лаборатории и другие производства с установками обратного осмоса.", ""],
            ],
            "crit_badge": "Критерии подбора", "crit_h2": "Что влияет на выбор антискаланта",
            "crit": [
                "Жёсткость и щёлочность исходной воды", "Сульфаты, барий и стронций", "Кремний и железо",
                "pH и температура воды", "Выход пермеата и число ступеней установки", "Тип и производитель мембран",
            ],
            "cta_h2": "Расскажите о вашем производстве",
            "cta_p": "Подберём антискалант под состав воды и режим работы вашей установки.",
        },
        "service": {
            "title": "Расчёт дозировки антискаланта — бесплатно | ONSITE",
            "desc": "Бесплатный расчёт дозировки антискаланта по анализу воды, пуск и мониторинг установки обратного осмоса. Инженерная поддержка ONSITE в Узбекистане.",
            "tag": "Сервис",
            "h1": "Расчёт дозировки и техническая поддержка",
            "lead": "Антискалант работает только при правильной дозировке. Рассчитываем её по анализу вашей воды и сопровождаем установку после запуска.",
            "summary": "Расчёт дозировки антискаланта CLEAN RO — бесплатно, по анализу исходной воды и параметрам установки обратного осмоса.",
            "inc_badge": "Что входит", "inc_h2": "От расчёта до сопровождения установки",
            "inc": [
                "Бесплатный расчёт дозировки по анализу исходной воды",
                "Подбор продукта: CLEAN RO или CLEAN RO-1",
                "Помощь в настройке дозирующего насоса",
                "Пуск и инструктаж операторов",
                "Мониторинг: давление, перепад давления, выход пермеата, электропроводность",
                "Рекомендации по химической промывке мембран",
            ],
            "need_badge": "Для расчёта", "need_h2": "Что прислать",
            "need": [
                ["Анализ исходной воды", "Кальций, магний, щёлочность, сульфаты, хлориды, кремний, железо, барий и стронций (если есть), pH, солесодержание или электропроводность, температура."],
                ["Параметры установки", "Производительность, выход пермеата, число ступеней, тип и количество мембран."],
                ["Текущая схема", "Используемый антискалант и его дозировка, история промывок, основные проблемы."],
            ],
            "steps_badge": "Как проходит", "steps_h2": "От заявки до работы установки",
            "steps": [
                ["Заявка", "Присылаете анализ воды и данные установки"],
                ["Расчёт", "Готовим расчёт дозировки и предложение"],
                ["Пуск", "Поставка, настройка дозирования, инструктаж"],
                ["Сопровождение", "Мониторинг показателей и корректировка дозировки"],
            ],
            "note": "Технической поддержкой занимается инженер с опытом 8 лет в Nalco Water (An Ecolab Company).",
            "cta_h2": "Отправьте анализ воды",
            "cta_p": "Рассчитаем дозировку и пришлём предложение.",
        },
        "cases": {
            "title": "Кейсы: антискаланты для НГМК, SamAvto, Refresh Water | ONSITE",
            "desc": "Проекты ONSITE: поставка антискаланта для АО «НГМК» ГМЗ-3 (−15% затрат), подбор антискаланта для SamAvto, CLEAN RO-1 для Refresh Water.",
            "tag": "Кейсы",
            "h1": "Проекты и кейсы",
            "lead": "Что сделано на каждом объекте — с результатами и подтверждающими документами.",
            "cta_h2": "Следующий кейс — ваше предприятие",
            "cta_p": "Пришлите анализ воды — подберём антискалант и дозировку.",
        },
        "about": {
            "title": "О компании ONSITE — производство антискалантов в Ташкенте",
            "desc": "ONSITE — узбекистанский производитель антискалантов CLEAN RO для обратного осмоса. Производство в Ташкенте, 40 тонн в месяц, инженерная поддержка.",
            "tag": "О компании",
            "h1": "ONSITE — производитель антискалантов в Узбекистане",
            "lead": "Производим антискаланты для обратного осмоса и помогаем предприятиям снижать затраты на водоподготовку.",
            "prose": [
                "ONSITE — узбекистанская компания, которая производит антискаланты для систем обратного осмоса под брендом CLEAN RO. Производство находится в Ташкенте, мощность — 40 тонн в месяц.",
                "Наши продукты CLEAN RO и CLEAN RO-1 созданы на основе фосфонатов. Их применяют предприятия горнодобывающей и пищевой промышленности, автомобилестроения, строительства и других отраслей.",
                "Техническую экспертизу компании обеспечивает Шерозбек Долимов — инженер по промышленной водоподготовке. Он 8 лет проработал в Nalco Water (An Ecolab Company), учился в Национальном университете Узбекистана и Кембриджском университете.",
                "Мы продаём не просто реагент, а результат: подбираем продукт и дозировку под состав вашей воды, помогаем с пуском и следим за работой установки.",
            ],
            "photo_alt": "Шерозбек Долимов, ONSITE",
            "stats": [["40 т", "мощность в месяц"], ["8 лет", "опыт в Nalco Water"]],
            "exp_badge": "Что мы делаем", "exp_h2": "Производство, сервис и документы",
            "exp": [
                ["Производство", "Выпуск антискалантов в Ташкенте и запас продукции на складе."],
                ["Инженерная поддержка", "Расчёт дозировки, пуск, мониторинг и рекомендации по промывкам мембран."],
                ["Документы", "TDS и SDS на каждый продукт, договор и закрывающие документы для отдела закупок."],
            ],
            "cta_h2": "Свяжитесь с нами",
            "cta_p": "Напишите о задаче вашего предприятия — ответим и предложим решение.",
        },
        "news": {
            "title": "Новости ONSITE — антискаланты CLEAN RO",
            "desc": "Новые проекты, продукты и события компании ONSITE — производителя антискалантов CLEAN RO в Узбекистане.",
            "tag": "Новости",
            "h1": "Новости ONSITE",
            "lead": "Новые проекты, продукты и события компании.",
            "cta_h2": "Обсудим вашу установку",
            "cta_p": "Пришлите анализ воды — рассчитаем дозировку бесплатно.",
        },
    },
    "cases": [
        {"badge": "Поставка антискаланта · Горнодобыча", "kicker": "Горнодобыча · Поставка", "name": "АО «НГМК», ГМЗ-3", "proof": "Договор, −15% затрат",
         "short": "Поставлено более 10 тонн антискаланта, подобранного под параметры воды.",
         "task": "Затраты предприятия на водоподготовку были выше, чем позволяла имеющаяся схема реагентов.",
         "sol": "Поставлено более 10 тонн антискаланта, подобранного под параметры воды и технологический процесс предприятия.",
         "res": "Расходы на водоподготовку снижены на 15%. Поставка оформлена договором."},
        {"badge": "Подбор антискаланта для обратного осмоса · Автомобилестроение", "kicker": "Автомобилестроение · Подбор", "name": "SamAvto", "proof": "Официальное письмо",
         "short": "Подобран более эффективный антискалант для системы обратного осмоса.",
         "task": "Действующий антискалант не обеспечивал оптимальную защиту системы обратного осмоса от накипеобразования.",
         "sol": "Проведена оценка параметров воды и действующей схемы дозирования, подобран более эффективный антискалант, соответствующий параметрам системы.",
         "res": "Новый антискалант подтверждён официальным письмом предприятия."},
        {"badge": "CLEAN RO-1 · Производство напитков", "kicker": "Напитки · CLEAN RO-1", "name": "Refresh Water", "proof": "Проект в работе · 2026",
         "short": "Запущена обработка системы обратного осмоса антискалантом CLEAN RO-1; накипеобразование заметно снизилось.",
         "task": "Производству бутилированной воды требовалась защита системы обратного осмоса от накипеобразования.",
         "sol": "Запущена обработка системы обратного осмоса антискалантом CLEAN RO-1.",
         "res": "Накипеобразование на оборудовании заметно снизилось. Итоговые результаты подводить пока рано — проект продолжается."},
    ],
    "news": [
        ["Сентябрь 2026", "Запущен сайт onsite.uz", "Информация о продуктах CLEAN RO и CLEAN RO-1, отраслях и сервисе — на русском, узбекском и английском языках."],
        ["Июнь 2026", "Запущена обработка антискалантом CLEAN RO-1 для Refresh Water", "На производстве бутилированной воды Refresh Water запущена обработка системы обратного осмоса антискалантом CLEAN RO-1. Накипеобразование на оборудовании уже заметно снизилось — итоговые результаты пока подводить рано."],
        ["2026", "Поставка антискаланта для АО «НГМК», ГМЗ-3", "Поставлено более 10 тонн антискаланта; расходы на водоподготовку снижены на 15%."],
        ["2026", "Подобран антискалант для SamAvto", "Для системы обратного осмоса подобран более эффективный антискалант; результат подтверждён официальным письмом предприятия."],
    ],
},
# ============================== UZ ==============================
"uz": {
    "nav": {"home": "Bosh sahifa", "product": "CLEAN RO", "industries": "Tarmoqlar", "service": "Servis",
            "cases": "Keyslar", "about": "Kompaniya haqida", "news": "Yangiliklar"},
    "nav_cta": "Hisob-kitob so'rash",
    "contact_note": "O'zbekistondan qo'ng'iroq qilish qulayroq. Chet eldan — email yoki Telegram.",
    "btn_call": "Qo'ng'iroq qilish", "btn_email": "Email", "btn_tg": "Telegram",
    "footer_about": "Teskari osmos tizimlari uchun CLEAN RO antiskalantlari ishlab chiqaruvchisi. Toshkent, O'zbekiston.",
    "footer_more": "Kompaniya haqida",
    "footer_products": "Mahsulotlar", "footer_company": "Kompaniya", "footer_contacts": "Kontaktlar",
    "footer_dosing": "Dozani hisoblash",
    "footer_rights": "© 2026 ONSITE. Barcha huquqlar himoyalangan.",
    "footer_city": "Toshkent sh., Olmazor tumani, General G'ofurov ko'chasi, 2-tupik, 16-uy",
    "cs_labels": ["Vazifa", "Yechim", "Natija"],
    "pages": {
        "home": {
            "title": "ONSITE — O'zbekistonda CLEAN RO antiskalantlari ishlab chiqaruvchisi",
            "desc": "Toshkentdagi ishlab chiqaruvchidan teskari osmos uchun CLEAN RO va CLEAN RO-1 antiskalantlari. Dozani bepul hisoblash, ombordan yetkazib berish, so'mda to'lov.",
            "eyebrow": "O'zbekistonda antiskalant ishlab chiqarish",
            "h1": "CLEAN RO antiskalantlari — teskari osmos membranalarini cho'kindidan himoya qilish",
            "lead": "Toshkentda fosfonat asosidagi antiskalantlar ishlab chiqaramiz va dozani suvingiz tahlili asosida hisoblaymiz. Ombordan yetkazib berish, so'mda to'lov, muhandisning texnik yordami.",
            "cta1": "Dozani hisoblashni so'rash", "cta2": "Mahsulotlar",
            "tiles_badge": "Mahsulotlar va servis",
            "tiles_h2": "Antiskalant va muhandislik yordami — bitta yetkazib beruvchidan",
            "tiles_p": "Biz shunchaki reagent sotmaymiz: mahsulot va dozani suvingizga moslab tanlaymiz va ishga tushirilgandan keyin ham qurilmani kuzatib boramiz.",
            "tiles": [
                ["Mahsulot", "CLEAN RO", "Teskari osmos, nano- va ultrafiltratsiya uchun ishqoriy antiskalant (pH 10,0–11,5). Karbonat va sulfat cho'kindilarini ingibirlaydi, doza 3–10 mg/l.", "CLEAN RO haqida batafsil", "product", "#clean-ro"],
                ["Mahsulot", "CLEAN RO-1", "Xuddi shu tizimlar uchun kislotali antiskalant (pH 1,5–1,7). Ichimlik suvi uchun 7 g/t gacha ruxsat etiladi — qadoqlangan suv ishlab chiqarishda qo'llaniladi.", "CLEAN RO-1 haqida batafsil", "product", "#clean-ro-1"],
                ["Servis", "Dozani hisoblash va texnik yordam", "Manba suvi tahlili asosida dozani bepul hisoblash, ishga tushirishda yordam va ONSITE muhandisi tomonidan qurilma ishini monitoring qilish.", "Servis haqida batafsil", "service", ""],
            ],
            "why_badge": "Nega ONSITE",
            "why_h2": "Xalqaro darajadagi muhandislik tajribasiga ega mahalliy ishlab chiqarish",
            "why": [
                ["O'z ishlab chiqarishimiz", "Antiskalantlar Toshkentda ishlab chiqariladi, omborda doimiy zaxira mavjud."],
                ["Tez yetkazib berish va so'mda to'lov", "Import, bojxona va valyuta riskisiz. O'zbekiston bo'ylab yetkazib berish."],
                ["Muhandislik yordami", "Jamoaning texnik tajribasi — Nalco Water (An Ecolab Company) kompaniyasida 8 yil: dozani hisoblash, ishga tushirish, monitoring."],
                ["Mahsulot hujjatlari", "Har bir mahsulot uchun TDS va SDS — texnik xizmatlar va xarid bo'limlari uchun."],
            ],
            "stats": [["40 t", "oylik ishlab chiqarish quvvati"], ["−15%", "suv tayyorlash xarajatlari, AO «NGMK», GMZ-3"]],
            "ind_badge": "Tarmoqlar", "ind_h2": "CLEAN RO antiskalantlari qayerda qo'llaniladi", "ind_link": "Barcha tarmoqlar",
            "ind": [
                ["Tog'-kon sanoati va metallurgiya", "Kon-boyitish kombinatlari va GMZlarda texnik, ichimlik va tuzsizlantirilgan suv uchun teskari osmos."],
                ["Oziq-ovqat sanoati va ichimliklar", "Qadoqlangan suv, ichimliklar, pivo pishirish, sut mahsulotlari ishlab chiqarish."],
                ["Avtomobilsozlik", "Bo'yash sexlari va ishlab chiqarish liniyalari uchun texnologik suv."],
                ["Qurilish va binolar", "Turar-joy majmualari, mehmonxonalar va biznes-markazlardagi teskari osmos qurilmalari."],
            ],
            "cases_badge": "Tasdiqlangan natijalar", "cases_h2": "Mijozlarimiz keyslari", "cases_link": "Barcha keyslar",
            "news_badge": "Yangiliklar", "news_h2": "So'nggi yangiliklar", "news_link": "Barcha yangiliklar",
            "faq_badge": "Savollar", "faq_h2": "Tez-tez so'raladigan savollar",
            "faq": [
                ["Antiskalant nima va u nima uchun kerak?", "Antiskalant — teskari osmosdan oldin manba suviga dozalanadigan reagent bo'lib, qattiqlik tuzlarining membranalarda cho'kishiga yo'l qo'ymaydi. Usiz membranalar tezroq ifloslanadi, unumdorlik pasayadi, yuvish va membranalarni almashtirish xarajatlari oshadi."],
                ["CLEAN RO va CLEAN RO-1 nimasi bilan farq qiladi?", "CLEAN RO — ishqoriy mahsulot (pH 10,0–11,5, zichligi 1,20 g/sm³), CLEAN RO-1 — kislotali (1% eritma pH 1,5–1,7, zichligi 1,10 g/sm³). Ikkalasi ham karbonat va sulfat cho'kindilarini ingibirlaydi. Ichimlik suvi uchun CLEAN RO 5 g/t dan, CLEAN RO-1 esa 7 g/t dan ko'p dozalanmaydi. Qaysi mahsulot qurilmangizga mosligini suv tahlili asosida aniqlaymiz."],
                ["Doza qanday hisoblanadi?", "Odatiy doza — 3–10 mg/l, standart bo'yicha qo'shimcha suvning 1 tonnasiga 5 g. Aniq doza manba suvi tahlili (qattiqlik, ishqoriylik, sulfatlar, kremniy, temir, pH, tuz miqdori) va qurilma parametrlariga (unumdorlik, permeat chiqishi, membrana turi) bog'liq. Hisob-kitob bepul."],
                ["Qanday idishda yetkaziladi va qancha saqlanadi?", "25 kg kanistra, 240 kg bochka yoki 1300 kg IBC. Saqlash muddati — yopiq zavod idishida +5…+25 °C da kamida 36 oy. Muzlash harorati −3 °C, qishda mahsulotni sovuqdan asrash kerak."],
                ["Mahsulot uchun texnik hujjatlar bormi?", "Ha, har bir mahsulot uchun TDS (texnik tavsif) va SDS (xavfsizlik pasporti) mavjud. So'rov bo'yicha yuboramiz."],
                ["To'lov va yetkazib berish qanday amalga oshiriladi?", "Shartnoma asosida ishlaymiz, to'lov so'mda. Toshkentdagi ombordan O'zbekiston bo'ylab yetkazib beramiz."],
            ],
            "cta_h2": "Suv tahlilini yuboring — dozani hisoblab beramiz",
            "cta_p": "Teskari osmos qurilmangizni tasvirlab bering va manba suvi tahlilini ilova qiling — mahsulot va dozani bepul tanlab beramiz.",
        },
        "product": {
            "title": "Teskari osmos uchun CLEAN RO va CLEAN RO-1 antiskalantlari — ONSITE",
            "desc": "Teskari osmos va nanofiltratsiya membranalari uchun fosfonat asosidagi CLEAN RO va CLEAN RO-1 antiskalantlari. Toshkentda ishlab chiqarilgan, TDS va SDS, dozani bepul hisoblash.",
            "tag": "Mahsulotlar · Antiskalantlar",
            "h1": "CLEAN RO va CLEAN RO-1 antiskalantlari",
            "lead": "Teskari osmos va nanofiltratsiya tizimlari uchun fosfonat asosidagi cho'kindi ingibitorlari. Ishlab chiqaruvchi — ONSITE, Toshkent.",
            "summary": "CLEAN RO va CLEAN RO-1 — ONSITE (Toshkent, O'zbekiston) ishlab chiqargan, teskari osmos, nano- va ultrafiltratsiya uchun organik kompleksonlar asosidagi antiskalantlar. Karbonat va sulfat cho'kindilarini ingibirlaydi; doza 3–10 mg/l (standart 5 g/t). Qadoqlash 25 kg, 240 kg va 1300 kg; saqlash muddati 36 oy.",
            "line_badge": "Mahsulot qatori", "line_h2": "Ikki mahsulot — bitta vazifa: toza membranalar",
            "spec_labels": ["Ko'rinishi", "Rangi", "pH", "Zichligi", "Asosi", "Doza", "Ichimlik suvi", "Membranalar", "Qadoqlash", "Saqlash muddati"],
            "spec_ro": ["Suyuqlik", "Rangsizdan och sariqqacha", "10,0–11,5", "1,20 g/sm³", "Organik kompleksonlar", "3–10 mg/l, standart 5 g/t", "Qo'shimcha suvning 1 tonnasiga 5 g dan ko'p emas", "Barcha poliamid membranalar", "25 kg kanistra, 240 kg bochka, 1300 kg IBC", "+5…+25 °C da 36 oy"],
            "spec_ro1": ["Suyuqlik", "Rangsizdan och sariqqacha", "1,5–1,7 (1% eritma)", "1,10 ± 0,02 g/sm³", "Organik kompleksonlar", "3–10 mg/l, standart 5 g/t", "Qo'shimcha suvning 1 tonnasiga 7 g dan ko'p emas", "Barcha poliamid membranalar", "25 kg kanistra, 240 kg bochka, 1300 kg IBC", "+5…+25 °C da 36 oy"],
            "tag_ro": "Ishqoriy antiskalant · pH 10,0–11,5",
            "tag_ro1": "Kislotali antiskalant · pH 1,5–1,7 (1%)",
            "p_clean_ro": "Teskari osmos, nano- va ultrafiltratsiya uchun antiskalant. O'ta to'yingan tuz eritmalarini barqarorlashtiradi, metall karbonatlari va sulfatlari cho'kishini ingibirlaydi hamda membrana yuzasidagi mavjud tuzlarni ketkazuvchi komponentlarni o'z ichiga oladi.",
            "p_clean_ro_1": "Xuddi shu vazifalarni bajaradigan teskari osmos, nano- va ultrafiltratsiya uchun kislotali antiskalant. Ichimlik suvi uchun 7 g/t gacha dozaga ruxsat beradi — qadoqlangan suv ishlab chiqarishda qo'llaniladi (Refresh Water).",
            "how_badge": "Afzalliklar", "how_h2": "CLEAN RO va CLEAN RO-1 nima beradi",
            "how": [
                "Metall karbonatlari va sulfatlari cho'kishini ingibirlaydi",
                "Suv sifatining keng doirasida ishlaydi",
                "Ko'plab ishlov berish dasturlarida xlorid yoki boshqa kislotani dozalashni talab qilmaydi",
                "Membrana yuzasidagi mavjud tuzlarni ketkazuvchi komponentlarni o'z ichiga oladi",
                "Poliamid asosidagi barcha membranalar bilan mos keladi",
                "Kimyoviy yuvishlar orasidagi muddatni va membranalar xizmat muddatini uzaytiradi",
            ],
            "hand_badge": "Dozalash va saqlash", "hand_h2": "Qanday qo'llash va saqlash",
            "hand": [
                "Mahsulotni doimiy ravishda, yopiq idishdan, atmosfera bilan aloqa qilmasdan bering",
                "Dozalash nasosini maksimal chastotaga sozlang va dozani to'g'rilang",
                "Nasoslar, liniyalar va idishlar — PVX, polietilen, teflon yoki zanglamaydigan po'latdan",
                "Suyultirilmagan mahsulotning alyuminiy, latun va uglerodli po'lat bilan aloqasiga yo'l qo'ymang",
                "Saqlash: yopiq zavod idishida +5…+25 °C da kamida 36 oy; muzlash harorati −3 °C",
                "Ishlashda himoya vositalari: ko'zoynak va rezina qo'lqoplar",
            ],
            "steps_badge": "Ishni boshlash", "steps_h2": "4 qadamda ishni boshlash",
            "steps": [
                ["Suv tahlili", "Manba suvi tahlili va qurilma ma'lumotlarini yuborasiz"],
                ["Hisob-kitob", "Mahsulot va dozani tanlaymiz — bepul"],
                ["Yetkazish va ishga tushirish", "Ombordan yetkazamiz va dozalashni sozlashda yordam beramiz"],
                ["Monitoring", "Qurilma ko'rsatkichlarini kuzatamiz va dozani to'g'rilaymiz"],
            ],
            "price_amount": "40", "price_unit": "tonna oyiga — ishlab chiqarish quvvati",
            "price_note": "Toshkentda ombor, O'zbekiston bo'ylab yetkazib berish",
            "price_h4": "Yetkazib berish shartlari",
            "price_list": [
                "Qadoqlash: 25 kg kanistra, 240 kg bochka, 1300 kg IBC",
                "Narx — so'rov bo'yicha, hajm va yetkazib berish formatiga bog'liq",
                "Shartnoma asosida so'mda to'lov",
                "TDS va SDS yetkazib berish bilan birga taqdim etiladi",
                "Birinchi yetkazib berishdan oldin dozani bepul hisoblash",
            ],
            "cta_h2": "TDS, SDS va doza hisobini so'rang",
            "cta_p": "Antiskalant qaysi qurilma uchun kerakligini yozing — hujjatlar va taklifni yuboramiz.",
        },
        "industries": {
            "title": "Tog'-kon, oziq-ovqat va boshqa tarmoqlar uchun antiskalantlar — ONSITE",
            "desc": "O'zbekistonda tog'-kon sanoati, oziq-ovqat sanoati, avtomobilsozlik, qurilish va energetikadagi teskari osmos qurilmalari uchun CLEAN RO antiskalantlari.",
            "tag": "Tarmoqlar",
            "h1": "Tarmog'ingiz uchun antiskalantlar",
            "lead": "Teskari osmos qurilmalari turli tarkibdagi suvda va turli rejimlarda ishlaydi. Mahsulot va dozani aniq korxona vazifasiga moslab tanlaymiz.",
            "grid_badge": "Qo'llanilish sohalari", "grid_h2": "Qaysi korxonalar bilan ishlaymiz",
            "cards": [
                ["Tog'-kon sanoati va metallurgiya", "Kon-boyitish kombinatlari va gidrometallurgiya zavodlarida texnik, ichimlik va tuzsizlantirilgan suv uchun teskari osmos. Yuqori qattiqlik va sulfatlar dozani aniq hisoblashni talab qiladi.", "Keys: AO «NGMK», GMZ-3 — suv tayyorlash xarajatlari −15%"],
                ["Oziq-ovqat sanoati va ichimliklar", "Qadoqlangan suv, alkogolsiz ichimliklar, pivo pishirish, sut va sharbat ishlab chiqarish. Permeatning barqaror sifati va oldindan rejalashtirilgan yuvishlar.", "Keys: Refresh Water — CLEAN RO-1"],
                ["Avtomobilsozlik", "Bo'yash sexlari, yuvish va texnologik liniyalar uchun tuzsizlantirilgan suv.", "Keys: SamAvto — antiskalant tanlash"],
                ["Qurilish va binolar", "Turar-joy majmualari, mehmonxonalar, biznes-markazlar va infratuzilma obyektlaridagi teskari osmos qurilmalari.", ""],
                ["Energetika va qozonxonalar", "Bug' va suv isitish qozonlari uchun to'ldiruvchi suv tayyorlash, bunda teskari osmos ion almashinuvi yoki EDI oldidan o'rnatiladi.", ""],
                ["Boshqa tarmoqlar", "Farmatsevtika, kimyo sanoati, laboratoriyalar va teskari osmos qurilmalariga ega boshqa ishlab chiqarishlar.", ""],
            ],
            "crit_badge": "Tanlov mezonlari", "crit_h2": "Antiskalant tanloviga nimalar ta'sir qiladi",
            "crit": [
                "Manba suvining qattiqligi va ishqoriyligi", "Sulfatlar, bariy va stronsiy", "Kremniy va temir",
                "Suvning pH darajasi va harorati", "Permeat chiqishi va qurilma bosqichlari soni", "Membranalar turi va ishlab chiqaruvchisi",
            ],
            "cta_h2": "Ishlab chiqarishingiz haqida gapirib bering",
            "cta_p": "Antiskalantni suv tarkibi va qurilmangiz ish rejimiga moslab tanlaymiz.",
        },
        "service": {
            "title": "Antiskalant dozasini hisoblash — bepul | ONSITE",
            "desc": "Suv tahlili asosida antiskalant dozasini bepul hisoblash, teskari osmos qurilmasini ishga tushirish va monitoring. O'zbekistonda ONSITE muhandislik yordami.",
            "tag": "Servis",
            "h1": "Dozani hisoblash va texnik yordam",
            "lead": "Antiskalant faqat to'g'ri dozada samarali ishlaydi. Dozani suvingiz tahlili asosida hisoblaymiz va ishga tushirilgandan keyin ham qurilmani kuzatib boramiz.",
            "summary": "CLEAN RO antiskalanti dozasini hisoblash — bepul, manba suvi tahlili va teskari osmos qurilmasi parametrlari asosida.",
            "inc_badge": "Nimalar kiradi", "inc_h2": "Hisob-kitobdan qurilmani kuzatib borishgacha",
            "inc": [
                "Manba suvi tahlili asosida dozani bepul hisoblash",
                "Mahsulot tanlash: CLEAN RO yoki CLEAN RO-1",
                "Dozalash nasosini sozlashda yordam",
                "Ishga tushirish va operatorlarga yo'riqnoma",
                "Monitoring: bosim, bosim farqi, permeat chiqishi, elektr o'tkazuvchanlik",
                "Membranalarni kimyoviy yuvish bo'yicha tavsiyalar",
            ],
            "need_badge": "Hisob-kitob uchun", "need_h2": "Nimalarni yuborish kerak",
            "need": [
                ["Manba suvi tahlili", "Kalsiy, magniy, ishqoriylik, sulfatlar, xloridlar, kremniy, temir, bariy va stronsiy (agar bo'lsa), pH, tuz miqdori yoki elektr o'tkazuvchanlik, harorat."],
                ["Qurilma parametrlari", "Unumdorlik, permeat chiqishi, bosqichlar soni, membranalar turi va soni."],
                ["Joriy sxema", "Ishlatilayotgan antiskalant va uning dozasi, yuvishlar tarixi, asosiy muammolar."],
            ],
            "steps_badge": "Qanday o'tadi", "steps_h2": "So'rovdan qurilma ishlashigacha",
            "steps": [
                ["So'rov", "Suv tahlili va qurilma ma'lumotlarini yuborasiz"],
                ["Hisob-kitob", "Doza hisobi va taklif tayyorlaymiz"],
                ["Ishga tushirish", "Yetkazib berish, dozalashni sozlash, yo'riqnoma"],
                ["Kuzatib borish", "Ko'rsatkichlar monitoringi va dozani to'g'rilash"],
            ],
            "note": "Texnik yordamni Nalco Water (An Ecolab Company) kompaniyasida 8 yillik tajribaga ega muhandis ko'rsatadi.",
            "cta_h2": "Suv tahlilini yuboring",
            "cta_p": "Dozani hisoblab, taklif yuboramiz.",
        },
        "cases": {
            "title": "Keyslar: NGMK, SamAvto, Refresh Water uchun antiskalantlar | ONSITE",
            "desc": "ONSITE loyihalari: AO «NGMK» GMZ-3 uchun antiskalant yetkazib berish (xarajatlar −15%), SamAvto uchun antiskalant tanlash, Refresh Water uchun CLEAN RO-1.",
            "tag": "Keyslar",
            "h1": "Loyihalar va keyslar",
            "lead": "Har bir obyektda nima qilingani — natijalar va tasdiqlovchi hujjatlar bilan.",
            "cta_h2": "Keyingi keys — sizning korxonangiz",
            "cta_p": "Suv tahlilini yuboring — antiskalant va dozani tanlab beramiz.",
        },
        "about": {
            "title": "ONSITE haqida — Toshkentda antiskalant ishlab chiqarish",
            "desc": "ONSITE — teskari osmos uchun CLEAN RO antiskalantlarini ishlab chiqaruvchi o'zbekistonlik kompaniya. Toshkentda ishlab chiqarish, oyiga 40 tonna, muhandislik yordami.",
            "tag": "Kompaniya haqida",
            "h1": "ONSITE — O'zbekistondagi antiskalant ishlab chiqaruvchi",
            "lead": "Teskari osmos uchun antiskalantlar ishlab chiqaramiz va korxonalarga suv tayyorlash xarajatlarini kamaytirishda yordam beramiz.",
            "prose": [
                "ONSITE — teskari osmos tizimlari uchun CLEAN RO brendi ostida antiskalantlar ishlab chiqaradigan o'zbekistonlik kompaniya. Ishlab chiqarish Toshkentda joylashgan, quvvati — oyiga 40 tonna.",
                "CLEAN RO va CLEAN RO-1 mahsulotlarimiz fosfonatlar asosida yaratilgan. Ulardan tog'-kon va oziq-ovqat sanoati, avtomobilsozlik, qurilish va boshqa tarmoqlar korxonalari foydalanadi.",
                "Kompaniyaning texnik ekspertizasini sanoat suv tayyorlash bo'yicha muhandis Sherozbek Dolimov ta'minlaydi. U Nalco Water (An Ecolab Company) kompaniyasida 8 yil ishlagan, O'zbekiston Milliy universiteti va Kembrij universitetida tahsil olgan.",
                "Biz faqat reagent emas, natija sotamiz: mahsulot va dozani suvingiz tarkibiga moslab tanlaymiz, ishga tushirishda yordam beramiz va qurilma ishini kuzatib boramiz.",
            ],
            "photo_alt": "Sherozbek Dolimov, ONSITE",
            "stats": [["40 t", "oylik quvvat"], ["8 yil", "Nalco Water tajribasi"]],
            "exp_badge": "Biz nima qilamiz", "exp_h2": "Ishlab chiqarish, servis va hujjatlar",
            "exp": [
                ["Ishlab chiqarish", "Toshkentda antiskalantlar ishlab chiqarish va omborda mahsulot zaxirasi."],
                ["Muhandislik yordami", "Dozani hisoblash, ishga tushirish, monitoring va membranalarni yuvish bo'yicha tavsiyalar."],
                ["Hujjatlar", "Har bir mahsulot uchun TDS va SDS, xarid bo'limi uchun shartnoma va yopuvchi hujjatlar."],
            ],
            "cta_h2": "Biz bilan bog'laning",
            "cta_p": "Korxonangiz vazifasi haqida yozing — javob beramiz va yechim taklif qilamiz.",
        },
        "news": {
            "title": "ONSITE yangiliklari — CLEAN RO antiskalantlari",
            "desc": "O'zbekistondagi CLEAN RO antiskalantlari ishlab chiqaruvchisi ONSITE kompaniyasining yangi loyihalari, mahsulotlari va voqealari.",
            "tag": "Yangiliklar",
            "h1": "ONSITE yangiliklari",
            "lead": "Kompaniyaning yangi loyihalari, mahsulotlari va voqealari.",
            "cta_h2": "Qurilmangizni muhokama qilamiz",
            "cta_p": "Suv tahlilini yuboring — dozani bepul hisoblab beramiz.",
        },
    },
    "cases": [
        {"badge": "Antiskalant yetkazib berish · Tog'-kon sanoati", "kicker": "Tog'-kon sanoati · Yetkazib berish", "name": "AO «NGMK», GMZ-3", "proof": "Shartnoma, xarajatlar −15%",
         "short": "Suv parametrlariga moslab tanlangan 10 tonnadan ortiq antiskalant yetkazib berildi.",
         "task": "Korxonaning suv tayyorlash xarajatlari mavjud reagentlar sxemasi imkon berganidan yuqori edi.",
         "sol": "Korxona suvi parametrlari va texnologik jarayoniga moslab tanlangan 10 tonnadan ortiq antiskalant yetkazib berildi.",
         "res": "Suv tayyorlash xarajatlari 15% ga kamaydi. Yetkazib berish shartnoma bilan rasmiylashtirilgan."},
        {"badge": "Teskari osmos uchun antiskalant tanlash · Avtomobilsozlik", "kicker": "Avtomobilsozlik · Tanlash", "name": "SamAvto", "proof": "Rasmiy xat",
         "short": "Teskari osmos tizimi uchun samaraliroq antiskalant tanlab berildi.",
         "task": "Amaldagi antiskalant teskari osmos tizimini cho'kindi hosil bo'lishidan optimal himoya qilmayotgan edi.",
         "sol": "Suv parametrlari va amaldagi dozalash sxemasi baholandi, tizim parametrlariga mos keladigan samaraliroq antiskalant tanlandi.",
         "res": "Yangi antiskalant korxonaning rasmiy xati bilan tasdiqlangan."},
        {"badge": "CLEAN RO-1 · Ichimliklar ishlab chiqarish", "kicker": "Ichimliklar · CLEAN RO-1", "name": "Refresh Water", "proof": "Loyiha davom etmoqda · 2026",
         "short": "Teskari osmos tizimiga CLEAN RO-1 antiskalanti bilan ishlov berish boshlandi; cho'kindi hosil bo'lishi sezilarli kamaydi.",
         "task": "Qadoqlangan suv ishlab chiqarishda teskari osmos tizimini cho'kindi hosil bo'lishidan himoya qilish kerak edi.",
         "sol": "Teskari osmos tizimiga CLEAN RO-1 antiskalanti bilan ishlov berish yo'lga qo'yildi.",
         "res": "Uskunada cho'kindi hosil bo'lishi sezilarli kamaydi. Yakuniy natijalar haqida gapirish hali erta — loyiha davom etmoqda."},
    ],
    "news": [
        ["2026-yil sentabr", "onsite.uz sayti ishga tushirildi", "CLEAN RO va CLEAN RO-1 mahsulotlari, tarmoqlar va servis haqida ma'lumot — rus, o'zbek va ingliz tillarida."],
        ["2026-yil iyun", "Refresh Water uchun CLEAN RO-1 antiskalanti bilan ishlov berish ishga tushirildi", "Refresh Water suv ishlab chiqarish korxonasida teskari osmos tizimiga CLEAN RO-1 antiskalanti bilan ishlov berish boshlandi. Uskunada cho'kindi hosil bo'lishi allaqachon sezilarli kamaydi — yakuniy natijalar haqida gapirish hali erta."],
        ["2026", "AO «NGMK», GMZ-3 uchun antiskalant yetkazib berildi", "10 tonnadan ortiq antiskalant yetkazib berildi; suv tayyorlash xarajatlari 15% ga kamaydi."],
        ["2026", "SamAvto uchun antiskalant tanlandi", "Teskari osmos tizimi uchun samaraliroq antiskalant tanlandi; natija korxonaning rasmiy xati bilan tasdiqlangan."],
    ],
},
# ============================== EN ==============================
"en": {
    "nav": {"home": "Home", "product": "CLEAN RO", "industries": "Industries", "service": "Service",
            "cases": "Case studies", "about": "About", "news": "News"},
    "nav_cta": "Request dosing",
    "contact_note": "In Uzbekistan, calling is easiest. From abroad — email or Telegram.",
    "btn_call": "Call", "btn_email": "Email", "btn_tg": "Telegram",
    "footer_about": "Manufacturer of CLEAN RO antiscalants for reverse osmosis systems. Tashkent, Uzbekistan.",
    "footer_more": "About the company",
    "footer_products": "Products", "footer_company": "Company", "footer_contacts": "Contacts",
    "footer_dosing": "Dosing calculation",
    "footer_rights": "© 2026 ONSITE. All rights reserved.",
    "footer_city": "16 General Gafurov St., dead-end 2, Almazar district, Tashkent, Uzbekistan",
    "cs_labels": ["Challenge", "Solution", "Result"],
    "pages": {
        "home": {
            "title": "ONSITE — CLEAN RO antiscalant manufacturer in Uzbekistan",
            "desc": "CLEAN RO and CLEAN RO-1 antiscalants for reverse osmosis, made in Tashkent. Free dosing calculation, local stock, payment in UZS.",
            "eyebrow": "Antiscalant manufacturer in Uzbekistan",
            "h1": "CLEAN RO antiscalants — scale protection for reverse osmosis membranes",
            "lead": "We manufacture phosphonate-based antiscalants in Tashkent and calculate the dose from your water analysis. Local stock, payment in UZS, engineer support.",
            "cta1": "Request a dosing calculation", "cta2": "Products",
            "tiles_badge": "Products and service",
            "tiles_h2": "Antiscalant and engineering support from one supplier",
            "tiles_p": "We don't just sell a chemical: we match the product and dose to your water and stay with your system after start-up.",
            "tiles": [
                ["Product", "CLEAN RO", "Alkaline antiscalant (pH 10.0–11.5) for reverse osmosis, nanofiltration and ultrafiltration. Inhibits carbonate and sulfate scale at 3–10 mg/L.", "More about CLEAN RO", "product", "#clean-ro"],
                ["Product", "CLEAN RO-1", "Acidic antiscalant (pH 1.5–1.7) for the same systems. Up to 7 g/t allowed for drinking water — used in bottled water production.", "More about CLEAN RO-1", "product", "#clean-ro-1"],
                ["Service", "Dosing calculation and support", "Free dose calculation from your feed water analysis, start-up assistance and system monitoring by an ONSITE engineer.", "More about the service", "service", ""],
            ],
            "why_badge": "Why ONSITE",
            "why_h2": "Local manufacturing backed by international engineering experience",
            "why": [
                ["Own production", "Our antiscalants are made in Tashkent, with product kept in stock."],
                ["Fast delivery, payment in UZS", "No imports, customs or currency risk. Delivery across Uzbekistan."],
                ["Engineering support", "Our technical expertise comes from 8 years at Nalco Water (An Ecolab Company): dosing calculation, start-up, monitoring."],
                ["Product documentation", "TDS and SDS for every product — for technical teams and procurement."],
            ],
            "stats": [["40 t", "monthly production capacity"], ["−15%", "water treatment costs, JSC NMMC, GMZ-3"]],
            "ind_badge": "Industries", "ind_h2": "Where CLEAN RO antiscalants are used", "ind_link": "All industries",
            "ind": [
                ["Mining and metallurgy", "Reverse osmosis for process, drinking and demineralized water at mining and processing plants."],
                ["Food and beverage", "Bottled water, soft drinks, brewing and dairy production."],
                ["Automotive", "Process water for paint shops and production lines."],
                ["Construction and buildings", "Reverse osmosis units in residential complexes, hotels and business centers."],
            ],
            "cases_badge": "Proven results", "cases_h2": "Client case studies", "cases_link": "All case studies",
            "news_badge": "News", "news_h2": "Latest updates", "news_link": "All news",
            "faq_badge": "Questions", "faq_h2": "Frequently asked questions",
            "faq": [
                ["What is an antiscalant and why is it needed?", "An antiscalant is dosed into the feed water ahead of reverse osmosis and keeps hardness salts from precipitating on the membranes. Without it, membranes foul faster, output drops, and cleaning and membrane replacement costs rise."],
                ["What is the difference between CLEAN RO and CLEAN RO-1?", "CLEAN RO is alkaline (pH 10.0–11.5, density 1.20 g/cm³); CLEAN RO-1 is acidic (1% solution pH 1.5–1.7, density 1.10 g/cm³). Both inhibit carbonate and sulfate scale. For drinking water, CLEAN RO is dosed at no more than 5 g/t and CLEAN RO-1 at no more than 7 g/t. We determine which suits your system from your water analysis."],
                ["How is the dose calculated?", "The typical dose is 3–10 mg/L, with 5 g per tonne of feed water as standard. The exact dose depends on your feed water analysis (hardness, alkalinity, sulfates, silica, iron, pH, TDS) and system parameters (capacity, recovery, membrane type). The calculation is free."],
                ["What packaging is available and what is the shelf life?", "25 kg canister, 240 kg drum or 1300 kg IBC. Shelf life is at least 36 months in the sealed original container at +5…+25 °C. The freezing point is −3 °C, so protect the product from frost in winter."],
                ["Do you provide technical documents?", "Yes, every product has a TDS (technical data sheet) and an SDS (safety data sheet). We send them on request."],
                ["How do payment and delivery work?", "We work under contract with payment in UZS, and deliver from our Tashkent warehouse across Uzbekistan."],
            ],
            "cta_h2": "Send us your water analysis — we'll calculate the dose",
            "cta_p": "Describe your reverse osmosis system and attach a feed water analysis — we'll select the product and dose free of charge.",
        },
        "product": {
            "title": "CLEAN RO and CLEAN RO-1 antiscalants for reverse osmosis — ONSITE",
            "desc": "Phosphonate-based CLEAN RO and CLEAN RO-1 antiscalants for reverse osmosis and nanofiltration membranes. Made in Tashkent, TDS and SDS, free dosing calculation.",
            "tag": "Products · Antiscalants",
            "h1": "CLEAN RO and CLEAN RO-1 antiscalants",
            "lead": "Phosphonate-based scale inhibitors for reverse osmosis and nanofiltration systems. Made in Tashkent by ONSITE.",
            "summary": "CLEAN RO and CLEAN RO-1 are antiscalants made by ONSITE (Tashkent, Uzbekistan) from organic complexones for reverse osmosis, nanofiltration and ultrafiltration. They inhibit carbonate and sulfate scale at 3–10 mg/L (typically 5 g/t). Packed in 25 kg, 240 kg and 1300 kg; 36-month shelf life.",
            "line_badge": "Product line", "line_h2": "Two products, one job: clean membranes",
            "spec_labels": ["Form", "Color", "pH", "Density", "Base", "Dose", "Drinking water", "Membranes", "Packaging", "Shelf life"],
            "spec_ro": ["Liquid", "Colorless to slightly yellow", "10.0–11.5", "1.20 g/cm³", "Organic complexones", "3–10 mg/L, typically 5 g/t", "Max 5 g per tonne of feed water", "All polyamide membranes", "25 kg PE canister, 240 kg PE drum, 1300 kg IBC", "36 months at +5…+25 °C"],
            "spec_ro1": ["Liquid", "Colorless to slightly yellow", "1.5–1.7 (1% solution)", "1.10 ± 0.02 g/cm³", "Organic complexones", "3–10 mg/L, typically 5 g/t", "Max 7 g per tonne of feed water", "All polyamide membranes", "25 kg PE canister, 240 kg PE drum, 1300 kg IBC", "36 months at +5…+25 °C"],
            "tag_ro": "Alkaline antiscalant · pH 10.0–11.5",
            "tag_ro1": "Acidic antiscalant · pH 1.5–1.7 (1%)",
            "p_clean_ro": "Antiscalant for reverse osmosis, nanofiltration and ultrafiltration. Stabilizes supersaturated salt solutions, inhibits metal carbonate and sulfate scale, and contains components that remove existing salts from the membrane surface.",
            "p_clean_ro_1": "Acidic antiscalant for reverse osmosis, nanofiltration and ultrafiltration with the same functions. Allows up to 7 g/t for drinking water — used in bottled water production (Refresh Water).",
            "how_badge": "Benefits", "how_h2": "What CLEAN RO and CLEAN RO-1 deliver",
            "how": [
                "Inhibit metal carbonate and sulfate scale",
                "Work across a wide range of water quality",
                "In many treatment programs, no hydrochloric or other acid dosing is needed",
                "Contain components that remove existing salts from the membrane surface",
                "Compatible with all polyamide membranes",
                "Extend the time between chemical cleanings and membrane life",
            ],
            "hand_badge": "Dosing and storage", "hand_h2": "How to apply and store",
            "hand": [
                "Dose continuously from a closed tank, without contact with the atmosphere",
                "Set the dosing pump to maximum stroke frequency and adjust the dose",
                "Pumps, lines and tanks: PVC, polyethylene, PTFE or stainless steel",
                "Keep the neat product away from aluminum, brass and carbon steel",
                "Shelf life: at least 36 months in the sealed original container at +5…+25 °C; freezing point −3 °C",
                "PPE when handling: goggles and rubber gloves",
            ],
            "steps_badge": "Getting started", "steps_h2": "Get started in 4 steps",
            "steps": [
                ["Water analysis", "You send us a feed water analysis and system data"],
                ["Calculation", "We select the product and dose — free"],
                ["Delivery and start-up", "We deliver from stock and help set up dosing"],
                ["Monitoring", "We track system performance and adjust the dose"],
            ],
            "price_amount": "40", "price_unit": "tonnes per month — production capacity",
            "price_note": "Warehouse in Tashkent, delivery across Uzbekistan",
            "price_h4": "Supply terms",
            "price_list": [
                "Packaging: 25 kg canister, 240 kg drum, 1300 kg IBC",
                "Price on request, depending on volume and delivery format",
                "Payment in UZS under contract",
                "TDS and SDS provided with delivery",
                "Free dosing calculation before the first delivery",
            ],
            "cta_h2": "Request TDS, SDS and a dosing calculation",
            "cta_p": "Tell us which system needs an antiscalant — we'll send the documents and a proposal.",
        },
        "industries": {
            "title": "Antiscalants for mining, food and beverage and other industries — ONSITE",
            "desc": "CLEAN RO antiscalants for reverse osmosis systems in mining, food and beverage, automotive, construction and power in Uzbekistan.",
            "tag": "Industries",
            "h1": "Antiscalants for your industry",
            "lead": "Reverse osmosis systems run on different water and in different modes. We match the product and dose to each plant's task.",
            "grid_badge": "Applications", "grid_h2": "Who we work with",
            "cards": [
                ["Mining and metallurgy", "Reverse osmosis for process, drinking and demineralized water at mining, processing and hydrometallurgical plants. High hardness and sulfates call for precise dosing.", "Case: JSC NMMC, GMZ-3 — −15% water treatment costs"],
                ["Food and beverage", "Bottled water, soft drinks, brewing, dairy and juice production. Stable permeate quality and predictable cleanings.", "Case: Refresh Water — CLEAN RO-1"],
                ["Automotive", "Demineralized water for paint shops, washing and process lines.", "Case: SamAvto — antiscalant selection"],
                ["Construction and buildings", "Reverse osmosis units in residential complexes, hotels, business centers and infrastructure facilities.", ""],
                ["Power and boiler houses", "Make-up water for steam and hot-water boilers where reverse osmosis sits ahead of ion exchange or EDI.", ""],
                ["Other industries", "Pharmaceuticals, chemicals, laboratories and other plants running reverse osmosis.", ""],
            ],
            "crit_badge": "Selection criteria", "crit_h2": "What drives antiscalant selection",
            "crit": [
                "Feed water hardness and alkalinity", "Sulfates, barium and strontium", "Silica and iron",
                "Water pH and temperature", "Recovery and number of stages", "Membrane type and manufacturer",
            ],
            "cta_h2": "Tell us about your plant",
            "cta_p": "We'll match the antiscalant to your water chemistry and system operation.",
        },
        "service": {
            "title": "Free antiscalant dosing calculation | ONSITE",
            "desc": "Free antiscalant dosing calculation from your water analysis, plus start-up and monitoring of your reverse osmosis system. ONSITE engineering support in Uzbekistan.",
            "tag": "Service",
            "h1": "Dosing calculation and technical support",
            "lead": "An antiscalant only works at the right dose. We calculate it from your water analysis and stay with your system after start-up.",
            "summary": "CLEAN RO dosing calculation is free, based on your feed water analysis and reverse osmosis system parameters.",
            "inc_badge": "What's included", "inc_h2": "From calculation to ongoing support",
            "inc": [
                "Free dose calculation from your feed water analysis",
                "Product selection: CLEAN RO or CLEAN RO-1",
                "Help setting up the dosing pump",
                "Start-up and operator briefing",
                "Monitoring: pressure, differential pressure, recovery, conductivity",
                "Recommendations on membrane chemical cleaning",
            ],
            "need_badge": "For the calculation", "need_h2": "What to send us",
            "need": [
                ["Feed water analysis", "Calcium, magnesium, alkalinity, sulfates, chlorides, silica, iron, barium and strontium (if present), pH, TDS or conductivity, temperature."],
                ["System parameters", "Capacity, recovery, number of stages, membrane type and count."],
                ["Current setup", "Current antiscalant and dose, cleaning history, main issues."],
            ],
            "steps_badge": "How it works", "steps_h2": "From request to running system",
            "steps": [
                ["Request", "You send your water analysis and system data"],
                ["Calculation", "We prepare the dose calculation and proposal"],
                ["Start-up", "Delivery, dosing setup, operator briefing"],
                ["Support", "Performance monitoring and dose adjustment"],
            ],
            "note": "Technical support is provided by an engineer with 8 years at Nalco Water (An Ecolab Company).",
            "cta_h2": "Send your water analysis",
            "cta_p": "We'll calculate the dose and send you a proposal.",
        },
        "cases": {
            "title": "Case studies: antiscalants for NMMC, SamAvto, Refresh Water | ONSITE",
            "desc": "ONSITE projects: antiscalant supply to JSC NMMC GMZ-3 (−15% costs), antiscalant selection for SamAvto, CLEAN RO-1 for Refresh Water.",
            "tag": "Case studies",
            "h1": "Projects and case studies",
            "lead": "What we did at each site — with results and supporting documents.",
            "cta_h2": "Your plant could be the next case study",
            "cta_p": "Send us your water analysis — we'll select the antiscalant and dose.",
        },
        "about": {
            "title": "About ONSITE — antiscalant manufacturing in Tashkent",
            "desc": "ONSITE is an Uzbek manufacturer of CLEAN RO antiscalants for reverse osmosis. Production in Tashkent, 40 tonnes per month, engineering support.",
            "tag": "About",
            "h1": "ONSITE — antiscalant manufacturer in Uzbekistan",
            "lead": "We make antiscalants for reverse osmosis and help plants cut water treatment costs.",
            "prose": [
                "ONSITE is an Uzbek company that manufactures antiscalants for reverse osmosis systems under the CLEAN RO brand. Production is in Tashkent, with a capacity of 40 tonnes per month.",
                "Our CLEAN RO and CLEAN RO-1 products are phosphonate-based. They are used by companies in mining, food and beverage, automotive, construction and other industries.",
                "The company's technical expertise comes from Sherozbek Dalimov, an industrial water treatment engineer. He spent 8 years at Nalco Water (An Ecolab Company) and studied at the National University of Uzbekistan and the University of Cambridge.",
                "We sell results, not just a chemical: we match the product and dose to your water, help with start-up and monitor your system.",
            ],
            "photo_alt": "Sherozbek Dalimov, ONSITE",
            "stats": [["40 t", "monthly capacity"], ["8 years", "at Nalco Water"]],
            "exp_badge": "What we do", "exp_h2": "Production, service and documentation",
            "exp": [
                ["Production", "Antiscalant manufacturing in Tashkent with product kept in stock."],
                ["Engineering support", "Dosing calculation, start-up, monitoring and membrane cleaning recommendations."],
                ["Documentation", "TDS and SDS for every product; contract and accounting documents for procurement."],
            ],
            "cta_h2": "Get in touch",
            "cta_p": "Tell us about your plant's needs — we'll reply and propose a solution.",
        },
        "news": {
            "title": "ONSITE news — CLEAN RO antiscalants",
            "desc": "New projects, products and updates from ONSITE, the CLEAN RO antiscalant manufacturer in Uzbekistan.",
            "tag": "News",
            "h1": "ONSITE news",
            "lead": "New projects, products and company updates.",
            "cta_h2": "Let's discuss your system",
            "cta_p": "Send us your water analysis — we'll calculate the dose free of charge.",
        },
    },
    "cases": [
        {"badge": "Antiscalant supply · Mining", "kicker": "Mining · Supply", "name": "JSC NMMC, GMZ-3", "proof": "Contract, −15% costs",
         "short": "Supplied 10+ tonnes of antiscalant selected for the site's water parameters.",
         "task": "The plant's water treatment costs were higher than its chemical program should allow.",
         "sol": "Supplied more than 10 tonnes of antiscalant matched to the plant's water parameters and process.",
         "res": "Water treatment costs fell by 15%. The supply is covered by a contract."},
        {"badge": "Antiscalant selection for reverse osmosis · Automotive", "kicker": "Automotive · Selection", "name": "SamAvto", "proof": "Official letter",
         "short": "Selected a more effective antiscalant for the reverse osmosis system.",
         "task": "The existing antiscalant did not give the reverse osmosis system optimal scale protection.",
         "sol": "We assessed the water parameters and the current dosing scheme and selected a more effective antiscalant for the system.",
         "res": "The new antiscalant is confirmed by an official letter from the company."},
        {"badge": "CLEAN RO-1 · Beverage production", "kicker": "Beverages · CLEAN RO-1", "name": "Refresh Water", "proof": "Ongoing project · 2026",
         "short": "Started treating the reverse osmosis system with CLEAN RO-1; scaling has noticeably decreased.",
         "task": "A bottled water plant needed scale protection for its reverse osmosis system.",
         "sol": "We started treating the reverse osmosis system with CLEAN RO-1 antiscalant.",
         "res": "Scaling on the equipment has noticeably decreased. It is too early for final results — the project continues."},
    ],
    "news": [
        ["September 2026", "onsite.uz goes live", "Information on CLEAN RO and CLEAN RO-1, industries and service — in Russian, Uzbek and English."],
        ["June 2026", "CLEAN RO-1 treatment launched at Refresh Water", "The reverse osmosis system at the Refresh Water bottled water plant is now treated with CLEAN RO-1. Scaling on the equipment has already noticeably decreased — it is too early for final results."],
        ["2026", "Antiscalant supplied to JSC NMMC, GMZ-3", "More than 10 tonnes of antiscalant supplied; water treatment costs cut by 15%."],
        ["2026", "Antiscalant selected for SamAvto", "A more effective antiscalant was selected for the reverse osmosis system; the result is confirmed by an official letter."],
    ],
},
}

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
esc = html.escape


def url(key, lang):
    return PATHS[key][lang]


def abs_url(key, lang):
    return CONFIG["base"] + PATHS[key][lang]


def arrow(color):
    return (f'<svg width="16" height="12" viewBox="0 0 16 12" fill="none"><path d="M0 6H15M15 6L10 1M15 6L10 11" '
            f'stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def check(color="var(--teal)"):
    return (f'<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="9" fill="{color}"/>'
            '<path d="M5 9.2L7.6 11.8L13 6.2" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def org_ld():
    return {
        "@type": "Organization",
        "@id": CONFIG["base"] + "/#org",
        "name": "ONSITE",
        "url": CONFIG["base"] + "/",
        "logo": CONFIG["base"] + "/favicon.svg",
        "email": "mailto:" + CONFIG["email"],
        "telephone": CONFIG["phone"],
        "address": {"@type": "PostalAddress", "streetAddress": "General Gafurov St., dead-end 2, 16", "addressRegion": "Almazar district", "addressLocality": "Tashkent", "addressCountry": "UZ"},
        "areaServed": "UZ",
        "brand": [{"@type": "Brand", "name": "CLEAN RO"}],
        "sameAs": [CONFIG["telegram"]],
    }


def layout(lang, key, body, jsonld=None):
    t = CONTENT[lang]
    p = t["pages"][key]
    title, desc = p["title"], p["desc"]
    canonical = abs_url(key, lang)
    alt_links = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{abs_url(key, l)}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{abs_url(key, "ru")}">'
    ld_blocks = ""
    for block in (jsonld or []):
        ld_blocks += '<script type="application/ld+json">\n' + json.dumps(block, ensure_ascii=False) + "\n</script>\n"

    def nav_links():
        return "\n".join(
            f'    <a href="{url(k, lang)}" class="{"active" if k == key else ""}">{esc(t["nav"][k])}</a>'
            for k in NAV_ORDER
        )

    lang_switch = "".join(
        f'<a href="{url(key, l)}" class="{"active" if l == lang else ""}" hreflang="{l}">{l.upper()}</a>' for l in LANGS
    )
    og_image = CONFIG["base"] + CONFIG["og_image"]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{alt_links}
<meta property="og:type" content="website">
<meta property="og:site_name" content="ONSITE">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{ld_blocks}</head>
<body>

<header class="site-nav">
  <div class="nav-inner">
    <a href="{url('home', lang)}" class="logo"><span class="dot"></span><span>ONSITE</span></a>
    <nav class="links">
{nav_links()}
    </nav>
    <div class="nav-right">
      <div class="lang-switch">{lang_switch}</div>
      <a class="btn btn-primary" id="navCta" href="#contact">{esc(t["nav_cta"])}</a>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Menu">&#9776;</button>
    </div>
  </div>
  <nav class="mobile-menu" id="mobileMenu">
{nav_links()}
    <a href="{url('news', lang)}" class="{"active" if key == "news" else ""}">{esc(t["nav"]["news"])}</a>
  </nav>
</header>
<main>
{body}
{cta_band(lang, p["cta_h2"], p["cta_p"])}
</main>

{footer(lang)}
<script src="/app.js"></script>
</body>
</html>
"""


def cta_band(lang, h2, p):
    t = CONTENT[lang]
    return f"""  <section class="cta-band" id="contact">
    <div class="wrap">
      <h2>{esc(h2)}</h2>
      <p>{esc(p)}</p>
      <p style="color:#B8C4CC; font-size:13.5px; margin:14px 0 22px;">{esc(t["contact_note"])}</p>
      <div class="cta-row">
        <a class="btn btn-ghost-light" href="tel:{CONFIG["phone"]}">{esc(t["btn_call"])} &rarr;</a>
        <a class="btn btn-ghost-light" href="mailto:{CONFIG["email"]}">{esc(t["btn_email"])} &rarr;</a>
        <a class="btn btn-ghost-light" href="{CONFIG["telegram"]}" target="_blank" rel="noopener">{esc(t["btn_tg"])} &rarr;</a>
      </div>
    </div>
  </section>"""


def footer(lang):
    t = CONTENT[lang]
    n = t["nav"]
    return f"""<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h5 style="font-family:'Oswald',sans-serif; font-size:16px; font-weight:700; color:var(--ink); text-transform:none; margin-bottom:14px;">ONSITE</h5>
        <p style="color:var(--ink-soft); max-width:320px;">{esc(t["footer_about"])}<br><a href="{url('about', lang)}" style="color:var(--teal); font-weight:700; display:inline-block; margin-top:10px;">{esc(t["footer_more"])} &rarr;</a></p>
      </div>
      <div>
        <h5>{esc(t["footer_products"])}</h5>
        <a href="{url('product', lang)}#clean-ro">CLEAN RO</a>
        <a href="{url('product', lang)}#clean-ro-1">CLEAN RO-1</a>
        <a href="{url('service', lang)}">{esc(t["footer_dosing"])}</a>
        <h5 style="margin-top:22px;">{esc(t["footer_company"])}</h5>
        <a href="{url('industries', lang)}">{esc(n["industries"])}</a>
        <a href="{url('cases', lang)}">{esc(n["cases"])}</a>
        <a href="{url('news', lang)}">{esc(n["news"])}</a>
      </div>
      <div>
        <h5>{esc(t["footer_contacts"])}</h5>
        <p>{esc(t["footer_city"])}</p>
        <a href="tel:{CONFIG["phone"]}">{CONFIG["phone_display"]}</a>
        <a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a>
        <a href="{CONFIG["telegram"]}" target="_blank" rel="noopener">Telegram</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>{esc(t["footer_rights"])}</span>
      <span>onsite.uz</span>
    </div>
  </div>
</footer>"""


def page_hero(cls, tag, h1, lead):
    return f"""  <section class="page-hero {cls}">
    <div class="wrap">
      <div class="tag">{esc(tag)}</div>
      <h1>{esc(h1)}</h1>
      <p class="lead">{esc(lead)}</p>
    </div>
  </section>"""


def summary(text):
    return f"""  <section style="padding:26px 0 0;">
    <div class="wrap">
      <p class="summary-strip">{esc(text)}</p>
    </div>
  </section>"""


def section_head(badge, h2, p=None):
    ptag = f"\n        <p>{esc(p)}</p>" if p else ""
    return f"""      <div class="section-head">
        <div class="badge-inline">{esc(badge)}</div>
        <h2>{esc(h2)}</h2>{ptag}
      </div>"""


def section_head_row(badge, h2, link_text, link_href):
    return f"""      <div class="section-head-row">
        <div class="section-head">
          <div class="badge-inline">{esc(badge)}</div>
          <h2>{esc(h2)}</h2>
        </div>
        <a class="text-link" href="{link_href}">{esc(link_text)} {arrow("var(--teal)")}</a>
      </div>"""


def includes(items, color="var(--teal)"):
    return '<div class="includes-grid">' + "".join(
        f'<div class="inc-item">{check(color)}<p>{esc(i)}</p></div>' for i in items) + "</div>"


def steps(items):
    inner = "".join(
        f'<div class="pstep"><div class="circ">{n}</div><h4>{esc(h)}</h4><p>{esc(d)}</p></div>'
        for n, (h, d) in enumerate(items, 1))
    return f'<div class="process-rail"><div class="process-steps">{inner}</div></div>'


def case_cards(lang):
    return '<div class="cases-grid">' + "".join(
        f'<div class="case-card"><div class="kicker">{esc(c["kicker"])}</div><h4>{esc(c["name"])}</h4>'
        f'<p>{esc(c["short"])}</p><div class="proof">{esc(c["proof"])}</div></div>'
        for c in CONTENT[lang]["cases"]) + "</div>"


def expertise_grid(items, cls="expertise-grid"):
    out = []
    for it in items:
        case = f'<div class="ind-case">{esc(it[2])}</div>' if len(it) > 2 and it[2] else ""
        out.append(f'<div class="expertise-card"><h4>{esc(it[0])}</h4><p>{esc(it[1])}</p>{case}</div>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
TILE_CLASSES = ["water", "procurement", "safety"]
TILE_COLORS = ["var(--teal)", "var(--graphite)", "var(--green-text)"]


def page_home(lang):
    t = CONTENT[lang]
    p = t["pages"]["home"]
    tiles = ""
    for i, (tag, h3, txt, link, target, anchor) in enumerate(p["tiles"]):
        c = TILE_COLORS[i]
        tiles += f"""        <div class="service-tile {TILE_CLASSES[i]}">
          <div class="tag">{esc(tag)}</div>
          <h3>{esc(h3)}</h3>
          <p>{esc(txt)}</p>
          <a class="mini-cta" href="{url(target, lang)}{anchor}" style="color:{c}">{esc(link)} {arrow(c)}</a>
        </div>
"""
    why = "".join(
        f'<div class="bio-item"><div class="num">{n:02d}</div><div><h4>{esc(h)}</h4><p>{esc(d)}</p></div></div>'
        for n, (h, d) in enumerate(p["why"], 1))
    stats = "".join(f'<div class="stat-box"><div class="big">{esc(a)}</div><div class="lbl">{esc(b)}</div></div>' for a, b in p["stats"])
    news = "".join(
        f'<div class="news-teaser-card"><span class="date">{esc(d)}</span><h4>{esc(h)}</h4><p>{esc(x)}</p></div>'
        for d, h, x in t["news"][:3])
    faq = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"])
    body = f"""
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow-line">{arrow("var(--teal)")}<span>{esc(p["eyebrow"])}</span></div>
      <h1>{esc(p["h1"])}</h1>
      <p class="lead">{esc(p["lead"])}</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="{url('service', lang)}">{esc(p["cta1"])}</a>
        <a class="btn btn-outline" href="{url('product', lang)}">{esc(p["cta2"])}</a>
      </div>
      <div class="flow-strip"><svg viewBox="0 0 1120 70" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M0 40 C 120 40, 160 10, 280 10 S 440 60, 560 60 S 720 15, 840 15 S 1000 45, 1120 45" stroke="var(--line)" stroke-width="2" fill="none"/>
    <circle cx="280" cy="10" r="5" fill="var(--teal)"/>
    <circle cx="560" cy="60" r="5" fill="var(--graphite)"/>
    <circle cx="840" cy="15" r="5" fill="var(--green)"/>
  </svg></div>
    </div>
  </section>

  <section>
    <div class="wrap">
{section_head(p["tiles_badge"], p["tiles_h2"], p["tiles_p"])}
      <div class="services-grid">
{tiles}      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="wrap">
      <div class="bio-grid">
        <div>
          <div class="badge-inline">{esc(p["why_badge"])}</div>
          <h2 style="font-size:30px; margin-bottom:26px;">{esc(p["why_h2"])}</h2>
          <div class="bio-list">{why}</div>
        </div>
        <div>
          <div class="stat-pair">{stats}</div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
{section_head_row(p["ind_badge"], p["ind_h2"], p["ind_link"], url('industries', lang))}
      {expertise_grid(p["ind"], "ind-grid")}
    </div>
  </section>

  <section class="section-alt">
    <div class="wrap">
{section_head_row(p["cases_badge"], p["cases_h2"], p["cases_link"], url('cases', lang))}
      {case_cards(lang)}
    </div>
  </section>

  <section>
    <div class="wrap">
{section_head_row(p["news_badge"], p["news_h2"], p["news_link"], url('news', lang))}
      <div class="news-teaser-grid">{news}</div>
    </div>
  </section>

  <section class="section-alt">
    <div class="wrap narrow">
      <div class="badge-inline">{esc(p["faq_badge"])}</div>
      <h2 style="font-size:30px; margin-bottom:28px;">{esc(p["faq_h2"])}</h2>
      <div class="faq-list">{faq}</div>
    </div>
  </section>
"""
    ld = [
        {"@context": "https://schema.org", "@graph": [
            org_ld(),
            {"@type": "WebSite", "@id": CONFIG["base"] + "/#website", "url": CONFIG["base"] + "/", "name": "ONSITE",
             "inLanguage": lang, "publisher": {"@id": CONFIG["base"] + "/#org"}},
        ]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]
    return layout(lang, "home", body, ld)


def page_product(lang):
    p = CONTENT[lang]["pages"]["product"]

    def card(pid, name, text, tag, values, alt=False):
        rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in zip(p["spec_labels"], values))
        return f"""        <div class="product-card{' alt' if alt else ''}" id="{pid}">
          <div class="tag">{esc(tag)}</div>
          <h3>{esc(name)}</h3>
          <p>{esc(text)}</p>
          <table class="spec-table">{rows}</table>
        </div>
"""
    price_list = "".join(f"<li>{esc(i)}</li>" for i in p["price_list"])
    body = f"""
{page_hero("pg-water", p["tag"], p["h1"], p["lead"])}
{summary(p["summary"])}
  <section>
    <div class="wrap">
{section_head(p["line_badge"], p["line_h2"])}
      <div class="product-grid">
{card("clean-ro", "CLEAN RO", p["p_clean_ro"], p["tag_ro"], p["spec_ro"])}{card("clean-ro-1", "CLEAN RO-1", p["p_clean_ro_1"], p["tag_ro1"], p["spec_ro1"], True)}      </div>
    </div>
  </section>
  <section class="section-alt">
    <div class="wrap">
{section_head(p["how_badge"], p["how_h2"])}
      {includes(p["how"])}
    </div>
  </section>
  <section>
    <div class="wrap">
{section_head(p["steps_badge"], p["steps_h2"])}
      {steps(p["steps"])}
    </div>
  </section>
  <section class="section-alt">
    <div class="wrap">
{section_head(p["hand_badge"], p["hand_h2"])}
      {includes(p["hand"], "var(--green)")}
    </div>
  </section>
  <section>
    <div class="wrap">
      <div class="price-card">
        <div class="price-left">
          <div class="amount">{esc(p["price_amount"])}</div>
          <div class="unit">{esc(p["price_unit"])}</div>
          <div class="note">{esc(p["price_note"])}</div>
        </div>
        <div class="price-right">
          <h4>{esc(p["price_h4"])}</h4>
          <ul>{price_list}</ul>
        </div>
      </div>
    </div>
  </section>
"""
    products = []
    for pid, name, text, values in (("clean-ro", "CLEAN RO", p["p_clean_ro"], p["spec_ro"]),
                                    ("clean-ro-1", "CLEAN RO-1", p["p_clean_ro_1"], p["spec_ro1"])):
        products.append({
            "@type": "Product", "@id": abs_url("product", lang) + "#" + pid, "name": name,
            "description": text, "category": "Antiscalant", "url": abs_url("product", lang) + "#" + pid,
            "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v}
                                   for k, v in zip(p["spec_labels"], values)],
            "brand": {"@type": "Brand", "name": "CLEAN RO"}, "manufacturer": {"@id": CONFIG["base"] + "/#org"},
        })
    ld = [{"@context": "https://schema.org", "@graph": [org_ld()] + products}]
    return layout(lang, "product", body, ld)


def page_industries(lang):
    p = CONTENT[lang]["pages"]["industries"]
    body = f"""
{page_hero("pg-procurement", p["tag"], p["h1"], p["lead"])}
  <section>
    <div class="wrap">
{section_head(p["grid_badge"], p["grid_h2"])}
      {expertise_grid(p["cards"])}
    </div>
  </section>
  <section class="section-alt">
    <div class="wrap">
{section_head(p["crit_badge"], p["crit_h2"])}
      {includes(p["crit"], "var(--graphite)")}
    </div>
  </section>
"""
    return layout(lang, "industries", body)


def page_service(lang):
    p = CONTENT[lang]["pages"]["service"]
    body = f"""
{page_hero("pg-safety", p["tag"], p["h1"], p["lead"])}
{summary(p["summary"])}
  <section>
    <div class="wrap">
{section_head(p["inc_badge"], p["inc_h2"])}
      {includes(p["inc"], "var(--green)")}
    </div>
  </section>
  <section class="section-alt">
    <div class="wrap">
{section_head(p["need_badge"], p["need_h2"])}
      {expertise_grid(p["need"])}
    </div>
  </section>
  <section>
    <div class="wrap">
{section_head(p["steps_badge"], p["steps_h2"])}
      {steps(p["steps"])}
      <p class="expert-note">{esc(p["note"])}</p>
    </div>
  </section>
"""
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "description": p["summary"],
           "provider": {"@type": "Organization", "name": "ONSITE", "url": CONFIG["base"] + "/"},
           "areaServed": "UZ", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "UZS"}}]
    return layout(lang, "service", body, ld)


def page_cases(lang):
    t = CONTENT[lang]
    p = t["pages"]["cases"]
    labels = t["cs_labels"]
    studies = ""
    for c in t["cases"]:
        studies += f"""        <div class="case-study">
          <div class="cs-head">
            <div>
              <div class="badge-inline" style="margin-bottom:10px;">{esc(c["badge"])}</div>
              <h3>{esc(c["name"])}</h3>
            </div>
            <div class="cs-proof">{esc(c["proof"])}</div>
          </div>
          <div class="cs-grid">
            <div class="cs-block"><h5>{esc(labels[0])}</h5><p>{esc(c["task"])}</p></div>
            <div class="cs-block"><h5>{esc(labels[1])}</h5><p>{esc(c["sol"])}</p></div>
            <div class="cs-block"><h5>{esc(labels[2])}</h5><p>{esc(c["res"])}</p></div>
          </div>
        </div>
"""
    body = f"""
{page_hero("pg-news", p["tag"], p["h1"], p["lead"])}
  <section>
    <div class="wrap">
{studies}    </div>
  </section>
"""
    return layout(lang, "cases", body)


def page_about(lang):
    p = CONTENT[lang]["pages"]["about"]
    prose = "".join(f"<p>{esc(x)}</p>" for x in p["prose"])
    stats = "".join(f'<div class="stat-box"><div class="big">{esc(a)}</div><div class="lbl">{esc(b)}</div></div>' for a, b in p["stats"])
    body = f"""
{page_hero("pg-bio", p["tag"], p["h1"], p["lead"])}
  <section>
    <div class="wrap">
      <div class="bio-photo-grid">
        <img src="/images/sherozbek-dalimov.jpg" alt="{esc(p["photo_alt"])}" width="700" height="1254" loading="lazy">
        <div>
          <div class="bio-prose">{prose}</div>
          <div class="stat-pair" style="max-width:420px; margin-top:8px;">{stats}</div>
          <a class="btn btn-outline" style="margin-top:22px;" href="{CONFIG["linkedin"]}" target="_blank" rel="noopener">LinkedIn &rarr;</a>
        </div>
      </div>
    </div>
  </section>
  <section class="section-alt">
    <div class="wrap">
{section_head(p["exp_badge"], p["exp_h2"])}
      {expertise_grid(p["exp"])}
    </div>
  </section>
"""
    ld = [{"@context": "https://schema.org", "@graph": [org_ld(), {
        "@type": "Person", "name": "Sherozbek Dalimov", "alternateName": "Шерозбек Долимов",
        "worksFor": {"@id": CONFIG["base"] + "/#org"}, "image": CONFIG["base"] + CONFIG["og_image"],
        "sameAs": [CONFIG["linkedin"]],
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "National University of Uzbekistan"},
                     {"@type": "CollegeOrUniversity", "name": "University of Cambridge"}]}]}]
    return layout(lang, "about", body, ld)


def page_news(lang):
    t = CONTENT[lang]
    p = t["pages"]["news"]
    items = "".join(
        f"""        <div class="news-item">
          <div class="date">{esc(d)}</div>
          <div>
            <h4>{esc(h)}</h4>
            <p>{esc(x)}</p>
          </div>
        </div>
""" for d, h, x in t["news"])
    body = f"""
{page_hero("pg-news", p["tag"], p["h1"], p["lead"])}
  <section>
    <div class="wrap">
      <div class="news-list">
{items}      </div>
    </div>
  </section>
"""
    return layout(lang, "news", body)


BUILDERS = {
    "home": page_home, "product": page_product, "industries": page_industries, "service": page_service,
    "cases": page_cases, "about": page_about, "news": page_news,
}


def out_path(u):
    rel = u.lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return os.path.join(OUT, rel)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_sitemap():
    rows = []
    for key in PATHS:
        for lang in LANGS:
            alts = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(key, l)}"/>' for l in LANGS)
            rows.append(f"""  <url>
    <loc>{abs_url(key, lang)}</loc>
    <lastmod>{CONFIG["lastmod"]}</lastmod>
{alts}
    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_url(key, "ru")}"/>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def build_llms():
    b = CONFIG["base"]
    ru = CONTENT["ru"]
    cases = ", ".join(c["name"] for c in ru["cases"])
    return f"""# ONSITE

> ONSITE is an antiscalant manufacturer in Tashkent, Uzbekistan. Brand: CLEAN RO — CLEAN RO (alkaline, pH 10.0–11.5, density 1.20 g/cm³) and CLEAN RO-1 (acidic, 1% solution pH 1.5–1.7, density 1.10 g/cm³), liquid antiscalants based on organic complexones for reverse osmosis, nanofiltration and ultrafiltration. Dose 3–10 mg/L (standard 5 g/t; drinking water max 5 g/t for CLEAN RO, 7 g/t for CLEAN RO-1). Packaging: 25 kg canister, 240 kg drum, 1300 kg IBC. Shelf life 36 months at +5…+25 °C. Production capacity: 40 tonnes per month. Free dosing calculation from feed water analysis; TDS and SDS available for every product; delivery across Uzbekistan, payment in UZS.

## Products
- [CLEAN RO and CLEAN RO-1]({b}{PATHS["product"]["en"]}): antiscalants for reverse osmosis, nanofiltration and ultrafiltration; carbonate and sulfate scale inhibition; compatible with all polyamide membranes.

## Service
- [Dosing calculation and technical support]({b}{PATHS["service"]["en"]}): free dose calculation, start-up, monitoring, membrane cleaning recommendations.

## Industries
- [Industries]({b}{PATHS["industries"]["en"]}): mining and metallurgy, food and beverage, automotive, construction and buildings, power and boiler houses.

## Case studies
- [Case studies]({b}{PATHS["cases"]["en"]}): {cases}.

## About
- [About ONSITE]({b}{PATHS["about"]["en"]}): technical expertise by Sherozbek Dalimov, 8 years at Nalco Water (An Ecolab Company).

## Languages
- Russian (default): {b}/
- Uzbek: {b}/uz/
- English: {b}/en/

## Contact
- Company: OOO «ONSITE», 16 General Gafurov St., dead-end 2, Almazar district, Tashkent, Uzbekistan
- Email: {CONFIG["email"]}
- Phone: {CONFIG["phone_display"]}
- Telegram: {CONFIG["telegram"]}
"""


def main():
    count = 0
    for key, fn in BUILDERS.items():
        for lang in LANGS:
            write(out_path(PATHS[key][lang]), fn(lang))
            count += 1
    write(os.path.join(OUT, "sitemap.xml"), build_sitemap())
    write(os.path.join(OUT, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {CONFIG['base']}/sitemap.xml\n")
    write(os.path.join(OUT, "llms.txt"), build_llms())
    print(f"Built {count} pages into {OUT}")


if __name__ == "__main__":
    main()
