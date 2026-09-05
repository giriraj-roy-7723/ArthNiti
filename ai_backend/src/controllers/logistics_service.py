import json
import requests
from typing import Any
from google.genai import types

from src.config.config import GEMINI_MODEL_NAME, OVERPASS_URL, HEADERS
from src.utils.ai_utils import get_gemini_client
from src.utils.geo_utils import (
    get_coordinates,
    normalize_coordinates,
    get_dynamic_road_metrics,
    haversine_distance_km,
)

from src.services.supply_chain_service import get_supply_chain_profile


def discover_nodes_for_logistics(
    lat: float, lon: float, profile: dict[str, Any], radius_meters: int = 30000
) -> dict[str, Any]:
    """
    Local discovery function for logistics.
    Retrieves the raw coordinates needed to calculate road freight metrics.
    """
    discovered = {}

    for pillar in profile.get("pillars", []):
        pid = pillar.get("id", "unknown")
        label = pillar.get("label", "Facility")

        clause_str = "\n".join(
            f"  {q}(around:{radius_meters},{lat},{lon});"
            for q in pillar.get("osm_queries", [])
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
            name = tags.get("name") or tags.get("operator") or f"Regional {label} Hub"
            pois.append({"name": name, "lat": float(p_lat), "lon": float(p_lon)})

        if pois:
            nearest = min(
                pois, key=lambda p: haversine_distance_km(lat, lon, p["lat"], p["lon"])
            )
            discovered[pid] = {
                "pillar_label": label,
                "status": "Found",
                "name": nearest["name"],
                "coordinates": {"lat": nearest["lat"], "lon": nearest["lon"]},
            }
        else:
            discovered[pid] = {
                "pillar_label": label,
                "status": "Unmapped",
                "name": f"Estimated {label} Node",
                "coordinates": {
                    "lat": lat + 0.05,
                    "lon": lon + 0.05,
                },  # Fallback estimation
            }

    return discovered


def generate_dynamic_freight_parameters(
    business_type: str,
    origin_name: str,
    destinations: dict[str, dict[str, Any]],
    orig_lat: float,
    orig_lon: float,
) -> dict[str, Any]:
    client = get_gemini_client()
    summary = {}

    for key, destination in destinations.items():
        dest_lat, dest_lon = normalize_coordinates(destination["coordinates"])
        distance_km = (
            destination.get("straight_distance_km")
            or get_dynamic_road_metrics(orig_lat, orig_lon, dest_lat, dest_lon)[
                "straight_line_km"
            ]
        )
        summary[key] = {
            "facility_name": destination.get("name", "Unknown Facility"),
            "distance_km": distance_km,
        }

    prompt = f"""You are a commercial freight cost estimator for rural and peri-urban India.
Business Type: "{business_type}"
Origin: "{origin_name}"
Target Facilities: {json.dumps(summary, ensure_ascii=False)}
For each node key return: recommended_vehicle, payload_capacity_kg, base_fare_inr, base_km, rate_per_km_inr, round_trip_multiplier, monthly_trips, handling_notes.
Return ONLY JSON:
{{ "freight_specifications": {{ "<node_key>": {{ "recommended_vehicle": "Tata Ace", "payload_capacity_kg": 1000, "base_fare_inr": 200.0, "base_km": 4.0, "rate_per_km_inr": 24.0, "round_trip_multiplier": 1.8, "monthly_trips": 4, "handling_notes": "Bulk bags / crates" }} }} }}"""

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", temperature=0.1
        ),
    )
    return json.loads(response.text).get("freight_specifications", {})


def compute_trip_cost(distance_km: float, spec: dict[str, Any]) -> dict[str, float]:
    base_fare = float(spec.get("base_fare_inr", 180.0))
    base_km = float(spec.get("base_km", 4.0))
    rate_km = float(spec.get("rate_per_km_inr", 22.0))
    round_trip_multiplier = float(spec.get("round_trip_multiplier", 1.8))

    one_way = (
        base_fare
        if distance_km <= base_km
        else base_fare + (distance_km - base_km) * rate_km
    )

    return {
        "one_way_inr": round(one_way, 2),
        "round_trip_inr": round(one_way * round_trip_multiplier, 2),
    }


def run_supply_chain_and_transportation_analysis(
    business_type: str,
    origin_location: str,
    search_radius_meters: int = 30000,
) -> dict[str, Any]:

    # 1. Resolve origin coordinates
    orig_lat, orig_lon = get_coordinates(origin_location)

    # 2. Get profile from untouched supply chain file
    profile = get_supply_chain_profile(business_type)

    # 3. Discover nodes locally to get coordinates
    discovered_nodes = discover_nodes_for_logistics(
        lat=orig_lat, lon=orig_lon, profile=profile, radius_meters=search_radius_meters
    )

    # 4. Request dynamic freight costs
    freight_specs = generate_dynamic_freight_parameters(
        business_type, origin_location, discovered_nodes, orig_lat, orig_lon
    )

    logistics_report = {}
    total_monthly_transport_opex = 0.0

    # 5. Compile route metrics and fares
    for node_key, node_data in discovered_nodes.items():
        dest_lat, dest_lon = normalize_coordinates(node_data.get("coordinates"))
        route_metrics = get_dynamic_road_metrics(orig_lat, orig_lon, dest_lat, dest_lon)
        road_km = route_metrics["road_distance_km"]

        spec = freight_specs.get(
            node_key,
            {
                "recommended_vehicle": "Mini Commercial Truck",
                "payload_capacity_kg": 1000,
                "base_fare_inr": 200.0,
                "base_km": 4.0,
                "rate_per_km_inr": 24.0,
                "round_trip_multiplier": 1.8,
                "monthly_trips": 4,
                "handling_notes": "General freight",
            },
        )

        fares = compute_trip_cost(road_km, spec)
        monthly_trips = int(spec.get("monthly_trips", 4))
        monthly_cost = round(fares["round_trip_inr"] * monthly_trips, 2)
        total_monthly_transport_opex += monthly_cost

        logistics_report[node_key] = {
            "pillar_label": node_data.get("pillar_label"),
            "status": node_data.get("status"),
            "destination_facility": node_data.get("name", "Unknown Facility"),
            "destination_coordinates": {"lat": dest_lat, "lon": dest_lon},
            "route_metrics": route_metrics,
            "vehicle_specification": spec,
            "freight_rates": {
                "one_way_fare_inr": fares["one_way_inr"],
                "round_trip_fare_inr": fares["round_trip_inr"],
            },
            "dispatch_schedule": {
                "estimated_monthly_trips": monthly_trips,
                "estimated_monthly_cost_inr": monthly_cost,
            },
        }

    return {
        "business_type": business_type,
        "origin": {
            "name": origin_location,
            "coordinates": {"lat": orig_lat, "lon": orig_lon},
        },
        "discovered_supply_chain_nodes": discovered_nodes,
        "transportation_logistics_opex": logistics_report,
        "summary": {
            "active_routes_modeled": len(logistics_report),
            "total_monthly_freight_opex_inr": round(total_monthly_transport_opex, 2),
        },
    }
