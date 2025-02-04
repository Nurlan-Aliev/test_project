from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.database import db_helper
from src.models import User, Account
from src.user.schema import CreateUserSchemas


async def create_account(email, balance):
    user = await get_user(email)
    spongebob = Account(
        balance=balance,
        user_id=user.id,
        user=user,
    )
    async with db_helper.async_session() as session:
        session.add(spongebob)
        await session.commit()


async def create_new_user(user: CreateUserSchemas):
    user = user.model_dump()
    new_user = User(**user)
    async with db_helper.async_session() as session:
        session.add(new_user)
        await session.commit()


async def get_user(user_email):
    stmt = select(User).where(User.email == user_email)
    async with db_helper.async_session() as session:
        user = await session.scalars(stmt)
    return user.first()


async def get_accounts(user_email: str) -> list:
    stmt = (
        select(User).where(User.email == user_email).options(joinedload(User.accounts))
    )
    async with db_helper.async_session() as session:
        result = await session.scalars(stmt)
        user = result.first()
    if user:
        return [{"id": acc.id, "balance": acc.balance} for acc in user.accounts]
    return []
