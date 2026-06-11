from fastapi import APIRouter
from controllers.chat_controller import process_chat
from models.chat_model import ChatRequest
from utils.logger import logger

router = APIRouter()

@router.post('/api/chat')
async def chatbot(request: ChatRequest):

    logger.info('Request to chatbot')

    return await process_chat(
        request.session_id,
        request.message
    )