#!/usr/bin/env python3
"""
MCP-style / agent tool wrapper around the Niche Data Refinery data.

Exposes simple functions an AI agent (or Claude/Cursor MCP server) can call:
  - search_clinics
  - get_pricing_summary
  - get_hiring_signals
  - get_clinic_by_id
"""

from pathlib import Path
import json
from typing import Optional, List, Dict, Any

DATA = Path(__file__).parent / "data" / "clinics.json"

def _load() -> List[Dict[str, Any]]:
    with open(DATA) as f:
        return json.load(f)

def search_clinics(
    neighborhood: Optional[str] = None,
    min_reviews: int = 0,
    min_rating: float = 0.0,
    has_hiring_signal: bool = False,
    limit: int = 20,
) -> Dict[str, Any]:
    """Search structured Miami med spa records."""
    data = _load()
    out = []
    for c in data:
        if neighborhood and neighborhood.lower() not in (c.get("neighborhood") or "").lower():
            continue
        if (c.get("review_count") or 0) < min_reviews:
            continue
        if (c.get("google_rating") or 0) < min_rating:
            continue
        hiring = (c.get("hiring_signals") or "").lower()
        if has_hiring_signal and ("none" in hiring or not hiring.strip()):
            continue
        out.append(c)
    out = sorted(out, key=lambda x: x.get("review_count") or 0, reverse=True)[:limit]
    return {"count": len(out), "clinics": out}

def get_pricing_summary() -> Dict[str, Any]:
    """Market-level Botox and filler price ranges."""
    data = _load()
    botox = [c["botox_price_per_unit_est"] for c in data if c.get("botox_price_per_unit_est") is not None]
    filler = [c["filler_price_syringe_est"] for c in data if c.get("filler_price_syringe_est") is not None]
    return {
        "botox_per_unit_usd": {
            "min": min(botox) if botox else None,
            "max": max(botox) if botox else None,
            "avg": round(sum(botox) / len(botox), 1) if botox else None,
            "sample_size": len(botox),
        },
        "filler_per_syringe_usd": {
            "min": min(filler) if filler else None,
            "max": max(filler) if filler else None,
            "avg": round(sum(filler) / len(filler), 1) if filler else None,
            "sample_size": len(filler),
        },
        "note": "Estimates derived from public signals. Live prices usually require consultation.",
    }

def get_hiring_signals(limit: int = 20) -> Dict[str, Any]:
    """Clinics with non-empty hiring / capacity signals."""
    data = _load()
    hits = [
        c for c in data
        if c.get("hiring_signals") and "none" not in (c.get("hiring_signals") or "").lower()
    ]
    hits = sorted(hits, key=lambda x: x.get("review_count") or 0, reverse=True)[:limit]
    return {"count": len(hits), "clinics": hits}

def get_clinic_by_id(clinic_id: int) -> Dict[str, Any]:
    """Fetch a single clinic by internal id."""
    for c in _load():
        if c.get("id") == clinic_id:
            return c
    return {"error": f"clinic id {clinic_id} not found"}

if __name__ == "__main__":
    print("=== Pricing Summary ===")
    print(json.dumps(get_pricing_summary(), indent=2))
    print("\n=== Hiring signals (top) ===")
    print(json.dumps(get_hiring_signals(limit=5), indent=2)[:800], "...")
    print("\n=== Brickell sample ===")
    print(json.dumps(search_clinics(neighborhood="Brickell", limit=3), indent=2)[:600], "...")
