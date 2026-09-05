import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String, Text

from src.config.database import Base


class BusinessStatus(str, enum.Enum):
    pending="pending"
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

    business_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    village = Column(String, nullable=True)
    district = Column(String, nullable=False)
    city = Column(String, nullable=True)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
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
