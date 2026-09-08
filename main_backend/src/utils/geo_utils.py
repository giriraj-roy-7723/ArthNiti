import requests
from src.config.config import NOMINATIM_URL, HEADERS


def get_coordinates(location_name: str) -> tuple[float, float]:
    """Geocode an address string to (latitude, longitude)."""
    params = {"q": location_name, "format": "json", "limit": 1}
    res = requests.get(
        f"{NOMINATIM_URL}/search", params=params, headers=HEADERS, timeout=30
    )
    res.raise_for_status()
    data = res.json()
    if not data:
        raise ValueError(f"Could not geocode location: '{location_name}'")
    return float(data[0]["lat"]), float(data[0]["lon"])
