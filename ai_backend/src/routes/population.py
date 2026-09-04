from fastapi import APIRouter, HTTPException
from src.models.populations import MarketReachRequest, MarketReachResponse
from src.services.population_service import analyze_market_reach

router = APIRouter()


@router.post("/analyze-reach", response_model=MarketReachResponse)
async def get_market_reach(request: MarketReachRequest):
    try:
        result = analyze_market_reach(
            location=request.location, radius_km=request.radius_km, year=request.year
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
