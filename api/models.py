from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    version: str


class Order(BaseModel):
    index: Optional[int] = None  # Optional since it's nullable in the schema
    OrderID: Optional[str] = None
    Date: Optional[str] = None
    Status: Optional[str] = None
    Fulfilment: Optional[str] = None
    SalesChannel: Optional[str] = None
    ship_service_level: Optional[str] = None
    Style: Optional[str] = None
    SKU: Optional[str] = None
    Category: Optional[str] = None
    Size: Optional[str] = None
    ASIN: Optional[str] = None
    courier_status: Optional[str] = None
    Qty: Optional[int] = None  # Assuming Qty is intended to be an integer
    currency: Optional[str] = None
    Amount: Optional[float] = None
    ship_city: Optional[str] = None
    ship_state: Optional[str] = None
    ship_postal_code: Optional[float] = None  # Keeping as float since schema specifies double
    ship_country: Optional[str] = None
    promotion_ids: Optional[str] = None
    B2B: Optional[bool] = None  # Assuming B2B is a boolean (tinyint(1) suggests 0 or 1)
    fulfilled_by: Optional[str] = None


class OrderResponse(BaseModel):
    index: Optional[int] = None  # Optional since it's nullable in the schema
    OrderID: Optional[str] = None
    Date: Optional[str] = None
    Status: Optional[str] = None
    Fulfilment: Optional[str] = None
    SalesChannel: Optional[str] = None
    ship_service_level: Optional[str] = None
    Style: Optional[str] = None
    SKU: Optional[str] = None
    Category: Optional[str] = None
    Size: Optional[str] = None
    ASIN: Optional[str] = None
    courier_status: Optional[str] = None
    Qty: Optional[int] = None  # Assuming Qty is intended to be an integer
    currency: Optional[str] = None
    Amount: Optional[float] = None
    ship_city: Optional[str] = None
    ship_state: Optional[str] = None
    ship_postal_code: Optional[float] = None  # Keeping as float since schema specifies double
    ship_country: Optional[str] = None
    promotion_ids: Optional[str] = None
    B2B: Optional[bool] = None  # Assuming B2B is a boolean (tinyint(1) suggests 0 or 1)
    fulfilled_by: Optional[str] = None

    class Config:
        orm_mode = True
