from database import mongodb
from utils.logger import logger
import bcrypt
from database.mongodb import db

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
         
         }
    )
    return{
        "message":"User Regestered"
    }
