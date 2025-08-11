from datetime import date, timedelta

from sqlalchemy import and_, desc, func, select

from databases.db import async_session
from models.spimex import SpimexTradingResult
from schemas.spimex import SpimexTradingResultOut

from .base import AbstractRepository


class SpimexSQLRepository(AbstractRepository):
    def __init__(self):
        self.model = SpimexTradingResult
        self.session = async_session

    async def get_all(self, n: int) -> list[SpimexTradingResult]:
        """
        Дать торги строго за дату (today - n дней).
        Безопасно считаем целевую дату в Python, чтобы не собирать raw SQL для INTERVAL.
        """
        target_date: date = date.today() - timedelta(days=n)
        async with async_session() as session:
            stmt = (
                select(self.model)
                .where(func.DATE(self.model.date) == target_date)
                .order_by(desc(self.model.date))
            )
            res = await session.execute(stmt)
            items = list(res.scalars().all())
            return [SpimexTradingResultOut.model_validate(it) for it in items]  # type: ignore

    async def get_dynamic(
        self,
        oil_id: str,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[SpimexTradingResult]:
        conds = [self.model.oil_id == oil_id]
        if delivery_type_id is not None:
            conds.append(self.model.delivery_type_id == delivery_type_id)
        if delivery_basis_id is not None:
            conds.append(self.model.delivery_basis_id == delivery_basis_id)
        if start_date is not None:
            conds.append(self.model.date >= start_date)
        if end_date is not None:
            conds.append(self.model.date <= end_date)
        async with async_session() as session:
            stmt = (
                select(self.model).where(and_(*conds)).order_by(self.model.date.asc())
            )
            res = await session.execute(stmt)
            items = list(res.scalars().all())
            return [SpimexTradingResultOut.model_validate(it) for it in items]  # type: ignore

    async def get_trading_results(
        self,
        oil_id: str,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
    ) -> list[SpimexTradingResult]:
        async with async_session() as session:
            conditions = [self.model.oil_id == oil_id]

            if delivery_type_id is not None:
                conditions.append(self.model.delivery_type_id == delivery_type_id)

            if delivery_basis_id is not None:
                conditions.append(self.model.delivery_basis_id == delivery_basis_id)

            last_date_subq = (
                select(func.max(self.model.date)).where(*conditions).scalar_subquery()
            )

            stmt = (
                select(self.model)
                .where(self.model.date == last_date_subq, *conditions)
                .order_by(self.model.date)
            )

            result = await session.execute(stmt)
            items = result.scalars().all()
            return [SpimexTradingResultOut.model_validate(it) for it in items]  # type: ignore
