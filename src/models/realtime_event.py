from tortoise import fields, Model
from enum import Enum


class EventDirection(str, Enum):
    RECEIVED = "received"
    SENT = "sent"


class RealtimeEvent(Model):
    id = fields.IntField(primary_key=True)
    session_id = fields.IntField()
    type = fields.CharField(max_length=100)
    event_body = fields.JSONField()
    direction = fields.CharEnumField(enum_type=EventDirection)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "realtime_events"