# Buddy - Accessibility Assistant

Buddy is an innovative accessibility tool designed to assist people with low vision and blindness, providing an enhanced digital interaction experience through audio processing and AI-powered features.

## 🌟 Features

- **Audio Processing**: Real-time conversion between different audio formats (PCM/MP3)
- **Speech-to-Text Transcription**: Accurate audio transcription powered by OpenAI
- **Cloud Storage Integration**: Secure audio file storage using S3
- **Database Management**: Efficient storage and retrieval of transcriptions

## 🛠 Technology Stack

### Backend Services
- **Python**: Core programming language
- **FFmpeg**: Audio processing and format conversion
- **OpenAI**: AI-powered audio transcription
- **AWS S3**: Cloud storage for audio files

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL**: Database management

## 📋 Prerequisites

- Docker and Docker Compose
- AWS Account (for S3 storage)
- OpenAI API Key

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/buddy.git
cd buddy
```

2. Create a `.env` file in the project root:
```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
S3_BUCKET=your_bucket_name

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
POSTGRES_DB=buddy
POSTGRES_USER=buddy_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Start the application using Docker Compose:
```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`

## 🏗 Project Structure

```
buddy/
├── src/
│   ├── conversations/
│   │   ├── services/
│   │   │   └── audio_transcription_service.py  # Audio processing and transcription
│   │   └── repositories/                       # Data access layer
│   ├── files/
│   │   └── services/                          # File handling and S3 storage
│   └── utils/
│       ├── ai.py                              # AI client configuration
│       └── logger.py                          # Logging utilities
├── docker/                                    # Docker configuration files
├── docker-compose.yml
└── requirements.txt
```

## 🐳 Docker Compose Services

The application runs using the following containers:

- **app**: Main Python application
- **db**: PostgreSQL database
- **redis**: Cache and message broker (if applicable)

```yaml
# Example docker-compose.yml structure
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: postgres:14-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

volumes:
  postgres_data:
```

## 🔧 Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 storage |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 storage |
| `OPENAI_API_KEY` | OpenAI API key for transcription |
| `POSTGRES_*` | Database configuration variables |

## 📝 API Documentation

The API provides the following main endpoints:

- `POST /api/audio/transcribe`: Upload and transcribe audio files
- `GET /api/transcriptions/{id}`: Retrieve a specific transcription
- `GET /api/transcriptions`: List all transcriptions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the transcription capabilities
- FFmpeg for audio processing functionality
- The open-source community for various tools and libraries used in this project
