import pytest
from app.db import db
from app.models.board import Board


def test_board_to_dict():
    board = Board(id=1, title="Daily Affirmations")
    result = board.to_dict()
    assert result == {"id": 1, "title": "Daily Affirmations", "cards": []}


def test_board_from_dict():
    data = {"title": "Daily Affirmations"}
    board = Board.from_dict(data)
    assert board.title == "Daily Affirmations"


def test_board_from_dict_missing_title():
    with pytest.raises(KeyError, match="title"):
        Board.from_dict({})


def test_get_boards_no_saved_boards(client):
    response = client.get("/boards")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_boards_one_saved_board(client, one_board):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{"id": 1, "title": "Daily Affirmations", "card_count": 0}]


def test_get_boards_includes_card_count(client, board_with_cards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1, "title": "Daily Affirmations", "card_count": 2}
    ]


def test_create_board(client):
    response = client.post("/boards", json={"title": "New Board"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"id": 1, "title": "New Board", "card_count": 0}

    board = db.session.scalar(db.select(Board).where(Board.id == 1))
    assert board
    assert board.title == "New Board"


def test_create_board_requires_title(client):
    response = client.post("/boards", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}
    assert db.session.scalars(db.select(Board)).all() == []


def test_get_one_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Daily Affirmations",
        "cards": []
    }


def test_get_one_board_not_found(client):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}


def test_update_board(client, one_board):
    response = client.put("/boards/1", json={
        "title": "Updated Board Title"
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["title"] == "Updated Board Title"

    board = db.session.scalar(db.select(Board).where(Board.id == 1))
    assert board.title == "Updated Board Title"


def test_update_board_not_found(client):
    response = client.put("/boards/1", json={
        "title": "Updated Board Title"
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}


def test_delete_board(client, one_board):
    response = client.delete("/boards/1")

    assert response.status_code == 204
    assert db.session.scalar(db.select(Board).where(Board.id == 1)) is None


def test_delete_board_not_found(client):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}
    assert db.session.scalars(db.select(Board)).all() == []
