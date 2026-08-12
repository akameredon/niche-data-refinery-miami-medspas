# Niche Data Refinery – Miami Med Spas
**Handoff package · 2026-08-12**

## What you have
- 80 structured med spa records (Excel + JSON)
- Pricing, competitor gap, hiring, and market movement reports
- Interactive dashboard (HTML – zero install)
- Streamlit + FastAPI + MCP-style tool wrappers
- Change-detection script for monthly refreshes
- Sales one-pager aimed at marketing agencies / consultants

## Immediate next actions (recommended)
1. Open `dashboard.html` and verify the data looks right for your use case.
2. Pick 3–5 target agencies that already sell into Miami med spas.
3. Send the sales one-pager + a sample pricing map for one neighborhood.
4. Price the first pilots at $300–600/mo while the collection is still partly manual.
5. Use `scripts/refresh_check.py --snapshot` as the baseline; re-run after each data update.

## Data caveats (be transparent)
- Prices are estimates / public ranges. Exact live prices almost always require a consultation.
- Hiring signals are only those publicly visible.
- Review themes are high-level; deeper NLP is future work.

## File map
- `Miami_MedSpas_Data_Refinery_v1.xlsx` – master spreadsheet (add separately)
- `data/clinics.json` – machine-readable
- `dashboard.html` – open in browser
- `00_Sales_OnePager.md` – outreach
- `01–05_*.md` – sample deliverables
- `api_sketch.py` / `mcp_tool_wrapper.py` / `dashboard_streamlit.py` – technical surfaces
- `scripts/` – collection & refresh helpers

Built under full autonomy as a working prototype of the Niche Data Refinery concept.
