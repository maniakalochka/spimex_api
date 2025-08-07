from models.spimex import SpimexTradingResult
from .base import AbstractRepository
from sqlalchemy import select, distinct, desc, func, text
from datetime import datetime

from databases.db import async_session
from calendar import Day



class SpimexSQLRepository(AbstractRepository):
    def __init__(self):
        super().__init__(SpimexTradingResult, async_session)  # type: ignore


    async def get_all(self, n: int) -> list[SpimexTradingResult]:

        async with async_session() as session:
            stmt = (
                select(self.mode)
                .where(func.DATE(self.model.date) == func.DATE(func.now() - text(f"INTERVAL '{n} days'"))) # type: ignore
                .order_by(desc(self.model.date)) # type: ignore
        )
        result = await session.execute(stmt)
        return result.scalars().all()  # type: ignore

    async def get_dynamic(self,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        start_date: datetime,
        end_date: datetime) -> list[SpimexTradingResult]:
        async with async_session() as session:
            start_date_subq = (
                select(self.model.date)  # type: ignore
                .order_by(desc(self.model.date))  # type: ignore
                .limit(1)
            )
            end_date_subq = (
                select(self.model.date)
                .order_by((self.model.date))  # type: ignore
                .limit(1)
            )
            stmt  = (
                select(self.model)  # type: ignore
                .where(self.model.date >= start_date_subq,
                       self.model.date <= end_date_subq,
                       self.model.oil_id == oil_id,
                       self.model.delivery_type_id == delivery_type_id,
                       self.model.delivery_basis_id == delivery_basis_id)
                .order_by(self.model.date) # type: ignore
            )
            result = await session.execute(stmt)
            return result.scalars().all()  #type: ignore
