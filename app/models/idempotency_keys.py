from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, ForeignKey, UUID
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column
from app.config.database import Base
import uuid
from sqlalchemy.dialects.postgresql import JSONB

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), nullable=True, default="created")
    response_status: Mapped[int] = mapped_column(Integer, nullable=True, default=200)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=True, default="created")  # What was created, e.g. ORDER
    resource_id: Mapped[str] = mapped_column(String(255), nullable=True)
    response_body: Mapped[dict] = mapped_column(JSONB, nullable=True)

    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)