from pydantic import BaseModel
from typing import Any, Optional


class AdvisoryRequest(BaseModel):
    location_name: str
    business_type: str
    sample_12m_mandi_prices: Optional[list[float]] = None


class AdvisoryResponse(BaseModel):
    location: str
    coordinates: dict[str, float]
    business_category: str
    supply_chain_metrics: dict[str, Any]
    dynamic_seasonality_analysis: dict[str, Any]
