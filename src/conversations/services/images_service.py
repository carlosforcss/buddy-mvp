import uuid
from io import BytesIO
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
        """
        Process an uploaded image:
        1. Read the image content
        2. Get a detailed description using Gemini Vision
        3. Save the image to S3
        4. Store the transcription in the database
        """
        self.logger.info(f"Processing image: {image.filename}")

        # Read image content
        image_content = BytesIO(await image.read())

        # Get image description from Gemini
        image_text_transcription = self.client.describe_image(image_content)
        self.logger.info(
            f"Generated image description: {image_text_transcription[:100]}..."
        )

        # Save image to S3
        file_format = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_format}"
        image_content.seek(0)  # Reset buffer position for upload
        file = await self.files_service.upload_file(
            image_content.read(), file_format, file_name
        )

        # Store transcription in database
        image_transcription = await self.image_transcription_repository.create(
            file=file, transcription=image_text_transcription
        )

        return image_transcription
