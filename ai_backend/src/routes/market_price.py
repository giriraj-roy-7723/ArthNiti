from fastapi import APIRouter, HTTPException,Depends
from src.models.market_price import MarketPriceRequest, MarketPriceResponse
from src.controllers.market_price_service import analyze_market_price

from src.middlewares.auth import verify_token

router = APIRouter()


@router.post("/analyze", response_model=MarketPriceResponse)
async def get_market_price(
    request: MarketPriceRequest,
    user_id: str = Depends(verify_token)
):
    try:
        result = analyze_market_price(
            business_type=request.business_type,
            state=request.state,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
