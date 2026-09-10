import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from src.config.database import Base


class BusinessStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    closed = "closed"


class Business(Base):
    __tablename__ = "businesses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    owner_id = Column(
        String,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Multilingual fields
    business_name = Column(JSONB, nullable=False, default=dict)
    category = Column(JSONB, nullable=False, default=dict)
    description = Column(JSONB, nullable=True, default=dict)

    village = Column(JSONB, nullable=True, default=dict)
    district = Column(JSONB, nullable=False, default=dict)
    city = Column(JSONB, nullable=True, default=dict)
    state = Column(JSONB, nullable=False, default=dict)
    country = Column(JSONB, nullable=False, default=dict)
    image_urls = Column(JSONB, nullable=True)

    # Numeric/System fields (not translated)
    margin_capital = Column(Float, nullable=False)
    pincode = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    status = Column(
        Enum(BusinessStatus),
        default=BusinessStatus.pending,
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
