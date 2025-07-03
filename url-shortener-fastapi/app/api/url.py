from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db import get_db
from app.models import Url, User
from app.schemas import CreateUrlDTO, GetUrlDTO
from app.utils import generate_random_string, get_expiration_time

router = APIRouter(prefix="/urls", tags=["urls"])


@router.get("/get_user_urls", response_model=List[GetUrlDTO])
async def get_user_urls(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    stmt = select(Url).where(Url.user_id == user.id)
    urls = db.execute(stmt).scalars().all()
    return urls


@router.post("/shorten", response_model=GetUrlDTO)
async def shorten(
    url: CreateUrlDTO,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if url.ttl_minutes > user.max_ttl_minutes:  # pyright: ignore
        raise HTTPException(status_code=400, detail="TTL minutes exceeds user limit")
    short_code = generate_random_string()
    stmt = select(Url).where(Url.short_url == short_code)
    while db.execute(stmt).scalars().first():
        short_code = generate_random_string()

    expiry = get_expiration_time(url.ttl_minutes)
    new_url = Url(
        short_url=short_code,
        original_url=url.original_url,
        user_id=user.id,
        expires_at=expiry,
    )
    db.add(new_url)
    db.commit()
    return new_url


@router.get("/{short_code}")
async def get_url(short_code: str, db: Session = Depends(get_db)):
    stmt = text("SELECT get_url_by_short_code_and_update(:short_code)")
    url = db.execute(stmt, {"short_code": short_code}).scalar_one_or_none()
    if not url or url == "url not found":
        raise HTTPException(status_code=404, detail="URL not found")
    if url == "url has expired":
        raise HTTPException(status_code=410, detail="URL expired")
    return Response(status_code=302, headers={"Location": url})


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
