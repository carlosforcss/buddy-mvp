from tortoise import fields, Model
from enum import Enum


class SessionStatus(str, Enum):
    OPENED = "opened"
    CLOSED = "closed"


class Session(Model):
    id = fields.IntField(primary_key=True)
    external_id = fields.UUIDField(unique=True)
    status = fields.CharEnumField(enum_type=SessionStatus, default=SessionStatus.OPENED)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "sessions"
