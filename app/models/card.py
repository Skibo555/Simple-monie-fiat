from sqlalchemy import Column, String, Integer, TIMESTAMP, text, ForeignKey

from app.database.database import Base


class Card(Base):
    __table__ = "cards"
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    last_four_num = Column(String(4), nullable=False)
    exp_month = Column(String(2), nullable=False)
    exp_year = Column(String(4), nullable=False)
    bank_name = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    currency = Column(String(10), nullable=False)
    country = Column(String(100), nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))