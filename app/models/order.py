from typing import Optional
from enum import Enum
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class Status(str, Enum):
    pending = "pending" 
    confirmed = "confirmed"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    refunded = "refunded"

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    amount: Mapped[float] = mapped_column(Float, nullable=False)

    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )
    
    product_id: Mapped[int] = mapped_column(
            ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    status: Mapped[Status] = mapped_column(SQLEnum(Status), server_default=Status.pending, nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="orders")
    
    product: Mapped["Product"] = relationship(back_populates="orders")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)

    expected_delivery_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    processing_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    out_for_delivery_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
    refunded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)