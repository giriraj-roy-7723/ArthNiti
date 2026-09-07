from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.government_official_request import GovernmentOfficialCreateRequest
from src.schema.government_officials import GovernmentOfficial


async def create_government_official(
    data: GovernmentOfficialCreateRequest,
    user_id: str,
    db: AsyncSession,
) -> GovernmentOfficial:
    official = GovernmentOfficial(user_id=user_id, **data.model_dump())
    db.add(official)

    try:
        await db.commit()
        await db.refresh(official)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to create government official profile",
        )

    return official