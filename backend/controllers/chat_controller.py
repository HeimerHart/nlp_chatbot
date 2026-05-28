from utils.logger import logger

async def process_chat(message: str):

    logger.info(f'User message: {message}')

    return {
        'response': f'You said: {message}'
    }