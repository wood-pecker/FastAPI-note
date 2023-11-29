from fastapi import HTTPException

from app.models.database import database
from app.models.note_boards import note_boards
from app.utils import boards as board_utils
from app.utils import notes as note_utils


async def get_note_board(board_id: int, note_id: int):
    query = (
        note_boards.select()
        .where(note_boards.c.board_id == board_id)
        .where(note_boards.c.note_id == note_id)
    )
    result = await database.fetch_one(query)
    return result


async def add_note(board_id: int, note_id: int):
    await board_utils.is_board_exist(board_id)
    await note_utils.is_note_exist(note_id)
    if await get_note_board(board_id, note_id):
        raise HTTPException(status_code=404, detail="Note already added")
    query = note_boards.insert().values(board_id=board_id, note_id=note_id)
    async with database.transaction():
        await database.execute(query)
        await board_utils.update_updated_at(board_id)


async def remove_note(board_id: int, note_id: int):
    if not await get_note_board(board_id, note_id):
        raise HTTPException(
            status_code=404, detail="There is no such note on the board"
        )
    query = (
        note_boards.delete()
        .where(note_boards.c.board_id == board_id)
        .where(note_boards.c.note_id == note_id)
    )
    async with database.transaction():
        await database.execute(query)
        await board_utils.update_updated_at(board_id)
