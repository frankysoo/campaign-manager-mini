from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.db import get_session
from api.models import Campaign
from api.schemas.campaign import CampaignCreate, CampaignOut
from common.auth import get_current_active_user, get_admin_user, User
from common.metrics import campaigns_created_total

router = APIRouter()

@router.get("/")
async def list_campaigns():
    async with get_session() as session:
        result = await session.execute(select(Campaign))
        campaigns = result.scalars().all()
        return [
            CampaignOut(
                id=db_campaign.id,
                name=db_campaign.name,
                rules=db_campaign.rules,
                created_at=db_campaign.created_at.isoformat()
            )
            for db_campaign in campaigns
        ]

@router.get("/{campaign_id}")
async def get_campaign(campaign_id: int):
    async with get_session() as session:
        result = await session.execute(select(Campaign).where(Campaign.id == campaign_id))
        db_campaign = result.scalars().first()

        if not db_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        return CampaignOut(
            id=db_campaign.id,
            name=db_campaign.name,
            rules=db_campaign.rules,
            created_at=db_campaign.created_at.isoformat()
        )

@router.post("/", response_model=CampaignOut)
async def create_campaign(campaign: CampaignCreate, current_user: User = Depends(get_admin_user)) -> CampaignOut:
    async with get_session() as session:
        # Check if campaign with same name exists?
        # For now, just create
        campaigns_created_total.inc()
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
