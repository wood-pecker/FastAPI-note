from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.sql import update

from app.models.boards import boards
from app.models.database import database
from app.models.note_boards import note_boards
from app.schemas import boards as board_schemas
from app.utils import base


async def get_boards(skip: int = 0, limit: int = 100):
    base.check_skip_limit(skip, limit)
    query = boards.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


async def get_board(board_id: int, board_notes=False):
    query = boards.select().where(boards.c.id == board_id)
    db_board = await database.fetch_one(query)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not created")
    if not board_notes:
        return db_board
    db_board = dict(db_board)
    board_notes_query = note_boards.select().where(
        note_boards.c.board_id == board_id
    )
    board_notes = await database.fetch_all(board_notes_query)
    if not board_notes:
        db_board.update({"notes_id": []})
        return db_board
    notes_id = [board_note["note_id"] for board_note in board_notes]
    db_board.update({"notes_id": notes_id})
    return db_board


async def create_board(board: board_schemas.BaseBoard):
    db_note = boards.insert().values(name=board.name)
    note_id = await database.execute(db_note)
    return {"id": note_id}


async def is_board_exist(board_id: int):
    return await get_board(board_id)


async def delete_board(board_id: int):
    await is_board_exist(board_id)
    query_note_boards = note_boards.delete().where(
        note_boards.c.board_id == board_id
    )
    query_board = boards.delete().where(boards.c.id == board_id)
    async with database.transaction():
        await database.execute(query_note_boards)
        await database.execute(query_board)


async def update_name(board_id: int, new_data: dict):
    await is_board_exist(board_id)
    query = update(boards).where(boards.c.id == board_id).values(**new_data)
    await database.execute(query)


async def update_updated_at(board_id: int):
    new_data = {"updated_at": func.current_timestamp()}
    query = update(boards).where(boards.c.id == board_id).values(**new_data)
    await database.execute(query)
