from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func, Enum as SQLEnum, Integer
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base
import bcrypt

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Role(str, Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)
    lastname: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    age: Mapped[int | None]= mapped_column(Integer, nullable=True)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), server_default=Role.user, nullable=False)

    password_hash: Mapped[str] = mapped_column(
        "password",
        String(500),
        nullable=False
    )

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, value: str) -> None:
        self.password_hash = bcrypt.hashpw(
            value.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password_hash(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)

    carts: Mapped[list["Cart"]] = relationship(
           back_populates="user"
    )

    orders: Mapped[list["Order"]] = relationship(
               back_populates="user"
        )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)