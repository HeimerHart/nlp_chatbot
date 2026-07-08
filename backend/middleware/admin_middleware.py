from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt 
from database.mongodb import db
from utils.jwt_handler import SECRET_KEY, ALGORITHM

security = HTTPBearer()


user_collection = db["users"]


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["email"]
        role = payload.get("role")

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user = user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return user