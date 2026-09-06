from fastapi import APIRouter, HTTPException, Depends

from src.models.finance import FinancialPlanRequest

from src.middlewares.role import require_enterpreneur
from src.schema.enterpreneur import Enterpreneur

from src.controllers.finance_service import (
    generate_ai_analysis,
    generate_financial_plan,
)

router = APIRouter()


@router.post("/analyze-plan")
def analyze_plan(
    request: FinancialPlanRequest,
    enterpreneur: Enterpreneur = Depends(require_enterpreneur),
):
    try:
        plan_result = generate_financial_plan(
            margin=request.margin,
            monthly_revenue=request.monthly_revenue,
            monthly_direct_costs=request.monthly_direct_costs,
            monthly_fixed_costs=request.monthly_fixed_costs,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    ai_commentary = generate_ai_analysis(plan_result, request.language)

    return {
        "raw_financial_plan": plan_result,
        "ai_analysis": ai_commentary,
        "analysis_language": request.language,
    }
