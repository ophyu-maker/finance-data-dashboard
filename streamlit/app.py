import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Finance Data Dashboard",
    layout="wide"
)

st.title("Finance Data Dashboard")

st.markdown("""
<style>
    .main {
        background-color: #F7F9FC;
    }

    .main-header {
        background: linear-gradient(90deg, #1F4E79, #2E86C1);
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        color: white;
    }

    .main-header h1 {
        margin-bottom: 5px;
        font-size: 40px;
        font-weight: 700;
    }

    .main-header p {
        font-size: 18px;
        margin: 0;
        color: #EAF2F8;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E5E7EB;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    h2, h3 {
        color: #1F2937;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SQLite database path
# -----------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
DB_PATH = PROJECT_ROOT / "database" / "workforce_analytics.db"


# -----------------------------
# Helper function to load SQL data
# -----------------------------
@st.cache_data
def load_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# -----------------------------
# Load data
# -----------------------------
df = load_query("""
    SELECT *
    FROM company_status_summary;
""")

monthly_df = load_query("""
    SELECT *
    FROM monthly_invoice_summary
    ORDER BY invoice_month;
""")




# -----------------------------
# Prepare Vendor Bar Chart Data
# -----------------------------
chart_df = df.groupby("client", as_index=False)["outstanding_balance"].sum()
chart_df = chart_df.sort_values("outstanding_balance", ascending=False)

vendor_options = {
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "shadow"
        }
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
        "left": "8%",
        "right": "5%",
        "bottom": "20%",
        "containLabel": True
    },
    "xAxis": {
        "type": "category",
        "data": chart_df["client"].tolist(),
        "axisLabel": {
            "rotate": 45
        }
    },
    "yAxis": {
        "type": "value",
        "name": "Outstanding Balance",
        "axisLabel": {
            "formatter": "${value}"
        }
    },
    "series": [
        {
            "name": "Outstanding Balance",
            "data": chart_df["outstanding_balance"].round(2).tolist(),
            "type": "bar"
        }
    ]
}


# -----------------------------
# Prepare Invoice Trend Chart Data
# -----------------------------
months = monthly_df["invoice_month"].tolist()
total_invoice = monthly_df["total_invoiced"].round(2).tolist()
outstanding = monthly_df["total_outstanding_balance"].round(2).tolist()

trend_options = {
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
        "left": "8%",
        "right": "5%",
        "bottom": "22%",
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


# -----------------------------
# Side-by-side chart section
# -----------------------------
st.header("How are we trending?")
st.caption("Track invoice amount and outstanding balances using interactive charts.")

left_col, right_col = st.columns([1.4, 1])

with left_col:
    st.subheader("Invoice Amount & Outstanding Balance Trend")
    st_echarts(
        options=trend_options,
        height="550px"
    )

with right_col:
    st.subheader("Outstanding Balance by Vendor")
    st_echarts(
        options=vendor_options,
        height="550px"
    )


# -----------------------------
# Data table
# -----------------------------
st.subheader("Company Status Summary")

st.dataframe(
    df,
    use_container_width=True
)
