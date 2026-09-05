from typing import Any, Literal

from pydantic import BaseModel


class ReportTranslationRequest(BaseModel):
    language: Literal["english", "hindi", "bengali"]


class ReportTranslationResponse(BaseModel):
    status: str
    analysis_id: str
    language: str
    report_markdown: str
    raw_evidence: dict[str, Any]
