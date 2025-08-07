from models.spimex import SpimexTradingResult
from .base import AbstractRepository
from sqlalchemy import select, distinct, desc, func, text
from datetime import date

from databases.db import async_session



class SpimexSQLRepository(AbstractRepository):
    def __init__(self):
        super().__init__(SpimexTradingResult, async_session)  # type: ignore


    async def get_all(self, n: int) -> list[SpimexTradingResult]:

        async with async_session() as session:
            stmt = (
                select(self.model)
                .where(func.DATE(self.model.date) == func.DATE(func.now() - text(f"INTERVAL '{n} days'"))) # type: ignore
                .order_by(desc(self.model.date)) # type: ignore
        )
        result = await session.execute(stmt)
        return result.scalars().all()  # type: ignore

    async def get_dynamic(
        self,
        oil_id: str,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[SpimexTradingResult]:
        async with async_session() as session:
            conditions = [self.model.oil_id == oil_id]

            if delivery_type_id is not None:
                conditions.append(self.model.delivery_type_id == delivery_type_id)

            if delivery_basis_id is not None:
                conditions.append(self.model.delivery_basis_id == delivery_basis_id)

            if start_date is not None:
                conditions.append(self.model.date >= start_date)

            if end_date is not None:
                conditions.append(self.model.date <= end_date)

            stmt = (
                select(self.model)
                .where(*conditions)
                .order_by(self.model.date)
            )

            result = await session.execute(stmt)
            return result.scalars().all()
