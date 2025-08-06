from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Category, Post
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories with pagination"""
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@router.get("/{id}", response_model=CategoryRead)
def get_category(id: int, db: Session = Depends(get_db)):
    """Get a single category by ID"""
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    # Check if category already exists
    existing_category = (
        db.query(Category).filter(Category.name == category.name).first()
    )
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put("/{id}", response_model=CategoryRead)
def update_category(
    id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)
):
    """Update an existing category"""
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if new name already exists
    if category_update.name != category.name:
        existing_category = (
            db.query(Category).filter(Category.name == category_update.name).first()
        )
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")

    for field, value in category_update.model_dump().items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if category is being used by posts
    posts_count = db.query(Post).filter(Post.category_id == id).count()
    if posts_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category. It is being used by {posts_count} post(s)",
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
