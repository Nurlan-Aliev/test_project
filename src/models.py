from typing import List
from sqlalchemy import String, LargeBinary, ForeignKey, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"
    fullname: Mapped[str] = mapped_column(String(30))
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="user")
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(server_default=text("true"), default=True)
    accounts: Mapped[List["Account"]] = relationship(
        "Account", back_populates="user", cascade="all, delete"
    )


class Account(Base):
    __tablename__ = "accounts"

    balance: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="accounts")
    is_active: Mapped[bool] = mapped_column(server_default=text("true"), default=True)
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="account", cascade="all, delete"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
