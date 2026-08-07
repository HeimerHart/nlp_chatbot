from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException
from jose import jwt, JWTError
from database.mongodb import db
from services.cache import conversation_cache
from utils.jwt_handler import SECRET_KEY, ALGORITHM
from middleware.admin_middleware import get_current_admin

router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"]
)

conversation_collection = db["conversations"]


def get_optional_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def _check_authorized(session_id: str, user) -> None:
    if user and user.get("role") != "admin" and user.get("email") != session_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session")


@router.get("/threads/{session_id}")
async def list_threads(
    session_id: str,
    user=Depends(get_optional_user)
):
    _check_authorized(session_id, user)

    messages = list(
        conversation_collection.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )

    threads: dict = {}
    for msg in messages:
        conv_id = msg.get("conversation_id") or "default"
        if conv_id not in threads:
            threads[conv_id] = {
                "conversation_id": conv_id,
                "title": (msg.get("user_message") or "New chat")[:60],
                "started_at": msg.get("timestamp"),
                "last_message_at": msg.get("timestamp"),
                "message_count": 0,
            }
        threads[conv_id]["last_message_at"] = msg.get("timestamp")
        threads[conv_id]["message_count"] += 1

    ordered = sorted(
        threads.values(),
        key=lambda t: t["last_message_at"] or "",
        reverse=True,
    )
    return ordered


@router.get("/{session_id}/thread/{conversation_id}")
async def get_thread_history(
    session_id: str,
    conversation_id: str,
    user=Depends(get_optional_user)
):
    _check_authorized(session_id, user)

    cache_key = f"{session_id}:{conversation_id}"
    if cache_key in conversation_cache:
        return conversation_cache[cache_key]

    conversations = list(
        conversation_collection.find(
            {"session_id": session_id, "conversation_id": conversation_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )
    conversation_cache[cache_key] = conversations
    return conversations


@router.get("/{session_id}")
async def get_session_history(
    session_id: str,
    user=Depends(get_optional_user)
):
    _check_authorized(session_id, user)

    if session_id in conversation_cache:
        return conversation_cache[session_id]

    conversations = list(
        conversation_collection.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )
    conversation_cache[session_id] = conversations
    return conversations


@router.get("/")
async def get_all_conversations(admin=Depends(get_current_admin)):
    conversations = list(
        conversation_collection.find(
            {},
            {"_id": 0}
        ).sort("timestamp", 1)
    )
    return conversations
