from fastapi import HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from src.auth.db_user import get_user

auth2_bearer = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_auth_user(username: str = Form(), password: str = Form()):

    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )

    if not (user := await get_user(username)):
        raise unauthed_exp
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exp

    return user


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
