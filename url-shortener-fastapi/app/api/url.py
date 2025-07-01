from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db import get_db
from app.models import Url, User
from app.schemas import GetUrlDTO
from app.utils import generate_random_string

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post("/shorten", response_model=GetUrlDTO)
async def shorten(
    url: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    short_code = generate_random_string()
    stmt = select(Url).where(Url.short_url == short_code)
    while db.execute(stmt).scalars().first():
        short_code = generate_random_string()

    new_url = Url(short_url=short_code, original_url=url, user_id=user.id)
    db.add(new_url)
    db.commit()
    return new_url


@router.get("/{short_code}")
async def get_url(short_code: str, db: Session = Depends(get_db)):
    stmt = select(Url).where(Url.short_url == short_code)
    url = db.execute(stmt).scalars().first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    update_stmt = (
        update(Url)
        .where(Url.short_url == short_code)
        .values(click_count=Url.click_count + 1)
    )
    db.execute(update_stmt)
    db.commit()
    return Response(status_code=302, headers={"Location": str(url.original_url)})


@router.delete("/{short_code}")
async def delete_url(
    short_code: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Url).where(Url.short_url == short_code)
    url = db.execute(stmt).scalars().first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    if url.user_id != user.id:  # pyright: ignore
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(url)
    db.commit()
    return {"message": "URL deleted"}


@router.get("/user")
async def get_user_urls(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    stmt = select(Url).where(Url.user_id == user.id)
    urls = db.execute(stmt).scalars().all()
    return {"urls": urls}
