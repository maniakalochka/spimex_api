from abc import ABC, abstractmethod
from models.spimex import SpimexTradingResult
from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)




class AbstractRepository(ABC):

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    @abstractmethod
    def get_all(self, n: int):
        raise NotImplementedError("This method should be overridden by subclasses")
