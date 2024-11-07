from sqlalchemy import Column, String, Integer, TIMESTAMP, text

from app.database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    middle_name = Column(String(150))
    city = Column(String(150), nullable=False)
    country = Column(String(150), nullable=False)
    address_1 = Column(String(150), nullable=False)
    address_2 = Column(String(150))
    postal_code = Column(String(20))
    email = Column(String(150), unique=True, nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

