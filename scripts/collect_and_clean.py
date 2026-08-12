#!/usr/bin/env python3
"""
Niche Data Refinery - lightweight collection & cleaning skeleton
Target: Miami Med Spas
"""

import json
from datetime import datetime
from pathlib import Path

SCHEMA = [
    "id", "business_name", "neighborhood", "address", "phone", "website",
    "google_rating", "review_count", "primary_services", "botox_price_per_unit_est",
    "filler_price_syringe_est", "hiring_signals", "review_themes", "social_ig",
    "booking_method", "last_updated", "notes", "data_confidence"
]

def clean_rating(val):
    try:
        return round(float(val), 1)
    except (TypeError, ValueError):
        return None

def clean_count(val):
    try:
        return int(str(val).replace(",", "").strip())
    except (TypeError, ValueError):
        return None

def normalize_business(raw: dict) -> dict:
    return {
        "business_name": (raw.get("name") or "").strip(),
        "neighborhood": raw.get("neighborhood") or raw.get("area") or "",
        "address": raw.get("address") or raw.get("formatted_address") or "",
        "phone": raw.get("phone") or raw.get("formatted_phone_number") or "",
        "website": raw.get("website") or raw.get("url") or "",
        "google_rating": clean_rating(raw.get("rating")),
        "review_count": clean_count(raw.get("user_ratings_total") or raw.get("review_count")),
        "primary_services": raw.get("services") or raw.get("types") or "",
        "botox_price_per_unit_est": raw.get("botox_ppu"),
        "filler_price_syringe_est": raw.get("filler_price"),
        "hiring_signals": raw.get("hiring") or "",
        "review_themes": raw.get("review_summary") or "",
        "social_ig": raw.get("instagram") or "",
        "booking_method": raw.get("booking") or "",
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d"),
        "notes": raw.get("notes") or "",
        "data_confidence": raw.get("confidence") or "Medium",
    }

if __name__ == "__main__":
    print("Collection skeleton ready.")
    print("Schema fields:", SCHEMA)
