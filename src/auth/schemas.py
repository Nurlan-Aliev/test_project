from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: EmailStr
    password: bytes
    status: str
