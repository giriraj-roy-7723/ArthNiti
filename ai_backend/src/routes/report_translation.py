from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.translator_service import (
    ReportTranslationError,
    translate_feasibility_report,
)
from src.middlewares.role import require_enterpreneur
from src.models.report_translation import (
    ReportTranslationRequest,
    ReportTranslationResponse,
)
from src.schema.business import Business
from src.schema.business_analysis import BusinessAnalysis
from src.schema.report_translations import (
    ReportLanguage,
    ReportTranslation,
)

# Make sure to import Enterpreneur or type hint as 'Any' if import is unavailable
from src.schema.enterpreneur import Enterpreneur

router = APIRouter()


@router.post(
    "/{business_id}/translate",
    response_model=ReportTranslationResponse,
)
async def translate_report(
    business_id: str,
    request: ReportTranslationRequest,
    current_user: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    """
    Translate the latest feasibility analysis of a business.

    The client provides only business_id. The latest BusinessAnalysis
    is fetched internally and the original English report/evidence
    are never modified.
    """

    # ========================================================
    # Fetch business and verify ownership
    # ========================================================
    business_stmt = select(Business).where(
        Business.id == business_id,
        Business.owner_id == current_user.user_id,
    )
    result = await db.execute(business_stmt)
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found.",
        )

    # ========================================================
    # Fetch latest analysis for this business
    # ========================================================
    analysis_stmt = (
        select(BusinessAnalysis)
        .where(BusinessAnalysis.business_id == business.id)
        .order_by(BusinessAnalysis.version.desc())
    )
    result = await db.execute(analysis_stmt)
    analysis = result.scalars().first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No feasibility analysis found for this business.",
        )

    language = request.language.strip().lower()

    # ========================================================
    # English
    # ========================================================
    if language == "english":
        raw_evidence = {
            "population": analysis.population_payload,
            "competitors": analysis.competitor_payload,
            "market_price": analysis.market_price_payload,
            "supply_chain": analysis.supply_chain_payload,
            "transportation": analysis.transportation_payload,
            "seasonality": analysis.seasonality_payload,
        }

        return ReportTranslationResponse(
            status="success",
            analysis_id=analysis.id,
            language="english",
            report_markdown=analysis.report_markdown,
            raw_evidence=raw_evidence,
        )

    # ========================================================
    # Validate language
    # ========================================================
    try:
        report_language = ReportLanguage(language)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported language: {language}. "
                "Supported languages: english, hindi, bengali."
            ),
        )

    # ========================================================
    # Check existing translation
    # ========================================================
    translation_stmt = select(ReportTranslation).where(
        ReportTranslation.report_id == analysis.id,
        ReportTranslation.language == report_language,
    )
    result = await db.execute(translation_stmt)
    existing_translation = result.scalar_one_or_none()

    if existing_translation:
        translated_evidence = {
            "population": existing_translation.population_payload,
            "competitors": existing_translation.competitor_payload,
            "market_price": existing_translation.market_price_payload,
            "supply_chain": existing_translation.supply_chain_payload,
            "transportation": existing_translation.transportation_payload,
            "seasonality": existing_translation.seasonality_payload,
        }

        return ReportTranslationResponse(
            status="success",
            analysis_id=analysis.id,
            language=language,
            report_markdown=existing_translation.content or "",
            raw_evidence=translated_evidence,
        )

    # ========================================================
    # Build original English evidence
    # ========================================================
    original_evidence = {
        "population": analysis.population_payload,
        "competitors": analysis.competitor_payload,
        "market_price": analysis.market_price_payload,
        "supply_chain": analysis.supply_chain_payload,
        "transportation": analysis.transportation_payload,
        "seasonality": analysis.seasonality_payload,
    }

    # ========================================================
    # Translate
    # ========================================================
    try:
        translated_result = translate_feasibility_report(
            report_markdown=analysis.report_markdown,
            raw_evidence=original_evidence,
            target_language=language,
        )
    except ReportTranslationError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    # ========================================================
    # Save translation
    # ========================================================
    try:
        translated_evidence = translated_result["raw_evidence"]

        translation = ReportTranslation(
            report_id=analysis.id,
            language=report_language,
            content=translated_result["report_markdown"],
            population_payload=translated_evidence.get("population"),
            competitor_payload=translated_evidence.get("competitors"),
            market_price_payload=translated_evidence.get("market_price"),
            supply_chain_payload=translated_evidence.get("supply_chain"),
            transportation_payload=translated_evidence.get("transportation"),
            seasonality_payload=translated_evidence.get("seasonality"),
        )

        db.add(translation)
        await db.commit()
        await db.refresh(translation)

    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save translation: {exc}",
        )

    # ========================================================
    # Response
    # ========================================================
    return ReportTranslationResponse(
        status="success",
        analysis_id=analysis.id,
        language=language,
        report_markdown=translation.content or "",
        raw_evidence=translated_evidence,
    )
