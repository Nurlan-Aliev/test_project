from fastapi import APIRouter, status, HTTPException
from src.transaction import schema
from src.transaction.validator import validate
from src.transaction.update import update_transactions

router = APIRouter(tags=["Transaction"])


@router.post("/", status_code=status.HTTP_200_OK)
async def payment(transaction: schema.Transaction):
    if validate(transaction):
        await update_transactions(transaction)
        return
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
