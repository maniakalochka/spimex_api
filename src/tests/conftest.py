from pathlib import Path
import asyncio
import pytest
from starlette.testclient import TestClient
from sqlalchemy import text
import gzip
import subprocess

from core.config import settings
from databases.db import async_session, engine
from main import app
from models.base import Base


@pytest.fixture(scope="function", autouse=True)
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    dump_path = Path(__file__).parents[2] / "db" / "init" / "10_dump.sql.gz"
    if not dump_path.exists():
        raise FileNotFoundError(f"Dump not found: {dump_path}")

    subprocess.run(
        f"gunzip -c {dump_path} | psql {settings.TEST_DB_URL.replace('+asyncpg', '')}",
        shell=True,
        check=True,
    )

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def session():
    async with async_session() as session:
        yield session
