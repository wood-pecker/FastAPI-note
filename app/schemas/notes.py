from datetime import datetime

from pydantic import BaseModel


class BaseNote(BaseModel):
    content: str


class Note(BaseNote):
    id: int
    created_at: datetime
    updated_at: datetime
    view_count: int


class CreatedNote(BaseModel):
    id: int
