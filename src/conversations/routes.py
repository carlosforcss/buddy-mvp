from fastapi import APIRouter
from utils.ai import OpenAIClient
from utils.logger import Logger
from config import settings
from src.conversations.services import ConversationsService

router = APIRouter(prefix="/conversations", tags=["conversations"])


logger = Logger(__name__)


@router.post("/conversations/message")
async def get_conversations(message: str):
    service = ConversationsService(
        OpenAIClient(settings.OPENAI_API_KEY),
        None,
        logger
    )
    answer = await service.send_simple_message(message)
    return {
        "answer": answer
    }
