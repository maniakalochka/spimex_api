import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from core.config import settings
from models.base import Base
from models.spimex import SpimexTradingResult

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# Настройка логирования
config = context.config

config.set_main_option("sqlalchemy.url", settings.DB_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url") or settings.DB_URL
    if url.startswith("postgresql+asyncpg"):
        sync_url = url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    else:
        sync_url = url

    from sqlalchemy import create_engine

    connectable = create_engine(sync_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
