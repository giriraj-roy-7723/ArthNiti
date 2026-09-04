from pydantic import BaseModel

class CompetitorRequest(BaseModel):
    latitude: float
    longitude: float
    population: int
    business_type: str
    radius_km: float = 10.0


class CompetitorResponse(BaseModel):
    search: dict
    competitor_summary: dict
    sources: dict
    competitors: list[dict]
