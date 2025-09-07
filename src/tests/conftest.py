import asyncio
import subprocess
from pathlib import Path

import httpx
import pytest_asyncio
from asgi_lifespan import LifespanManager

from core.config import settings
from databases.db import async_session, engine
from main import app
from models.base import Base


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    dump_path = Path(__file__).parents[2] / "db" / "init" / "10_dump.sql.gz"
    if not dump_path.exists():
        raise FileNotFoundError(f"Dump not found: {dump_path}")

    cmd = f"gunzip -c {dump_path} | psql {settings.DB_URL.replace('+asyncpg', '')}"
    await asyncio.to_thread(
        subprocess.run,
        cmd,
        shell=True,
        check=True,
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_app():
    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(test_app):
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session():
    async with async_session() as s:
        yield s
