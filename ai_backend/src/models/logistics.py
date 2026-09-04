from pydantic import BaseModel
from typing import Any, Optional


class LogisticsRequest(BaseModel):
    business_type: str
    origin_location: str
    search_radius_meters: int = 30000

class LogisticsResponse(BaseModel):
    business_type: str
    origin: dict[str, Any]
    discovered_supply_chain_nodes: dict[str, Any]
    transportation_logistics_opex: dict[str, Any]
    summary: dict[str, Any]
