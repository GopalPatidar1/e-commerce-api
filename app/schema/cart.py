from pydantic import BaseModel, Field
from enum import Enum

class CartDateFilter(str, Enum):
    PAST_WEEK = "past_week"
    PAST_MONTH = "past_month"
    LAST_3_MONTHS = "last_3_months"
    CUSTOM = "custom"

class CartItem(BaseModel):
    product_id: int

class ProductInfo(BaseModel):
    id: int
    name: str
    description: str
    amount: int
    img_path: str

class CartResponseItem(BaseModel):
    id: int
    product_id: int
    product: ProductInfo


class CartResponse(BaseModel):
    next_cursor: int | None = None
    avail_next: bool
    result: list[CartResponseItem]