# src/models/financial_analysis.py

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Text
)
from sqlalchemy.dialects.postgresql import JSONB

from src.config.database import Base


class FinancialAnalysis(Base):
    __tablename__ = "financial_analysis"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    business_id = Column(
        String,
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    business_analysis_id = Column(
        String,
        ForeignKey("business_analysis.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    version = Column(
        Integer,
        nullable=False,
    )

    # Original entrepreneur inputs
    input_payload = Column(
        JSONB,
        nullable=False,
    )

    # Gemini validation + low/expected/high estimation
    estimation_payload = Column(
        JSONB,
        nullable=False,
    )

    # Deterministic Python financial calculations
    financial_plan_payload = Column(
        JSONB,
        nullable=False,
    )

    # Canonical AI-generated analysis — always English
    ai_analysis = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "business_id",
            "version",
            name="uq_financial_analysis_version",
        ),
    )
