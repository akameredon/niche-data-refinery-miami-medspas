# Runbook – Niche Data Refinery (Miami Med Spas)

## Zero-install
1. Open `dashboard.html` in any modern browser.
2. Read `HANDOFF.md` and `00_Sales_OnePager.md`.

## Data files
- Master spreadsheet: `Miami_MedSpas_Data_Refinery_v1.xlsx` (not in git – binary; request or generate)
- Machine-readable: `data/clinics.json`

## Optional local services
```bash
# Streamlit dashboard
pip install streamlit pandas
streamlit run dashboard_streamlit.py

# FastAPI
pip install fastapi uvicorn
uvicorn api_sketch:app --reload --port 8000
# then visit http://localhost:8000/docs

# Agent tool smoke-test
python mcp_tool_wrapper.py
```

## Monthly refresh workflow (manual stage)
1. Update rows in the Excel (or re-run collection when automated).
2. Re-export JSON if needed.
3. `python scripts/refresh_check.py`  → see what changed vs last snapshot.
4. `python scripts/refresh_check.py --snapshot` → lock new baseline.
5. Regenerate any customer-facing reports that depend on the deltas.

## Sales motion (recommended)
- Target: marketing agencies, freelance consultants, and AI implementers who already serve med spas.
- Offer: monthly market intelligence package for one city/niche.
- Entry price while still semi-manual: $300–800 / month.
- Lead with a free or low-cost neighborhood deep-dive.

## Data limitations (always disclose)
- Prices are public-range estimates; live quotes almost always require consultation.
- Hiring signals are only those visible on public job boards.
- Not medical, legal, or financial advice.
