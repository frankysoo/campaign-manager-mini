from pydantic import BaseModel


class CampaignCreate(BaseModel):
    name: str
    rules: dict


class CampaignOut(BaseModel):
    id: int
    name: str
    rules: dict
    created_at: str
