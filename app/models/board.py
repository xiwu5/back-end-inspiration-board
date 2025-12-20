from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from ..db import db


class Board(db.Model):
    __tablename__ = "boards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    cards: Mapped[List["Card"]] = relationship("Card", back_populates="board", cascade="all, delete-orphan")


    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"])
        return new_board
    
    def to_dict(self):
        board_as_dict = {}
        board_as_dict["id"] = self.id
        board_as_dict["title"] = self.title
        board_as_dict["cards"] = [card.to_dict() for card in self.cards]
        return board_as_dict


    @classmethod
    def get_by_id(cls, board_id):
        board = db.session.get(cls, board_id)
        
        if board is None:
            return {"message": f"Board with ID {board_id} not found"}, 404
        return board, 200


