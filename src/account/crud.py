from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
from src.database import db_helper
from src.models import User, Account
from src.user.crud import get_user
from src.account.schemas import (
    AccountSchema,
    CreateAccount,
)


async def create_new_account(account: CreateAccount) -> Account:
    user = await get_user(account.email)
    if user:
        account = Account(
            balance=account.balance,
            user_id=user.id,
            user=user,
        )
        async with db_helper.async_session() as session:
            session.add(account)
            await session.commit()
        return account
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


async def update_account(account: AccountSchema):
    stmt = select(Account).where(Account.id == account.id)

    async with db_helper.async_session() as session:
        acc = await session.scalars(stmt)
        acc = acc.first()
        if acc:
            acc.balance = account.balance
            await session.commit()
            return acc


async def delete_account(account: AccountSchema):
    async with db_helper.async_session() as session:
        acc = await session.get(Account, account.id)
        if acc:
            await session.delete(acc)
            await session.commit()
            return acc
    return None
