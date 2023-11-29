from sqlalchemy.orm import sessionmaker

from app.main import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from fastapi.testclient import TestClient

from app.main import app
from app.models.boards import boards
from app.tests.conftests import clear_db, set_up_and_teardown, temp_db


def test_create_board(temp_db):
    request_data = {"name": "This is the first test board!"}

    with TestClient(app) as client:
        response = client.post("/boards", json=request_data)
    board_id = response.json()["id"]
    with SessionLocal() as db:
        item_from_db = db.query(boards).filter(boards.c.id == board_id).first()

    assert response.status_code == 201
    assert item_from_db
    assert dict(item_from_db).get("name") == request_data.get("name")


def test_create_board_failed(temp_db):
    request_data = {"content": "This is the first test board!"}

    with TestClient(app) as client:
        response = client.post("/boards", json=request_data)
    assert response.status_code == 422


def test_get_boards(temp_db, set_up_and_teardown):
    excepted_boards_count = 2

    with TestClient(app) as client:
        response = client.get("/boards")

    response_boards = response.json()
    assert response.status_code == 200
    assert len(response_boards) == excepted_boards_count


def test_get_boards_by_id(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        single_board = db.query(boards).first()
    with TestClient(app) as client:
        response = client.get(f"/boards/{single_board.id}")

    response_board = response.json()
    assert response.status_code == 200
    assert response_board.get("id") == single_board.id


def test_get_boards_by_id_failed_404(temp_db, clear_db):
    board_id = 1
    with TestClient(app) as client:
        response = client.get(f"/boards/{board_id}")

    assert response.status_code == 404


def test_get_boards_by_id_422(temp_db, set_up_and_teardown):
    board_id = 0
    with TestClient(app) as client:
        response = client.get(f"/boards/{board_id}")

    assert response.status_code == 422


def test_update_board(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        response_board = db.query(boards).first()
    board_id = response_board.id
    updated_data = "Updated name"

    with TestClient(app) as client:
        response = client.put(f"/boards/{board_id}/{updated_data}")

    with SessionLocal() as db:
        updated_board = db.query(boards).filter(boards.c.id == board_id).first()

    assert response.status_code == 204
    assert updated_board.name == updated_data


def test_update_board_failed_404(temp_db, clear_db):
    board_id = 1
    updated_data = "Updated name"

    with TestClient(app) as client:
        response = client.put(f"/boards/{board_id}/{updated_data}")

    assert response.status_code == 404


def test_update_board_failed_422(temp_db):
    board_id = 0
    updated_data = "Updated name"

    with TestClient(app) as client:
        response = client.put(f"/boards/{board_id}/{updated_data}")

    assert response.status_code == 422


def test_delete_board(temp_db, set_up_and_teardown):
    with SessionLocal() as db:
        response_board = db.query(boards).first()
    board_id = response_board.id

    with TestClient(app) as client:
        response = client.delete(f"/boards/{board_id}")

    assert response.status_code == 204
    with SessionLocal() as db:
        deleted_board = db.query(boards).filter(boards.c.id == board_id).first()
    assert deleted_board is None


def test_delete_board_failed_404(temp_db, clear_db):
    board_id = 1
    with TestClient(app) as client:
        response = client.delete(f"/boards/{board_id}")

    assert response.status_code == 404


def test_delete_board_failed_422(temp_db):
    board_id = 0
    with TestClient(app) as client:
        response = client.delete(f"/boards/{board_id}")

    assert response.status_code == 422
