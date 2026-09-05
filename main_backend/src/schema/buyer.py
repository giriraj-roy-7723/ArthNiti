from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String

from src.config.database import Base


class Buyer(Base):
    __tablename__ = "Buyers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    user_id = Column(
        String,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
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
