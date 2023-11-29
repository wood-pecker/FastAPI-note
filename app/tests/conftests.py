import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from app.main import engine
from app.models.boards import boards
from app.models.database import SQLALCHEMY_DATABASE_URL
from app.models.note_boards import note_boards
from app.models.notes import notes

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def temp_db():
    try:
        yield SQLALCHEMY_DATABASE_URL
    finally:
        # pass
        drop_database(SQLALCHEMY_DATABASE_URL)
        create_database(SQLALCHEMY_DATABASE_URL)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
        command.upgrade(alembic_cfg, "head")


@pytest.fixture()
def set_up_and_teardown():
    connection = engine.connect()

    connection.execute(note_boards.delete())
    connection.execute(notes.delete())
    connection.execute(boards.delete())

    note_1 = connection.execute(
        notes.insert().values(content="This is a 1 Note!").returning(notes.c.id)
    )
    note_1_id = note_1.fetchone()[0]
    note_2 = connection.execute(
        notes.insert().values(content="This is a 2 Note!").returning(notes.c.id)
    )
    note_2_id = note_2.fetchone()[0]
    connection.execute(notes.insert().values(content="This is a 3 Note!"))

    board_1 = connection.execute(
        boards.insert().values(name="This is a 1 Board!").returning(boards.c.id)
    )
    board_1_id = board_1.fetchone()[0]
    connection.execute(boards.insert().values(name="This is a 2 Board!"))

    connection.execute(
        note_boards.insert().values(board_id=board_1_id, note_id=note_1_id)
    )
    connection.execute(
        note_boards.insert().values(board_id=board_1_id, note_id=note_2_id)
    )

    connection.close()


@pytest.fixture()
def clear_db():
    connection = engine.connect()

    connection.execute(note_boards.delete())
    connection.execute(notes.delete())
    connection.execute(boards.delete())

    connection.close()
