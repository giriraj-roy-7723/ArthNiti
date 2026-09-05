from sqlalchemy import Column, String, DateTime, Enum
from src.config.database import Base
from datetime import datetime, timezone
import enum
import random
from sqlalchemy import select


async def generate_unique_username(first_name: str, db) -> str:
    base = "".join(first_name.split()).lower()

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

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)

    password = Column(String, nullable=False)

    profile_pic = Column(String, nullable=True)

    role = Column(Enum(UserRole), default=UserRole.user,nullable=False)

    address = Column(String, nullable=False)
    village = Column(String, nullable=False)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))