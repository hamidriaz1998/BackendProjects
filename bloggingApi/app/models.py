from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


def get_time():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class PostTags(Base):
    __tablename__ = "post_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    category = Column(Integer, ForeignKey("categories.id"), nullable=True)
    tags = Column(Integer, ForeignKey("post_tags.post_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_time)
    created_at = Column(
        DateTime(timezone=True),
        default=get_time,
        onupdate=get_time,
    )
