# Sales Gym — архитектура (этап 1, discovery)

Комплекс тренажёров для B2B-продаж AGROWIN / sdalimov.uz: Telegram-бот + веб-дашборд.

## 1. Зафиксированные решения

| # | Вопрос | Решение |
|---|--------|---------|
| 1 | Где код | Папка `sales-gym/` в этом репозитории, старый проект не трогаем |
| 2 | Стек | Python 3.12: aiogram 3, FastAPI, SQLAlchemy 2 + Alembic, APScheduler, pytest |
| 3 | Пользователи | Один (белый список Telegram ID из `.env`) |
| 4 | ИИ-бюджет | $10/мес, жёсткий лимит в коде + лимит в консоли Anthropic |
| 5 | Персонажи MVP | Закупщик-«ценовик», эколог (не ЛПР), «молчащий» клиент после КП |
| 6 | Разбор | Только в конце сессии, без подсказок по ходу |
| 7 | Критерии | 4 базовых + этика (обещал экономию до аудита → оценка ≤ 4) + шаг с датой + доля вопросов |
| 8 | Ввод | Сначала текст, голос отдельным шагом позже |
| 9 | Воронка | Todoist: один проект = один клиент. Валюта — UZS |
| 10 | Ритм | Часы работы отмечаются вручную в боте. Домена нет → дашборд через SSH-туннель |

Названия клиентов в промтах: по умолчанию обобщённые («молочный завод с иностранным собственником»).
Реальные названия можно вписать в YAML персонажа самостоятельно.

## 2. Архитектура

```
 Telegram (вы)
     │  long polling (входящие порты не нужны)
     ▼
┌──────────────────────── docker compose: project "sales-gym" ────────────────────────┐
│                                                                                     │
│  bot  (aiogram 3 + APScheduler)                     web (FastAPI, этап 6)           │
│   ├─ trainer      М1 тренажёр переговоров            └─ дашборд метрик              │
│   ├─ assumptions  М3 проверка допущений                 порт 127.0.0.1:8088         │
│   ├─ ritual       М5 утро/вечер/неделя                  (доступ по SSH-туннелю)     │
│   ├─ funnel       М4 воронка + Todoist (read)                                       │
│   ├─ deals        М2 симулятор + калькулятор                                        │
│   └─ load         М6 нагрузка                                                       │
│          │                          │                                               │
│          ▼                          ▼                                               │
│   ai/ (Claude API + учёт бюджета)   db: PostgreSQL 16 (порт наружу не открыт)       │
│                                                                                     │
│  content/  ← промты персонажей, критерии, упражнения (YAML/MD, правите сами)        │
└─────────────────────────────────────────────────────────────────────────────────────┘
       │                        │
       ▼                        ▼
  api.anthropic.com       api.todoist.com (только чтение)
```

**Почему Python:** aiogram — самый зрелый фреймворк Telegram-ботов; Whisper/STT для голоса — на Python;
калькулятор и прогнозы проще писать и тестировать. Один язык для бота, API и расчётов.

**Почему PostgreSQL сразу, а не SQLite:** в Docker Compose это одна строка, а переезд с SQLite потом — лишняя работа.
Тесты чистой логики (оценка, калькулятор, приоритет) работают без БД.

**Как не сломать n8n на Hetzner:**
- отдельный compose-проект `sales-gym` и своя docker-сеть;
- бот работает через long polling, поэтому входящие порты не нужны;
- у Postgres нет порта наружу, дашборд слушает только `127.0.0.1:8088`;
- `mem_limit` на контейнеры: ~512 МБ на всё, чтобы не отнимать память у n8n.

## 3. Модели Claude и бюджет $10/мес

Модели задаются в `.env`:

```
CLAUDE_MODEL_DIALOG=claude-sonnet-5     # реплики персонажа
CLAUDE_MODEL_REVIEW=claude-opus-5       # разбор после сессии
AI_MONTHLY_BUDGET_USD=10
```

Оценка одной сессии: ~12 реплик и разбор; ~34k входных и ~7k выходных токенов.

