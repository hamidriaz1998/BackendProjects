from datetime import datetime
from typing import List

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class TagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    category: str | None = None
    tags: List[str] | None = None


class PostRead(PostBase):
    id: int
    category: CategoryRead | None = None
    tags: List[TagRead] | None = None
    created_at: datetime
    updated_at: datetime


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    tags: List[str] | None = None

    class Config:
        from_attributes = True
