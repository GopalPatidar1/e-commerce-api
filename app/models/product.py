from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Integer, nullable=False)
    img_path: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    carts: Mapped[list["Cart"]] = relationship(back_populates="product")

    orders: Mapped[list["Order"]] = relationship(back_populates="product")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)