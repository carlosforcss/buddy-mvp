from abc import ABC
from io import BytesIO
import openai


class AIClient(ABC):
    
    api_key: str
    api_url: str
    
    def text_to_audio(self, text: str) -> BytesIO:
        """
        Getting audio from text.
        """
        raise Exception("This method should be overridden by subclasses.")
    
    def audio_to_text(self, audio_file: BytesIO) -> str:
        """
        Getting text from audio file.
        """
        raise Exception("This method should be overridden by subclasses.")


class OpenAIClient(AIClient):
    
    api_url = "https://api.openai.com/v1/audio/transcriptions"
    
    def __init__(self, api_key: str):
        self.openai = openai
        self.openai.api_key = api_key

    def text_to_audio(self, text: str, voice: str = "nova") -> BytesIO:
        """
        Converts input text to speech and saves it as an MP3 file using OpenAI's.
        """
        response = self.openai.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
        )
        audio_content = BytesIO(response.content)
        return audio_content
    
    def audio_to_text(self, audio_file: BytesIO) -> str:
        """
        Converts input audio file to text using OpenAI's API.
        """
        audio_file.name = "transcription.mp3"  # Whicper requires this property
        response = self.openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return response
    
    def send_message(self, message: str, model: str = "gpt-4o-mini") -> str:
        """
        Sends a list of messages to ChatGPT and returns the response text.
        Args:
            messages: A list of {"role": "user" | "assistant" | "system", "content": str}
            model: The OpenAI chat model to use (default: gpt-4o)
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant, be short, friendly and concise, and use only plain text withoht emogies. Prepare the text to be formated to audio"},
            {"role": "user", "content": message}
        ]
        response = self.openai.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content
