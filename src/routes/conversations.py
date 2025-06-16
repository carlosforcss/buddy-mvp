from fastapi import APIRouter, WebSocket, File, UploadFile, Path
from utils.logger import Logger
from config import settings
from src.services.session_service import SessionService
from src.services.conversations_service import ConversationsService
from src.integrations.realtime import RealtimeSessionService
from src.repositories import SessionRepository
from src.schemas.image_transcription import ImageTranscriptionSchema
from src.schemas.session import Session as SessionSchema



router = APIRouter(prefix="/api/conversations", tags=["conversations"])
logger = Logger(__name__)


@router.post("/sessions", response_model=SessionSchema)
async def create_session():
    """
    Create a new conversation session
    """
    session_repository = SessionRepository()
    service = SessionService(session_repository, logger)
    session = await service.create_session()
    return SessionSchema.model_validate(session)


@router.post("/message")
async def get_conversations(message: str):
    service = ConversationsService()
    answer = await service.send_simple_message(message)
    return {"answer": answer}


@router.websocket("/realtime/{session_id}")
async def audio_websocket(
    websocket: WebSocket,
    session_id: int = Path(..., description="ID of the session this audio belongs to"),
):
    await websocket.accept()
    service = RealtimeSessionService()
    await service.connect(websocket, session_id)


@router.post("/image/{session_id}", response_model=ImageTranscriptionSchema)
async def upload_image(
    image: UploadFile = File(...),
    session_id: int = Path(..., description="ID of the session this image belongs to"),
):
    service = ImageTranscriptionService()
    image_description = await service.transcribe_image(image, session_id)
    return ImageTranscriptionSchema.model_validate(image_description)
