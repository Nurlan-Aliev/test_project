from pydantic import BaseModel, EmailStr


class BaseAccountSchemas(BaseModel):
    balance: float


class CreateAccount(BaseAccountSchemas):
    email: EmailStr


class AccountSchema(BaseAccountSchemas):
    id: int


class DeleteAccountSchemas(BaseModel):
    id: int
