from datetime import date

import pytest

from repositories.sql_repository import SpimexSQLRepository

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("n", [1, 2])
async def test_spimex_repo_get_all_n_last_days(n: int):
    repo = SpimexSQLRepository
    res = await repo().get_all_trade_days(n)
    assert len(res) > 0


@pytest.mark.parametrize(
    "oil_id, start_date, end_date",
    [
        ("A100", date(2025, 8, 7), date(2025, 8, 7)),
    ],
)
async def test_get_dynamic(session, oil_id: str, start_date: date, end_date: date):
    repo = SpimexSQLRepository(session)
    res = await repo.get_dynamic(oil_id, start_date=start_date, end_date=end_date)
    res = res[0].model_dump(exclude_none=True)
    assert res.get("id") is not None


@pytest.mark.parametrize(
    "oil_id, delivery_type_id, delivery_basis_id", [("A100", None, None)]
)
async def test_get_trading_results(
    oil_id: str, delivery_type_id: str | None, delivery_basis_id: str | None
):
    repo = SpimexSQLRepository
    res = await repo().get_trading_results(oil_id, delivery_type_id, delivery_basis_id)
    assert len(res) > 0
    res = res[0].model_dump(exclude_none=True)
    assert res.get("id") is not None
    assert res.get("oil_id") == oil_id
