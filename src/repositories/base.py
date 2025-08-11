from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    __abstract__ = True

    def __init__(self, model, session: AsyncSession) -> None:
        self.model = model
        self.session = session

    @abstractmethod
    async def get_all_trade_days(self, n: int):
        raise NotImplementedError("This method should be overridden by subclasses")
