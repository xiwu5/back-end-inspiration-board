from flask import Blueprint, request
from ..models.card import Card
from ..db import db
from .route_utilities import validate_model, create_model, create_no_content_response

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.get("/<card_id>")
def get_one_card(card_id):
    card = validate_model(Card, card_id)
    return card.to_dict(), 200

@cards_bp.put("/<card_id>")
def update_card(card_id):
    card = validate_model(Card, card_id)
    request_body = request.get_json()
    
    new_message = request_body.get("message")
    if new_message is not None:
        if not new_message or len(new_message) > 40:
            return {"details": "Invalid data"}, 400
        card.message = new_message
    
    card.likes = request_body.get("likes", card.likes)
    
    db.session.commit()
    
    return card.to_dict(), 200

@cards_bp.patch("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)
    
    card.likes += 1
    db.session.commit()
    
    return card.to_dict(), 200

@cards_bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    
    db.session.delete(card)
    db.session.commit()
    
    return create_no_content_response()