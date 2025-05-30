import websockets
import json
import base64
import asyncio
import uuid
from fastapi import APIRouter, WebSocket, File, UploadFile
from utils.s3 import S3Client
from utils.ai import OpenAIClient, GeminiClient
from utils.logger import Logger
from config import settings
from src.conversations.services import ConversationsService
from src.conversations.services import (
    RealtimeSessionService,
    ImageService
)
from src.files.services import FileService


router = APIRouter(prefix="/conversations", tags=["conversations"])


logger = Logger(__name__)


@router.post("/message")
async def get_conversations(message: str):
    gemini_service = GeminiClient(settings.GOOGLE_API_KEY)
    openai_service = OpenAIClient(settings.OPENAI_API_KEY)
    service = ConversationsService(
        gemini_service,
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
    

@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    logger = Logger(__name__)
    gemini_client = GeminiClient(settings.GEMINI_API_KEY)
    files_service = FilesService(
        S3Client(
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_REGION,
            settings.AWS_BUCKET_NAME
        ),
        FilesRepository(),
        logger
    )
    service = ImageService(gemini_client, files_service, logger)
    image_description = service.upload_image(image)
    return {
        "image_description": image_description
    }
