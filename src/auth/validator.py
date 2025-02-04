import jwt
from fastapi import Depends, HTTPException, status
from src.auth.utils import auth2_bearer
from src.auth.jwt_helper import decode_jwt
from src.auth.schemas import UserAuthSchema
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


async def get_user_by_token_sub(payload: dict) -> UserAuthSchema:
    """
    Returns the user by his sub
    """
    email: str | None = payload.get("email")
    if user := await get_user(email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user not found",
    )


async def get_auth_user_from_token(
    payload: dict = Depends(get_current_token_payload),
) -> UserAuthSchema:
    return await get_user_by_token_sub(payload)


def get_pages_by_status(user: UserAuthSchema = Depends(get_user_by_token_sub)):

    if user.status == "admin":
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="not enough rights"
    )


def is_admin(payload: dict = Depends(get_current_token_payload)):
    if payload.get("status") == "admin":
        return payload
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="You don’t have permission"
    )
