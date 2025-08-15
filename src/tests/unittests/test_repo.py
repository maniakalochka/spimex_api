import pytest
from datetime import date
from repositories.sql_repository import SpimexSQLRepository


@pytest.mark.parametrize("n",
    [
    1,
    2]
)
async def test_spimex_repo_get_all_n_last_days(n: int):
    repo = SpimexSQLRepository
    res = await repo().get_all_trade_days(n)
    assert len(res) > 0


@pytest.mark.parametrize("oil_id, start_date, end_date",
[
        ("A100", date(2025, 8, 7), date(2025, 8, 7)),
        ("A100", date(2023, 8, 7), date(2023, 8, 7)),
    ])

async def test_get_dynamic(oil_id: str, start_date: date,  end_date: date):
    repo = SpimexSQLRepository
    res = await repo().get_dynamic(oil_id, start_date=start_date, end_date=end_date)
    res = res[0].model_dump(exclude_none=True)
    print(res)
    # if 'id' not in res[0].model_fields:
    assert res.get('id') is not None # type: ignore
    # assert res[0].model_fields() # type: ignore

    # assert res.oil_id == oil_id  # type: ignore
    # assert res.date == start_date  # type: ignore
    # assert res.date == end_date  # type: ignore
