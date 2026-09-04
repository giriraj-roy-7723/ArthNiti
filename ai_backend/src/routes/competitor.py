from fastapi import APIRouter, HTTPException
from src.models.competitor import CompetitorRequest, CompetitorResponse
from src.services.competitor_service import analyze_competitors

router = APIRouter()


@router.post("/analyze-competitors", response_model=CompetitorResponse)
async def get_competitors(request: CompetitorRequest):
    try:
        result = analyze_competitors(
            latitude=request.latitude,
            longitude=request.longitude,
            population=request.population,
            business_type=request.business_type,
            radius_km=request.radius_km,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
