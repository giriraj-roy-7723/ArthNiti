import json
import requests
from typing import Any
from google.genai import types

from src.config.config import GEMINI_MODEL_NAME, OVERPASS_URL, HEADERS
from src.utils.ai_utils import get_gemini_client
from src.utils.geo_utils import (
    get_coordinates,
    get_road_distance_km,
    haversine_distance_km,
)


def get_supply_chain_profile(business_type: str) -> dict[str, Any]:
    client = get_gemini_client()
    prompt = f"""
    You are an expert in rural/semi-urban supply chain networks.
    Analyze the business type: "{business_type}".
    Define exactly 3 to 4 critical supply chain pillars (e.g., raw materials, specialist services, marketplace, logistics).

    Return a strictly valid JSON object:
    {{
      "pillars": [
        {{
          "id": "raw_materials",
          "label": "Raw Materials & Inputs",
          "weight": 0.35,
          "ideal_km": 5.0,
          "cutoff_km": 25.0,
          "osm_queries": ["nwr['shop'~'agrarian|fertilizer']", "nwr['commercial'='agricultural']"]
        }}
      ]
    }}
    Weights must sum to 1.0. Use realistic Overpass QL tag clauses inside `osm_queries`.
    """

    resp = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", temperature=0.1
        ),
    )
    return json.loads(resp.text)


def calculate_score(dist_km: float, ideal_km: float, cutoff_km: float) -> int:
    if dist_km <= ideal_km:
        return int(100 - (dist_km / ideal_km) * 10)
    elif dist_km >= cutoff_km:
        return 10
    decay = (dist_km - ideal_km) / (cutoff_km - ideal_km)
    return max(10, int(90 - decay * 80))


def evaluate_supply_chain(
    location_name: str, business_type: str
) -> dict[str, Any]:
    lat, lon = get_coordinates(location_name)
    profile = get_supply_chain_profile(business_type)
    radius_meters = 25000

    results = {}
    weighted_sum = 0.0

    for pillar in profile.get("pillars", []):
        pid, label, weight = pillar["id"], pillar["label"], pillar["weight"]
        ideal_km = pillar.get("ideal_km", 5.0)
        cutoff_km = pillar.get("cutoff_km", 25.0)

        clause_str = "\n".join(
            f"  {q}(around:{radius_meters},{lat},{lon});" for q in pillar["osm_queries"]
        )
        overpass_q = f"[out:json][timeout:25];\n(\n{clause_str}\n);\nout center 15;"

        elements = []
        try:
            res = requests.post(
                OVERPASS_URL, data={"data": overpass_q}, headers=HEADERS, timeout=30
            )
            if res.status_code == 200:
                elements = res.json().get("elements", [])
        except Exception:
            pass

        pois = []
        for el in elements:
            p_lat = el.get("lat") or el.get("center", {}).get("lat")
            p_lon = el.get("lon") or el.get("center", {}).get("lon")
            if not p_lat or not p_lon:
                continue
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("operator") or f"Local {label} Facility"
            pois.append({"name": name, "lat": p_lat, "lon": p_lon})

        if pois:
            nearest = min(
                pois, key=lambda p: haversine_distance_km(lat, lon, p["lat"], p["lon"])
            )
            dist_km = get_road_distance_km(lat, lon, nearest["lat"], nearest["lon"])
            score = calculate_score(dist_km, ideal_km, cutoff_km)
            results[pid] = {
                "pillar": label,
                "status": "Found",
                "nearest_name": nearest["name"],
                "distance_km": dist_km,
                "score": score,
            }
        else:
            score = 15
            results[pid] = {
                "pillar": label,
                "status": "Unmapped / Not Found within 25km",
                "nearest_name": None,
                "distance_km": None,
                "score": score,
            }

        weighted_sum += score * weight

    return {
        "location": location_name,
        "coordinates": {"latitude": lat, "longitude": lon},
        "business_type": business_type,
        "pillars": results,
        "overall_supply_chain_score": round(weighted_sum, 1),
    }
