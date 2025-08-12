from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SpimexTradingResultOut(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str | None = None
    delivery_basis_name: str | None = None
    delivery_type_id: str | None = None
    volume: float | None = None
    total: float | None = None
    count: int | None = None
    date: datetime
    id: int
    created_on: datetime | None = None
    updated_on: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class LastTradingDatesRequest(BaseModel):
    n: int = Field(..., ge=1, description="Количество последних торговых дней")


class DynamicsRequest(BaseModel):
    start_date: date = Field(..., description="Дата начала периода")
    end_date: date = Field(..., description="Дата конца периода")
    oil_id: str = Field(..., description="Фильтр по нефти")
    delivery_type_id: Optional[int] = Field(None, description="Тип поставки")
    delivery_basis_id: Optional[int] = Field(None, description="Базис поставки")

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("Дата конца периода должна быть >= даты начала")
        return self

class TradingResultsRequest(BaseModel):
    oil_id: int = Field(..., description="Фильтр по нефти")
    delivery_type_id: Optional[int] = Field(None, description="Тип поставки")
    delivery_basis_id: Optional[int] = Field(None, description="Базис поставки")
