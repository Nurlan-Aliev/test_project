from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.login import http_bearer
from src.auth.validator import is_admin
from src.admin.account.crud import (
    create_new_account,
    update_account,
    delete_account,
)
from src.admin.account.schemas import CreateAccount, AccountSchema


router = APIRouter()


@router.post("/")
async def create_acc(
    account: CreateAccount,
):
    acc = await create_new_account(account)
    return AccountSchema(id=acc.id, balance=acc.balance)


@router.patch("/")
async def update_acc(
    account: AccountSchema,
):
    acc = await update_account(account)
    if acc:
        return acc
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="account not found"
    )


@router.delete("/")
async def delete_acc(account: AccountSchema):

    acc = await delete_account(account)
    if acc:
        return f"{acc.id} was deleted"
    return f"account is not exist"
