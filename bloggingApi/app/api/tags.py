from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import PostTagsLink, Tag
from app.schemas import TagCreate, TagRead, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagRead])
def get_all_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tags with pagination"""
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags


@router.get("/{id}", response_model=TagRead)
def get_tag(id: int, db: Session = Depends(get_db)):
    """Get a single tag by ID"""
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=TagRead)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Create a new tag"""
    # Check if tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")

    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.put("/{id}", response_model=TagRead)
def update_tag(id: int, tag_update: TagUpdate, db: Session = Depends(get_db)):
    """Update an existing tag"""
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if new name already exists
    if tag_update.name != tag.name:
        existing_tag = db.query(Tag).filter(Tag.name == tag_update.name).first()
        if existing_tag:
            raise HTTPException(status_code=400, detail="Tag name already exists")

    for field, value in tag_update.model_dump().items():
        setattr(tag, field, value)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{id}")
def delete_tag(id: int, db: Session = Depends(get_db)):
    """Delete a tag"""
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if tag is being used by posts
    posts_count = db.query(PostTagsLink).filter(PostTagsLink.tag_id == id).count()
    if posts_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete tag. It is being used by {posts_count} post(s)",
        )

    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
