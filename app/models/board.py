from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from datetime import datetime
from typing import List
from ..db import db


class Board(db.Model):
    __tablename__ = "boards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    cards: Mapped[List["Card"]] = relationship("Card", back_populates="board", cascade="all, delete-orphan")


    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"], owner=board_data["owner"])
        return new_board
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card.to_dict() for card in self.cards],
        }

    def to_dict_with_card_count(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "card_count": len(self.cards),
        }

    def to_dict_with_cards(self):
        return self.to_dict()

    @classmethod
    def get_by_id(cls, board_id):
        board = db.session.get(cls, board_id)
        
        if board is None:
            return {"message": f"Board with ID {board_id} not found"}, 404
        return board, 200


