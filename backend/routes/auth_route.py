from fastapi import APIRouter
from models.usermodel import UserRegister
from controllers.auth_controller import register_user

router = APIRouter()


@router.post("/api/auth/register")
async def register(request: UserRegister):

    return await register_user(
        request.email,
        request.password
    )