from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer

from app.utils import get_time

from ..base import Base


class UserOTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    otp = Column(Integer, unique=True, nullable=False)
    used = Column(Boolean, default=False)
    expiration = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_time)
    updated_at = Column(DateTime(timezone=True), default=get_time, onupdate=get_time)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
