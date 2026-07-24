from fastapi import APIRouter
from models.usermodel import UserRegister,UserLogin
from middleware.auth_middleware import get_current_user
from fastapi import Depends
from controllers.auth_controller import (
    register_user,
    login_user
)
from main import limiter
from fastapi import Request


router = APIRouter()


@router.get("/me")
@limiter.limit("5/minute")
async def get_me(
    user=Depends(get_current_user)
):
    return user



@router.post("/api/auth/register")
@limiter.limit("5/minute")
async def register(request: UserRegister):

    return await register_user(
        request.email,
        request.password
    )


@router.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: UserLogin):
    return await login_user(
        request.email,
        request.password
    )

