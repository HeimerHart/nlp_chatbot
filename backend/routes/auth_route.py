from fastapi import APIRouter
from models.usermodel import UserRegister,UserLogin
from middleware.auth_middleware import get_current_user
from fastapi import Request, Depends
from limiter import limiter
from controllers.auth_controller import (
    register_user,
    login_user
)

from fastapi import Request


router = APIRouter()


@router.get("/me")
@limiter.limit("5/minute")
async def get_me(
    request: Request,
    user=Depends(get_current_user)
):
    return user


@router.post("/api/auth/register")
@limiter.limit("5/minute")
async def register(
    request: Request,
    user: UserRegister
):
    return await register_user(
        user.email,
        user.password
    )


@router.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    user: UserLogin
):
    return await login_user(
        user.email,
        user.password
    )

