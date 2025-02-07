from sqlalchemy import select
from src.database import db_helper
from src.models import User, Account


async def get_user(user_email):
    stmt = select(User).where(User.email == user_email)
    async with db_helper.async_session() as session:
        user = await session.scalars(stmt)
    return user.first()


async def get_accounts(user_email: str) -> list:
    stmt = (
        select(Account)
        .join(User)
        .where(User.email == user_email)
        .where(User.is_active == True)
    )
    async with db_helper.async_session() as session:
        result = await session.scalars(stmt)
        user = result.all()
    if user:
        return user
    return []
