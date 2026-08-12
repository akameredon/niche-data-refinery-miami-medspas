# Niche Data Refinery – Miami Med Spas Prototype
**Version:** 1.0 | **Date:** 2026-08-12  
**Owner decision:** Full autonomy granted by user; all choices made by the system.

## What Was Built

### 1. Core Dataset
- **File:** `Miami_MedSpas_Data_Refinery_v1.xlsx` (add locally or download from releases)
- **80 real Miami-area med spas** structured from public sources.
- Sheets: MedSpas_Miami, Pricing_Snapshot, Hiring_Signals, Market_Overview, Schema_Definition

### 2. Sample Reports (Markdown)
- `00_Sales_OnePager.md` – pitch for agencies
- `01_Local_Pricing_Map.md`
- `02_Competitor_Gap_Analysis.md`
- `03_Hiring_Signal_Report.md`
- `04_Market_Movement_Notes.md`
- `05_Neighborhood_Deep_Dives.md` (Brickell, Doral, Coral Gables, Coconut Grove)

### 3. Dashboards & Tools
- `dashboard.html` – zero-install interactive dashboard
- `dashboard_streamlit.py` – Streamlit version
- `api_sketch.py` – FastAPI endpoints for agents
- `mcp_tool_wrapper.py` – agent-callable functions
- `scripts/refresh_check.py` – change detection

### Why This Niche + City
Med spas were the canonical example. Miami has extreme density, opaque pricing, active injector hiring, and clear agency buyers.

### Quick start
1. Open `dashboard.html`
2. Read `HANDOFF.md` and `RUNBOOK.md`
3. `python mcp_tool_wrapper.py` for agent tool demo

See full README history in the conversation that built this prototype.
