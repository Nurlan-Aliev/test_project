from sqlalchemy import select, and_

from src.database import db_helper
from src.models import Transaction, Account
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.crud import get_user


async def update_transactions(transaction):

    stmt = select(Transaction).where(
        Transaction.transaction_id == str(transaction.transaction_id)
    )
    stmt_account = select(Account).where(Account.id == transaction.account_id)
    async with db_helper.async_session() as session:
        is_transaction_exist = (await session.scalars(stmt)).first()
        if is_transaction_exist:
            return "Transaction is already exist"
        account_exist = (await session.scalars(stmt_account)).first()
        if not account_exist:
            await create_acc(transaction, session)

        new_transaction = Transaction(
            transaction_id=str(transaction.transaction_id),
            amount=transaction.amount,
            account_id=transaction.account_id,
        )
        session.add(new_transaction)
        await update_balance(
            transaction.account_id,
            transaction.user_id,
            transaction.amount,
            session,
        )
        await session.commit()
        return new_transaction


async def update_balance(account_id, user_id, balance, session: AsyncSession):
    stmt = select(Account).where(
        and_(Account.user_id == user_id, Account.id == account_id)
    )
    acc = await session.scalars(stmt)
    acc = acc.first()
    if acc:
        acc.balance += balance


async def create_acc(transaction, session: AsyncSession):
    user = await get_user(transaction.user_id)
    account = Account(
        id=transaction.account_id,
        balance=0,
        user_id=transaction.user_id,
        user=user,
    )
    session.add(account)
    await session.flush()
