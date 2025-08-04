from fastapi import APIRouter


spimex_router = APIRouter(tags=["spimex"])


@spimex_router.get("/last_trading_dates")
async def get_last_trading_dates():
    pass

@spimex_router.get("/dynamic")
async def get_dynamic():
    pass

@spimex_router.get("/results")
async def get_trading_results():
    pass
