# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Local Development
```bash
# Install dependencies
uv sync

# Run development server with auto-reload
uv run main.py
# Server runs on http://localhost:8000 with reload on src/ changes

# Using Docker for development
docker-compose up -d
```

### Production Deployment
```bash
# Production deployment
docker-compose -f production.yaml up -d
```

### Database Management
- Uses SQLite for development (`db.sqlite3`)
- Tortoise ORM handles schema generation automatically
- Database models are auto-registered from `src.models`

## Architecture Overview

### Application Structure
This is a FastAPI-based accessibility assistant API designed for low-vision and blind users, with real-time audio/visual processing capabilities.

**Key Components:**
- **FastAPI Application**: Main entry point in `main.py` with factory pattern (`get_app()`)
- **Real-time Communication**: WebSocket-based real-time audio processing via OpenAI's Realtime API
- **Multi-modal Support**: Audio transcription, image description, and conversational AI
- **External Integrations**: OpenAI (audio/text), Google Cloud (speech), AWS S3 (storage)

### Service Layer Architecture
The application follows a clean architecture pattern:

```
src/
├── routes/          # FastAPI endpoints (/api prefix)
├── services/        # Business logic layer
├── repositories/    # Data access layer
├── models/          # Tortoise ORM database models
├── schemas/         # Pydantic request/response models
└── integrations/    # External service integrations
```

### Key Services
- **RealtimeSessionService**: Manages WebSocket connections between client and OpenAI Realtime API
- **ConversationsService**: Handles simple text-based conversations
- **AudioTranscriptionService**: Processes audio files for transcription
- **ImageTranscriptionService**: Processes images for visual description using Google Gemini
- **SessionService**: Manages conversation sessions

### Real-time Processing Flow
1. Client connects via WebSocket to `/api/conversations/realtime/{session_id}`
2. `RealtimeSessionService` establishes connection to OpenAI Realtime API
3. Bidirectional audio streaming between client ↔ Buddy ↔ OpenAI
4. Image uploads trigger automatic visual context injection into conversations
5. Spanish-first accessibility-focused responses with 1000-token limits

### Configuration Management
- Environment variables loaded via `python-dotenv` in `config/settings.py`
- Required variables: AWS credentials, OpenAI API keys, Google API key
- Optional: Sentry DSN for error monitoring
- Configuration is centralized and imported throughout the application

### Database Schema
Uses Tortoise ORM with models for:
- **Session**: Conversation sessions
- **AudioTranscription**: Audio processing records
- **ImageTranscription**: Image processing records
- **Files**: File upload tracking

### External Dependencies
- **OpenAI**: Realtime API for conversational AI, standard API for transcription
- **Google Cloud**: Speech-to-Text, Text-to-Speech, Gemini for image analysis
- **AWS S3**: File storage and retrieval
- **FFmpeg**: Audio format conversion (PCM/MP3)
- **Sentry**: Error monitoring and performance tracking

### API Endpoints
All routes use `/api` prefix:
- `POST /api/conversations/sessions` - Create new session
- `POST /api/conversations/message` - Send simple text message
- `WebSocket /api/conversations/realtime/{session_id}` - Real-time audio communication
- `POST /api/conversations/image/{session_id}` - Upload image for description
- `POST /api/audio/transcribe` - Audio transcription
- `POST /api/files/upload` - File upload

### Spanish-First Accessibility Design
The application is specifically designed for Spanish-speaking users with visual impairments:
- All AI instructions emphasize Spanish communication
- Responses are optimized for clarity and brevity
- Visual context is automatically provided through image processing
- Real-time audio interaction for natural communication flow