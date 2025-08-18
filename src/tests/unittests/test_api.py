import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_get_last_trading_dates(async_client) -> None:
    response = await async_client.get("/spimex/last_trading_dates/5")
    logger.info("Response status: %s, body: %s", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "date" in data[0]


@pytest.mark.asyncio
async def test_get_dynamics(async_client) -> None:
    params = {"oil_id": "A100", "start_date": "2024-06-01", "end_date": "2024-06-03"}
    response = await async_client.get("/spimex/dynamics", params=params)
    logger.info("Response status: %s, body: %s", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "date" in data[0]

@pytest.mark.asyncio
async def test_get_trading_results(async_client) -> None:
    params = {"oil_id": "A100", "date": "2024-06-03"}
    response = await async_client.get("/spimex/trading_results", params=params)
    logger.info("Response status: %s, body: %s", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "date" in data[0]
