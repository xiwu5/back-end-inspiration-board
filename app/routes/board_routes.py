from flask import Blueprint, jsonify, request

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.get("")
def list_boards():
    return jsonify([]), 200

@boards_bp.post("")
def create_board():
    data = request.get_json() or {}
    return jsonify({"id": 1, "title": data.get("title", ""), "card_count": 0}), 201