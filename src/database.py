from settings import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(primary_key=True)

    create_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None),
        nullable=False,
    )


class DataBaseHelper:
    def __init__(self, url: str, echo=False):
        self.async_engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.async_session = async_sessionmaker(
            self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DataBaseHelper(
    settings.db_connect,
)
