from datetime import date

import pytest
from sqlalchemy import text

from repositories.sql_repository import SpimexSQLRepository
from models.spimex import SpimexTradingResult
from databases.db import async_session

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("n", [1, 2])
async def test_spimex_repo_get_all_n_last_days(n: int):
    tbl = SpimexTradingResult.__tablename__
    raw_sql = text(f"""
            SELECT *
            FROM {tbl}
            WHERE CAST(date AS DATE) IN (
                SELECT CAST(date AS DATE) AS d
                FROM {tbl}
                GROUP BY d
                ORDER BY d DESC
                LIMIT :n
            )
            ORDER BY date DESC;
        """)

    repo = SpimexSQLRepository()
    repo_res = await repo.get_all_trade_days(n)
    repo_ids = {r.id for r in repo_res}

    async with async_session() as session:
        rows = await session.execute(raw_sql, {"n": n})
        sql_res = rows.mappings().all()
        sql_ids = {row["id"] for row in sql_res}

    assert repo_ids == sql_ids


@pytest.mark.parametrize(
    "oil_id, start_date, end_date",
    [
        ("A100", date(2025, 8, 7), date(2025, 8, 7)),
    ],
)
async def test_get_dynamic(session, oil_id: str, start_date: date, end_date: date):
    tbl = SpimexTradingResult.__tablename__
    raw_sql = text(f"""
        SELECT *
        FROM {tbl}
        WHERE oil_id = :oil_id
          AND delivery_type_id  = COALESCE(CAST(:delivery_type_id  AS VARCHAR), delivery_type_id)
          AND delivery_basis_id = COALESCE(CAST(:delivery_basis_id AS VARCHAR), delivery_basis_id)
          AND date >= COALESCE(CAST(:start_date AS DATE), date)
          AND date <= COALESCE(CAST(:end_date   AS DATE), date)
        ORDER BY date ASC;
    """)
    repo = SpimexSQLRepository()
    repo_res = await repo.get_dynamic(
        oil_id=oil_id,
        delivery_type_id=None,
        delivery_basis_id=None,
        start_date=start_date,
        end_date=end_date,
    )
    repo_ids = {r.id for r in repo_res}

    async with async_session() as session:
        rows = await session.execute(raw_sql, {
            "oil_id": oil_id,
            "delivery_type_id": None,
            "delivery_basis_id": None,
            "start_date": start_date,
            "end_date": end_date,
        })
        sql_res = rows.mappings().all()
        sql_ids = {row["id"] for row in sql_res}

    assert repo_ids == sql_ids


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
