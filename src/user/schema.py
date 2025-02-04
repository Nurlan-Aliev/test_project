from pydantic import BaseModel
from typing import List


class UserSchemas(BaseModel):
    fullname: str
    status: str
    email: str


class CreateUserSchemas(UserSchemas):
    password: str | bytes
