from datetime import date

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text

from app.utils import get_time

from .base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), unique=True, nullable=False)
    publishing_date = Column(Date, nullable=False, default=date.today)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_time)
    updated_at = Column(DateTime(timezone=True), default=get_time, onupdate=get_time)