| Вариант | $/сессия | 30 сессий + ритуалы/мес |
|---------|---------:|------------------------:|
| Всё на Opus 5 ($5/$25 за 1M) | ~0.35 | ~11–12 $ — выше лимита |
| **Диалог Sonnet 5 + разбор Opus 5** (по умолчанию) | ~0.21 | ~7–8 $ |
| Всё на Sonnet 5 ($2/$10) | ~0.14 | ~5 $ |
| Всё на Haiku 4.5 ($1/$5) | ~0.07 | ~2–3 $ |

Защита бюджета:
- каждый вызов API пишется в `ai_usage` вместе с ценой;
- при 80% лимита бот предупреждает;
- при 100% лимита новые сессии не стартуют до 1-го числа.

Системный промт персонажа кешируется (prompt caching), это снижает стоимость входных токенов.

## 4. Структура проекта

```
sales-gym/
├── docker-compose.yml
├── Dockerfile
├── .env.example                 # секреты только в .env (в .gitignore)
├── pyproject.toml
├── alembic/                     # миграции БД
├── content/                     # ← редактируете сами, без кода
│   ├── personas/
│   │   ├── purchaser_price.yaml     # закупщик-«ценовик»
│   │   ├── ecologist_non_dm.yaml    # эколог, не ЛПР
│   │   └── silent_after_kp.yaml     # молчит после КП
│   ├── prompts/
│   │   ├── persona_base.md          # общие правила ролевой игры
│   │   └── reviewer.md              # инструкция разбора
│   ├── rubrics/negotiation.yaml     # критерии, веса, правило этики
│   ├── exercises/objections.yaml    # микро-упражнения для утра (этап 3)
│   └── funnel.yaml                  # этапы воронки и вероятности (этап 4)
├── app/
│   ├── config.py
│   ├── db/            models.py, session.py
│   ├── ai/            client.py, budget.py
│   ├── trainer/       М1
│   ├── assumptions/   М3
│   ├── ritual/        М5
│   ├── funnel/        М4 (todoist.py, priority.py)
│   ├── deals/         М2 (calculator.py)
│   ├── load/          М6
│   ├── bot/           handlers/, keyboards.py, main.py
│   ├── web/           дашборд (этап 6)
│   └── cli.py         консольный режим тренажёра — тест без Telegram
└── tests/
```

Пример персонажа (`content/personas/purchaser_price.yaml`):

```yaml
key: purchaser_price
title: Закупщик-«ценовик»
company: Молочный завод, иностранный собственник, Ташкентская обл.
role: Менеджер по закупкам, KPI — снижение цены
situation: >
  Получил ваше КП на антискалант для котельной. Параллельно есть КП Nalco и двух дистрибьюторов.
hidden_needs:
  - Боится остановки котельной и претензий главного энергетика
  - Нужна отсрочка 60 дней по внутреннему регламенту
objections:
  - "У Nalco дешевле на 15%"
  - "Дайте скидку, тогда подпишем"
  - "Гарантируйте, что расход будет ниже"
hangup_if: Трижды подряд говорите только о цене или давите
difficulty:
  1: Идёт навстречу, если вы задаёте вопросы
  2: Скептичен, ценовое давление каждые 2 реплики
  3: Жёсткий торг, упоминает тендер и сроки
```

## 5. Схема БД

Во всех таблицах есть `id` и `created_at`, если не указано иное. Суммы хранятся в сумах (`BIGINT`).

