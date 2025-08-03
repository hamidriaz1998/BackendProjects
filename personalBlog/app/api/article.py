from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from markdown import markdown
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_utils import get_current_user
from app.db import get_db
from app.models import Article, User
from app.templates import templates

router = APIRouter(prefix="/article", tags=["Article"])


@router.get("/{id}", response_class=HTMLResponse)
async def get_article(id: int, request: Request, db: Session = Depends(get_db)):
    stmt = select(Article).where(Article.id == id)
    article = db.scalars(stmt).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    html_content = markdown(text=article.content)

    # Get all articles for sidebar
    all_articles = get_all_articles(db)

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "article": article,
            "content_html": html_content,
            "articles": all_articles,
        },
    )


def get_all_articles(db: Session = Depends(get_db)):
    stmt = select(Article)
    articles = db.scalars(stmt).all()
    return list(articles)


@router.get("/new", response_class=HTMLResponse)
async def new_article_form(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("new_article.html", {"request": request})


@router.post("/new_article")
async def new_article(
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_article = Article(title=title, content=content, author_id=user.id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_article_form(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    stmt = select(Article).where(Article.id == id)
    article = db.scalars(stmt).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if user.id != article.author_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return templates.TemplateResponse(
        "edit_article.html",
        {"request": request, "article": article},
    )


@router.put("/edit/{id}")
async def edit_article(
    id: int,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Article).where(Article.id == id)
    article = db.scalars(stmt).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if user.id != article.author_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    article.title = title
    article.content = content
    db.commit()
    db.refresh(article)
    return article
