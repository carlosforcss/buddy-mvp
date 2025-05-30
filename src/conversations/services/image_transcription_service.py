from utils.ai import AIClient
from utils.logger import Logger
from src.conversations.repositories import ImageTranscriptionRepository
from src.files.services import FileService


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

    def upload_image(self, image):
        pass
