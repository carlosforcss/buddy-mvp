from tortoise import fields, Model


class AudioTranscription(Model):
    id = fields.IntField(primary_key=True)
    file = fields.ForeignKeyField("models.File", on_delete=fields.CASCADE)
    transcription = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "audio_transcriptions"
