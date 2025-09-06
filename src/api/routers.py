from typing import Annotated

from fastapi import APIRouter, Depends, Path

from dependencies.deps import get_spimex_repo
from repositories.sql_repository import SpimexSQLRepository
from schemas.spimex import (
    DynamicsRequest,
    SpimexTradingResultOut,
    TradingResultsRequest,
)

router = APIRouter(prefix="/spimex", tags=["spimex"])


@router.get("/last_trading_dates/{n}", response_model=list[SpimexTradingResultOut])
async def get_last_trading_dates(
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
    n: int = Path(..., ge=1, description="Количество последних торговых дней"),
) -> list[SpimexTradingResultOut]:
    result = await repo.get_all_trade_days(n)
    if not result:
        return []
    return result


@router.get("/dynamics", response_model=list[SpimexTradingResultOut])
async def get_dynamics(
    params: Annotated[DynamicsRequest, Depends()],
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
) -> list[SpimexTradingResultOut]:
    result = await repo.get_dynamic(**params.model_dump())
    if not result:
        return []
    return result


@router.get("/trading_results", response_model=list[SpimexTradingResultOut])
async def get_trading_results(
    params: Annotated[TradingResultsRequest, Depends()],
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
) -> list[SpimexTradingResultOut]:
    result = await repo.get_trading_results(**params.model_dump())
    if not result:
        return []
    return result
