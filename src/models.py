from typing import List
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String(10))
    email: Mapped[str] = mapped_column(String, nullable=False)
    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="user")
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    transaction: Mapped[List["Account"]] = relationship(
        "User", back_populates="accounts"
    )
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
