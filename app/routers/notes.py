from typing import List

from fastapi import APIRouter, Path

from app.schemas.notes import BaseNote, CreatedNote, Note
from app.utils import notes as note_utils

router = APIRouter()


@router.post("/notes/", response_model=CreatedNote, status_code=201)
async def create_note(note: BaseNote):
    return await note_utils.create_note(note)


@router.get("/notes/", response_model=List[Note])
async def get_notes(skip: int = 0, limit: int = 100):
    return await note_utils.get_notes(skip=skip, limit=limit)


@router.get("/notes_from_board/{board_id}", response_model=List[Note])
async def get_note_from_board(
    skip: int = 0, limit: int = 100, board_id: int = Path(gt=0)
):
    return await note_utils.get_notes(skip=skip, limit=limit, board_id=board_id)


@router.get("/notes/{note_id}", response_model=Note)
async def get_note_by_id(note_id: int = Path(gt=0)):
    return await note_utils.get_note_by_id(note_id)


@router.put("/notes/{note_id}/{content}", response_model=Note)
async def update_note(content: str, note_id: int = Path(gt=0)):
    await note_utils.update_note(note_id, {"content": content})
    return await note_utils.get_note(note_id)


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int = Path(gt=0)):
    await note_utils.delete_note(note_id)
