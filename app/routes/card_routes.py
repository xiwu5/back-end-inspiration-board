from flask import Blueprint, jsonify, request

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


@cards_bp.post("")
def create_card():
    data = request.get_json() or {}
    return jsonify(
        {
            "id": 1,
            "card_message": data.get("card_message", ""),
            "likes": data.get("likes", 0),
            "board_id": data.get("board_id"),
        }
    ), 201