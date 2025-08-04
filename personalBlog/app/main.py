from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import article_router, auth_router, get_all_articles
from app.auth_utils import get_current_user_optional
from app.models import User
from app.templates import templates

app = FastAPI()
app.include_router(auth_router)
app.include_router(article_router)


@app.get("/")
async def root(
    request: Request,
    articles: list = Depends(get_all_articles),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "articles": articles, "current_user": current_user},
    )


# Configure Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
