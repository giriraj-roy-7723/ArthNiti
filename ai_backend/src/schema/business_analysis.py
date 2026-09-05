# src/models/feasibility_analysis.py

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from src.config.database import Base


class BusinessAnalysis(Base):
    __tablename__ = "business_analysis"

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

    # Version of the planner execution for this business
    version = Column(
        Integer,
        nullable=False,
    )

    # Analysis inputs
    radius_km = Column(
        Float,
        nullable=False,
    )

    latitude = Column(
        Float,
        nullable=True,
    )

    longitude = Column(
        Float,
        nullable=True,
    )

    # Original Gemini-generated report
    report_markdown = Column(
        Text,
        nullable=False,
    )

    # Evidence supplied to Gemini
    population_payload = Column(
        JSONB,
        nullable=True,
    )

    competitor_payload = Column(
        JSONB,
        nullable=True,
    )

    market_price_payload = Column(
        JSONB,
        nullable=True,
    )

    supply_chain_payload = Column(
        JSONB,
        nullable=True,
    )

    transportation_payload = Column(
        JSONB,
        nullable=True,
    )
    
    seasonality_payload = Column(
        JSONB,
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
            name="uq_business_analysis_version",
        ),
    )