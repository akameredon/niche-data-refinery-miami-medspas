#!/usr/bin/env python3
"""
Minimal FastAPI sketch for agent-callable Niche Data Refinery.
Run: uvicorn api_sketch:app --reload --port 8000

Example agent queries:
  GET /clinics?neighborhood=Brickell&min_reviews=100
  GET /pricing/summary
  GET /hiring
  GET /clinic/{id}
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from typing import Optional

app = FastAPI(
    title="Niche Data Refinery – Miami Med Spas",
    description="Clean, structured med-spa data for AI agents and agencies",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA = Path(__file__).parent / "data" / "clinics.json"

def load():
    with open(DATA) as f:
        return json.load(f)

@app.get("/")
def root():
    return {
        "service": "Niche Data Refinery – Miami Med Spas",
        "clinics": len(load()),
        "endpoints": ["/clinics", "/pricing/summary", "/hiring", "/clinic/{id}", "/docs"],
    }

@app.get("/clinics")
def list_clinics(
    neighborhood: Optional[str] = None,
    min_reviews: int = Query(0, ge=0),
    min_rating: float = Query(0.0, ge=0, le=5),
    limit: int = Query(50, ge=1, le=200),
):
    data = load()
    out = []
    for c in data:
        if neighborhood and neighborhood.lower() not in (c.get("neighborhood") or "").lower():
            continue
        if (c.get("review_count") or 0) < min_reviews:
            continue
        if (c.get("google_rating") or 0) < min_rating:
            continue
        out.append(c)
    out = sorted(out, key=lambda x: x.get("review_count") or 0, reverse=True)[:limit]
    return {"count": len(out), "clinics": out}

@app.get("/pricing/summary")
def pricing_summary():
    data = load()
    botox = [c["botox_price_per_unit_est"] for c in data if c.get("botox_price_per_unit_est")]
    filler = [c["filler_price_syringe_est"] for c in data if c.get("filler_price_syringe_est")]
    return {
        "botox_per_unit": {
            "min": min(botox) if botox else None,
            "max": max(botox) if botox else None,
            "avg": round(sum(botox)/len(botox), 1) if botox else None,
            "n": len(botox),
        },
        "filler_per_syringe": {
            "min": min(filler) if filler else None,
            "max": max(filler) if filler else None,
            "avg": round(sum(filler)/len(filler), 1) if filler else None,
            "n": len(filler),
        },
        "note": "Estimates from public signals; exact live prices usually require consultation.",
    }

@app.get("/hiring")
def hiring_signals():
    data = load()
    hits = [c for c in data if c.get("hiring_signals") and "none" not in (c.get("hiring_signals") or "").lower()]
    return {"count": len(hits), "clinics_with_signals": hits}

@app.get("/clinic/{clinic_id}")
def get_clinic(clinic_id: int):
    data = load()
    for c in data:
        if c.get("id") == clinic_id:
            return c
    return {"error": "not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
