import jwt
from fastapi import Depends, HTTPException, status
from src.auth.utils import auth2_bearer, decode_jwt
from src.auth.schemas import User
from src.auth.db_user import get_user


def get_current_token_payload(
    token: str = Depends(auth2_bearer),
) -> dict:
    """returns payload from jwt"""
    try:
        payload = decode_jwt(token=token)
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )


def get_user_by_token_sub(payload: dict) -> User:
    """
    Returns the user by his sub
    """
    username: str | None = payload.get("email")
    if user := get_user(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token not found (user not found)",
    )


def get_auth_user_from_token(
    payload: dict = Depends(get_current_token_payload),
) -> User:

    return get_user_by_token_sub(payload)
