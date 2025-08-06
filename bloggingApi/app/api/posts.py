from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Category, Post, PostTagsLink, Tag
from app.schemas import PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostRead])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all posts with pagination"""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts


@router.get("/{id}", response_model=PostRead)
def get_post(id: int, db: Session = Depends(get_db)):
    """Get a single post by ID"""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostRead)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Create a new post"""
    post_data = post.model_dump()
    category_name = post_data.pop("category", None)
    tag_names = post_data.pop("tags", None) or []

    # Handle category
    category_id = None
    if category_name:
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.flush()
        category_id = category.id

    # Create the post
    new_post = Post(
        title=post_data["title"], content=post_data["content"], category_id=category_id
    )
    db.add(new_post)
    db.flush()

    # Handle tags
    for tag_name in tag_names:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()

        # Create the many-to-many relationship
        post_tag = PostTagsLink(post_id=new_post.id, tag_id=tag.id)
        db.add(post_tag)

    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=PostRead)
def update_post(id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    """Update an existing post"""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = post_update.model_dump(exclude_unset=True)
    category_name = update_data.pop("category", None)
    tag_names = update_data.pop("tags", None)

    # Update basic fields
    for field, value in update_data.items():
        if hasattr(post, field) and value is not None:
            setattr(post, field, value)

    # Update category if provided
    if category_name is not None:
        if category_name == "":
            setattr(post, "category_id", None)
        else:
            category = db.query(Category).filter(Category.name == category_name).first()
            if not category:
                category = Category(name=category_name)
                db.add(category)
                db.flush()
            setattr(post, "category_id", category.id)

    # Update tags if provided
    if tag_names is not None:
        # Remove existing tags
        db.query(PostTagsLink).filter(PostTagsLink.post_id == id).delete()

        # Add new tags
        for tag_name in tag_names:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()

            post_tag = PostTagsLink(post_id=post.id, tag_id=tag.id)
            db.add(post_tag)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Delete associated tags relationships
    db.query(PostTagsLink).filter(PostTagsLink.post_id == id).delete()

    # Delete the post
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}


@router.get("/category/{category_id}", response_model=List[PostRead])
def get_posts_by_category(
    category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all posts in a specific category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    posts = (
        db.query(Post)
        .filter(Post.category_id == category_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


@router.get("/tag/{tag_id}", response_model=List[PostRead])
def get_posts_by_tag(
    tag_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all posts with a specific tag"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    posts = (
        db.query(Post)
        .join(PostTagsLink)
        .filter(PostTagsLink.tag_id == tag_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


@router.get("/search/", response_model=List[PostRead])
def search_posts(
    q: str = None,
    category: str = None,
    tag: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Search posts by title, content, category, or tag"""
    query = db.query(Post)

    if q:
        query = query.filter(Post.title.contains(q) | Post.content.contains(q))

    if category:
        query = query.join(Category).filter(Category.name.ilike(f"%{category}%"))

    if tag:
        query = query.join(PostTagsLink).join(Tag).filter(Tag.name.ilike(f"%{tag}%"))

    posts = query.offset(skip).limit(limit).all()
    return posts
