from pydantic import BaseModel
from typing import Any, Optional


class MarketPriceRequest(BaseModel):
    business_type: str
    state: str = "West Bengal"


class MarketPriceResponse(BaseModel):
    business_type: str
    state: str
    state_id: int
    ai_generated_profile: dict[str, Any]
    sources: dict[str, Any]
