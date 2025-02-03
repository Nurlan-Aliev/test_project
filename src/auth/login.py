from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from src.auth.schemas import UserAuthSchema
from src.auth import utils
from src.auth import jwt_helper


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(tags=["login"], dependencies=[Depends(http_bearer)])


@router.post("/login")
async def auth_user_issue_jwt(
    user: UserAuthSchema = Depends(utils.validate_auth_user),
):
    access_token = jwt_helper.create_jwt(user)
    return access_token
