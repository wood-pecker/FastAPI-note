from sqlalchemy import Column, ForeignKey, Table

from app.models.database import metadata

note_boards = Table(
    "note_boards",
    metadata,
    Column("note_id", ForeignKey("notes.id")),
    Column("board_id", ForeignKey("boards.id")),
)
