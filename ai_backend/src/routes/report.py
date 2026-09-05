from fastapi import APIRouter, HTTPException, Depends
from src.models.report import ReportRequest, ReportResponse
from src.controllers.report_service import generate_feasibility_report

from src.middlewares.auth import verify_token

router = APIRouter()


@router.post("/generate", response_model=ReportResponse)
def generate_report(request: ReportRequest, user_id: str = Depends(verify_token)):
    """
    Orchestrates the entire pipeline (Population, Competitors, Prices, Supply Chain, Logistics, Advisory)
    and generates a comprehensive Markdown Feasibility Report.
    """
    try:
        # Note: Using standard `def` instead of `async def` because this endpoint
        # orchestrates multiple blocking, synchronous requests.
        result = generate_feasibility_report(
            location=request.location,
            business_type=request.business_type,
            margin_capital=request.margin_capital,
            radius_km=request.radius_km,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
