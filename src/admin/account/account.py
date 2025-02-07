from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.login import http_bearer
from src.auth.validator import is_admin
from src.admin.account.crud import (
    create_new_account,
    update_account,
    delete_account,
)
from src.admin.account import schemas


router = APIRouter()


@router.post("/")
async def create_acc(
    account: schemas.CreateAccount,
):
    acc = await create_new_account(account)
    if acc:
        return schemas.AccountSchema(id=acc.id, balance=acc.balance)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


@router.patch("/")
async def update_acc(
    account: schemas.AccountSchema,
):
    acc = await update_account(account)
    if acc:
        return acc
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="account not found"
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_acc(account: schemas.DeleteAccountSchemas):

    await delete_account(account)
