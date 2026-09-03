from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base


class Cart(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )
    
    product_id: Mapped[int] = mapped_column(
            ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )
    
    user: Mapped["User"] = relationship(back_populates="carts")
    
    product: Mapped["Product"] = relationship(back_populates="carts")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)