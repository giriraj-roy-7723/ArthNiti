from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.report_service import generate_feasibility_report
from src.controllers.business_report_persistence_service import save_business_analysis
from src.controllers.translator_service import (
    ReportTranslationError,
    translate_feasibility_report,
)
from src.middlewares.role import require_enterpreneur
from src.schema.business import Business, BusinessStatus
from src.schema.business_analysis import BusinessAnalysis
from src.schema.enterpreneur import Enterpreneur
from src.schema.report_translations import ReportLanguage, ReportTranslation
from src.models.report import ReportRequest, ReportResponse

router = APIRouter()


@router.post(
    "/generate",
    response_model=ReportResponse,
)
async def generate_report(
    request: ReportRequest,
    force: bool = False,
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a pending business, generate its feasibility analysis,
    persist the analysis, and return the result.
    """

    business_result = await db.execute(
        select(Business).where(
            Business.id == request.business_id,
            Business.owner_id == entrepreneur.user_id,
        )
    )
    business = business_result.scalar_one_or_none()

    if not business:
        business = Business(
            owner_id=entrepreneur.user_id,
            business_name=request.business_name,
            category=request.business_type,
            margin_capital=request.margin_capital,
            description=request.business_description,
            village=request.village,
            district=request.district,
            city=request.city,
            state=request.state,
            country=request.country,
            pincode=request.pincode,
            latitude=0.0,
            longitude=0.0,
            status=BusinessStatus.pending,
        )
        db.add(business)
        await db.flush()

    if force:
        analysis_ids_result = await db.execute(
            select(BusinessAnalysis.id).where(
                BusinessAnalysis.business_id == business.id
            )
        )
        analysis_ids = analysis_ids_result.scalars().all()

        if analysis_ids:
            await db.execute(
                delete(ReportTranslation).where(
                    ReportTranslation.report_id.in_(analysis_ids)
                )
            )
            await db.execute(
                delete(BusinessAnalysis).where(
                    BusinessAnalysis.id.in_(analysis_ids)
                )
            )
        await db.flush()

    latest_result = await db.execute(
        select(BusinessAnalysis)
        .where(BusinessAnalysis.business_id == business.id)
        .order_by(BusinessAnalysis.version.desc())
        .limit(1)
    )
    existing_analysis = latest_result.scalar_one_or_none()

    if existing_analysis:
        language = request.language.strip().lower()

        original_evidence = {
            "population": existing_analysis.population_payload,
            "competitors": existing_analysis.competitor_payload,
            "market_price": existing_analysis.market_price_payload,
            "supply_chain": existing_analysis.supply_chain_payload,
            "transportation": existing_analysis.transportation_payload,
            "seasonality": existing_analysis.seasonality_payload,
        }

        if language == "english":
            return ReportResponse(
                status="success",
                analysis_id=existing_analysis.id,
                version=existing_analysis.version,
                language="english",
                report_markdown=existing_analysis.report_markdown,
                raw_evidence=original_evidence,
            )

        try:
            report_language = ReportLanguage(language)
        except ValueError:
            raise HTTPException(status_code=400, detail="Unsupported language.")

        translation_result = await db.execute(
            select(ReportTranslation).where(
                ReportTranslation.report_id == existing_analysis.id,
                ReportTranslation.language == report_language,
            )
        )
        existing_translation = translation_result.scalar_one_or_none()

        if existing_translation:
            translated_evidence = {
                "population": existing_translation.population_payload,
                "competitors": existing_translation.competitor_payload,
                "market_price": existing_translation.market_price_payload,
                "supply_chain": existing_translation.supply_chain_payload,
                "transportation": existing_translation.transportation_payload,
                "seasonality": existing_translation.seasonality_payload,
            }
            return ReportResponse(
                status="success",
                analysis_id=existing_analysis.id,
                version=existing_analysis.version,
                language=language,
                report_markdown=existing_translation.content or "",
                raw_evidence=translated_evidence,
            )

        try:
            translated_result = translate_feasibility_report(
                report_markdown=existing_analysis.report_markdown,
                raw_evidence=original_evidence,
                target_language=language,
            )
        except ReportTranslationError as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        translated_evidence = translated_result["raw_evidence"]
        translation = ReportTranslation(
            report_id=existing_analysis.id,
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

        return ReportResponse(
            status="success",
            analysis_id=existing_analysis.id,
            version=existing_analysis.version,
            language=language,
            report_markdown=translation.content,
            raw_evidence=translated_evidence,
        )

    # ========================================================
    # Generate report
    # ========================================================

    try:
        result = generate_feasibility_report(
            business_name=request.business_name,
            business_type=request.business_type,
            business_description=request.business_description,
            country=request.country,
            state=request.state,
            district=request.district,
            city=request.city,
            village=request.village,
            pincode=request.pincode,
            margin_capital=request.margin_capital,
            radius_km=request.radius_km,
            language=request.language,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    # ========================================================
    # Get coordinates from generated population response
    # ========================================================

    latitude = result.get("analysis_latitude")
    longitude = result.get("analysis_longitude")

    if latitude is not None and longitude is not None:
        business.latitude = latitude
        business.longitude = longitude

    # ========================================================
    # Persist analysis
    # ========================================================

    try:
        analysis = await save_business_analysis(
            db=db,
            business_id=business.id,
            result=result,
            radius_km=request.radius_km,
            latitude=latitude,
            longitude=longitude,
        )

        # Business has successfully received an analysis.
        await db.commit()
        await db.refresh(analysis)

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save analysis: {str(e)}",
        )

    # ========================================================
    # Response
    # ========================================================

    return ReportResponse(
        status="success",
        # report=result,
        analysis_id=analysis.id,
        version=analysis.version,
        language=result["language"],
        report_markdown=result["report_markdown"],
        raw_evidence=result["raw_evidence"],
    )
