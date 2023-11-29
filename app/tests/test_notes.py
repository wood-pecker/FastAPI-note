from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app, engine
from app.models.notes import notes
from app.tests.conftests import clear_db, set_up_and_teardown, temp_db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_create_note(temp_db):
    request_data = {"content": "This is the first test note!"}

    with TestClient(app) as client:
        response = client.post("/notes", json=request_data)
    note_id = response.json()["id"]
    with SessionLocal() as db:
        item_from_db = db.query(notes).filter(notes.c.id == note_id).first()

    assert response.status_code == 201
    assert item_from_db
    assert dict(item_from_db).get("content") == request_data.get("content")


def test_create_note_failed(temp_db):
    request_data = {"name": "This is the first test note!"}

    with TestClient(app) as client:
        response = client.post("/notes", json=request_data)

    assert response.status_code == 422


def test_get_notes(temp_db, set_up_and_teardown):
    excepted_notes_count = 3

    with TestClient(app) as client:
        response = client.get("/notes")

    response_notes = response.json()
    assert response.status_code == 200
    assert len(response_notes) == excepted_notes_count


def test_get_notes_by_id(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        single_note = db.query(notes).first()
    with TestClient(app) as client:
        response = client.get(f"/notes/{single_note.id}")

    response_note = response.json()
    assert response.status_code == 200
    assert response_note.get("id") == single_note.id


def test_get_notes_by_id_failed_404(temp_db, clear_db):
    note_id = 1
    with TestClient(app) as client:
        response = client.get(f"/notes/{note_id}")

    assert response.status_code == 404


def test_get_notes_by_id_422(temp_db, set_up_and_teardown):
    note_id = 0
    with TestClient(app) as client:
        response = client.get(f"/notes/{note_id}")

    assert response.status_code == 422


def test_update_note(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        response_note = db.query(notes).first()
    note_id = response_note.id
    updated_data = "Updated content"

    with TestClient(app) as client:
        response = client.put(f"/notes/{note_id}/{updated_data}")

    assert response.status_code == 200
    updated_note = response.json()
    assert updated_note["content"] == updated_data


def test_update_note_failed_404(temp_db, clear_db):
    note_id = 1
    updated_data = "Updated content"

    with TestClient(app) as client:
        response = client.put(f"/notes/{note_id}/{updated_data}")

    assert response.status_code == 404


def test_update_note_failed_422(temp_db):
    note_id = 0
    updated_data = "Updated content"

    with TestClient(app) as client:
        response = client.put(f"/notes/{note_id}/{updated_data}")

    assert response.status_code == 422


def test_delete_note(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        response_note = db.query(notes).first()
    note_id = response_note.id

    with TestClient(app) as client:
        response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 204
    with SessionLocal() as db:
        deleted_note = db.query(notes).filter(notes.c.id == note_id).first()
    assert deleted_note is None


def test_delete_note_failed_404(temp_db, clear_db):
    note_id = 1
    with TestClient(app) as client:
        response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 404


def test_delete_note_failed_422(temp_db):
    note_id = 0
    with TestClient(app) as client:
        response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 422
