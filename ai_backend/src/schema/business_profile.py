import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from src.config.database import Base


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    business_id = Column(
        String,
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    analysis_id = Column(
        String,
        ForeignKey("business_analysis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    business_profile = Column(
        JSONB,
        nullable=False,
    )

    eligibility_profile = Column(
        JSONB,
        nullable=False,
    )

    embedding_text = Column(
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
