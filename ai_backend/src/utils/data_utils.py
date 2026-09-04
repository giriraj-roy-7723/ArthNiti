import time
from pathlib import Path
from typing import Any


def cache_is_fresh(path: Path, max_age_seconds: int) -> bool:
    return path.exists() and (time.time() - path.stat().st_mtime) < max_age_seconds


def normalize_name(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(
        str(value).strip().lower().replace("_", " ").replace("-", " ").split()
    )


def recursive_find_lists(obj: Any) -> list[dict[str, Any]]:
    results = []
    if isinstance(obj, dict):
        for val in obj.values():
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        results.append(item)
            results.extend(recursive_find_lists(val))
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                results.append(item)
            results.extend(recursive_find_lists(item))
    return results


def flatten_json_records(obj: Any) -> list[dict[str, Any]]:
    records = []
    if isinstance(obj, dict):
        if any(
            k.lower()
            in {
                "minprice",
                "maxprice",
                "modalprice",
                "modal_price",
                "price",
                "commodityprice",
            }
            for k in obj.keys()
        ):
            records.append(obj)
        for value in obj.values():
            records.extend(flatten_json_records(value))
    elif isinstance(obj, list):
        for item in obj:
            records.extend(flatten_json_records(item))
    return records


def safe_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return float(value)
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", "")
            if not value:
                return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def normalize_index(value: Any, default: float = 100.0) -> float:
    return safe_float(value, default)