import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)

from src.config.database import Base


class FinancialAnalysisTranslation(Base):
    __tablename__ = "financial_analysis_translations"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    financial_analysis_id = Column(
        String,
        ForeignKey("financial_analysis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language = Column(
        String(50),
        nullable=False,
    )

    ai_analysis = Column(
        Text,
        nullable=False,
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
            "financial_analysis_id",
            "language",
            name="uq_financial_analysis_translation_language",
        ),
    )
