from fastapi import APIRouter
from database.mongodb import db
from services.cache import conversation_cache

router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"]
)

conversation_collection = db["conversations"]


@router.get("/")
async def get_all_conversations():

    conversations = list(
        conversation_collection.find(
            {},
            {"_id": 0}
        )
    )
    conversation_cache["all_conversations"] = conversations
    return conversations


@router.get("/{session_id}")
async def get_session_history(
    session_id: str
):
    if session_id in conversation_cache:
        return conversation_cache[session_id]

    conversations = list(
        conversation_collection.find(
            {
                "session_id": session_id
            },
            {
                "_id": 0
            }
        )
    )
    conversation_cache[session_id] = conversations
    return conversations