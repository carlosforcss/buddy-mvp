from typing import List
from fastapi import WebSocket
from starlette.websockets import WebSocketState
from config import settings
import json
import base64
import uuid
import websockets
from starlette.websockets import WebSocketState
import asyncio
from utils.constants import OPENAI_REALTIME_INSTRUCTIONS
from websockets.exceptions import ConnectionClosed
from utils.logger import Logger
from utils.ai import OpenAIClient, GeminiClient
from utils.s3 import S3Client
from src.services import FileService
from src.repositories import FilesRepository
from src.repositories import ImageTranscriptionRepository
from src.services import ImageTranscriptionService
from src.repositories import AudioTranscriptionRepository
from src.services import AudioTranscriptionService
from src.repositories import SessionRepository
from src.services import SessionService

logger = Logger(__name__)


class RealtimeEventsService:
    def __init__(
        self,
        modalities: List[str],
        voice: str,
        instructions: str,
        input_audio_format: str,
        input_audio_transcription: dict,
        tools: List[dict],
    ):
        self.session_id = str(uuid.uuid4())[:8]
        self.modalities = modalities
        self.voice = voice
        self.instructions = instructions
        self.input_audio_format = input_audio_format
        self.input_audio_transcription = input_audio_transcription
        self.tools = tools

    def get_first_session_update_event(self, modalities: List[str]):
        logger.info("sending first session update event")
        return {
            "type": "session.update",
            "session": {
                "modalities": modalities,
                "voice": "alloy",
                "instructions": "You are a specialized assistant for low-vision and blind users. Always communicate in Spanish. Provide clear, friendly, and concise responses. Keep explanations brief but informative. Be direct and avoid unnecessary details. You have a 1000-token limit per response - if your answer would exceed this, pause at a natural breaking point and ask in Spanish if the user would like you to continue.",
                "input_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "gpt-4o-transcribe",
                    "prompt": "Transcribe this audio in Spanish, focusing on clarity and accuracy",
                    "language": "es",
                },
                "tools": self.tools,
            },
        }

    def get_response_create_event(self, modalities: List[str]):
        logger.info("sending response create event")
        return {
            "event_id": "event_234",
            "type": "response.create",
            "response": {
                "modalities": modalities,
                "instructions": "You are assisting a low-vision or blind user. Always communicate in Spanish. Keep responses clear, friendly, and concise. You have a 1000-token limit - for longer responses, pause and ask in Spanish if the user wants to continue.",
                "tools": [],
                "tool_choice": "auto",
                "temperature": 1,
                "max_output_tokens": 1000,
            },
        }

    def get_conversation_text_item_create_event(self, text: str, role: str = "user"):
        logger.info("sending conversation text item create event")
        return {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": role,
                "content": [
                    {
                        "type": "input_text",
                        "text": text,
                    }
                ],
            },
        }

    def get_conversation_audio_item_create_event(self, audio_base64: str):
        logger.info("sending conversation audio item create event")
        return {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "audio": audio_base64,
                    }
                ],
            },
        }

    def get_connection_headers(self):
        logger.info("sending connection headers")
        return {
            "Authorization": f"Bearer {settings.OPENAI_REALTIME_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "realtime=v1",
        }

    def get_connection_url(self, model: str):
        logger.info("connection url sent")
        return f"{settings.OPENAI_REALTIME_URL}?model={model}"

    def get_audio_buffer_append_event(self, audio_base64: str):
        logger.info("sending audio buffer append event")
        return {
            "event_id": f"audio_append_{id(audio_base64)}",
            "type": "input_audio_buffer.append",
            "audio": audio_base64,
        }

    def get_audio_buffer_commit_event(self):
        logger.info("sending audio buffer commit event")
        return {
            "event_id": f"audio_commit_{id(object())}",
            "type": "input_audio_buffer.commit",
        }


