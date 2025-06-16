from typing import Optional
from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    id: Optional[int] = Field(None, null=True)
    name: str
    bucket: Optional[str] = Field(None, null=True) 