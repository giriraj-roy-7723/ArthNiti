from fastapi import APIRouter, HTTPException, Depends
from src.models.supply_chain import SupplyChainRequest, SupplyChainResponse
from src.controllers.supply_chain_service import evaluate_supply_chain


from src.middlewares.auth import verify_token

router = APIRouter()


@router.post("/evaluate", response_model=SupplyChainResponse)
async def get_supply_chain(
    request: SupplyChainRequest, user_id: str = Depends(verify_token)
):
    try:
        result = evaluate_supply_chain(
            location_name=request.location_name,
            business_type=request.business_type,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
