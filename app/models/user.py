from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # 與訂單的關聯，使用 lazy="dynamic" 來提高性能和避免循環引用問題
    orders = relationship("Order", back_populates="user", lazy="dynamic")
