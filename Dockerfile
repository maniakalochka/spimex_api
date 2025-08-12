FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl ca-certificates \
    postgresql-client redis-tools \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.0.0
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY src ./src
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 8000
