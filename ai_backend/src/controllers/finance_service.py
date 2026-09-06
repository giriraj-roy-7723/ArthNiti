import os
import json
from google import genai
from google.genai import types
from src.models.finance import SCHEMES
from src.config.config import GEMINI_MODEL_NAME
from src.utils.ai_utils import get_gemini_client

# Initialize the Gemini Client
client = get_gemini_client()


def calculate_project_finance(margin: float):
    if margin <= 0:
        raise ValueError("Margin capital must be greater than zero.")
    project_cost = margin / 0.10
    loan_amount = project_cost * 0.90
    return {
        "margin": round(margin, 2),
        "project_cost": round(project_cost, 2),
        "loan_amount": round(loan_amount, 2),
    }


def select_scheme(project_cost: float):
    if project_cost <= SCHEMES["micro_finance"].max_project_cost:
        return SCHEMES["micro_finance"]
    if project_cost <= SCHEMES["term_loan"].max_project_cost:
        return SCHEMES["term_loan"]
    return None


def calculate_emi(principal: float, annual_rate: float, tenure_years: int):
    monthly_rate = annual_rate / 100 / 12
    months = tenure_years * 12
    if monthly_rate == 0:
        return principal / months
    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** months
        / ((1 + monthly_rate) ** months - 1)
    )
    return round(emi, 2)


def calculate_break_even(fixed_costs: float, contribution_margin: float):
    if contribution_margin <= 0:
        raise ValueError("Contribution margin must be greater than zero.")
    return round(fixed_costs / contribution_margin, 2)


def calculate_dscr(
    monthly_revenue: float,
    monthly_operating_expenses: float,
    monthly_debt_payment: float,
):
    if monthly_debt_payment <= 0:
        return None
    cash_available = monthly_revenue - monthly_operating_expenses
    return round(cash_available / monthly_debt_payment, 2)


def classify_dscr(dscr: float | None):
    if dscr is None:
        return "No Debt"
    if dscr >= 1.5:
        return "Strong"
    if dscr >= 1.25:
        return "Moderate"
    if dscr >= 1.0:
        return "Risky"
    return "Unsustainable"


def calculate_profit(revenue: float, direct_costs: float, operating_expenses: float):
    gross_profit = revenue - direct_costs
    net_profit = gross_profit - operating_expenses
    profit_margin = (net_profit / revenue) * 100 if revenue > 0 else 0
    return {
        "gross_profit": round(gross_profit, 2),
        "net_profit": round(net_profit, 2),
        "profit_margin": round(profit_margin, 2),
    }


def calculate_working_capital(monthly_operating_cost: float, months_required: int = 2):
    return round(monthly_operating_cost * months_required, 2)


def generate_scenario(
    revenue: float,
    expenses: float,
    emi: float,
    revenue_change: float = 0,
    expense_change: float = 0,
):
    scenario_revenue = revenue * (1 + revenue_change)
    scenario_expenses = expenses * (1 + expense_change)
    operating_surplus = scenario_revenue - scenario_expenses
    dscr = operating_surplus / emi if emi > 0 else None
    return {
        "revenue": round(scenario_revenue, 2),
        "expenses": round(scenario_expenses, 2),
        "operating_surplus": round(operating_surplus, 2),
        "dscr": round(dscr, 2) if dscr is not None else None,
        "risk": classify_dscr(dscr),
    }


def generate_financial_plan(
    margin: float,
    monthly_revenue: float,
    monthly_direct_costs: float,
    monthly_fixed_costs: float,
):
    finance = calculate_project_finance(margin)
    scheme = select_scheme(finance["project_cost"])

    if scheme is None:
        return {
            "status": "NOT_ELIGIBLE",
            "reason": "Calculated project cost exceeds supported scheme limits.",
            "finance": finance,
        }

    loan = min(finance["loan_amount"], scheme.max_loan)
    emi = calculate_emi(loan, scheme.interest_rate, scheme.tenure_years)
    profit = calculate_profit(
        monthly_revenue, monthly_direct_costs, monthly_fixed_costs
    )

    total_monthly_expenses = monthly_direct_costs + monthly_fixed_costs
    dscr = calculate_dscr(monthly_revenue, total_monthly_expenses, emi)

    contribution = (
        (monthly_revenue - monthly_direct_costs) / monthly_revenue
        if monthly_revenue > 0
        else 0
    )
    break_even = (
        calculate_break_even(monthly_fixed_costs, contribution)
        if contribution > 0
        else None
    )
    working_capital = calculate_working_capital(
        total_monthly_expenses, months_required=2
    )

    scenarios = {
        "best": generate_scenario(
            monthly_revenue,
            total_monthly_expenses,
            emi,
            revenue_change=0.20,
            expense_change=-0.05,
        ),
        "expected": generate_scenario(monthly_revenue, total_monthly_expenses, emi),
        "worst": generate_scenario(
            monthly_revenue,
            total_monthly_expenses,
            emi,
            revenue_change=-0.20,
            expense_change=0.15,
        ),
    }

    return {
        "status": "OK",
        "financing": {**finance, "actual_loan": round(loan, 2)},
        "scheme": {
            "name": scheme.name,
            "interest_rate": scheme.interest_rate,
            "tenure_years": scheme.tenure_years,
            "moratorium_months": scheme.moratorium_months,
        },
        "loan": {"emi": emi, "total_months": scheme.tenure_years * 12},
        "business": {
            "monthly_revenue": monthly_revenue,
            "monthly_expenses": total_monthly_expenses,
            **profit,
            "break_even_revenue": break_even,
        },
        "debt_capacity": {"dscr": dscr, "assessment": classify_dscr(dscr)},
        "working_capital": {"recommended": working_capital, "months": 2},
        "scenarios": scenarios,
    }


def generate_ai_analysis(plan_result: dict, language: str) -> str:
    prompt = (
        f"You are an expert commercial credit analyst. Review the following financial plan output. "
        f"Identify its strong points (positives) and its vulnerabilities (negatives) focusing on Debt Service Coverage Ratio (DSCR), "
        f"profit margins, break-even point, and the worst-case scenario.\n\n"
        f"CRITICAL INSTRUCTION: You MUST write your entire analysis exclusively in the following language: {language}.\n\n"
        f"Financial Plan Data:\n{json.dumps(plan_result, indent=2)}"
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.4),
        )
        return response.text
    except Exception as e:
        return f"AI analysis failed to generate: {str(e)}"
