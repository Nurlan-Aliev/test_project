from src.database import db_helper
from src.models import User
from sqlalchemy.future import select


async def get_user(email):

    stmt = select(User).where(User.email == email)

    async with db_helper.async_session() as session:
        result = await session.scalars(stmt)
    return result.first()
