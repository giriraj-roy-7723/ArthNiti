from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db

from src.middlewares.role import require_enterpreneur
from src.schema.enterpreneur import Enterpreneur
from src.schema.business_profile import BusinessProfile
from src.schema.business_profile_translation import BusinessProfileTranslation

# Ensure you import the combined service function we created
from src.controllers.business_profile_service import process_profile_and_recommendations
from src.models.business_profile_request import (
    CombinedRecommendationResponse,
    EligibilityProfileRequest,
)

router = APIRouter()


@router.post(
    "/{business_id}",
    response_model=CombinedRecommendationResponse,
)
async def route_create_profile_and_recommend_schemes(
    business_id: str,
    request: EligibilityProfileRequest,
    language: str = Query(
        "en", description="Target language code (e.g., 'en', 'hi', 'bn')"
    ),
    force: bool = Query(False),
    limit: int = Query(10, ge=1, le=20, description="Number of schemes to return"),
    enterpreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    try:
        if force:
            profile_result = await db.execute(
                select(BusinessProfile.id).where(
                    BusinessProfile.business_id == business_id
                )
            )
            profile_ids = profile_result.scalars().all()

            if profile_ids:
                await db.execute(
                    delete(BusinessProfileTranslation).where(
                        BusinessProfileTranslation.business_profile_id.in_(profile_ids)
                    )
                )
                await db.execute(
                    delete(BusinessProfile).where(BusinessProfile.id.in_(profile_ids))
                )
            await db.flush()

        # This single controller function now generates the profile,
        # searches the vector DB, translates, and saves to both tables.
        result = await process_profile_and_recommendations(
            db=db,
            business_id=business_id,
            eligibility_data=request.model_dump(exclude_unset=True),
            target_language=language,
            limit=limit,
        )

        return CombinedRecommendationResponse(
            business_id=business_id,
            analysis_id=result["analysis_id"],
            business_profile=result["business_profile"],
            eligibility_profile=result["eligibility_profile"],
            target_language=language,
            original_english_schemes=result["original_english_schemes"],
            translated_schemes=result["translated_schemes"],
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate profile and recommendations: {exc}",
        )
