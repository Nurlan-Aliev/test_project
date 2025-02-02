from datetime import timedelta, datetime, UTC
import jwt
from fastapi import HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from settings import settings
import bcrypt
from src.auth.schemas import User
from src.auth.db_user import get_user

auth2_bearer = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def create_jwt(
    user: User,
) -> str:

    jwt_pyload = {"email": user.username, "status": user.status}

    return encode_jwt(
        payload=jwt_pyload,
    )


async def validate_auth_user(username: str = Form(), password: str = Form()):

    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )

    if not (user := await get_user(username)):
        raise unauthed_exp
    print(f"\n\n\n{user}\n\n\n")
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exp

    return user


def encode_jwt(
    payload: dict,
):
    to_encode = payload.copy()
    utcnow = datetime.now(UTC)
    expire = utcnow + timedelta(minutes=settings.access_token_expire_min)
    to_encode.update(
        exp=expire,
        iat=utcnow,
    )

    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
):
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
    return decoded


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
