from pathlib import Path
import requests

# App Settings
GEMINI_MODEL_NAME = "gemini-3.5-flash-lite"
DATA_MAX_AGE_DAYS = 30
HEADERS = {
    "User-Agent": "FastAPI-Backend/1.0",
    "Accept": "application/json",
}

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_CACHE_DIR = BASE_DIR / "data_cache"
HOUSEHOLD_FILE = DATA_CACHE_DIR / "un_household_2026.xlsx"
COMPETETOR_CACHE_FILE_PATH = DATA_CACHE_DIR / "gemini_taxonomy_cache.json"

# URLs
NOMINATIM_URL = "https://nominatim.openstreetmap.org"
WORLDPOP_API_URL = "https://api.worldpop.org/v2"
HOUSEHOLD_DOWNLOAD_URL = (
    "https://population.un.org/household/assets/UNDESA_PD_2026_hh-size-composition.xlsx"
)
AGMARKNET_BASE_URL = "https://api.agmarknet.gov.in/v1"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OSRM_URL = "http://router.project-osrm.org/route/v1/driving"
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# Sessions
AGMARKNET_SESSION = requests.Session()
AGMARKNET_SESSION.headers.update(
    {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://agmarknet.gov.in",
        "Referer": "https://agmarknet.gov.in/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    }
)


# Add to existing config.py
PRICE_CACHE_DIR = DATA_CACHE_DIR / "market_price_data"
PRICE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_MAX_AGE_SECONDS = 24 * 60 * 60

DEFAULT_INDIAN_STATES = {
    "andaman and nicobar": 1,
    "andhra pradesh": 2,
    "arunachal pradesh": 3,
    "assam": 4,
    "bihar": 5,
    "chandigarh": 6,
    "chhattisgarh": 7,
    "dadra and nagar haveli": 8,
    "daman and diu": 9,
    "delhi": 10,
    "goa": 11,
    "gujarat": 12,
    "haryana": 13,
    "himachal pradesh": 14,
    "jammu and kashmir": 15,
    "jharkhand": 16,
    "karnataka": 17,
    "kerala": 18,
    "ladakh": 38,
    "lakshadweep": 19,
    "madhya pradesh": 20,
    "maharashtra": 21,
    "manipur": 22,
    "meghalaya": 23,
    "mizoram": 24,
    "nagaland": 25,
    "odisha": 26,
    "puducherry": 27,
    "punjab": 28,
    "rajasthan": 29,
    "sikkim": 30,
    "tamil nadu": 31,
    "telangana": 37,
    "tripura": 32,
    "uttar pradesh": 34,
    "uttarakhand": 33,
    "west bengal": 36,
}

# Add to existing configurations
MONTH_NAMES = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]