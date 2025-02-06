from fastapi import APIRouter, Depends, HTTPException, status
from starlette import status
from src.auth.utils import hash_password
from src.admin.user import crud
from src.admin.user import schema

router = APIRouter()


@router.post("/")
async def create_user(
    user: schema.CreateUserSchemas,
):
    user.password = hash_password(user.password)
    new_user = await crud.create_new_user(user)
    if new_user:
        return schema.UserSchemas(
            fullname=new_user.fullname,
            email=new_user.email,
            status=new_user.status,
        )
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="user is already exists"
    )


@router.patch("/")
async def update_user(user: schema.UpdateUserSchemas) -> schema.UserSchemas:
    updated_user = await crud.update_exist_user(user)
    if updated_user:
        return schema.UserSchemas(
            fullname=updated_user.fullname,
            status=updated_user.status,
            email=updated_user.email,
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: schema.DeleteUserSchemas):
    await crud.delete_exist_user(user)
