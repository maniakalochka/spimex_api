# Установка и запуск

- Предварительно создайте `.env` файл в корне проекта с переменными окружения по примеру `.env.example`.

```bash
git clone https://github.com/maniakalochka/spimex_api.git
cd spimex_api
docker compose up --build
docker compose exec spimex_web poetry run alembic revision --autogenerate -m "new table name"  #  костыль, в дампе база по-другому называется.
docker compose exec spimex_web poetry run alembic upgrade head

```

Переходим на `http://localhost:8000/docs` и проверяем работу API.

```bash
# Запуск тестов
docker compose exec web pytest
```
