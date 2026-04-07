from fastapi import FastAPI
from app.api.routes_rfq import router as rfq_router
from app.core.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://apexmaterials-website.onrender.com", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(rfq_router, prefix=settings.api_prefix)
