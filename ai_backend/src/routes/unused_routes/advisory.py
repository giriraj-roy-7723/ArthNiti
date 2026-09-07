# from fastapi import APIRouter, HTTPException, Depends
# from src.models.advisory import AdvisoryRequest, AdvisoryResponse
# from src.controllers.advisory_service import generate_dynamic_advisory_report


# from src.middlewares.auth import verify_token

# router = APIRouter()


# @router.post("/report", response_model=AdvisoryResponse)
# async def generate_advisory(
#     request: AdvisoryRequest, 
#     user_id: str = Depends(verify_token)
# ):
#     try:
#         result = generate_dynamic_advisory_report(
#             location_name=request.location_name,
#             business_type=request.business_type,
#             sample_12m_mandi_prices=request.sample_12m_mandi_prices,
#         )
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
