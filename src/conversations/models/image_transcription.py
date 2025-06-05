from tortoise import fields, Model
from enum import Enum


class ImageTranscriptionStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class ImageTranscription(Model):
    id = fields.IntField(primary_key=True)
    file = fields.ForeignKeyField("models.File", on_delete=fields.CASCADE)
    session = fields.ForeignKeyField("models.Session", on_delete=fields.CASCADE)
    transcription = fields.TextField()
    status = fields.CharEnumField(
        enum_type=ImageTranscriptionStatus, default=ImageTranscriptionStatus.CREATED
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "image_transcriptions"
