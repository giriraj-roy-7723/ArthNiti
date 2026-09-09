from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.government_schemes import GovernmentScheme

from pydantic import BaseModel, HttpUrl


class SchemeUrlResponse(BaseModel):
    scheme_id: int
    scheme_name: str
    url: str
    is_fallback: bool

    class Config:
        from_attributes = True
        
DEFAULT_MYSCHEME_URL = "https://www.myscheme.gov.in"


async def get_scheme_url_by_id(
    scheme_id: int,
    db: AsyncSession,
) -> SchemeUrlResponse:
    query = select(GovernmentScheme).where(GovernmentScheme.id == scheme_id)
    result = await db.execute(query)
    scheme = result.scalar_one_or_none()

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Government scheme with ID {scheme_id} not found",
        )

    # Check if a custom scheme_url exists and is non-empty
    if scheme.scheme_url and scheme.scheme_url.strip():
        resolved_url = scheme.scheme_url.strip()
        is_fallback = False
    elif scheme.slug and scheme.slug.strip():
        # Optional: Construct a specific myscheme detail URL if slug exists
        resolved_url = f"https://www.myscheme.gov.in/schemes/{scheme.slug.strip()}"
        is_fallback = False
    else:
        # Fallback to the main myscheme portal
        resolved_url = DEFAULT_MYSCHEME_URL
        is_fallback = True

    return SchemeUrlResponse(
        scheme_id=scheme.id,
        scheme_name=scheme.scheme_name,
        url=resolved_url,
        is_fallback=is_fallback,
    )
