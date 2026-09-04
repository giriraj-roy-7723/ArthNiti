from fastapi import APIRouter, HTTPException
from src.models.logistics import LogisticsRequest, LogisticsResponse
from src.services.logistics_service import run_supply_chain_and_transportation_analysis

router = APIRouter()


@router.post("/evaluate", response_model=LogisticsResponse)
async def evaluate_logistics(request: LogisticsRequest):
    try:
        result = run_supply_chain_and_transportation_analysis(
            business_type=request.business_type,
            origin_location=request.origin_location,
            search_radius_meters=request.search_radius_meters,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
