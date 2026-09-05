from typing import Any, Literal
from pydantic import BaseModel, Field


# class ReportRequest(BaseModel):
#     location: str
#     business_type: str
#     margin_capital: float
#     radius_km: float = 10.0


# class ReportResponse(BaseModel):
#     status: str
#     report_markdown: str
#     raw_evidence: dict[str, Any]

# # src/models/report.py


class ReportRequest(BaseModel):
    business_name: str
    business_type: str
    business_description: str | None = None

    country: str
    state: str
    district: str
    city: str | None = None
    village: str | None = None
    pincode: str | None = None

    margin_capital: float = Field(
        ...,
        ge=0,
        description="Available capital for the business",
    )

    radius_km: float = Field(
        default=10.0,
        gt=0,
    )

    language: Literal[
        "english",
        "hindi",
        "bengali",
    ] = "english"


class ReportResponse(BaseModel):
    status: str
    report: dict[str, Any]
    analysis_id: str
    version: int
    language: str
    report_markdown: str
    raw_evidence: dict
