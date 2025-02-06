from sqlalchemy import select, update
from src.admin.user import schema
from src.database import db_helper
from src.models import User, Account


async def create_new_user(user: schema.CreateUserSchemas):

    stmt = select(User).where(User.email == user.email)
    async with db_helper.async_session() as session:
        is_user_exist = await session.scalars(stmt)
        if not is_user_exist.first():
            user = user.model_dump()
            new_user = User(**user)
            session.add(new_user)
            await session.commit()
            return new_user


async def update_exist_user(user: schema.UpdateUserSchemas):
    stmt = select(User).where(User.id == user.id)
    async with db_helper.async_session() as session:
        is_user_exist = await session.scalars(stmt)
        user_exist = is_user_exist.first()
        if user_exist:
            user_exist.fullname = (
                user.fullname if user.fullname else user_exist.fullname
            )
            user_exist.status = user.status if user.status else user_exist.status
            user_exist.email = user.email if user.email else user_exist.email
            user_exist.password = (
                user.password if user.password else user_exist.password
            )
            await session.commit()
            return user_exist


async def delete_exist_user(user: schema.DeleteUserSchemas):
    stmt = update(Account).where(Account.user_id == user.id).values(is_active=False)

    async with db_helper.async_session() as session:
        user_exist = await session.get(User, user.id)
        if user_exist:
            user_exist.is_active = False
            await session.execute(stmt)
            await session.commit()
