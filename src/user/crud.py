from sqlalchemy import select
from src.database import db_helper
from src.models import User, Account


async def get_user(id):
    stmt = select(User).where(User.id == id)
    async with db_helper.async_session() as session:
        user = await session.scalars(stmt)
    return user.first()


async def get_accounts(id: int) -> list:
    stmt = (
        select(Account).join(User).where(User.id == id).where(Account.is_active == True)
    )
    async with db_helper.async_session() as session:
        result = await session.scalars(stmt)
        user = result.all()
    if user:
        return user
    return []