**Общее**
- `users` — `tg_id`, `tz` (Asia/Tashkent)
- `ai_usage` — `purpose` (dialog/review/assumption/…), `model`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cost_usd`

**М1 — тренажёр** (этап 2)
- `training_sessions` — `persona_key`, `language` (ru / uz_cyrl / uz_latn), `difficulty` 1–3,
  `status` (active / finished / hung_up / abandoned), `started_at`, `ended_at`, `turns`
- `training_messages` — `session_id`, `role` (user/persona), `content`
- `session_reviews` — `session_id`, `score_needs`, `score_value`, `score_objections`, `score_close` (1–10),
  `overall`, `ethics_violation` bool, `next_step_with_date` bool, `question_ratio`,
  `rephrasings` jsonb (3 × {сказал, лучше, почему}), `summary`

**М3 — допущения** (этап 3)
- `assumptions` — `belief`, `hypothesis`, `action_15min`, `contact`, `due_at`,
  `status` (open / confirmed / busted / expired), `result_note`, `checked_at`

**М5 — ритуал** (этап 3)
- `daily_rituals` — `date` PK, `morning_done_at`, `exercise_key`, `exercise_answer`, `exercise_score`,
  `focus_actions` jsonb (3 действия), `evening_done_at`, `money_today`, `fear_or_assumption`, `tomorrow_change`

**М4 — воронка** (этап 4)
- `deals` — `todoist_project_id`, `client_name`, `title`,
  `stage` (lead / contact / meeting / kp / pilot / paid / lost), `amount_uzs`,
  `probability` (по умолчанию из `funnel.yaml`), `expected_pay_date`, `kp_sent_at`,
  `last_touch_at`, `next_step`, `next_step_date`
- `deal_stage_history` — `deal_id`, `from_stage`, `to_stage`, `at`
- `touches` — `deal_id`, `channel` (call / telegram / email / meeting), `at`, `note`
- `todoist_tasks` — кеш: `task_id`, `project_id`, `content`, `labels[]`, `due`, `completed_at`, `synced_at`

**М2 — большая сделка** (этап 5)
- `deal_cases` — `source` (generated/real), `title`, `params` jsonb, `result` jsonb (маржа, кэш-разрыв, …),
  `checklist` jsonb, `decision`
- `fx_rates` — `date` PK, `usd_uzs` (курс ЦБ, cbu.uz), нужен для импортных закупок в USD

**М6 — нагрузка** (этап 6)
- `work_logs` — `date`, `started_at`, `ended_at` (отмечаете «начал / закончил»)
- `daily_load` — `date` PK, `tasks_done`, `calls`, `work_minutes`, `is_day_off`
- `load_alerts` — `date`, `rule`, `message`, `acknowledged`

### Ключевые правила (покрываются тестами)

- **Оценка сессии:** `overall` — среднее 4 критериев.
  Если `ethics_violation`, то `overall = min(overall, 4)`.
  Если нет `next_step_with_date`, то `score_close ≤ 6`.
- **Приоритет сделки:** `amount_uzs × вероятность этапа`.
  Бонус, если КП без ответа > 2 дней или следующий шаг просрочен.
  Сортировка по убыванию — это и есть «3 денежных действия дня».
- **Калькулятор (М2):** маржа, кэш-разрыв по дням (оплата поставщику → импорт → поставка → отсрочка клиента),
  стоимость денег инвестора, точка безубыточности.
- **Выгорание (М6):** 12+ дней подряд без выходного; > 30 задач в день 5 дней подряд;
  > 11 ч работы 3 дня подряд. Пороги задаются в `.env`/YAML.

## 6. План этапов

| Этап | Содержание | Оценка разработки |
|------|------------|------------------:|
| **2. MVP: М1** | Каркас, Docker Compose, БД + миграции, Claude-клиент с бюджетом, 3 персонажа, 3 языка, 3 уровня, `/train` → диалог → `/end` → разбор, консольный режим, тесты оценки | 1–1.5 дня |
| 3. М3 + М5 | Допущения с напоминанием по сроку и статистикой; утро 07:30 (упражнение + фокус), вечер 21:00, недельный отчёт в воскресенье | 1 день |
| 4. М4 + Todoist | Синхронизация проектов и задач (read), привязка сумм и этапов через бот, ежедневная сводка, КП без ответа > 2 дней, приоритизация | 1–1.5 дня |
| 5. М2 | Генератор кейсов $100–500k, калькулятор, чек-лист финансирования и плана Б, разбор решения | 1 день |
| 6. М6 + дашборд + деплой | Учёт часов, сигналы риска, веб-дашборд, деплой на Hetzner рядом с n8n | 1.5 дня |

После каждого этапа будут: что сделано, команды запуска для Windows + Docker Desktop, как тестировать, что дальше.

## 7. Что нужно от вас

**Для этапа 2** (секреты не присылайте в чат — только в свой локальный `.env`):
1. Токен бота от @BotFather.
2. Ваш Telegram ID (узнать у @userinfobot).
3. API-ключ Anthropic (console.anthropic.com) и лимит расходов $10 в настройках консоли.
4. Docker Desktop на Windows.

**Позже:**
- токен Todoist (этап 4);
- характеристики VPS и как запущен n8n (этап 6).
