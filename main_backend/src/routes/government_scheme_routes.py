# src/routers/government_scheme_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db  # Import your DB dependency
from src.controllers.government_scheme_controller import get_scheme_url_by_id


from pydantic import BaseModel, HttpUrl


class SchemeUrlResponse(BaseModel):
    scheme_id: int
    scheme_name: str
    url: str
    is_fallback: bool

    class Config:
        from_attributes = True
router = APIRouter()


@router.get(
    "/{scheme_id}/url",
    response_model=SchemeUrlResponse,
    status_code=status.HTTP_200_OK,
    summary="Get scheme URL details by ID",
    description="Retrieves the URL for a government scheme. Falls back to myscheme.gov.in if no custom URL is available.",
)
async def fetch_scheme_url(
    scheme_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_scheme_url_by_id(scheme_id=scheme_id, db=db)
