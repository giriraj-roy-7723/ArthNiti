# src/models/report_translation.py

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

from src.config.database import Base


class ReportLanguage(str, enum.Enum):
    english = "english"
    hindi = "hindi"
    bengali = "bengali"


class ReportTranslation(Base):
    __tablename__ = "report_translations"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    report_id = Column(
        String,
        ForeignKey("business_analysis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language = Column(
        Enum(ReportLanguage),
        nullable=False,
    )

    # Translation/generated report
    content = Column(
        Text,
        nullable=True,
    )

    # Translated evicence
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
            "report_id",
            "language",
            name="uq_report_language",
        ),
    )
