from models.spimex import SpimexTradingResult
from .base import AbstractRepository
from sqlalchemy import select, distinct, desc
from datetime import datetime

from databases.db import async_session



class SpimexSQLRepository(AbstractRepository):
    def __init__(self):
        super().__init__(SpimexTradingResult, async_session)  # type: ignore


    async def get_all(self, n: int) -> list[SpimexTradingResult]:
        async with async_session() as session:
            stmt = (
                select(self.model)
                .order_by(desc(self.model.date))  # type: ignore
                .limit(n)
        )
        result = await session.execute(stmt)
        return result.scalars().all()  # type: ignore

    async def get_dynamic(self,
        oil_id: int,
        delivery_type_id: int,
        delivery_basis_id,
        start_date: datetime,
        end_date: datetime) -> list[SpimexTradingResult]:
        async with async_session() as session:
            stmt  = (
                select(self.model)  # type: ignore
                .where(
                    self.model.oil_id == oil_id,  # type: ignore
                    self.model.delivery_type_id == delivery_type_id,  # type: ignore
                    self.model.delivery_basis_id == delivery_basis_id,  # type: ignore
                    self.model.date >= start_date, # type: ignore
                    self.model.date <= end_date  # type: ignore
                )
                .order_by(self.model.date)  # type: ignore
            )
            result = await session.execute(stmt)
            return result.scalars().all()  #type: ignore
