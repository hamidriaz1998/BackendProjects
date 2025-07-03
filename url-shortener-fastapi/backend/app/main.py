from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_router
from app.api import url_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(url_router)

@app.get("/test")
def test(request: Request):
    user_agent = request.headers.get("User-Agent")
    referrer = request.headers.get("Referer")
    return {"ip": request.client.host, "user_agent": user_agent, "referrer": referrer} # pyright: ignore

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
