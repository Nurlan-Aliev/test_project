from asyncio import current_task
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)


class Base(DeclarativeBase):
    pass


class DataBaseHelper:
    def __init__(self, url, echo=False):
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
