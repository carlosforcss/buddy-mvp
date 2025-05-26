import websockets
import json
import base64
import asyncio
import uuid
from fastapi import APIRouter, WebSocket
from utils.ai import OpenAIClient
from utils.logger import Logger
from config import settings
from src.conversations.services import ConversationsService
from src.conversations.services import RealtimeSessionService

router = APIRouter(prefix="/conversations", tags=["conversations"])


logger = Logger(__name__)


@router.post("/message")
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


@router.websocket("/realtime")
async def audio_websocket(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())[:8]
    service = RealtimeSessionService()
    await service.connect(websocket)
