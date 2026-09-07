# from fastapi import APIRouter, HTTPException, Depends
# from src.models.competitor import CompetitorRequest, CompetitorResponse
# from src.controllers.competitor_service import analyze_competitors

# from src.middlewares.auth import verify_token

# router = APIRouter()


# @router.post("/analyze-competitors", response_model=CompetitorResponse)
# async def get_competitors(
#     request: CompetitorRequest,
#     user_id: str = Depends(verify_token),
# ):
#     try:
#         result = analyze_competitors(
#             latitude=request.latitude,
#             longitude=request.longitude,
#             population=request.population,
#             business_type=request.business_type,
#             radius_km=request.radius_km,
#         )
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
