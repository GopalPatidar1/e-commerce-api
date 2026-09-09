from pydantic import BaseModel, Field
from enum import Enum

class Status(str, Enum):
    pending = "pending" 
    confirmed = "confirmed"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    refunded = "refunded"

class OrderDateFilter(str, Enum):
    PAST_WEEK = "past_week"
    PAST_MONTH = "past_month"
    LAST_3_MONTHS = "last_3_months"
    CUSTOM = "custom"

class OrderItem(BaseModel):
    quantity: int = Field(ge=1, default=1)
    product_id: int

class UpdateOrderItem(BaseModel):
    amount: int | None = Field(default=None, ge=1)
    # status: Status | None = None
    description: str | None = Field(min_length=5, max_length=255)
    name: int | None = None

class UserInfo(BaseModel):
    firstname: str
    lastname: str

class ProductInfo(BaseModel):
    id: int
    name: str
    description: str
    amount: int
    img_path: str

class OrderResponseItem(BaseModel):
    id: int
    amount: int
    quantity: int
    status: Status
    product: ProductInfo
    user: UserInfo


class OrderResponse(BaseModel):
    next_cursor: int | None = None
    avail_next: bool
    result: list[OrderResponseItem]