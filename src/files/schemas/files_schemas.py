from typing import Optional
from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    id: Optional[int] = Field(None, null=True)
    name: Optional[int] = Field(None, null=True)
    file_type: str
    content: str
