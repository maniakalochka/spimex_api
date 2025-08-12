# Установка и запуск

- Предварительно создайте `.env` файл в корне проекта с переменными окружения по примеру `.env.example`.

```bash
git clone https://github.com/maniakalochka/spimex_api.git
cd spimex_api
docker compose up --build
```

Переходим на `http://localhost:8000/docs` и проверяем работу API.
