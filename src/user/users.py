from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.validator import get_current_token_payload, is_admin
from src.auth.login import http_bearer
from src.user.schema import UserSchemas, CreateUserSchemas
from src.user.crud import get_user, get_accounts, create_new_user
from typing import List
from src.auth.utils import hash_password


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


@router.post("/create_user")
async def create_user(
    user: CreateUserSchemas,
    payload: dict = Depends(is_admin),
):

    user.password = hash_password(user.password)
    if not await get_user(user.email):
        await create_new_user(user)
        return user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="user already exists"
    )
