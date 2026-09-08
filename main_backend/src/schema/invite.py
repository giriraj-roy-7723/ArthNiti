from sqlalchemy import Column, String, Boolean, DateTime
from src.config.database import Base
import uuid


class Invite(Base):
    __tablename__ = "invites"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    email = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False, index=True)
    
    created_by = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    used = Column(Boolean, default=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
