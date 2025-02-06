from fastapi import FastAPI
from src.user.users import router as user_router
from src.auth.login import router as login_router
from src.admin.router import router as admin_router

app = FastAPI()
app.include_router(router=user_router, prefix="/user")
app.include_router(router=admin_router, prefix="/admin")
app.include_router(router=login_router)
