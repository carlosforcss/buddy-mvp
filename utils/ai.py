from abc import ABC
from io import BytesIO
import base64
import requests
import openai
from google.generativeai import configure, GenerativeModel
from google.api_core.exceptions import GoogleAPIError


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
            model="whisper-1", file=audio_file, response_format="text"
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
            {
                "role": "system",
                "content": "You are a helpful assistant, be short, friendly and concise, and use only plain text withoht emogies. Prepare the text to be formated to audio",
            },
            {"role": "user", "content": message},
        ]
        response = self.openai.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content


class GeminiClient(AIClient):
    def __init__(self, api_key: str):
        configure(api_key=api_key)
        self.model = GenerativeModel("gemini-1.5-pro-002")
        self.vision_model = GenerativeModel("gemini-1.5-flash")

    def text_to_audio(self, text: str, voice: str = "en-US-Wavenet-D") -> BytesIO:
        """
        Converts input text to speech using Google Cloud Text-to-Speech API.
        NOTE: Gemini itself doesn't generate audio. You'd need to call TTS separately.
        """
        # Example using Google Cloud TTS REST API (not Gemini)
        from google.cloud import texttospeech

        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code="en-US", name=voice
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice_params, audio_config=audio_config
        )

        return BytesIO(response.audio_content)

    def audio_to_text(self, audio_file: BytesIO) -> str:
        """
        Converts input audio to text using Google Cloud Speech-to-Text.
        Gemini itself doesn't transcribe audio.
        """
        from google.cloud import speech

        client = speech.SpeechClient()
        audio_file.seek(0)
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)
        return " ".join(
            result.alternatives[0].transcript for result in response.results
        )

    def send_message(self, message: str, model: str = "gemini-pro") -> str:
        """
        Sends a prompt to Gemini and returns the response text.
        """
        try:
            prompt = "You are a helpful assistant. Be short, friendly, and concise. Use only plain text."
            full_prompt = f"{prompt}\n\nUser: {message}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except GoogleAPIError as e:
            return f"Error from Gemini: {str(e)}"

    def describe_image(self, image_content: BytesIO) -> str:
        """
        Takes an image as BytesIO and returns a detailed description using Gemini Vision.
        The description is formatted to be informative and useful for future model interactions.

        Args:
            image_content (BytesIO): The image content to analyze

        Returns:
            str: A detailed description of the image
        """
        try:
            # Convert BytesIO to base64 for Gemini
            image_content.seek(0)
            image_bytes = image_content.read()
            image_parts = [{"mime_type": "image/jpeg", "data": image_bytes}]

            prompt = """
            Please provide a detailed description of this image that covers:
            1. Main subjects and their characteristics
            2. Important visual elements and their spatial relationships
            3. Colors, lighting, and overall composition
            4. Any text or numbers visible in the image
            5. Context and setting
            
            Format the description in clear, natural language that would be helpful for answering questions about the image later.
            """

            response = self.vision_model.generate_content(
                contents=[prompt, image_parts[0]]
            )

            return response.text.strip()
        except GoogleAPIError as e:
            return f"Error analyzing image: {str(e)}"
