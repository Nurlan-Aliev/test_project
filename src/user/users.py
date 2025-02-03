from fastapi import APIRouter, Depends
from src.auth.validator import get_current_token_payload
from src.auth.login import http_bearer
from src.user.schema import UserSchemas
from src.user.crud import get_user, get_accounts
from typing import List


router = APIRouter(tags=["users"], dependencies=[Depends(http_bearer)])


@router.get("/me")
async def get_me(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchemas:
    email = payload.get("email")
    user = await get_user(email)
    return UserSchemas(fullname=user.fullname, status=user.status, email=user.email)


@router.get("/me/accounts")
async def get_user_accounts(
    payload: dict = Depends(get_current_token_payload),
) -> List[dict]:
    email = payload.get("email")
    accounts = await get_accounts(email)
    return accounts
