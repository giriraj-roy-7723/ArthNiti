from fastapi import APIRouter, HTTPException
from src.models.market_price import MarketPriceRequest, MarketPriceResponse
from src.services.market_price_service import analyze_market_price

router = APIRouter()


@router.post("/analyze", response_model=MarketPriceResponse)
async def get_market_price(request: MarketPriceRequest):
    try:
        result = analyze_market_price(
            business_type=request.business_type,
            state=request.state,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
