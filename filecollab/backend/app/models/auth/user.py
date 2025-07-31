from sqlalchemy import Column, DateTime, Integer, String, Boolean

from app.utils import get_time

from ..base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    max_ttl_minutes = Column(Integer, nullable=False, default=60)
    created_at = Column(DateTime(timezone=True), default=get_time)
    updated_at = Column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username})"
