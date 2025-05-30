from utils.ai import AIClient
from utils.logger import Logger
from src.files.services import FileService


class ImageService:
    def __init__(self, ai_client: AIClient, files_service: FileService, logger: Logger):
        self.client = ai_client
        self.files_service = files_service
        self.logger = logger

    def upload_image(self, image):
        pass
