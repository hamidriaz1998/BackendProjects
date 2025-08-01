from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_router

app = FastAPI()
app.include_router(auth_router)


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
