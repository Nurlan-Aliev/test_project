from typing import List
from sqlalchemy import String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(30))
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    status: Mapped[str] = mapped_column(String(10))
    email: Mapped[str] = mapped_column(String, nullable=False)
    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="user")
    create_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None),
        nullable=False,
    )


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="accounts")

    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="account"
    )

    create_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None),
        nullable=False,
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
    create_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None),
        nullable=False,
    )
