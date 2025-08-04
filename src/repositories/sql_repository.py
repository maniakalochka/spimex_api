from sqlalchemy.sql.expression import distinct
from .base import AbstractRepository
from fastapi import HTTPException, status
from sqlalchemy import select, distinct, desc, asc

from sqlalchemy.ext.asyncio import AsyncSession
from databases.db import async_session



class SQLRepository(AbstractRepository):
    async def get_all(self, n: int):
        async with async_session() as session:
            stmt = select(distinct(self.model.date) # type: ignore
            .order_by(desc(self.model.date))  # type: ignore
            .limit(n)
            .subquery()
            )
        result = await session.execute(stmt)
        return result.scalars().all()
