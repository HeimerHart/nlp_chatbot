from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from database.mongodb import db
from utils.logger import logger
import bcrypt
from utils.jwt_handler import create_access_token

user_collection = db["users"]


async def register_user(email: str, password: str):
    email = email.strip().lower()

    logger.info(f"Register request: {email}")

    existing_user = user_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:
        user_collection.insert_one({
            "email": email,
            "password": hashed_password.decode("utf-8"),
            "role": "user"
        })
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Email already exists")

    return {"message": "User registered"}


async def login_user(email: str, password: str):
    email = email.strip().lower()
    user = user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not password_match:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "email": user["email"],
        "role": user.get("role", "user")
    })

    return {"token": token}
