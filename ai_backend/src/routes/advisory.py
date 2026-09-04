from fastapi import APIRouter, HTTPException
from src.models.advisory import AdvisoryRequest, AdvisoryResponse
from src.services.advisory_service import generate_dynamic_advisory_report

router = APIRouter()


@router.post("/report", response_model=AdvisoryResponse)
async def generate_advisory(request: AdvisoryRequest):
    try:
        result = generate_dynamic_advisory_report(
            location_name=request.location_name,
            business_type=request.business_type,
            sample_12m_mandi_prices=request.sample_12m_mandi_prices,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
