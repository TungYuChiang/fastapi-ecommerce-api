from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Association with orders, using lazy="dynamic" to improve performance and avoid circular reference problems
    orders = relationship("Order", back_populates="user", lazy="dynamic")
