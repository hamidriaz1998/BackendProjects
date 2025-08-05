from datetime import datetime
from typing import List

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    category: str | None
    tags: List[str] | None

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime


class PostUpdate(PostBase):
    id: int
