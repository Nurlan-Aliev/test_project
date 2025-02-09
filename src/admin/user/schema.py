from pydantic import BaseModel
from pydantic import EmailStr


class DeleteUserSchemas(BaseModel):
    id: int


class UserSchemas(BaseModel):
    fullname: str
    status: str
    email: EmailStr


class ReadUserSchema(UserSchemas):
    id: int
    is_active: bool
    accounts: list


class CreateUserSchemas(UserSchemas):
    password: str | bytes


class UpdateUserSchemas(CreateUserSchemas):
    id: int
    fullname: str | None = None
    status: str | None = None
    email: EmailStr | None = None
    password: str | None = None
