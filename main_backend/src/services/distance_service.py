import math
import asyncio
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from src.schema.user import User

from src.utils.geo_utils import get_coordinates


def calculate_haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Calculates great-circle distance between two points in kilometers."""
    radius = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def _extract_address_field(field_val: dict | str | None) -> str:
    """Safely extract address part from JSONB dictionary or string."""
    if isinstance(field_val, dict):
        return field_val.get("en") or next(iter(field_val.values()), "")
    return str(field_val) if field_val else ""


async def ensure_user_coordinates(
    user_id: str,
    db: AsyncSession,
) -> tuple[float, float]:
    """Fetches user coordinates.

    If missing, geocodes from address and persists them to DB.
    """
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.latitude is not None and user.longitude is not None:
        return user.latitude, user.longitude

    # Construct address query for geocoder
    parts = [
        _extract_address_field(user.city),
        _extract_address_field(user.district),
        _extract_address_field(user.state),
        _extract_address_field(user.country),
    ]
    location_str = ", ".join(p.strip() for p in parts if p and p.strip())

    if not location_str:
        raise HTTPException(
            status_code=400,
            detail="User address is insufficient to determine coordinates for sorting.",
        )

    try:
        latitude, longitude = await asyncio.to_thread(get_coordinates, location_str)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to geocode user location: {str(exc)}",
        ) from exc

    user.latitude = latitude
    user.longitude = longitude
    await db.commit()
    await db.refresh(user)

    return latitude, longitude
