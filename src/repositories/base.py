from abc import ABC, abstractmethod
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    __abstract__ = True

    def __init__(self, model, session: AsyncSession) -> None:
        self.model = model
        self.session = session

    @abstractmethod
    async def get_all_trade_days(self, n: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    async def get_dynamic(
        self,
        oil_id: str,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        raise NotImplementedError("This method should be overridden by subclasses")

    async def get_trading_results(
        self,
        oil_id: str,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
    ):
        raise NotImplementedError("This method should be overridden by subclasses")
