from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import article_router, auth_router, get_all_articles
from app.templates import templates

app = FastAPI()
app.include_router(auth_router)
app.include_router(article_router)


@app.get("/")
async def root(request: Request, articles: list = Depends(get_all_articles)):
    return templates.TemplateResponse(
        "index.html", {"request": request, "articles": articles}
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
