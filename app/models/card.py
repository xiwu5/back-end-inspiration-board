from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from datetime import datetime
from ..db import db

class Card(db.Model):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    card_message: Mapped[str] = mapped_column(String(255), nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    board: Mapped["Board"] = relationship("Board", back_populates="cards")

    def to_dict(self):
        return {
            "id": self.id,
            "card_message": self.card_message,
            "likes": self.likes,
            "board_id": self.board_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            card_message=data["card_message"],
            likes=data.get("likes", 0),
            board_id=data["board_id"],
        )