from fastapi import APIRouter, Depends
from middleware.admin_middleware import get_current_admin
from database.mongodb import db

router = APIRouter()

intent_collection = db["intents"]
user_collection = db["users"]
conversation_collection = db["conversations"]


@router.get("/api/admin/intents")
async def get_intents(admin=Depends(get_current_admin)):
    return list(intent_collection.find({}, {"_id": 0}))

@router.post("/api/admin/intents")
async def add_intent(data: dict, admin=Depends(get_current_admin)):
    intent_collection.insert_one(data)
    return {"message": "Intent added"}

@router.put("/api/admin/intents/{name}")
async def update_intent(name: str, data: dict, admin=Depends(get_current_admin)):
    intent_collection.update_one({"name": name}, {"$set": data})
    return {"message": "Updated"}

@router.delete("/api/admin/intents/{name}")
async def delete_intent(name: str, admin=Depends(get_current_admin)):
    intent_collection.delete_one({"name": name})
    return {"message": "Deleted"}

@router.get("/api/admin/users")
async def get_users(admin=Depends(get_current_admin)):
    return list(user_collection.find({}, {"_id": 0, "password": 0}))

@router.get("/api/admin/conversations")
async def get_all_conversations(admin=Depends(get_current_admin)):
    return list(conversation_collection.find({}, {"_id": 0}))

@router.get("/api/admin/conversations/{session_id}")
async def get_session(session_id: str, admin=Depends(get_current_admin)):
    return list(conversation_collection.find({"session_id": session_id}, {"_id": 0}))