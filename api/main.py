import logging

from fastapi import FastAPI

from api.routers.campaigns import router as campaigns_router
from api.routers.events import router as events_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Campaign Manager API",
    description="API for managing campaigns and processing events",
    version="1.0.0"
)

app.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
app.include_router(events_router, prefix="/events", tags=["events"])

@app.get("/health")
async def health():
    return {"status": "ok"}
