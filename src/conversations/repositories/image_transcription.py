from src.conversations.models import ImageTranscription


class ImageTranscriptionRepository:
    model = ImageTranscription

    @staticmethod
    async def create(
        file: "src.files.models.File", transcription: str
    ) -> ImageTranscription:
        return await ImageTranscription.create(file=file, transcription=transcription)
