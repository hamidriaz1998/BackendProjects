from .categories import router as categories_router
from .posts import router as posts_router
from .tags import router as tags_router

__all__ = ["posts_router", "categories_router", "tags_router"]
