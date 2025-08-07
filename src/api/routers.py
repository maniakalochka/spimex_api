from models.spimex import SpimexTradingResult
from fastapi import APIRouter

from repositories.sql_repository import SpimexSQLRepository


spimex_router = APIRouter(tags=["spimex"])


@spimex_router.get("/last_trading_dates/{n}")
async def get_last_trading_dates(n: int):
    repo = SpimexSQLRepository()
    return await repo.get_all(n)

@spimex_router.get("/dynamic")
async def get_dynamic():
    pass

@spimex_router.get("/results")
async def get_trading_results():
    pass
