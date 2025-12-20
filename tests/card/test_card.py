import pytest
from app.db import db
from app.models.card import Card


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


def test_get_one_card(client, one_card):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "card_message": "Stay kind",
        "likes": 0,
        "board_id": 1
    }


def test_get_one_card_not_found(client):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"}


def test_update_card(client, one_card):
    response = client.put("/cards/1", json={
        "card_message": "Updated message",
        "likes": 5
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["card_message"] == "Updated message"
    assert response_body["likes"] == 5

    card = db.session.scalar(db.select(Card).where(Card.id == 1))
    assert card.card_message == "Updated message"
    assert card.likes == 5


def test_update_card_not_found(client):
    response = client.put("/cards/1", json={
        "card_message": "Updated message"
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"}


def test_delete_card(client, one_card):
    response = client.delete("/cards/1")

    assert response.status_code == 204
    assert db.session.scalar(db.select(Card).where(Card.id == 1)) is None


def test_delete_card_not_found(client):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"}
    assert db.session.scalars(db.select(Card)).all() == []
