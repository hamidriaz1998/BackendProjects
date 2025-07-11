from .base import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from app.utils import get_time


class UrlVisit(Base):
    __tablename__ = "url_visits"

    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False)
    user_agent = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=get_time)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False, index=True)
