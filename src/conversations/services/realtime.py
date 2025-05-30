from typing import List
from fastapi import WebSocket
from config import settings
import json
import base64
import uuid
import websockets
import asyncio


class RealtimeEventsService:
    def get_first_session_update_event(modalities: List[str]):
        print("sending first session update event")
        return {
            "type": "session.update",
            "session": {
                "modalities": modalities,
                "voice": "alloy",
                "instructions": "You are a helpful assistant.",
                "input_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "gpt-4o-transcribe",
                    "prompt": "Transcribe this audio in Spanish",
                    "language": "es",
                },
            },
        }

    def get_response_create_event(modalities: List[str]):
        print("sending response create event")
        return {
            "event_id": "event_234",
            "type": "response.create",
            "response": {
                "modalities": modalities,
                "instructions": "Please assist the user.",
                "tools": [],
                "tool_choice": "auto",
                "temperature": 0.7,
                "max_output_tokens": 1000,
            },
        }

    def get_conversation_text_item_create_event(text: str):
        print("sending conversation text item create event")
        return {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": text,
                    }
                ],
            },
        }

    def get_conversation_audio_item_create_event(audio_base64: str):
        print("sending conversation audio item create event")
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

    def get_connection_headers():
        print("sending connection headers")
        return {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "realtime=v1",
        }

    def get_connection_url(model: str):
        print("connection url sent")
        return f"{OPENAI_WS_URL}?model={model}"

    def get_audio_buffer_append_event(audio_base64: str):
        print("sending audio buffer append event")
        return {
            "event_id": f"audio_append_{id(audio_base64)}",  # Generate unique event ID
            "type": "input_audio_buffer.append",
            "audio": audio_base64,
        }

    def get_audio_buffer_commit_event():
        print("sending audio buffer commit event")
        return {
            "event_id": f"audio_commit_{id(object())}",  # Generate unique event ID
            "type": "input_audio_buffer.commit",
        }


class RealtimeSessionService:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.modalities = ["audio", "text"]
        self.voice = "alloy"
        self.instructions = "You are a helpful assistant."
        self.input_audio_format = "pcm16"
        self.input_audio_transcription = {
            "model": "gpt-4o-transcribe",
            "prompt": "Trnascribe this audio in Spanish",
            "language": "es",
        }

    def _get_first_session_update_event(self):
        return {
            "type": "session.update",
            "session": {
                "modalities": self.modalities,
                "voice": self.voice,
                "instructions": self.instructions,
                "input_audio_format": self.input_audio_format,
            },
        }

    def _get_connection_headers(self):
        return {
            "Authorization": f"Bearer {settings.OPENAI_REALTIME_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "realtime=v1",
        }

    def _get_connection_url(self):
        return f"{settings.OPENAI_REALTIME_URL}?model={settings.OPENAI_REALTIME_MODEL}"

    async def _buddy_websocket_listener(
        self, internal_websocket: WebSocket, external_websocket: WebSocket
    ):
        while True:
            try:
                print("receiving audio")
                data = await internal_websocket.receive_bytes()
                print("audio received")
                # Convert audio bytes to base64
                audio_base64 = base64.b64encode(data).decode("utf-8")
                # Create a new audio message
                new_message = (
                    RealtimeEventsService.get_conversation_audio_item_create_event(
                        audio_base64
                    )
                )
                await external_websocket.send(json.dumps(new_message))
                print("commit event sent")
            except Exception as e:
                print(
                    f"Error in client_to_external audio handling {self.session_id}: {e}"
                )
                break

    async def _openai_websocket_listener(
        self, internal_websocket: WebSocket, external_websocket: WebSocket
    ):
        while True:
            try:
                data = await external_websocket.recv()
                event = json.loads(data)
                if not event.get("type") == "response.audio.delta":
                    await internal_websocket.send_text(
                        json.dumps({"log": f"{event}"}, indent=4)
                    )
                if event.get("type") == "conversation.item.created":
                    response_create_event = (
                        RealtimeEventsService.get_response_create_event(
                            ["audio", "text"]
                        )
                    )
                    await external_websocket.send(json.dumps(response_create_event))
                # Handle audio response
                if event.get("type") == "response.audio.delta":
                    audio_data = base64.b64decode(event.get("delta"))
                    await internal_websocket.send_bytes(audio_data)
            except Exception as e:
                print(
                    f"Error in external_to_client audio handling {self.session_id}: {e}"
                )
                break

    async def connect(self, internal_websocket: WebSocket):
        async with websockets.connect(
            self._get_connection_url(),
            extra_headers=self._get_connection_headers(),
        ) as external_ws:
            print(f"connected to external ws {self.session_id}")
            external_ws.send(json.dumps(self._get_first_session_update_event()))
            await asyncio.gather(
                self._openai_websocket_listener(internal_websocket, external_ws),
                self._buddy_websocket_listener(internal_websocket, external_ws),
            )
