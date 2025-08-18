# #!/usr/bin/env bash
# set -euo pipefail

# echo "Waiting for PostgreSQL..."
# RETRIES=30
# until pg_isready -h db -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" || [ $RETRIES -eq 0 ]; do
#   echo "  ... Postgres not ready yet"
#   sleep 2
#   RETRIES=$((RETRIES-1))
# done
# if [ $RETRIES -eq 0 ]; then
#   echo "PostgreSQL is not ready — exiting."
#   exit 1
# fi

# echo "Waiting for Redis..."
# RETRIES=15
# until redis-cli -h "${REDIS_HOST:-redis}" -p "${REDIS_PORT:-6379}" ping | grep -q "PONG" || [ $RETRIES -eq 0 ]; do
#   echo "  ... Redis not ready yet"
#   sleep 2
#   RETRIES=$((RETRIES-1))
# done
# if [ $RETRIES -eq 0 ]; then
#   echo "Redis is not ready — exiting."
#   exit 1
# fi

# echo "Starting FastAPI..."
# exec poetry run uvicorn src.main:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8000}" --reload

#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for PostgreSQL..."
RETRIES=30
until pg_isready -h db -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" || [ $RETRIES -eq 0 ]; do
  echo "  ... Postgres not ready yet"
  sleep 2
  RETRIES=$((RETRIES-1))
done
if [ $RETRIES -eq 0 ]; then
  echo "PostgreSQL is not ready — exiting."
  exit 1
fi

echo "Waiting for Redis..."
RETRIES=15
until redis-cli -h "${REDIS_HOST:-redis}" -p "${REDIS_PORT:-6379}" ping | grep -q "PONG" || [ $RETRIES -eq 0 ]; do
  echo "  ... Redis not ready yet"
  sleep 2
  RETRIES=$((RETRIES-1))
done
if [ $RETRIES -eq 0 ]; then
  echo "Redis is not ready — exiting."
  exit 1
fi

# --- применяем миграции ---
echo "Applying Alembic migrations to main DB..."
alembic -x dburl="$DB_URL" upgrade head

# тестовую БД мигрируем по наличию переменной (удобно, если локально её нет)
if [ -n "${TEST_DB_URL:-}" ]; then
  echo "Applying Alembic migrations to TEST DB..."
  alembic -x dburl="$TEST_DB_URL" upgrade head
fi

echo "Starting FastAPI..."
exec poetry run uvicorn src.main:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8000}" --reload
