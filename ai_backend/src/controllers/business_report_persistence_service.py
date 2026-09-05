from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.business_analysis import BusinessAnalysis
from src.schema.report_translations import (
    ReportLanguage,
    ReportTranslation,
)


async def save_business_analysis(
    db: AsyncSession,
    business_id: str,
    result: dict,
    radius_km: float,
    latitude: float | None,
    longitude: float | None,
) -> BusinessAnalysis:

    # ========================================================
    # Determine next version
    # ========================================================

    last_analysis = await db.execute(
        select(BusinessAnalysis)
        .where(BusinessAnalysis.business_id == business_id)
        .order_by(BusinessAnalysis.version.desc())
    )

    last_analysis = last_analysis.scalar_one_or_none()

    next_version = last_analysis.version + 1 if last_analysis else 1

    # ========================================================
    # Extract evidence
    # ========================================================

    original_evidence = result.get("original_evidence") or result.get(
        "raw_evidence",
        {},
    )

    modules = original_evidence

    # ========================================================
    # Create analysis
    # ========================================================

    analysis = BusinessAnalysis(
        business_id=business_id,
        version=next_version,
        radius_km=radius_km,
        latitude=result.get(
            "analysis_latitude",
            latitude,
        ),
        longitude=result.get(
            "analysis_longitude",
            longitude,
        ),
        # ALWAYS store the original English report
        report_markdown=result.get(
            "original_report_markdown",
            result["report_markdown"],
        ),
        population_payload=modules.get("population"),
        competitor_payload=modules.get("competitors"),
        market_price_payload=modules.get("market_price"),
        supply_chain_payload=modules.get("supply_chain"),
        transportation_payload=modules.get("transportation"),
        seasonality_payload=modules.get("seasonality"),
    )

    db.add(analysis)
    await db.flush()

    # ========================================================
    # Save translation if requested
    # ========================================================

    language = result.get("language", "english")

    if language != "english":
        translated_evidence = result.get("raw_evidence")

        translation = ReportTranslation(
            report_id=analysis.id,
            language=ReportLanguage(language),
            content=result["report_markdown"],
            population_payload=translated_evidence.get("population"),
            competitor_payload=translated_evidence.get("competitors"),
            market_price_payload=translated_evidence.get("market_price"),
            supply_chain_payload=translated_evidence.get("supply_chain"),
            transportation_payload=translated_evidence.get("transportation"),
            seasonality_payload=translated_evidence.get("seasonality"),
            created_at=datetime.now(timezone.utc),
        )

        db.add(translation)

    return analysis
