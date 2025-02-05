from pydantic import BaseModel


class BaseAccountSchemas(BaseModel):
    balance: float


class CreateAccount(BaseAccountSchemas):
    email: str


class AccountSchema(BaseAccountSchemas):
    id: int
