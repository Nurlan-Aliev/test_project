from sqlalchemy import select
from src.database import db_helper
from src.models import Transaction, Account
from sqlalchemy.ext.asyncio import AsyncSession


async def update_transactions(transaction):
    stmt = select(Transaction).where(
        Transaction.transaction_id == str(transaction.transaction_id)
    )
    async with db_helper.async_session() as session:
        is_transaction_exist = (await session.scalars(stmt)).first()
        if not is_transaction_exist:
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
    stmt = (
        select(Account)
        .where(Account.user_id == user_id)
        .where(Account.id == account_id)
    )
    acc = await session.scalars(stmt)
    acc = acc.first()
    if acc:
        acc.balance += balance
        await session.commit()
