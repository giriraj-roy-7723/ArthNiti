import time
from datetime import datetime, timedelta, timezone
import geopandas as gpd
import pandas as pd
import pycountry
import requests
from shapely.geometry import Point

from src.config.config import (
    NOMINATIM_URL,
    WORLDPOP_API_URL,
    HEADERS,
    HOUSEHOLD_FILE,
    HOUSEHOLD_DOWNLOAD_URL,
    DATA_MAX_AGE_DAYS,
)

# ============================================================
# 1. GEOCODING & SPATIAL BUFFER
# ============================================================


def geocode_location(location: str) -> tuple[float, float]:
    """Geocode an address string to (latitude, longitude)."""
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
    }

    response = requests.get(
        f"{NOMINATIM_URL}/search",
        params=params,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(f"Location not found: {location}")

    return float(results[0]["lat"]), float(results[0]["lon"])


def get_country_from_coordinates(
    latitude: float,
    longitude: float,
) -> dict:
    """Reverse geocode coordinates to obtain country name, ISO2, and ISO3 codes."""
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "jsonv2",
        "zoom": 3,
        "addressdetails": 1,
    }

    response = requests.get(
        f"{NOMINATIM_URL}/reverse",
        params=params,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    address = data.get("address", {})
    country = address.get("country")
    iso2 = address.get("country_code", "").upper()

    if not country or not iso2:
        raise RuntimeError(f"Could not resolve country for: {latitude}, {longitude}")

    country_obj = pycountry.countries.get(alpha_2=iso2)

    if country_obj is None:
        raise LookupError(f"Unknown ISO2 country code: {iso2}")

    return {
        "country": country,
        "country_code": iso2,
        "country_code_iso3": country_obj.alpha_3,
    }


def create_radius_geojson(
    latitude: float,
    longitude: float,
    radius_km: float,
) -> dict:
    """Generate a circular polygon buffer in meters via UTM and return GeoJSON geometry."""

    point = gpd.GeoDataFrame(
        geometry=[Point(longitude, latitude)],
        crs="EPSG:4326",
    )

    zone = int((longitude + 180) / 6) + 1
    utm_epsg = (32600 if latitude >= 0 else 32700) + zone

    point_utm = point.to_crs(f"EPSG:{utm_epsg}")

    buffer_utm = point_utm.geometry.iloc[0].buffer(radius_km * 1000)

    buffer_wgs84 = gpd.GeoSeries(
        [buffer_utm],
        crs=f"EPSG:{utm_epsg}",
    ).to_crs("EPSG:4326")

    return buffer_wgs84.iloc[0].__geo_interface__


# ============================================================
# 2. WORLDPOP API INTEGRATION
# ============================================================


def submit_worldpop_task(
    geojson: dict,
    year: int = 2025,
    resolution: str = "100m",
    max_retries: int = 5,
) -> dict:
    """Submit a calculation task to WorldPop."""

    payload = {
        "geojson": geojson,
        "year": year,
        "resolution": resolution,
    }

    url = f"{WORLDPOP_API_URL}/population"
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Submitting WorldPop task (attempt {attempt}/{max_retries})...")

            response = requests.post(
                url,
                json=payload,
                headers=HEADERS,
                timeout=(30, 180),
            )

            print(f"WorldPop HTTP status: {response.status_code}")

            response.raise_for_status()

            data = response.json()

            if "task_id" not in data:
                raise RuntimeError(f"WorldPop returned unexpected response: {data}")

            return data

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as e:
            last_error = e

            print(f"WorldPop connection error: {e}")

            if attempt < max_retries:
                wait = min(2**attempt, 20)
                print(f"Retrying in {wait}s...")
                time.sleep(wait)

        except requests.exceptions.HTTPError as e:
            # HTTP errors generally should not be retried blindly.
            try:
                error_body = response.text
            except Exception:
                error_body = "Unable to read response body."

            raise RuntimeError(
                f"WorldPop HTTP error {response.status_code}: {error_body}"
            ) from e

    raise RuntimeError(
        f"Failed to connect to WorldPop after {max_retries} attempts."
    ) from last_error


def wait_for_worldpop_result(
    task_id: str,
    timeout_seconds: int = 300,
    poll_interval: int = 3,
) -> dict:
    """Poll WorldPop task status until finished."""

    url = f"{WORLDPOP_API_URL}/tasks/{task_id}"
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("WorldPop calculation timed out.")

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as e:
            print(f"Polling connection issue: {e}")
            time.sleep(poll_interval)
            continue

        status = data.get("status")

        print(f"WorldPop status: {status}")

        if status == "success":
            return data.get("result", {})

        if status == "failure":
            raise RuntimeError(f"WorldPop calculation failed: {data}")

        time.sleep(poll_interval)


# ============================================================
# 3. UN HOUSEHOLD DATA HANDLERS
# ============================================================


def download_un_household_data():
    """Download the UN DESA household size Excel sheet."""

    HOUSEHOLD_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Downloading UN household dataset...")

    response = requests.get(
        HOUSEHOLD_DOWNLOAD_URL,
        headers=HEADERS,
        timeout=120,
    )

    response.raise_for_status()

    if not response.content:
        raise RuntimeError("UN household dataset returned empty content.")

    with open(HOUSEHOLD_FILE, "wb") as f:
        f.write(response.content)

    print(f"Dataset saved to: {HOUSEHOLD_FILE}")


def household_data_needs_refresh() -> bool:
    """Check if file exists and is under the max cache age threshold."""

    if not HOUSEHOLD_FILE.exists():
        return True

    modified_time = datetime.fromtimestamp(
        HOUSEHOLD_FILE.stat().st_mtime,
        tz=timezone.utc,
    )

    return (datetime.now(timezone.utc) - modified_time) > timedelta(
        days=DATA_MAX_AGE_DAYS
    )


def load_un_household_data() -> pd.DataFrame:
    """Read the UN Excel file and locate the header row."""

    if household_data_needs_refresh():
        download_un_household_data()
    else:
        modified_time = datetime.fromtimestamp(
            HOUSEHOLD_FILE.stat().st_mtime,
            tz=timezone.utc,
        )

        age_days = (datetime.now(timezone.utc) - modified_time).days

        print(f"Using cached UN dataset ({age_days} days old).")

    sheet = "HH size and composition 2026"

    # --------------------------------------------------------
    # Read the sheet without assuming a header.
    # --------------------------------------------------------

    raw = pd.read_excel(
        HOUSEHOLD_FILE,
        sheet_name=sheet,
        header=None,
        engine="openpyxl",
    )

    # --------------------------------------------------------
    # Locate the actual header row.
    #
    # IMPORTANT:
    # Do not use:
    #
    # " ".join(raw.iloc[i].astype(str).tolist())
    #
    # because Excel sheets can contain mixed data types.
    #
    # Explicitly convert every value to string.
    # --------------------------------------------------------

    header_row = None

    for i in range(min(30, len(raw))):
        row_values = []

        for value in raw.iloc[i].tolist():
            if pd.notna(value):
                row_values.append(str(value).strip().lower())

        row_text = " ".join(row_values)

        if "country and area" in row_text and "average household size" in row_text:
            header_row = i
            break

    if header_row is None:
        # Useful debugging information if UN changes
        # their Excel format.
        print("Could not locate expected header.")
        print("First rows detected in UN Excel file:")

        for i in range(min(15, len(raw))):
            debug_values = [
                str(value) for value in raw.iloc[i].tolist() if pd.notna(value)
            ]

            print(
                f"Row {i}:",
                " | ".join(debug_values),
            )

        raise RuntimeError("Could not locate UN household data header.")

    print(f"UN household data header found at row {header_row}.")

    # --------------------------------------------------------
    # Read the actual table using the discovered header.
    # --------------------------------------------------------

    df = pd.read_excel(
        HOUSEHOLD_FILE,
        sheet_name=sheet,
        header=header_row,
        engine="openpyxl",
    )

    # Remove completely empty columns and rows.
    df = df.dropna(
        axis=1,
        how="all",
    ).dropna(
        axis=0,
        how="all",
    )

    # Clean column names safely.
    df.columns = [
        str(column).strip().replace("\n", " ").replace("\r", " ")
        for column in df.columns
    ]

    return df


def get_average_household_size(
    country_code_iso3: str,
) -> float:
    """Retrieve the average household size for an ISO3 country code."""

    df = load_un_household_data()

    iso_col = "ISO3 Code"
    hh_col = "Average household size (number of members)"

    # --------------------------------------------------------
    # Check required columns.
    # --------------------------------------------------------

    if iso_col not in df.columns:
        raise RuntimeError(
            f"Required column missing from UN data: {iso_col}\n"
            f"Available columns: {list(df.columns)}"
        )

    if hh_col not in df.columns:
        raise RuntimeError(
            f"Required column missing from UN data: {hh_col}\n"
            f"Available columns: {list(df.columns)}"
        )

    # --------------------------------------------------------
    # Normalize ISO3 values.
    # --------------------------------------------------------

    iso_series = df[iso_col].fillna("").astype(str).str.strip().str.upper()

    matches = df[iso_series == country_code_iso3.upper()]

    if matches.empty:
        raise LookupError(f"No UN household data for ISO3: {country_code_iso3}")

    # --------------------------------------------------------
    # Convert household size to numeric.
    # --------------------------------------------------------

    values = pd.to_numeric(
        matches[hh_col],
        errors="coerce",
    ).dropna()

    values = values[values > 0]

    if values.empty:
        raise LookupError(
            f"Missing UN household size value for ISO3: {country_code_iso3}"
        )

    return float(values.iloc[0])


# ============================================================
# 4. MASTER ANALYSIS PIPELINE
# ============================================================


def analyze_market_reach(
    location: str,
    radius_km: float,
    year: int = 2025,
) -> dict:
    """
    End-to-end analysis:
    geocoding -> country -> radius -> population ->
    household estimate.
    """

    print(f"1. Geocoding location: {location}")

    latitude, longitude = geocode_location(location)

    print(f"   Coordinates: {latitude}, {longitude}")

    # --------------------------------------------------------
    # Country metadata
    # --------------------------------------------------------

    print("2. Querying country metadata...")

    country_info = get_country_from_coordinates(
        latitude,
        longitude,
    )

    iso3 = country_info["country_code_iso3"]

    print(f"   Found {country_info['country']} ({iso3})")

    # --------------------------------------------------------
    # Radius
    # --------------------------------------------------------

    print(f"3. Building {radius_km} km radius buffer...")

    geojson = create_radius_geojson(
        latitude,
        longitude,
        radius_km,
    )

    # --------------------------------------------------------
    # WorldPop
    # --------------------------------------------------------

    print("4. Calculating population via WorldPop...")

    task = submit_worldpop_task(
        geojson,
        year=year,
    )

    task_id = task["task_id"]

    print(f"   WorldPop task ID: {task_id}")

    wp_result = wait_for_worldpop_result(task_id)

    if "total_population" not in wp_result:
        raise RuntimeError(
            f"WorldPop result does not contain 'total_population': {wp_result}"
        )

    population = round(float(wp_result["total_population"]))

    # --------------------------------------------------------
    # Household size
    # --------------------------------------------------------

    print("5. Looking up UN average household size...")

    household_size = get_average_household_size(iso3)

    estimated_households = round(population / household_size)

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "radius_km": radius_km,
        "country": country_info["country"],
        "country_code": country_info["country_code"],
        "country_code_iso3": iso3,
        "population": population,
        "area_km2": wp_result.get("area_km2"),
        "population_density": wp_result.get("population_density"),
        "data_year": wp_result.get("data_year"),
        "population_data_source": wp_result.get("data_source"),
        "average_household_size": round(
            household_size,
            3,
        ),
        "estimated_households": estimated_households,
        "household_estimation_method": ("population / average household size"),
        "household_data_source": ("UN DESA Household Size and Composition 2026"),
    }
