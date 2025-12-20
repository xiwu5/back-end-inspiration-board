import pytest

from app.db import db
from app.models.board import Board
from app.models.card import Card


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


def test_card_to_dict():
    card = Card(id=2, card_message="Shine bright", likes=3, board_id=1)

    result = card.to_dict()

    assert result == {
        "id": 2,
        "card_message": "Shine bright",
        "likes": 3,
        "board_id": 1,
    }


def test_card_from_dict():
    data = {"card_message": "Shine bright", "board_id": 1}

    card = Card.from_dict(data)

    assert card.card_message == "Shine bright"
    assert card.board_id == 1
    assert card.likes == 0


def test_card_from_dict_missing_message():
    data = {"board_id": 1}

    with pytest.raises(KeyError, match="card_message"):
        Card.from_dict(data)


def test_card_from_dict_missing_board_id():
    data = {"card_message": "Shine bright"}

    with pytest.raises(KeyError, match="board_id"):
        Card.from_dict(data)


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


def test_create_card(client, one_board):
    response = client.post(
        "/cards", json={"card_message": "Stay positive", "board_id": 1}
    )
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "card_message": "Stay positive",
        "likes": 0,
        "board_id": 1,
    }

    card = db.session.scalar(db.select(Card).where(Card.id == 1))
    assert card
    assert card.card_message == "Stay positive"
    assert card.likes == 0
    assert card.board_id == 1


def test_create_card_requires_message(client, one_board):
    response = client.post("/cards", json={"board_id": 1})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}
    assert db.session.scalars(db.select(Card)).all() == []


def test_create_card_requires_board_id(client, one_board):
    response = client.post("/cards", json={"card_message": "Stay positive"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}
    assert db.session.scalars(db.select(Card)).all() == []
