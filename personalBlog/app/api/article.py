from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from markdown import markdown
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_utils import get_current_user, get_current_user_optional
from app.db import get_db
from app.models import Article, User
from app.templates import templates

router = APIRouter(prefix="/article", tags=["Article"])



def get_all_articles(db: Session = Depends(get_db)):
    stmt = select(Article)
    articles = list(db.scalars(stmt).all())
    return articles


@router.get("/new")
async def new_article_form(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "new_article.html", {"request": request, "current_user": user}
    )


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
    return RedirectResponse(url=f"/article/{new_article.id}", status_code=303)


@router.get("/edit/{id}")
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
        {"request": request, "article": article, "current_user": user},
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
    return {"status": "success", "article_id": article.id}


@router.delete("/{id}")
async def delete_article(
    id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Article).where(Article.id == id)
    article = db.scalars(stmt).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if user.id != article.author_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    db.delete(article)
    db.commit()
    return {"status": "success", "message": "Article deleted successfully"}


@router.get("/{id}")
async def get_article(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
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
            "current_user": current_user,
        },
    )
