from pydantic import BaseModel
from uuid import UUID


class Transaction(BaseModel):
    transaction_id: UUID
    account_id: int
    user_id: int
    amount: int
    signature: str
