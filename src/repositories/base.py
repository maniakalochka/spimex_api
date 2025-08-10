from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from models.spimex import SpimexTradingResult

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    __abstract__ = True

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    @abstractmethod
    async def get_all(self, n: int) -> list[ModelType]:
        raise NotImplementedError("This method should be overridden by subclasses")
