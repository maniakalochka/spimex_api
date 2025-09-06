import logging

import orjson
import pytest

from dependencies.deps import get_spimex_repo
from main import app

logger = logging.getLogger(__name__)


class FakeRepo:
    def __init__(self, result):
        self._result = result
        self.called = False

    async def get_all_trade_days(self, n):
        self.called = True
        return self._result

    async def get_dynamic(self, **kwargs):
        self.called = True
        return self._result

    async def get_trading_results(self, **kwargs):
        self.called = True
        return self._result


class DummyRedis:
    def __init__(self, cached_payload=None):
        self.cached_payload = cached_payload
        self.set_calls = []

    async def get(self, key):
        if self.cached_payload is None:
            return None
        return orjson.dumps(self.cached_payload)

    async def set(self, key, value, ex=None):
        self.set_calls.append((key, value, ex))
        return True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "scenario, repo_result, cached_payload, expected_len, expect_repo_call",
    [
        (
            "repo_nonempty",
            [
                {
                    "exchange_product_id": "1",
                    "exchange_product_name": "prod",
                    "oil_id": "A100",
                    "delivery_basis_id": "DB",
                    "delivery_basis_name": "DB-name",
                    "delivery_type_id": "DT",
                    "volume": 1.0,
                    "total": 100.0,
                    "count": 1,
                    "date": "2024-06-03T00:00:00",
                    "id": 1,
                    "created_on": "2024-06-03T00:00:00",
                    "updated_on": "2024-06-03T00:00:00",
                }
            ],
            None,
            1,
            True,
        ),
        ("repo_empty", [], None, 0, True),
        (
            "redis_hit",
            [
                {
                    "exchange_product_id": "1",
                    "exchange_product_name": "prod",
                    "oil_id": "A100",
                    "delivery_basis_id": "DB",
                    "delivery_basis_name": "DB-name",
                    "delivery_type_id": "DT",
                    "volume": 1.0,
                    "total": 100.0,
                    "count": 1,
                    "date": "2024-06-03T00:00:00",
                    "id": 1,
                    "created_on": "2024-06-03T00:00:00",
                    "updated_on": "2024-06-03T00:00:00",
                }
            ],
            [
                {
                    "exchange_product_id": "1",
                    "exchange_product_name": "prod",
                    "oil_id": "A100",
                    "delivery_basis_id": "DB",
                    "delivery_basis_name": "DB-name",
                    "delivery_type_id": "DT",
                    "volume": 1.0,
                    "total": 100.0,
                    "count": 1,
                    "date": "2024-06-03T00:00:00",
                    "id": 1,
                    "created_on": "2024-06-03T00:00:00",
                    "updated_on": "2024-06-03T00:00:00",
                }
            ],
            1,
            False,
        ),
    ],
)
async def test_get_last_trading_dates_parametrized(
    async_client,
    monkeypatch,
    scenario,
    repo_result,
    cached_payload,
    expected_len,
    expect_repo_call,
) -> None:
    fake_repo = FakeRepo(repo_result)

    app.dependency_overrides[get_spimex_repo] = lambda: fake_repo

    monkeypatch.setattr(
        "middlewares.redis_mw.redis_client",
        DummyRedis(cached_payload),
        raising=True,
    )

    response = await async_client.get("/spimex/last_trading_dates/5")
    logger.info("Response status: %s, body: %s", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == expected_len
    assert fake_repo.called is expect_repo_call


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, repo_result, cached_payload, expected_len",
    [
        (
            {"oil_id": "A100", "start_date": "2024-06-01", "end_date": "2024-06-03"},
            [
                {
                    "exchange_product_id": "1",
                    "exchange_product_name": "prod",
                    "oil_id": "A100",
                    "delivery_basis_id": "DB",
                    "delivery_basis_name": "DB-name",
                    "delivery_type_id": "DT",
                    "volume": 1.0,
                    "total": 100.0,
                    "count": 1,
                    "date": "2024-06-01T00:00:00",
                    "id": 1,
                    "created_on": "2024-06-01T00:00:00",
                    "updated_on": "2024-06-01T00:00:00",
                },
                {
                    "exchange_product_id": "2",
                    "exchange_product_name": "prod2",
                    "oil_id": "A100",
                    "delivery_basis_id": "DB",
                    "delivery_basis_name": "DB-name",
                    "delivery_type_id": "DT",
                    "volume": 2.0,
                    "total": 200.0,
                    "count": 2,
                    "date": "2024-06-03T00:00:00",
                    "id": 2,
                    "created_on": "2024-06-03T00:00:00",
                    "updated_on": "2024-06-03T00:00:00",
                },
            ],
            None,
            2,
        ),
        (
            {"oil_id": "A100", "start_date": "2024-06-01", "end_date": "2024-06-03"},
            [],
            None,
            0,
        ),
    ],
)
async def test_get_dynamics_parametrized(
    async_client, monkeypatch, params, repo_result, cached_payload, expected_len
):
    fake_repo = FakeRepo(repo_result)

    app.dependency_overrides[get_spimex_repo] = lambda: fake_repo
    monkeypatch.setattr(
        "middlewares.redis_mw.redis_client", DummyRedis(cached_payload), raising=True
    )

    response = await async_client.get("/spimex/dynamics", params=params)
    logger.info("Response status: %s, body: %s", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == expected_len


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, repo_result, expected_len",
    [
        (
            {"oil_id": "A100", "date": "2024-06-03"},
            [
                {
                    "exchange_product_id": "1",
                    "exchange_product_name": "prod",
                    "oil_id": "A100",
                    "delivery_basis_id": "DB",
                    "delivery_basis_name": "DB-name",
                    "delivery_type_id": "DT",
                    "volume": 1.0,
                    "total": 100.0,
                    "count": 1,
                    "date": "2024-06-03T00:00:00",
                    "id": 1,
                    "created_on": "2024-06-03T00:00:00",
                    "updated_on": "2024-06-03T00:00:00",
                }
            ],
            1,
        ),
        ({"oil_id": "A100", "date": "1900-01-01"}, [], 0),
    ],
)
async def test_get_trading_results_parametrized(
    async_client, monkeypatch, params, repo_result, expected_len
):
    fake_repo = FakeRepo(repo_result)

    app.dependency_overrides[get_spimex_repo] = lambda: fake_repo
    monkeypatch.setattr(
        "middlewares.redis_mw.redis_client", DummyRedis(None), raising=True
    )

    response = await async_client.get("/spimex/trading_results", params=params)
    logger.info("Response status: %s, body: %s", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == expected_len


@pytest.mark.asyncio
async def test_nonexistent_endpoint_returns_404(async_client):
    r = await async_client.get("/spimex/nonexistent")
    assert r.status_code == 404
