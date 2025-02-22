from sqlalchemy import select
from src.database import db_helper
from src.models import Account
from src.user.crud import get_user
from src.admin.account import schemas


async def create_new_account(account: schemas.CreateAccount) -> Account:
    user = await get_user(account.user_id)
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


async def update_account(account: schemas.AccountSchema):
    stmt = select(Account).where(Account.id == account.id)

    async with db_helper.async_session() as session:
        acc = await session.scalars(stmt)
        acc = acc.first()
        if acc:
            acc.balance = account.balance
            await session.commit()
            return acc


async def delete_account(account: schemas.DeleteAccountSchemas):
    async with db_helper.async_session() as session:
        acc = await session.get(Account, account.id)
        if acc:
            await session.delete(acc)
            await session.commit()
