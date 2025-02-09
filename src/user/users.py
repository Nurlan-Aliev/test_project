from typing import List
from fastapi import APIRouter, Depends
from src.admin.account.schemas import AccountSchema
from src.auth.validator import is_active
from src.auth.login import http_bearer
from src.admin.user.schema import UserSchemas
from src.user.crud import get_user, get_accounts

router = APIRouter(tags=["Users"], dependencies=[Depends(http_bearer)])


@router.get("/me")
async def get_me(
    payload: dict = Depends(is_active),
) -> UserSchemas:
    email = payload.get("email")
    user = await get_user(email)
    return UserSchemas(
        fullname=user.fullname,
        status=user.status,
        email=user.email,
    )


@router.get("/accounts")
async def get_user_accounts(
    payload: dict = Depends(is_active),
) -> List[AccountSchema]:
    email = payload.get("email")
    accounts = await get_accounts(email)
    return [
        AccountSchema(id=acc.id, balance=acc.balance, is_active=acc.is_active)
        for acc in accounts
    ]
