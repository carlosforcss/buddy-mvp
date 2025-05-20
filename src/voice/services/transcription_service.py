from io import BytesIO
from utils.ai import AIClient


class TranscriptionService:
    def __init__(self, ai_client: AIClient, transcription_repository, logger):
        self.transcription_repository = transcription_repository
        self.logger = logger
        self.ai_client = ai_client
        
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
