from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from src.files.schemas.files_schemas import FileSchema


class AudioTranscriptionBase(BaseModel):
    """Base schema for audio transcription without the id and timestamps"""

    file_id: int = Field(..., description="Id of the file object in the database")
    transcription: str = Field(..., description="The text transcription of the audio")


class AudioTranscriptionCreate(AudioTranscriptionBase):
    """Schema for creating a new audio transcription"""

    pass


class AudioTranscriptionSchema(BaseModel):
    id: Optional[int] = None
    file: FileSchema
    transcription: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("file", pre=True)
    def parse_file(cls, v):
        return FileSchema(id=v.id, name=v.name, bucket=v.bucket)

    class Config:
        from_attributes = True
