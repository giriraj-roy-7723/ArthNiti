from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.business_request import BusinessCreateRequest
from src.schema.business import Business


async def create_business(
    data: BusinessCreateRequest,
    owner_id: str,
    db: AsyncSession,
) -> Business:
    business = Business(owner_id=owner_id, **data.model_dump())
    db.add(business)

    try:
        await db.commit()
        await db.refresh(business)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Unable to create business")

    return business