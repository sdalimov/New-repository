FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /srv

COPY pyproject.toml ./
COPY app ./app
RUN pip install ".[dev]"

COPY alembic.ini ./
COPY alembic ./alembic
COPY content ./content
COPY tests ./tests

CMD ["sh", "-c", "alembic upgrade head && python -m app.bot.main"]
