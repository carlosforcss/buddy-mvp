from io import BytesIO
import uuid
import ffmpeg
import tempfile
from utils.logger import Logger
from src.repositories import AudioTranscriptionRepository
from utils.ai import OpenAIClient
from src.services.files_service import FileService
from config.settings import OPENAI_API_KEY


logger = Logger(__name__)


class AudioTranscriptionService:
    def __init__(self):
        self.client = OpenAIClient(OPENAI_API_KEY)
        self.files_service = FileService()
        self.audio_transcription_repository = AudioTranscriptionRepository()

    async def transform_pcm_to_mp3(self, audio_content: bytes) -> bytes:
        """
        Convert raw PCM (16-bit mono, 16kHz) audio bytes to MP3 using ffmpeg.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".pcm"
        ) as pcm_file, tempfile.NamedTemporaryFile(suffix=".mp3") as mp3_file:
            # Write the raw PCM to a file
            pcm_file.write(audio_content)
            pcm_file.flush()

            # Run ffmpeg to convert PCM to MP3
            (
                ffmpeg.input(pcm_file.name, f="s16le", ar="24000", ac="1")
                .output(mp3_file.name, format="mp3")
                .run(quiet=True, overwrite_output=True)
            )

            # Read the resulting MP3
            mp3_file.seek(0)
            return mp3_file.read()

    def transform_mp3_to_pcm(self, audio_content: bytes) -> bytes:
        """
        Convert MP3 audio bytes to raw PCM (16-bit mono, 24kHz) using ffmpeg.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".mp3"
        ) as mp3_file, tempfile.NamedTemporaryFile(suffix=".pcm") as pcm_file:
            # Write the MP3 content to a temporary file
            mp3_file.write(audio_content)
            mp3_file.flush()

            # Run ffmpeg to convert MP3 to PCM
            (
                ffmpeg.input(mp3_file.name)
                .output(
                    pcm_file.name,
                    format="s16le",  # 16-bit PCM
                    acodec="pcm_s16le",
                    ac=1,  # mono
                    ar="24000",  # 24kHz sampling rate
                )
                .run(quiet=True, overwrite_output=True)
            )

            # Read the resulting PCM data
            pcm_file.seek(0)
            return pcm_file.read()

    async def transcribe_audio(
        self, audio_content: bytes
    ) -> AudioTranscriptionRepository.model:
        """
        Process an audio file:
        1. Convert bytes to BytesIO
        2. Get a transcription using OpenAI
        3. Save the audio to S3
        4. Store the transcription in the database
        """
        self.logger.info("Processing audio file")

        # Convert bytes to BytesIO
        mp3_content = await self.transform_pcm_to_mp3(audio_content)

        # Get audio transcription from OpenAI
        # audio_text_transcription = self.client.audio_to_text(audio_content)
        # Dummy audio transcription
        audio_text_transcription = "This is a dummy transcription"
        self.logger.info(
            f"Generated audio transcription: {audio_text_transcription[:100]}..."
        )

        # Save audio to S3
        file_name = f"{uuid.uuid4()}.mp3"  # Using .wav as default format
        # audio_content.seek(0)  # Reset buffer position for upload
        self.logger.info(f"Uploading file to S3: {file_name}")
        self.logger.info(f"File size: {len(mp3_content)}")
        file = await self.files_service.upload_file(mp3_content, "mp3", file_name)

        # Store transcription in database
        audio_transcription = await self.audio_transcription_repository.create(
            file=file, transcription=audio_text_transcription
        )

        return audio_transcription
