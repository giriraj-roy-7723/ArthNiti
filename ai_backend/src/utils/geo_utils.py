import math
import requests
from typing import Any
from src.config.config import NOMINATIM_URL, OSRM_URL, HEADERS


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


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return round(2 * r * math.asin(math.sqrt(a)), 2)


def get_road_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    try:
        url = f"{OSRM_URL}/{lon1},{lat1};{lon2},{lat2}?overview=false"
        res = requests.get(url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            routes = res.json().get("routes", [])
            if routes:
                return round(routes[0]["distance"] / 1000.0, 2)
    except Exception:
        pass
    return round(haversine_distance_km(lat1, lon1, lat2, lon2) * 1.25, 2)




def normalize_coordinates(coordinates: Any) -> tuple[float, float]:
    if isinstance(coordinates, dict):
        lat = (
            coordinates.get("lat")
            if coordinates.get("lat") is not None
            else coordinates.get("latitude")
        )
        lon = (
            coordinates.get("lon")
            if coordinates.get("lon") is not None
            else coordinates.get("longitude")
        )
        if lat is None or lon is None:
            raise ValueError(f"Invalid coordinate dictionary: {coordinates}")
        return float(lat), float(lon)
    if isinstance(coordinates, (tuple, list)):
        if len(coordinates) < 2:
            raise ValueError(f"Invalid coordinate tuple/list: {coordinates}")
        return float(coordinates[0]), float(coordinates[1])
    raise TypeError(
        f"Unsupported coordinate type: {type(coordinates).__name__}: {coordinates}"
    )


def get_dynamic_road_metrics(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> dict[str, any]:
    # Ensure you are using the haversine_distance_km function already present in geo_utils
    straight_line_km = haversine_distance_km(lat1, lon1, lat2, lon2)
    try:
        url = f"{OSRM_URL}/{lon1},{lat1};{lon2},{lat2}?overview=false"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            routes = response.json().get("routes", [])
            if routes:
                road_km = round(routes[0]["distance"] / 1000.0, 2)
                duration_min = round(routes[0]["duration"] / 60.0, 1)
                detour = (
                    round(road_km / straight_line_km, 2)
                    if straight_line_km > 0
                    else 1.0
                )
                return {
                    "straight_line_km": straight_line_km,
                    "road_distance_km": road_km,
                    "duration_minutes": duration_min,
                    "detour_factor": detour,
                    "routing_engine": "OSRM Live Network",
                }
    except Exception:
        pass

    # Fallback
    estimated_road_km = round(straight_line_km * 1.30, 2)
    estimated_duration = round((estimated_road_km / 25.0) * 60, 1)
    return {
        "straight_line_km": straight_line_km,
        "road_distance_km": estimated_road_km,
        "duration_minutes": estimated_duration,
        "detour_factor": 1.30,
        "routing_engine": "Haversine Rural Approximation (1.30x)",
    }