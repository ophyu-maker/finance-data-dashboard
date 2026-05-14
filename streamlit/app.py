import sqlite3
from pathlib import Path
from streamlit_echarts import st_echarts

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Finance Data Dashboard",
    layout="wide"
)

st.title("Finance Data Dashboard")
st.caption("Simple invoice dashboard using SQLite and Streamlit")

# -----------------------------
# SQLite database path
# -----------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
DB_PATH = PROJECT_ROOT / "database" / "workforce_analytics.db"

# Optional debug check - keep this until app works
st.write("Database path:", DB_PATH)
st.write("Database exists:", DB_PATH.exists())

# -----------------------------
# Load data from SQLite
# -----------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
        SELECT *
        FROM company_status_summary;
    """, conn)

    conn.close()
    return df


df = load_data()

# -----------------------------
# Charts
# -----------------------------

st.subheader("Outstanding Balance by Vendor - ECharts")

chart_df = df.groupby("client", as_index=False)["outstanding_balance"].sum()
chart_df = chart_df.sort_values("outstanding_balance", ascending=False)

options = {
    "tooltip": {"trigger": "axis"},
    "xAxis": {
        "type": "category",
        "data": chart_df["client"].tolist(),
        "axisLabel": {"rotate": 45}
    },
    "yAxis": {
        "type": "value",
        "name": "Outstanding Balance"
    },
    "series": [
        {
            "name": "Outstanding Balance",
            "data": chart_df["outstanding_balance"].round(2).tolist(),
            "type": "bar"
        }
    ],
}

st_echarts(options=options, height="500px")

