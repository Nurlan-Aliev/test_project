from fastapi import FastAPI, Depends
from src.user.user_router import router as user_router
from src.auth.login import router as login_router, http_bearer
from src.admin.router import router as admin_router

app = FastAPI(dependencies=[Depends(http_bearer)])
app.include_router(router=user_router, prefix="/user")
app.include_router(router=admin_router, prefix="/admin")
app.include_router(router=login_router)
