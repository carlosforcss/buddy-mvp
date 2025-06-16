from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from src.models import ImageTranscriptionStatus
from src.schemas.files import FileSchema


class ImageTranscriptionBase(BaseModel):
    """Base schema for image transcription without the id and timestamps"""

    file_id: int = Field(..., description="Id of the file object in the database")
    session_id: int = Field(
        ..., description="Id of the session this transcription belongs to"
    )
    transcription: str = Field(..., description="The text transcription of the image")
    status: ImageTranscriptionStatus = Field(
        default=ImageTranscriptionStatus.CREATED,
        description="Current status of the image transcription",
    )


class ImageTranscriptionCreate(ImageTranscriptionBase):
    """Schema for creating a new image transcription"""

    pass


class ImageTranscription(ImageTranscriptionBase):
    """Schema for a complete image transcription with id and timestamps"""

    id: str = Field(..., description="Unique identifier for the image transcription")
    created_at: datetime = Field(
        ..., description="Timestamp when the transcription was created"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the transcription was last updated"
    )

    class Config:
        from_attributes = True


class ImageTranscriptionSchema(BaseModel):
    id: Optional[int] = None
    file: FileSchema
    session_id: int
    transcription: str
    status: ImageTranscriptionStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("file", pre=True)
    def parse_file(cls, v):
        return FileSchema(id=v.id, name=v.name, bucket=v.bucket)

    class Config:
        from_attributes = True
