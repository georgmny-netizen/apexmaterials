from fastapi import FastAPI
from app.api.routes_rfq import router as rfq_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(rfq_router, prefix=settings.api_prefix)
