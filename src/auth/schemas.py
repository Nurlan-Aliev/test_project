from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: bytes
    status: str
    is_active: bool
