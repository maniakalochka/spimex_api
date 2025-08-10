# dependencies.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.db import get_db
from repositories.sql_repository import SpimexSQLRepository


def get_spimex_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> SpimexSQLRepository:
    return SpimexSQLRepository()
