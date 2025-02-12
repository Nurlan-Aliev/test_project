from fastapi import FastAPI, Depends
from src.user.user_router import router as user_router
from src.auth.login import router as login_router, http_bearer
from src.admin.router import router as admin_router
from src.transaction.transaction_router import router as transaction_router


app = FastAPI()
app.include_router(router=user_router, prefix="/user")
app.include_router(router=admin_router, prefix="/admin")
app.include_router(router=transaction_router, prefix="/webhook")
app.include_router(router=login_router)
