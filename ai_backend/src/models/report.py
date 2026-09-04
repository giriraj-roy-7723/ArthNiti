from pydantic import BaseModel
from typing import Optional, Any


class ReportRequest(BaseModel):
    location: str
    business_type: str
    margin_capital: float
    radius_km: float = 10.0


class ReportResponse(BaseModel):
    status: str
    report_markdown: str
    raw_evidence: dict[str, Any]
