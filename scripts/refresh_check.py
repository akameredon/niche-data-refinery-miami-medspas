#!/usr/bin/env python3
"""
Lightweight change-detection helper for the Niche Data Refinery.
Compares current clinics.json against a previous snapshot and reports deltas.

Usage:
  python scripts/refresh_check.py
  python scripts/refresh_check.py --snapshot
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
CURRENT = ROOT / "data" / "clinics.json"
PREVIOUS = ROOT / "data" / "previous_clinics.json"

def load(path):
    if not path.exists():
        return {}
    with open(path) as f:
        data = json.load(f)
    return {c["id"]: c for c in data if c.get("id") is not None}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", action="store_true", help="Save current as previous baseline")
    args = parser.parse_args()

    if args.snapshot:
        if CURRENT.exists():
            PREVIOUS.write_text(CURRENT.read_text())
            print(f"Snapshot saved → {PREVIOUS}")
        else:
            print("No current data found")
        return

    curr = load(CURRENT)
    prev = load(PREVIOUS)

    if not prev:
        print("No previous snapshot. Run with --snapshot first after a collection cycle.")
        return

    print(f"Comparing {len(curr)} current vs {len(prev)} previous · {datetime.now().isoformat()}")
    print("-" * 60)

    new_ids = set(curr) - set(prev)
    gone_ids = set(prev) - set(curr)
    common = set(curr) & set(prev)

    if new_ids:
        print(f"\nNEW clinics ({len(new_ids)}):")
        for i in sorted(new_ids):
            print(f"  + {curr[i].get('business_name')} (id={i})")

    if gone_ids:
        print(f"\nREMOVED / missing ({len(gone_ids)}):")
        for i in sorted(gone_ids):
            print(f"  - {prev[i].get('business_name')} (id={i})")

    rating_changes = []
    review_changes = []
    hiring_changes = []

    for i in common:
        c, p = curr[i], prev[i]
        if c.get("google_rating") != p.get("google_rating"):
            rating_changes.append((c.get("business_name"), p.get("google_rating"), c.get("google_rating")))
        if (c.get("review_count") or 0) != (p.get("review_count") or 0):
            review_changes.append((c.get("business_name"), p.get("review_count"), c.get("review_count")))
        if (c.get("hiring_signals") or "") != (p.get("hiring_signals") or ""):
            hiring_changes.append((c.get("business_name"), p.get("hiring_signals"), c.get("hiring_signals")))

    if rating_changes:
        print(f"\nRating changes ({len(rating_changes)}):")
        for name, old, new in rating_changes[:20]:
            print(f"  {name}: {old} → {new}")

    if review_changes:
        print(f"\nReview count changes ({len(review_changes)}):")
        for name, old, new in sorted(review_changes, key=lambda x: abs((x[2] or 0) - (x[1] or 0)), reverse=True)[:20]:
            delta = (new or 0) - (old or 0)
            print(f"  {name}: {old} → {new} ({delta:+d})")

    if hiring_changes:
        print(f"\nHiring signal changes ({len(hiring_changes)}):")
        for name, old, new in hiring_changes:
            print(f"  {name}:\n    was: {old}\n    now: {new}")

    if not any([new_ids, gone_ids, rating_changes, review_changes, hiring_changes]):
        print("\nNo material changes detected.")

    print("\nDone.")

if __name__ == "__main__":
    main()
