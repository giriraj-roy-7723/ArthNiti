from pydantic import BaseModel
from typing import Optional


class MarketReachRequest(BaseModel):
    location: str
    radius_km: float = 3.28
    year: int = 2025


class MarketReachResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    radius_km: float
    country: str
    country_code: str
    country_code_iso3: str
    population: int
    area_km2: float
    population_density: float
    data_year: int
    population_data_source: str
    average_household_size: float
    estimated_households: int
    household_estimation_method: str
    household_data_source: str
