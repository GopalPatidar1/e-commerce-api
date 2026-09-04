from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class CreateProduct(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=255)
    amount: int = Field(ge=1)
    model_config = ConfigDict(extra="forbid")

class ProductGetResponse(BaseModel):
    id: int
    name: str
    description: str
    amount: int