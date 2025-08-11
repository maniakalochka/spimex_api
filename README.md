# Необходимые зависимости

- python>=3.13
- redis
- postgresql
- poetry 2.0

---

# Установка и запуск

- Предварительно создайте `.env` файл в корне проекта с переменными окружения по примеру `.env.example`.
- Используя этот репозиторий заполните БД данными:
  `https://github.com/maniakalochka/spimex_parser.git`

```bash
git clone https://github.com/maniakalochka/spimex_api.git
cd spimex_api
poetry install
. $(poetry env info --path)/bin/activate
cd src
uvicorn main:app --reload
```
