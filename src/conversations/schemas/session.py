from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class SessionBase(BaseModel):
    """Base schema for session without the id and timestamps"""
    external_id: UUID = Field(..., description="External UUID for the session")


class SessionCreate(SessionBase):
    """Schema for creating a new session"""
    pass


class Session(SessionBase):
    """Schema for a complete session with id and timestamps"""
    id: int = Field(..., description="Unique identifier for the session")
    created_at: datetime = Field(..., description="Timestamp when the session was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the session was last updated")

    class Config:
        from_attributes = True 