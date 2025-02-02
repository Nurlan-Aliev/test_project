from datetime import timedelta, datetime, UTC
import jwt
from settings import settings
from src.auth.schemas import UserSchema


def create_jwt(
    user: UserSchema,
) -> str:

    jwt_pyload = {"email": user.email, "status": user.status}

    return encode_jwt(
        payload=jwt_pyload,
    )


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
