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
from src.conversations.services import RealtimeSessionService, ImageTranscriptionService
from src.conversations.repositories import ImageTranscriptionRepository
from src.files.services import FileService
from src.files.repositories import FilesRepository
from src.conversations.schemas.image_transcription import ImageTranscriptionSchema

router = APIRouter(prefix="/conversations", tags=["conversations"])
logger = Logger(__name__)


@router.post("/message")
async def get_conversations(message: str):
    gemini_service = GeminiClient(settings.GOOGLE_API_KEY)
    openai_service = OpenAIClient(settings.OPENAI_API_KEY)
    service = ConversationsService(gemini_service, None, logger)
    answer = await service.send_simple_message(message)
    return {"answer": answer}


@router.websocket("/realtime")
async def audio_websocket(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())[:8]
    service = RealtimeSessionService()
    await service.connect(websocket)


@router.post("/image", response_model=ImageTranscriptionSchema)
async def upload_image(image: UploadFile = File(...)):
    logger = Logger(__name__)
    gemini_client = GeminiClient(settings.GOOGLE_API_KEY)
    files_service = FileService(
        S3Client(),
        FilesRepository(logger),
        logger,
    )
    image_transcriptino_repository = ImageTranscriptionRepository()
    service = ImageTranscriptionService(
        gemini_client, files_service, image_transcriptino_repository, logger
    )
    image_description = await service.transcribe_iamge(image)
    return ImageTranscriptionSchema.model_validate(image_description)
