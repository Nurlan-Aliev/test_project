from fastapi import FastAPI
from src.user.users import router as user_router
from src.auth.login import router as login_router

app = FastAPI()
app.include_router(router=user_router, prefix="/user")
app.include_router(router=login_router)
