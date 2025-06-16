from io import BytesIO
from utils.logger import Logger
from utils.ai import OpenAIClient
from config.settings import OPENAI_API_KEY


logger = Logger(__name__)


class TranscriptionService:
    def __init__(self):
        self.logger = logger
        self.ai_client = OpenAIClient(OPENAI_API_KEY)

    def get_audio_from_text(self, text: str):
        """
        Getting audio from text.
        """
        self.logger.info(f"Getting audio from text: {text}")
        audio = self.ai_client.text_to_audio(text)
        return audio

    def get_text_from_audio(self, audio_file: BytesIO):
        """
        Getting text from audio file.
        """
        self.logger.info(f"Getting text from audio file: {audio_file}")
        text = self.ai_client.audio_to_text(audio_file)
        return text 