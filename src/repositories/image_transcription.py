from src.models import ImageTranscription, ImageTranscriptionStatus
from utils.logger import Logger


logger = Logger(__name__)


class ImageTranscriptionRepository:
    model = ImageTranscription

    @staticmethod
    async def create(
        file: "src.files.models.File",
        session: "src.conversations.models.Session",
        transcription: str = "",
        status: ImageTranscriptionStatus = ImageTranscriptionStatus.CREATED,
    ) -> ImageTranscription:
        logger.info(
            f"Creating image transcription: {transcription} for file: {file.id} and session: {session.id}"
        )
        return await ImageTranscription.create(
            file=file, session=session, transcription=transcription, status=status
        )

    @staticmethod
    async def update_status(
        image_transcription: ImageTranscription, status: ImageTranscriptionStatus
    ) -> ImageTranscription:
        logger.info(
            f"Updating status of image transcription: {image_transcription.id} to {status}"
        )
        image_transcription.status = status
        await image_transcription.save()
        return image_transcription

    @staticmethod
    async def update_transcription(
        image_transcription: ImageTranscription,
        transcription: str,
        status: ImageTranscriptionStatus = ImageTranscriptionStatus.PROCESSED,
    ) -> ImageTranscription:
        logger.info(
            f"Updating transcription of image transcription: {image_transcription.id} to {transcription}"
        )
        image_transcription.transcription = transcription
        image_transcription.status = status
        await image_transcription.save()
        return image_transcription
    
    @staticmethod
    async def get_last_image_transcription(session_id: int) -> ImageTranscription:
        logger.info(f"Getting last image transcription for session: {session_id}")
        return await ImageTranscription.filter(session_id=session_id).order_by('-created_at').first()
