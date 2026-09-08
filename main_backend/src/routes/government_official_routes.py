from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.government_official_controller import (
    update_government_official,
    get_government_official,
)
from src.middlewares.auth import verify_token
from src.models.government_official_request import (
    GovernmentOfficialUpdateRequest,
    GovernmentOfficialResponse,
)

router = APIRouter()


@router.get(
    "/get",
    response_model=GovernmentOfficialResponse,
    status_code=status.HTTP_200_OK,
)
async def get_government_official_route(
    language: str = "english",
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    # Added endpoint to fetch the government official profile
    return await get_government_official(user_id=user_id, language=language, db=db)


@router.patch(
    "/update",
    response_model=GovernmentOfficialResponse,
    status_code=status.HTTP_200_OK,
)
async def update_government_official_route(
    data: GovernmentOfficialUpdateRequest,
    language: str = "english",
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    # Added endpoint to update the government official profile
    return await update_government_official(
        data=data, language=language, user_id=user_id, db=db
    )
