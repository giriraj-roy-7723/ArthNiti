from sqlalchemy import Column, String, DateTime, ForeignKey,Enum
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

    designation = Column(String, nullable=False)
    
    agency_type = Column(Enum(RoleType), nullable=False)  # sca / ca
    agency_name = Column(String, nullable=False)

    agency_address = Column(String, nullable=True)

    agency_city = Column(String, nullable=True)
    agency_state = Column(String, nullable=True)
    agency_country = Column(String, nullable=True)
    agency_pincode = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
