from typing import Optional

from fastapi import HTTPException
from sqlalchemy.sql import update

from app.models.database import database
from app.models.note_boards import note_boards
from app.models.notes import notes
from app.schemas import notes as note_schemas
from app.utils import base
from app.utils import boards as board_utils


async def get_notes(
    skip: int = 0, limit: int = 100, board_id: Optional[int] = None
):
    base.check_skip_limit(skip, limit)
    if board_id:
        db_board = await board_utils.get_board(board_id, True)
        note_ids = db_board.get("notes_id")
        query = (
            notes.select()
            .offset(skip)
            .limit(limit)
            .where(notes.c.id.in_(note_ids))
        )
    else:
        query = notes.select().offset(skip).limit(limit)
    result = await database.fetch_all(query)
    return result


async def get_note(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


async def is_note_exist(note_id: int):
    db_note = await get_note(note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not created")
    return db_note


async def get_note_by_id(note_id: int):
    db_note = await is_note_exist(note_id)
    view_count = db_note._mapping["view_count"] + 1
    await update_note(note_id, {"view_count": view_count}, False)
    return db_note


async def update_note(notes_id: int, new_data: dict, to_check=True):
    if to_check:
        await is_note_exist(notes_id)
    query = update(notes).where(notes.c.id == notes_id).values(**new_data)
    await database.execute(query)


async def create_note(note: note_schemas.BaseNote):
    db_note = notes.insert().values(content=note.content)
    note_id = await database.execute(db_note)
    return {"id": note_id}


async def delete_note(note_id: int):
    await is_note_exist(note_id)
    query_note_boards = note_boards.delete().where(
        note_boards.c.note_id == note_id
    )
    query_note = notes.delete().where(notes.c.id == note_id)
    async with database.transaction():
        await database.execute(query_note_boards)
        await database.execute(query_note)
