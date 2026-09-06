import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Index
from pgvector.sqlalchemy import Vector

from src.config.database import Base


class BusinessReportChunk(Base):
    __tablename__ = "business_report_chunks"

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
        ForeignKey("business_analysis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version = Column(
        Integer,
        nullable=False,
        index=True,
    )

    section_number = Column(
        Integer,
        nullable=False,
    )

    section_title = Column(
        String(500),
        nullable=False,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    embedding_text = Column(
        Text,
        nullable=False,
    )

    embedding = Column(
        Vector(384),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_business_report_chunks_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
