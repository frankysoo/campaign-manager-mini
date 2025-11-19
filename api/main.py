import logging
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from fastapi import FastAPI, Response

from api.routers.campaigns import router as campaigns_router
from api.routers.events import router as events_router
from api.routers.auth import router as auth_router
from common.metrics import registry, service_up

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Campaign Manager API",
    description="API for managing campaigns and processing events",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
app.include_router(events_router, prefix="/events", tags=["events"])

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        generate_latest(registry),
        headers={"Content-Type": CONTENT_TYPE_LATEST}
    )
