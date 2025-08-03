from .article import router as article_router, get_all_articles
from .auth import router as auth_router

__all__ = ["auth_router", "article_router", "get_all_articles"]
