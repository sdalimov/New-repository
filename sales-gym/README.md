# Sales Gym

Telegram-бот для ежедневной тренировки B2B-продаж. Архитектура и план — [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

**Готово (этап 2):** тренажёр переговоров. Три персонажа, три языка (RU / UZ-кириллица / UZ-латиница),
три уровня сложности. После каждой сессии — разбор: 4 оценки, правило этики, шаг с датой, 3 фразы «сказать иначе».

## Запуск на Windows (Docker Desktop)

PowerShell:

```powershell
git clone https://github.com/sdalimov/New-repository.git
cd New-repository
git checkout claude/bold-cori-lbzn5u
cd sales-gym
copy .env.example .env
notepad .env        # TELEGRAM_BOT_TOKEN, ALLOWED_TG_IDS, ANTHROPIC_API_KEY, POSTGRES_PASSWORD
docker compose up -d --build
docker compose logs -f bot    # «Бот запущен…» — Ctrl+C для выхода из логов
```

Откройте бота в Telegram → `/train`.

Если не знаете свой Telegram ID: оставьте `ALLOWED_TG_IDS` пустым, запустите бота и напишите ему —
он ответит вашим ID. Впишите ID в `.env` и выполните `docker compose up -d`.

## Команды бота

| Команда | Что делает |
|---------|-----------|
| `/train` | Новая тренировка: персонаж → язык → уровень |
| `/end` | Завершить и получить разбор (повторяет разбор, если в прошлый раз была ошибка) |
| `/history` | Последние 10 тренировок с оценками |
| `/budget` | Расход на Claude в этом месяце |

Сессия завершается сама, если персонаж «положил трубку», согласился на шаг с датой или прошло `MAX_TURNS` реплик.

## Проверка

```powershell
docker compose run --rm bot pytest -q                    # тесты (42)
docker compose run --rm bot python -m app.cli --demo     # консольная тренировка без ИИ, бесплатно
docker compose run --rm bot python -m app.cli            # консольная тренировка с настоящим Claude
```

## Правка персонажей и критериев

Всё в папке `content/`, код трогать не нужно:

- `content/personas/*.yaml` — персонажи (новый файл = новый персонаж в меню);
- `content/prompts/persona_base.md` — общие правила ролевой игры;
- `content/prompts/reviewer.md` — инструкция для разбора;
- `content/rubrics/negotiation.yaml` — критерии, веса, пороги правил.

После правки: `docker compose restart bot`.

## Бюджет ИИ

- Модели и лимит задаются в `.env`.
- Каждый вызов Claude записывается в таблицу `ai_usage` со стоимостью.
- При 80% лимита бот предупреждает при старте тренировки. При 100% новые тренировки не начинаются до 1-го числа; уже идущую можно закончить.
- Дополнительно поставьте лимит расходов в console.anthropic.com → Settings → Limits.

## Остановка

```powershell
docker compose down       # остановить (данные сохраняются)
docker compose down -v    # остановить и удалить базу
```
