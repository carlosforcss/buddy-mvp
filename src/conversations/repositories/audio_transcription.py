from src.conversations.models.audio_transcription import AudioTranscription


class AudioTranscriptionRepository:
    model = AudioTranscription

    @staticmethod
    async def create(
        file: "src.files.models.File", transcription: str
    ) -> AudioTranscription:
        """Create a new audio transcription"""
        return await AudioTranscription.create(file=file, transcription=transcription)

    @staticmethod
    async def get_by_id(id: int) -> AudioTranscription:
        """Get an audio transcription by its ID"""
        return await AudioTranscription.get(id=id)
