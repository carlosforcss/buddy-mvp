from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from config import settings
from utils.ai import OpenAIClient
from utils.logger import Logger
from src.voice.services import TranscriptionService


router = APIRouter(prefix="/voice", tags=["voice"])
logger = Logger(__name__)


@router.post("/transcription/audio")
async def get_text_from_audio(audio_file: UploadFile):
    """
    Getting text from audio an file.
    """
    service = TranscriptionService(OpenAIClient(settings.OPENAI_API_KEY), None, logger)
    file_content = BytesIO(await audio_file.read())
    text = service.get_text_from_audio(file_content)
    return {"text": text}


@router.post("/transcription/text")
async def get_audio_from_text(text: str):
    """
    Getting audio from text.
    """
    service = TranscriptionService(OpenAIClient(settings.OPENAI_API_KEY), None, logger)
    audio = service.get_audio_from_text(text)
    return StreamingResponse(
        audio,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=audio.mp3"},
    )
