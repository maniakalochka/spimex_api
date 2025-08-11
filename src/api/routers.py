from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.deps import get_spimex_repo
from repositories.sql_repository import SpimexSQLRepository


router = APIRouter(prefix="/spimex", tags=["spimex"])


@router.get("/last_trading_dates/{n}")
async def get_last_trading_dates(
    n: int,
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
):
    result = await repo.get_all_trade_days(n)
    if not result:
        return {"message": f"Нет данных за указанные {n} дней."}
    return result


@router.get("/dynamics")
async def get_dynamics(
    repo: Annotated[SpimexSQLRepository, Depends(get_spimex_repo)],
    oil_id: str,
    delivery_type_id: str | None = None,
    delivery_basis_id: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    return await repo.get_dynamic(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
        start_date=start_date,
        end_date=end_date,
    )



@router.get("/trading_results")
async def get_trading_results(
    repo: Annotated[
        SpimexSQLRepository, Depends(get_spimex_repo)
    ],
    oil_id: str,
    delivery_type_id: str | None = None,
    delivery_basis_id: str | None = None,
):
    return await repo.get_trading_results(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )
