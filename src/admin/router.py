from fastapi import APIRouter, Depends
from src.auth.login import http_bearer
from src.auth.validator import is_admin
from src.admin.account.account_router import router as account_router
from src.admin.user.user_router import router as user_router


router = APIRouter(
    tags=["Admin"], dependencies=[Depends(http_bearer), Depends(is_admin)]
)

router.include_router(router=user_router, prefix="/user")
router.include_router(router=account_router, prefix="/account")
