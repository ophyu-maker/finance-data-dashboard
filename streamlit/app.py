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

#--------------------------------
# Invoice Trend Chart
#--------------------------------
st.subheader("Invoice Trend")

monthly_df = pd.read_sql_query("""
    SELECT *
    FROM monthly_invoice_summary
    ORDER BY invoice_month;
""", sqlite3.connect(DB_PATH))

# Convert values to Python lists for ECharts
months = monthly_df["invoice_month"].tolist()
total_invoice = monthly_df["total_net_invoice_amount"].round(2).tolist()
outstanding = monthly_df["total_outstanding_balance"].round(2).tolist()

options = {
    "title": {
        "text": "Invoice Amount & Outstanding Balance Trend",
        "left": "center",
        "textStyle": {
            "fontSize": 22,
            "fontWeight": "bold"
        }
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "cross"
        }
    },
    "legend": {
        "data": ["Total Invoice Amount", "Outstanding Balance"],
        "bottom": 0
    },
    "toolbox": {
        "show": True,
        "right": 20,
        "feature": {
            "saveAsImage": {
                "show": True,
                "title": "Save as Image"
            },
            "restore": {
                "show": True,
                "title": "Restore"
            },
            "dataView": {
                "show": True,
                "readOnly": True,
                "title": "View Data"
            },
            "magicType": {
                "show": True,
                "type": ["line", "bar"],
                "title": {
                    "line": "Switch to Line",
                    "bar": "Switch to Bar"
                }
            }
        }
    },
    "grid": {
        "left": "5%",
        "right": "5%",
        "bottom": "18%",
        "containLabel": True
    },
    "xAxis": {
        "type": "category",
        "boundaryGap": False,
        "data": months
    },
    "yAxis": {
        "type": "value",
        "axisLabel": {
            "formatter": "${value}"
        }
    },
    "dataZoom": [
        {
            "type": "slider",
            "start": 0,
            "end": 100,
            "bottom": 45
        },
        {
            "type": "inside",
            "start": 0,
            "end": 100
        }
    ],
    "series": [
        {
            "name": "Total Invoice Amount",
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 8,
            "areaStyle": {
                "opacity": 0.15
            },
            "lineStyle": {
                "width": 3
            },
            "data": total_invoice
        },
        {
            "name": "Outstanding Balance",
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 8,
            "areaStyle": {
                "opacity": 0.08
            },
            "lineStyle": {
                "width": 3
            },
            "data": outstanding
        }
    ]
}

st_echarts(options=options, height="600px")

