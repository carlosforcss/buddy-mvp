import uuid
import asyncio
from typing import Optional
from io import BytesIO
from utils.ai import AIClient
from utils.logger import Logger
from src.repositories import ImageTranscriptionRepository
from src.models import ImageTranscriptionStatus
from src.repositories import SessionRepository


class ImageTranscriptionService:
    def __init__(
        self,
        ai_client: AIClient,
        files_service: "FileService",
        image_transcription_repository: ImageTranscriptionRepository,
        session_repository: SessionRepository,
        logger: Logger,
    ):
        self.client = ai_client
        self.files_service = files_service
        self.logger = logger
        self.image_transcription_repository = image_transcription_repository
        self.session_repository = session_repository

    async def transcribe_image(
        self, image, session_id: int
    ) -> ImageTranscriptionRepository.model:
        """
        Process an uploaded image:
        1. Save image to S3 and create initial record
        2. Get a detailed description using Gemini Vision
        3. Update the transcription in the database
        """
        self.logger.info(f"Processing image: {image.filename}")

        # Get session
        session = await self.session_repository.get_by_id(session_id)
        if not session:
            self.logger.error(f"Session {session_id} not found")
            raise ValueError(f"Session {session_id} not found")

        image_content = await image.read()

        # Save image to S3
        file_format = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_format}"
        file = await self.files_service.upload_file(
            image_content, file_format, file_name
        )

        # Create initial record
        image_transcription = await self.image_transcription_repository.create(
            file=file, session=session
        )

        try:
            # Update status to processing
            image_transcription = (
                await self.image_transcription_repository.update_status(
                    image_transcription, ImageTranscriptionStatus.PROCESSING
                )
            )

            # Get image description from Gemini
            image_text_transcription = self.client.describe_image(
                BytesIO(image_content)
            )
            self.logger.info(
                f"Generated image description: {image_text_transcription[:100]}..."
            )

            # Update transcription in database
            image_transcription = (
                await self.image_transcription_repository.update_transcription(
                    image_transcription,
                    image_text_transcription,
                    ImageTranscriptionStatus.PROCESSED,
                )
            )

        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            await self.image_transcription_repository.update_status(
                image_transcription, ImageTranscriptionStatus.FAILED
            )
            raise

        return image_transcription
    
    async def get_last_image_transcription(self, session_id: int) -> ImageTranscriptionRepository.model:
        return await self.image_transcription_repository.get_last_image_transcription(session_id)
    async def wait_for_last_image_transcription_processing(
        self, session_id: int
    ) -> Optional[ImageTranscriptionRepository.model]:
        """
        Waits for the last image transcription to be processed, polling every 100ms.
        Returns the transcription if processed, raises an error if failed,
        or returns None after a timeout (~10 seconds).
        """
        max_iterations = 100
        for _ in range(max_iterations):
            image_transcription = await self.get_last_image_transcription(session_id)
            
            if not image_transcription:
                return None
            
            if image_transcription.status == ImageTranscriptionStatus.PROCESSED:
                return image_transcription
            
            if image_transcription.status == ImageTranscriptionStatus.FAILED:
                raise RuntimeError("Image transcription failed")
            
            await asyncio.sleep(0.1)
        
        return None
