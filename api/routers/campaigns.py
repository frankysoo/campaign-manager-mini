from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.db import get_session
from api.models import Campaign
from api.schemas.campaign import CampaignCreate, CampaignOut

router = APIRouter()

@router.get("/")
async def list_campaigns():
    # Stub, return empty list for now
    return []

@router.post("/", response_model=CampaignOut)
async def create_campaign(campaign: CampaignCreate) -> CampaignOut:
    async with get_session() as session:
        # Check if campaign with same name exists?
        # For now, just create
        db_campaign = Campaign(name=campaign.name, rules=campaign.rules)
        session.add(db_campaign)
        await session.commit()
        await session.refresh(db_campaign)

        # Convert to out model
        return CampaignOut(
            id=db_campaign.id,
            name=db_campaign.name,
            rules=db_campaign.rules,
            created_at=db_campaign.created_at.isoformat()
        )
