from fastapi import APIRouter, Depends
from database.mongodb import db
from collections import Counter
from datetime import datetime
from middleware.admin_middleware import get_current_admin


router = APIRouter()

conversation_collection = db["conversations"]

@router.get("/api/analytics")
async def get_analytics(admin=Depends(get_current_admin)):

    conversations = list(
        conversation_collection.find({})
    )

    total_conversations = len(conversations)

    active_users = len(
        set(
            chat["user_id"]
            for chat in conversations
            if "user_id" in chat
        )
    )

    queries_per_day = {}

    for chat in conversations:

        if "timestamp" in chat:

            day = chat["timestamp"].strftime("%Y-%m-%d")

            queries_per_day[day] = (
                queries_per_day.get(day, 0) + 1
            )

    intent_counter = Counter()

    unresolved = 0

    for chat in conversations:

        if "intent" in chat:
            intent_counter[chat["intent"]] += 1

        if chat.get("intent") == "unknown":
            unresolved += 1

    unresolved_rate = 0

    if total_conversations > 0:

        unresolved_rate = (
            unresolved / total_conversations
        ) * 100

    return {

        "total_conversations":
            total_conversations,

        "active_users":
            active_users,

        "queries_per_day":
            queries_per_day,

        "top_intents":
            intent_counter.most_common(5),

        "unresolved_rate":
            unresolved_rate
    }
