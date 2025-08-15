import pytest
from starlette.testclient import TestClient

from core.config import settings
from databases.db import async_session, engine
from main import app
from models.base import Base


@pytest.fixture(scope="session", autouse=True)
async def prepare_db() -> None:
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

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
