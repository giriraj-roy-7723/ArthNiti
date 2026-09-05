# from pydantic import BaseModel, Field


# class EligibilityProfileRequest(BaseModel):
#     ownership_type: str | None = None
#     gender: str | None = None
#     age: int | None = Field(default=None, ge=18, le=100)
#     social_category: str | None = None
#     annual_income: float | None = Field(default=None, ge=0)
#     annual_turnover: float | None = Field(default=None, ge=0)
#     investment_amount: float | None = Field(default=None, ge=0)
#     business_registration: bool | None = None
#     farmer_status: bool | None = None
#     land_ownership: bool | None = None


# class BusinessProfileResponse(BaseModel):
#     business_id: str
#     analysis_id: str
#     business_profile: dict
#     eligibility_profile: dict
#     embedding_text: str | None = None


from pydantic import BaseModel, Field
from typing import Any


class EligibilityProfileRequest(BaseModel):
    ownership_type: str | None = None
    gender: str | None = None
    age: int | None = Field(default=None, ge=18, le=100)
    social_category: str | None = None
    annual_income: float | None = Field(default=None, ge=0)
    annual_turnover: float | None = Field(default=None, ge=0)
    investment_amount: float | None = Field(default=None, ge=0)
    business_registration: bool | None = None
    farmer_status: bool | None = None
    land_ownership: bool | None = None


class CombinedRecommendationResponse(BaseModel):
    business_id: str
    analysis_id: str
    business_profile: dict[str, Any]
    eligibility_profile: dict[str, Any]
    target_language: str
    original_english_schemes: list[dict[str, Any]]
    translated_schemes: list[dict[str, Any]] | None = None