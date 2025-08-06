from fastapi import FastAPI

from app.api import categories_router, posts_router, tags_router

app = FastAPI(
    title="Blogging API",
    description="A complete REST API for a blogging platform with posts, categories, and tags",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the Blogging API",
        "version": "1.0.0",
        "endpoints": {
            "posts": "/posts",
            "categories": "/categories",
            "tags": "/tags",
            "docs": "/docs",
            "health": "/health",
        },
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "blogging-api"}


app.include_router(posts_router)
app.include_router(categories_router)
app.include_router(tags_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
