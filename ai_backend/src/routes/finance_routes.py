from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.models.finance import FinancialPlanRequest
from src.middlewares.role import require_enterpreneur
from src.schema.enterpreneur import Enterpreneur
from src.schema.financial_analysis import FinancialAnalysis
from src.schema.finance_translation import FinancialAnalysisTranslation

from src.controllers.finance_service import (
    create_financial_translation,
    generate_ai_analysis,
    generate_financial_plan,
    get_existing_financial_translation,
    normalize_language,
)

router = APIRouter()


@router.post("/analyze-plan")
async def analyze_plan(
    request: FinancialPlanRequest,
    language: str = Query(
        "en",
        description="Target language code (e.g. en, hi, bn)",
    ),
    force: bool = Query(False),
    enterpreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    try:
        target_language = normalize_language(language)

        if force:
            analysis_ids_result = await db.execute(
                select(FinancialAnalysis.id).where(
                    FinancialAnalysis.business_id == request.business_id
                )
            )
            analysis_ids = analysis_ids_result.scalars().all()

            if analysis_ids:
                await db.execute(
                    delete(FinancialAnalysisTranslation).where(
                        FinancialAnalysisTranslation.financial_analysis_id.in_(
                            analysis_ids
                        )
                    )
                )
                await db.execute(
                    delete(FinancialAnalysis).where(
                        FinancialAnalysis.id.in_(analysis_ids)
                    )
                )
            await db.flush()

        existing_result = await db.execute(
            select(FinancialAnalysis)
            .where(FinancialAnalysis.business_id == request.business_id)
            .order_by(FinancialAnalysis.version.desc())
            .limit(1)
        )
        existing_analysis = existing_result.scalar_one_or_none()

        if existing_analysis:
            if target_language == "en":
                return {
                    "financial_analysis_id": existing_analysis.id,
                    "version": existing_analysis.version,
                    "language": "en",
                    "raw_financial_plan": existing_analysis.financial_plan_payload,
                    "ai_analysis": existing_analysis.ai_analysis,
                    "translated": False,
                    "cached": True,
                }

            translation = await get_existing_financial_translation(
                db=db,
                financial_analysis_id=existing_analysis.id,
                language=target_language,
            )

            if translation:
                return {
                    "financial_analysis_id": existing_analysis.id,
                    "version": existing_analysis.version,
                    "translation_id": translation.id,
                    "language": target_language,
                    "raw_financial_plan": existing_analysis.financial_plan_payload,
                    "ai_analysis": translation.ai_analysis,
                    "translated": True,
                    "cached": True,
                }

            translation = await create_financial_translation(
                db=db,
                financial_analysis=existing_analysis,
                language=target_language,
            )

            return {
                "financial_analysis_id": existing_analysis.id,
                "version": existing_analysis.version,
                "translation_id": translation.id,
                "language": target_language,
                "raw_financial_plan": existing_analysis.financial_plan_payload,
                "ai_analysis": translation.ai_analysis,
                "translated": True,
                "cached": False,
            }

        # ---------------------------------------------------------
        # 1. Generate financial plan
        # ---------------------------------------------------------
        plan_result = await generate_financial_plan(
            business_id=request.business_id,
            margin=request.margin,
            monthly_revenue=request.monthly_revenue,
            monthly_direct_costs=request.monthly_direct_costs,
            monthly_fixed_costs=request.monthly_fixed_costs,
            db=db,
        )

        # ---------------------------------------------------------
        # 2. Generate canonical English AI analysis
        # ---------------------------------------------------------
        ai_commentary = await generate_ai_analysis(
            plan_result,
        )

        # ---------------------------------------------------------
        # 3. Get next financial analysis version
        # ---------------------------------------------------------
        result = await db.execute(
            select(func.max(FinancialAnalysis.version)).where(
                FinancialAnalysis.business_id == request.business_id
            )
        )

        latest_version = result.scalar() or 0
        next_version = latest_version + 1

        # ---------------------------------------------------------
        # 4. Extract estimation data
        # ---------------------------------------------------------
        estimation_payload = {
            "input_validation": plan_result.get("input_validation"),
            "financial_estimation": plan_result.get("financial_estimation"),
            "used_values": plan_result.get("used_values"),
        }

        # ---------------------------------------------------------
        # 5. Store canonical English financial analysis
        # ---------------------------------------------------------
        financial_analysis = FinancialAnalysis(
            business_id=request.business_id,
            business_analysis_id=plan_result.get("business_analysis_id"),
            version=next_version,
            input_payload={
                "margin_capital": request.margin,
                "monthly_revenue": request.monthly_revenue,
                "monthly_direct_costs": request.monthly_direct_costs,
                "monthly_fixed_costs": request.monthly_fixed_costs,
            },
            estimation_payload=estimation_payload,
            financial_plan_payload=plan_result,
            ai_analysis=ai_commentary,
        )

        db.add(financial_analysis)

        await db.commit()
        await db.refresh(financial_analysis)

        # ---------------------------------------------------------
        # 6. English request
        # ---------------------------------------------------------
        if target_language == "en":
            return {
                "financial_analysis_id": financial_analysis.id,
                "version": financial_analysis.version,
                "language": "en",
                "raw_financial_plan": plan_result,
                "ai_analysis": financial_analysis.ai_analysis,
                "translated": False,
                "cached": False,
            }

        # ---------------------------------------------------------
        # 7. Check whether translation already exists
        # ---------------------------------------------------------
        translation = await get_existing_financial_translation(
            db=db,
            financial_analysis_id=financial_analysis.id,
            language=target_language,
        )

        # ---------------------------------------------------------
        # 8. Return cached translation
        # ---------------------------------------------------------
        if translation:
            return {
                "financial_analysis_id": financial_analysis.id,
                "version": financial_analysis.version,
                "translation_id": translation.id,
                "language": target_language,
                "raw_financial_plan": plan_result,
                "ai_analysis": translation.ai_analysis,
                "translated": True,
                "cached": True,
            }

        # ---------------------------------------------------------
        # 9. Generate and save translation
        # ---------------------------------------------------------
        translation = await create_financial_translation(
            db=db,
            financial_analysis=financial_analysis,
            language=target_language,
        )

        return {
            "financial_analysis_id": financial_analysis.id,
            "version": financial_analysis.version,
            "translation_id": translation.id,
            "language": target_language,
            "raw_financial_plan": plan_result,
            "ai_analysis": translation.ai_analysis,
            "translated": True,
            "cached": False,
        }

    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail=(f"Failed to generate and save financial analysis: {str(e)}"),
        )
