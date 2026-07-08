from database import mongodb
from utils.logger import logger
import bcrypt
from database.mongodb import db
from utils.jwt_handler import create_access_token

user_collection = db["users"]

async def register_user(email: str, password : str):
    logger.info(f"Regester request: {email}")
    existing_user = user_collection.find_one(
        {
        "email":email
        }
    )

    if existing_user:
        return{
            "message": "Mail already exists"
        }
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    user_collection.insert_one(
        {
            "email":email,
            "password":hashed_password.decode("utf-8"),
            "role": "user"
         }
    )
    return{
        "message":"User Regestered"
    }



async def login_user(
    email: str,
    password: str
):

    user = user_collection.find_one(
        {
            "email": email
        }
    )

    if not user:
        return {
            "message": "Invalid credentials"
        }

    print(user)
    print(user["password"])

    
    try:
        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        )
    except ValueError:
        return {
            "message": "Corrupted password hash"
        }

    if not password_match:
        return {
            "message": "Invalid credentials"
        }
    
    token = create_access_token({
        "email": user["email"],
        "role": user.get("role", "user")
    })

    return {
        "token": token
    }