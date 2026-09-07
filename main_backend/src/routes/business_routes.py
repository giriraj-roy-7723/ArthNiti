from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.business_controller import create_business
from src.middlewares.auth import verify_token
from src.models.business_request import BusinessCreateRequest, BusinessResponse

router = APIRouter()


@router.post(
    "",
    response_model=BusinessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_business_route(
    data: BusinessCreateRequest,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await create_business(data, user_id, db)