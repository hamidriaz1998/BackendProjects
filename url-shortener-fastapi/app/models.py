from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_time():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_time)
    updated_at = Column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username})"


class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String(255), nullable=False)
    short_url = Column(String(255), unique=True, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_time)
    updated_at = Column(DateTime(timezone=True), default=get_time, onupdate=get_time)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Url(id={self.id}, original_url={self.original_url}, short_url={self.short_url}, user_id={self.user_id})"
