from sqlalchemy.orm import sessionmaker

from app.main import engine
from app.models.boards import boards
from app.models.note_boards import note_boards
from app.models.notes import notes

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from fastapi.testclient import TestClient

from app.main import app
from app.tests.conftests import clear_db, set_up_and_teardown, temp_db


def test_board_add_note_failed_404(temp_db, clear_db):
    board_id = 1
    note_id = 1

    with TestClient(app) as client:
        response = client.put(f"/boards_add_note/{board_id}/{note_id}")

    assert response.status_code == 404


def test_board_add_note_failed_422(temp_db, clear_db):
    board_id = 0
    note_id = 0

    with TestClient(app) as client:
        response = client.put(f"/boards_add_note/{board_id}/{note_id}")

    assert response.status_code == 422


def test_board_remove_note(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        board_to_add = (
            db.query(notes)
            .filter(boards.c.name == "This is a 1 Board!")
            .first()
        )
        note_for_add = (
            db.query(notes)
            .filter(notes.c.content == "This is a 2 Note!")
            .first()
        )

    with TestClient(app) as client:
        response = client.put(
            f"/boards_remove_note/{board_to_add.id}/{note_for_add.id}"
        )

    assert response.status_code == 204
    with SessionLocal() as db:
        notes_from_board = (
            db.query(note_boards).filter(boards.c.id == board_to_add.id).all()
        )
    assert len(notes_from_board) == 1


def test_board_remove_note_failed_404(temp_db, clear_db):
    board_id = 1
    note_id = 1

    with TestClient(app) as client:
        response = client.put(f"/boards_remove_note/{board_id}/{note_id}")

    assert response.status_code == 404


def test_board_remove_note_failed_422(temp_db, clear_db):
    board_id = 0
    note_id = 0

    with TestClient(app) as client:
        response = client.put(f"/boards_remove_note/{board_id}/{note_id}")

    assert response.status_code == 422
