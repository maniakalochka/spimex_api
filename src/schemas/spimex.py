from datetime import date
from pydantic import BaseModel, field_validator


class TradingResultSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: float
    total: float
    count: int
    date: date

@field_validator("volume", "total", mode="before")
@classmethod
def parse_floats(cls, value):
    if isinstance(value, str):
        return float(value.replace(",", "."))
    return value
