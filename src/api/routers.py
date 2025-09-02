from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from dependencies.deps import get_spimex_repo
from repositories.sql_repository import SpimexSQLRepository
from schemas.spimex import (DynamicsRequest, SpimexTradingResultOut,
                            TradingResultsRequest)

router = APIRouter(prefix="/spimex", tags=["spimex"])


@router.get("/last_trading_dates/{n}", response_model=list[SpimexTradingResultOut])
async def get_last_trading_dates(
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
    n: int = Path(..., ge=1, description="Количество последних торговых дней"),
):
    result = await repo.get_all_trade_days(n)
    if not result:
        raise HTTPException(status_code=404, detail="No trading dates found")
    return result


@router.get("/dynamics", response_model=list[SpimexTradingResultOut])
async def get_dynamics(
    params: Annotated[DynamicsRequest, Depends()],
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
):
    result = await repo.get_dynamic(**params.model_dump())
    if not result:
        raise HTTPException(
            status_code=404, detail="No dynamics found for the given parameters"
        )
    return result


@router.get("/trading_results", response_model=list[SpimexTradingResultOut])
async def get_trading_results(
    params: Annotated[TradingResultsRequest, Depends()],
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
):
    result = await repo.get_trading_results(**params.model_dump())
    if not result:
        raise HTTPException(
            status_code=404, detail="No trading results found for the given parameters"
        )
    return result
