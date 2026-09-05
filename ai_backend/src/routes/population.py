from fastapi import APIRouter, HTTPException,Depends
from src.models.populations import MarketReachRequest, MarketReachResponse
from src.controllers.population_service import analyze_market_reach

from src.middlewares.auth import verify_token

router = APIRouter()


@router.post("/analyze-reach", response_model=MarketReachResponse)
async def get_market_reach(
    request: MarketReachRequest, 
    user_id: str = Depends(verify_token)
):
    try:
        result = analyze_market_reach(
            location=request.location, radius_km=request.radius_km, year=request.year
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
