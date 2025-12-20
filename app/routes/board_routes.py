from flask import Blueprint, request
from ..models.board import Board
from ..db import db
from .route_utilities import validate_model, create_model, create_no_content_response

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.get("")
def get_all_boards():
    boards = db.session.scalars(db.select(Board).order_by(Board.id)).all()
    boards_response = [board.to_dict_with_card_count() for board in boards]
    return boards_response, 200

@boards_bp.post("")
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board.from_dict(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_board)
    db.session.commit()
    
    return new_board.to_dict_with_card_count(), 201

@boards_bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200

@boards_bp.put("/<board_id>")
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    
    board.title = request_body.get("title", board.title)
    
    db.session.commit()
    
    return board.to_dict_with_card_count(), 200

@boards_bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)
    
    db.session.delete(board)
    db.session.commit()
    
    return create_no_content_response()