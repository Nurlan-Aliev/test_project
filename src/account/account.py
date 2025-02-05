from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.login import http_bearer
from src.auth.validator import get_current_token_payload, is_admin
from src.account.crud import (
    create_new_account,
    update_account,
    delete_account,
)
from src.account.schemas import CreateAccount, AccountSchema


router = APIRouter(
    tags=["Account"], dependencies=[Depends(http_bearer), Depends(is_admin)]
)


@router.post("/create_acc")
async def create_acc(
    account: CreateAccount,
):
    acc = await create_new_account(account)
    return AccountSchema(id=acc.id, balance=acc.balance)


@router.patch("/update_acc")
async def update_acc(
    account: AccountSchema,
):
    acc = await update_account(account)
    if acc:
        return acc
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="account not found"
    )


@router.delete("/delete_acc")
async def delete_acc(account: AccountSchema):

    acc = await delete_account(account)
    if acc:
        return f"{acc.id} was deleted"
    return f"account is not exist"
