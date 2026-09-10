from sqlalchemy import Boolean, Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from src.config.database import Base
from datetime import datetime, timezone
import enum
import random
from sqlalchemy import select


async def generate_unique_username(first_name: str, db) -> str:
    # Use English base for username if available, fallback to raw string logic
    base_name = first_name.get("en", "") if isinstance(first_name, dict) else str(first_name)
    base = "".join(base_name.split()).lower()

    while True:
        username = f"{base}{random.randint(10000, 99999)}"

        existing = await db.execute(select(User).where(User.username == username))
        existing = existing.scalar_one_or_none()

        if not existing:
            return username

        
class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    enterpreneur = "enterpreneur"
    buyer = "buyer"
    government = "government"


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)

    # Multilingual fields
    first_name = Column(JSONB, nullable=False, default=dict)
    last_name = Column(JSONB, nullable=False, default=dict)
    
    # System fields
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    email_verified = Column(Boolean, nullable=True, default=None)

    # Multilingual address fields
    address = Column(JSONB, nullable=False, default=dict)
    village = Column(JSONB, nullable=False, default=dict)
    district = Column(JSONB, nullable=False, default=dict)
    city = Column(JSONB, nullable=False, default=dict)
    state = Column(JSONB, nullable=False, default=dict)
    country = Column(JSONB, nullable=False, default=dict)
    
    # Non-translated address field
    pincode = Column(String, nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))