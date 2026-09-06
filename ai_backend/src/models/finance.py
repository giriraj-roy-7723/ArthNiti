from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class Scheme:
    name: str
    interest_rate: float
    tenure_years: int
    moratorium_months: int
    max_project_cost: float
    max_loan: float


SCHEMES = {
    "micro_finance": Scheme(
        name="Micro Finance Scheme",
        interest_rate=6.5,
        tenure_years=3,
        moratorium_months=3,
        max_project_cost=140_000,
        max_loan=125_000,
    ),
    "term_loan": Scheme(
        name="Term Loan Scheme",
        interest_rate=8.0,
        tenure_years=7,
        moratorium_months=6,
        max_project_cost=5_000_000,
        max_loan=4_500_000,
    ),
}


class FinancialPlanRequest(BaseModel):
    margin: float = Field(..., gt=0, description="Initial margin capital")
    monthly_revenue: float = Field(..., ge=0)
    monthly_direct_costs: float = Field(..., ge=0)
    monthly_fixed_costs: float = Field(..., ge=0)
    language: str = Field(
        default="English", description="Language for the AI commentary"
    )
