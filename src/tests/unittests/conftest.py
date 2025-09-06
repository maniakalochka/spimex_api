import pytest_asyncio


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_db():
    """No-op fixture to override integration `prepare_db` from parent `src/tests/conftest.py`.
    This prevents unit tests under `src/tests/unittests` from attempting real DB connections.
    """
    yield
