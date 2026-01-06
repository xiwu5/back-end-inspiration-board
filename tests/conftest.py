import os
import pytest
from app.db import db
from app import create_app
from datetime import datetime
from dotenv import load_dotenv
from app.models.board import Board
from app.models.card import Card
from flask.signals import request_finished

load_dotenv()


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_board(app):
    board = Board(title="Daily Affirmations", owner="Test Owner")
    db.session.add(board)
    db.session.commit()


@pytest.fixture
def three_boards(app):
    db.session.add_all(
        [
            Board(title="Daily Affirmations", owner="Owner 1"),
            Board(title="Weekly Wins", owner="Owner 2"),
            Board(title="Monthly Goals", owner="Owner 3"),
        ]
    )
    db.session.commit()


@pytest.fixture
def board_with_cards(app):
    board = Board(title="Daily Affirmations", owner="Test Owner")
    db.session.add(board)
    db.session.commit()

    cards = [
        Card(message="You can do it", likes=0, board_id=board.id),
        Card(message="Keep going", likes=1, board_id=board.id),
    ]
    db.session.add_all(cards)
    db.session.commit()


@pytest.fixture
def one_card(app, one_board):
    card = Card(message="Stay kind", board_id=1, likes=0)
    db.session.add(card)
    db.session.commit()


@pytest.fixture
def timestamped_card(app, one_board):
    card = Card(
        message="Shine bright",
        board_id=1,
        likes=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.session.add(card)
    db.session.commit()
