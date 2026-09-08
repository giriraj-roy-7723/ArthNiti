from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.business_controller import create_business, get_business
from src.middlewares.auth import verify_token
from src.models.business_request import BusinessCreateRequest, BusinessResponse

router = APIRouter()


@router.post(
    "/create",
    response_model=BusinessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_business_route(
    data: BusinessCreateRequest,
    language: str = "english",
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    # Added the 'language' parameter to match the updated controller
    return await create_business(data=data, owner_id=user_id, language=language, db=db)


@router.get(
    "/{business_id}",
    response_model=BusinessResponse,
    status_code=status.HTTP_200_OK,
)
async def get_business_route(
    business_id: str,
    language: str = "english",
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    # Added new endpoint to fetch a business using the updated controller
    return await get_business(
        business_id=business_id, language=language, owner_id=user_id, db=db
    )
