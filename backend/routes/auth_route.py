from fastapi import APIRouter
from models.usermodel import UserRegister,UserLogin
from middleware.auth_middleware import get_current_user
from fastapi import Depends
from controllers.auth_controller import (
    register_user,
    login_user
)

router = APIRouter()


@router.get("/me")
async def get_me(
    user=Depends(get_current_user)
):
    return user



@router.post("/api/auth/register")
async def register(request: UserRegister):

    return await register_user(
        request.email,
        request.password
    )


@router.post("/api/auth/login")
async def login(request: UserLogin):

    return await login_user(
        request.email,
        request.password
    )

