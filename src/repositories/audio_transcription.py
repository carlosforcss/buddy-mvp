from src.models import AudioTranscription
from utils.logger import Logger


logger = Logger(__name__)


class AudioTranscriptionRepository:
    model = AudioTranscription

    @staticmethod
    async def create(
        file: "src.files.models.File", transcription: str
    ) -> AudioTranscription:
        """Create a new audio transcription"""
        logger.info(
            f"Creating audio transcription: {transcription} for file: {file.id}"
        )
        return await AudioTranscription.create(file=file, transcription=transcription)

    @staticmethod
    async def get_by_id(id: int) -> AudioTranscription:
        """Get an audio transcription by its ID"""
        logger.info(f"Getting audio transcription by ID: {id}")
        return await AudioTranscription.get(id=id)
