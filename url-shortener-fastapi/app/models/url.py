from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from app.utils import get_time
from .base import Base


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
