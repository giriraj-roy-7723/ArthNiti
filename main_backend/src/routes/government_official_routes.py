from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.government_official_controller import (
    create_government_official,
)
from src.middlewares.auth import verify_token
from src.models.government_official_request import (
    GovernmentOfficialCreateRequest,
    GovernmentOfficialResponse,
)

router = APIRouter()


@router.post(
    "",
    response_model=GovernmentOfficialResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_government_official_route(
    data: GovernmentOfficialCreateRequest,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await create_government_official(data, user_id, db)