class RealtimeSessionService:
    def __init__(self):
        self.modalities = ["audio", "text"]
        self.voice = "alloy"
        self.instructions = OPENAI_REALTIME_INSTRUCTIONS
        self.input_audio_format = "pcm16"
        self.input_audio_transcription = {
            "model": "gpt-4o-transcribe",
            "prompt": "Transcribe this audio in Spanish, focusing on clarity and accuracy",
            "language": "es",
        }
        # Initialize services
        self.openai_client = OpenAIClient(settings.OPENAI_API_KEY)
        self.gemini_client = GeminiClient(settings.GOOGLE_API_KEY)
        self.files_service = FileService()
        self.audio_transcription_repository = AudioTranscriptionRepository()
        self.audio_transcription_service = AudioTranscriptionService(
            self.openai_client,
            self.files_service,
            self.audio_transcription_repository,
            logger,
        )
        self.session_repository = SessionRepository()
        self.session_service = SessionService(self.session_repository, logger)
        self.session_events_service = RealtimeEventsService(
            self.modalities,
            self.voice,
            self.instructions,
            self.input_audio_format,
            self.input_audio_transcription,
            self.get_tools(),
        )
        self.image_transcription_repository = ImageTranscriptionRepository()
        self.image_transcription_service = ImageTranscriptionService(
            self.gemini_client,
            self.files_service,
            self.image_transcription_repository,
            self.session_repository,
            logger,
        )

    def get_tools(self):
        return [
            {
                "name": "get_last_image_description",
                "type": "function",
                "description": "Use this tool whenever the user implies any need to visually interpret, read, identify, analyze, describe, or find something in an image. This includes phrases like 'What is this?', 'Can you read this?', 'Describe the image', 'What do you see?', 'Is there any text here?', 'Look at this and tell me…', or similar. If the user implies a visual task, always call this tool without guessing or answering directly. Use it to describe the most recently uploaded image.",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "get_chihuahua_weather",
                "type": "function",
                "description": "Use this tool whenever the user asks for the weather in Chihuahua, Mexico. This includes phrases like 'What is the weather in Chihuahua?' or similar. If the user implies a weather task, always call this tool without guessing or answering directly. Use it to get the weather in Chihuahua, Mexico.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location to get the weather for",
                        }
                    },
                },
            },
        ]

    def _get_connection_headers(self):
        return {
            "Authorization": f"Bearer {settings.OPENAI_REALTIME_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "realtime=v1",
        }

    def _get_connection_url(self):
        return f"{settings.OPENAI_REALTIME_URL}?model={settings.OPENAI_REALTIME_MODEL}"

    async def _handle_connection_close(self, session):
        logger.info(f"Connection closed for session {session.id}")
        await self.session_repository.close_session(session)
        if hasattr(self, "external_ws") and self.external_ws.open:
            await self.external_ws.close()
        if hasattr(self, "internal_ws") and self.internal_ws.client_state == WebSocketState.CONNECTED:
            await self.internal_ws.close()

    async def _buddy_websocket_listener(
        self, internal_websocket: WebSocket, external_websocket: WebSocket, session
    ):
        while True:
            try:
                logger.info("receiving audio")
                data = await internal_websocket.receive_bytes()
                logger.info("audio received")

                audio_transcription = (
                    await self.audio_transcription_service.transcribe_audio(data)
                )
                logger.info(f"Audio transcription created: {audio_transcription.id}")

                audio_base64 = base64.b64encode(data).decode("utf-8")
                new_message = self.session_events_service.get_conversation_audio_item_create_event(
                    audio_base64
                )
                await external_websocket.send(json.dumps(new_message))
                logger.info("commit event sent")
            except websockets.ConnectionClosed:
                await self._handle_connection_close(session)
                break
            except Exception as e:
                logger.error(
                    f"Error in client_to_external audio handling {session.id}: {e}"
                )
                await self._handle_connection_close(session)
                break

    async def _openai_websocket_listener(
        self, internal_websocket: WebSocket, external_websocket: WebSocket, session
    ):
        while True:
            try:
                data = await external_websocket.recv()
                event = json.loads(data)
                if not event.get("type") == "response.audio.delta":
                    await internal_websocket.send_text(
                        json.dumps({"log": f"{event}"}, indent=4)
                    )
                if (
                    event.get("type") == "conversation.item.created"
                    and event.get("item").get("role") == "user"
                ):
                    last_image_transcription = await self.image_transcription_service.wait_for_last_image_transcription_processing(session.id)
                    if last_image_transcription:
                        transcription_message = self.session_events_service.get_conversation_text_item_create_event(last_image_transcription.transcription, "system")
                        logger.info(f"Sending transcription event message.")
                        await external_websocket.send(json.dumps(transcription_message))
                    else:
                        response_create_event = (
                            self.session_events_service.get_response_create_event(
                                ["audio", "text"]
                            )
                        )
                        await external_websocket.send(json.dumps(response_create_event))
                if (
                    event.get("type") == "conversation.item.created"
                    and event.get("item").get("role") == "system"
                ):
                    logger.info(f"{session.id} - Sending response create event")
                    response_create_event = (
                        self.session_events_service.get_response_create_event(
                            ["audio", "text"]
                        )
                    )
                    await external_websocket.send(json.dumps(response_create_event))
                if event.get("type") == "response.audio.delta":
                    logger.info(f"{session.id} - Receiving audio delta chunk")
                    audio_data = base64.b64decode(event.get("delta"))
                    await internal_websocket.send_bytes(audio_data)
            except websockets.ConnectionClosed:
                break
            except Exception as e:
                logger.error(
                    f"Error in external_to_client audio handling {session.id}: {e}"
                )
                break

    async def connect(self, internal_websocket: WebSocket, session_id: int):
        session = await self.session_repository.get_by_id(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        async with websockets.connect(
            self._get_connection_url(),
            extra_headers=self._get_connection_headers(),
        ) as external_ws:
            logger.info(f"connected to external ws for session {session_id}")
            self.external_ws = external_ws
            self.internal_ws = internal_websocket
            await external_ws.send(
                json.dumps(
                    self.session_events_service.get_first_session_update_event(
                        self.modalities
                    )
                )
            )
            await asyncio.gather(
                self._openai_websocket_listener(
                    internal_websocket, external_ws, session
                ),
                self._buddy_websocket_listener(
                    internal_websocket, external_ws, session
                ),
            )
