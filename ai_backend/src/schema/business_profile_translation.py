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
from sqlalchemy.dialects.postgresql import JSONB

from src.config.database import Base


class BusinessProfileTranslation(Base):
    __tablename__ = "business_profile_translations"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    business_profile_id = Column(
        String,
        ForeignKey("business_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language = Column(
        String(50),
        nullable=False,
    )

    business_profile = Column(
        JSONB,
        nullable=True,
    )

    recommended_schemes = Column(
        JSONB,
        nullable=True,
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

    __table_args__ = (
        UniqueConstraint(
            "business_profile_id",
            "language",
            name="uq_business_profile_translation_language",
        ),
    )
