from datetime import datetime
from typing import List

from pydantic import BaseModel


class BaseBoard(BaseModel):
    name: str


class Board(BaseBoard):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class BoardNotes(Board):
    notes_id: List[int]


class CreatedBoard(BaseModel):
    id: int
