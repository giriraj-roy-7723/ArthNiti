from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from src.config.database import Base
import uuid
import enum


class RoleType(str, enum.Enum):
    sca = "sca"
    ca = "ca"


class GovernmentOfficial(Base):
    __tablename__ = "government_officials"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    # Multilingual fields
    designation = Column(JSONB, nullable=False, default=dict)
    agency_name = Column(JSONB, nullable=False, default=dict)
    agency_address = Column(JSONB, nullable=True, default=dict)
    agency_city = Column(JSONB, nullable=True, default=dict)
    agency_state = Column(JSONB, nullable=True, default=dict)
    agency_country = Column(JSONB, nullable=True, default=dict)

    # Enum and non-translated fields
    agency_type = Column(Enum(RoleType), nullable=False)  # sca / ca
    agency_pincode = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
