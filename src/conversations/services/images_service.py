import uuid
from utils.ai import AIClient
from utils.logger import Logger
from src.conversations.repositories import ImageTranscriptionRepository
from src.files.services import FileService
from src.conversations.repositories import ImageTranscriptionRepository


class ImageTranscriptionService:
    def __init__(
        self,
        ai_client: AIClient,
        files_service: FileService,
        image_transcription_repository: ImageTranscriptionRepository,
        logger: Logger,
    ):
        self.client = ai_client
        self.files_service = files_service
        self.logger = logger
        self.image_transcription_repository = image_transcription_repository

    async def transcribe_iamge(self, image) -> ImageTranscriptionRepository.model:
        file_format = image.filename.split(".")[1]
        file_name = f"{uuid.uuid4()}.{file_format}"
        image_content = await image.read()
        file = await self.files_service.upload_file(
            image_content, file_format, file_name
        )
        image_text_transcription = "This is just dummy text"
        image_transcription = await self.image_transcription_repository.create(
            file=file, transcription=image_text_transcription
        )
        return image_transcription
