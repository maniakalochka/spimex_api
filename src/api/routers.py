import datetime
from fastapi import APIRouter, Query

from models.spimex import SpimexTradingResult
from repositories.sql_repository import SpimexSQLRepository

spimex_router = APIRouter(tags=["spimex"])


@spimex_router.get("/last_trading_dates/{n}")
async def get_last_trading_dates(n: int):
    repo = SpimexSQLRepository()
    return await repo.get_all(n)

@spimex_router.get("/dynamic")
async def get_dynamic(
    oil_id: str = Query(..., description="ID of the oil"),
    delivery_type_id: str= Query(None, description="ID of the delivery type"),
    delivery_basis_id: str = Query(None, description="ID of the delivery basis"),
    start_date: datetime.date  = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime.date = Query(None, description="End date in YYYY-MM-DD format")
):
    repo = SpimexSQLRepository()
    return await repo.get_dynamic(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
        start_date=start_date,
        end_date=end_date)

@spimex_router.get("/latest")
async def get_latest_trading_results(
    oil_id: str = Query(..., description="ID of the oil"),
    delivery_type_id: str = Query(None, description="ID of the delivery type"),
    delivery_basis_id: str = Query(None, description="ID of the delivery basis")
):
    repo = SpimexSQLRepository()
    return await repo.get_trading_results(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id
    )
