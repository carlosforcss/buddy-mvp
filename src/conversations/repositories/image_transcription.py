from src.conversations.models import ImageTranscription
from src.conversations.models.image_transcription import ImageTranscriptionStatus


class ImageTranscriptionRepository:
    model = ImageTranscription

    @staticmethod
    async def create(
        file: "src.files.models.File",
        session: "src.conversations.models.Session",
        transcription: str = "",
        status: ImageTranscriptionStatus = ImageTranscriptionStatus.CREATED,
    ) -> ImageTranscription:
        return await ImageTranscription.create(
            file=file, session=session, transcription=transcription, status=status
        )

    @staticmethod
    async def update_status(
        image_transcription: ImageTranscription, status: ImageTranscriptionStatus
    ) -> ImageTranscription:
        image_transcription.status = status
        await image_transcription.save()
        return image_transcription

    @staticmethod
    async def update_transcription(
        image_transcription: ImageTranscription,
        transcription: str,
        status: ImageTranscriptionStatus = ImageTranscriptionStatus.PROCESSED,
    ) -> ImageTranscription:
        image_transcription.transcription = transcription
        image_transcription.status = status
        await image_transcription.save()
        return image_transcription
    
    @staticmethod
    async def get_last_image_transcription(session_id: int) -> ImageTranscription:
        return await ImageTranscription.filter(session_id=session_id).order_by('-created_at').first()
