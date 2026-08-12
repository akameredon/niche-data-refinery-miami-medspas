#!/usr/bin/env python3
"""
Streamlit dashboard for the Niche Data Refinery – Miami Med Spas
Run: streamlit run dashboard_streamlit.py
"""

import json
from pathlib import Path
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Miami Med Spas Data Refinery", page_icon="💉", layout="wide")

DATA = Path(__file__).parent / "data" / "clinics.json"

@st.cache_data
def load_data():
    with open(DATA) as f:
        return pd.DataFrame(json.load(f))

df = load_data()

st.title("Miami Med Spas – Niche Data Refinery")
st.caption("Prototype · 80 structured clinics · Public data only · For agencies & AI agents")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Clinics", len(df))
c2.metric("Avg Rating", f"{df['google_rating'].mean():.2f}")
c3.metric("Total Reviews", f"{int(df['review_count'].fillna(0).sum()):,}")
botox = df["botox_price_per_unit_est"].dropna()
c4.metric("Avg Botox $/unit", f"${botox.mean():.1f}" if len(botox) else "—")

st.divider()

col_a, col_b = st.columns(2)
neighborhoods = ["All"] + sorted([n for n in df["neighborhood"].dropna().unique() if n])
sel_nb = col_a.selectbox("Neighborhood", neighborhoods)
min_reviews = col_b.slider("Min reviews", 0, int(df["review_count"].max() or 100), 0)

filtered = df.copy()
if sel_nb != "All":
    filtered = filtered[filtered["neighborhood"] == sel_nb]
filtered = filtered[filtered["review_count"].fillna(0) >= min_reviews]

st.subheader(f"Clinics ({len(filtered)})")
show_cols = ["business_name", "neighborhood", "google_rating", "review_count",
             "botox_price_per_unit_est", "filler_price_syringe_est", "primary_services", "data_confidence"]
st.dataframe(
    filtered[show_cols].sort_values("review_count", ascending=False),
    use_container_width=True,
    height=420,
)

st.subheader("Top by reviews")
st.bar_chart(filtered.nlargest(10, "review_count").set_index("business_name")["review_count"])

with st.expander("Market notes"):
    st.markdown("""
- Botox typically **$12–$18 / unit** (most $14–16). Intro specials visible lower.
- Active NP/PA injector hiring = capacity expansion signal.
- Review concentration at top clinics is high.
- Pricing remains opaque → valuable for agency competitive intel.
    """)

st.caption("Path: spreadsheet → this dashboard → API / MCP tool")
