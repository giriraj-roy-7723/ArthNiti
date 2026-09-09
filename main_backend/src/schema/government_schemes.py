# src/schema/government_scheme.py

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text , Column
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    scheme_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    scheme_url = Column(String, nullable=True)

    slug: Mapped[str | None] = mapped_column(
        String(500),
        unique=True,
        index=True,
    )

    details: Mapped[str | None] = mapped_column(Text)

    benefits: Mapped[str | None] = mapped_column(Text)

    eligibility: Mapped[str | None] = mapped_column(Text)

    application: Mapped[str | None] = mapped_column(Text)

    documents: Mapped[str | None] = mapped_column(Text)

    level: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
    )

    scheme_category: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
    )

    tags: Mapped[str | None] = mapped_column(Text)

    # Text that was actually sent to the embedding model
    embedding_text: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
