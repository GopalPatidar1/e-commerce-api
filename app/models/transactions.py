from sqlalchemy import (Integer, String, ForeignKey, DateTime, Text, Boolean, UUID, Float)
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import datetime
import uuid

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
         UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
        )
    
    user_id: Mapped[int] = mapped_column(
                ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
                nullable=False,
            )

    order_id:  Mapped[int] = mapped_column(
            ForeignKey("orders.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    payment_link_id: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    payment_id: Mapped[str] = mapped_column(String(100), nullable=True, index=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    refund_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(10), nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=True, default="created")

    payment_method: Mapped[str] = mapped_column(String(50), nullable=True)
    razorpay_status: Mapped[str] = mapped_column(String(50), nullable=True)
    refund_status: Mapped[str] = mapped_column(String(50), nullable=True)
    refund_id: Mapped[str] = mapped_column(String(100), nullable=True)
    failure_reason: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="transactions")
    order: Mapped["Order"] = relationship(back_populates="transactions")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)