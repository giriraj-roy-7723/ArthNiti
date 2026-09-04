from pydantic import BaseModel
from typing import Any, Optional


class SupplyChainRequest(BaseModel):
    location_name: str
    business_type: str


class SupplyChainResponse(BaseModel):
    location: str
    coordinates: dict[str, float]
    business_type: str
    pillars: dict[str, Any]
    overall_supply_chain_score: float
