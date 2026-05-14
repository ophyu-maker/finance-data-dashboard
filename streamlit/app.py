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
    page_icon = "📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4f8ff 0%, #eef7f9 45%, #fdfcff 100%);
    color: #1f2937;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
    background: rgba(255, 255, 255, 0.94);
    border-radius: 24px;
    box-shadow: 0 8px 30px rgba(31, 41, 55, 0.10);
    margin-top: 2rem;
}

.hero-banner {
    background: linear-gradient(135deg, #2f80ed 0%, #56ccf2 100%);
    border-radius: 12px;
    padding: 0.4rem 0.9rem;
    margin-bottom: 0.7rem;
    color: white;
    box-shadow: 0 3px 10px rgba(15, 42, 58, 0.14);
}

.hero-banner h1 {
    color: white;
    font-size: 1.35rem;
    line-height: 1.1;
    margin: 0 0 0.1rem 0;
    font-weight: 700;
}

.hero-banner p {
    color: #d7ecf7;
    font-size: 0.8rem;
    line-height: 1.2;
    margin: 0;
}

h2, h3 {
    color: #1d3557;
    font-weight: 700;
}
.stButton > button {
    background: linear-gradient(135deg, #2f80ed 0%, #56ccf2 100%);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 1.4rem;
    font-weight: 700;
    font-size: 16px;
    box-shadow: 0 5px 16px rgba(47, 128, 237, 0.28);
}

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e5edf5;
}

footer, #MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Finance Data Dashboard")


# -----------------------------
# SQLite database path
# -----------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
DB_PATH = PROJECT_ROOT / "database" / "finance_data.db"


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

service_df = load_query(""" 
    SELECT *
    FROM invoice_service_summary
    ORDER BY total_invoiced DESC;
""")

country_service_df = load_query("""
    SELECT
        country,
        service,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_invoiced,
        ROUND(SUM(balance), 2) AS outstanding_balance
    FROM invoice_cleaned
    GROUP BY country, service
    ORDER BY total_invoiced DESC;
""")

raw_df = load_query(""" 
    SELECT *
    FROM invoice_cleaned;
""")

annual_budget_df = load_query("""
    SELECT *
    FROM department_annual_budget_vs_actual
    ORDER BY variance DESC;
""")

monthly_budget_df = load_query("""
    SELECT *
    FROM department_monthly_budget_vs_actual
    ORDER BY month, department_name;
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
            "bottom": 55
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
# Service Treemap Chart
# -----------------------------

treemap_data = []

for _, row in service_df.iterrows():
    treemap_data.append({
        "name": row["service"],
        "value": round(row["total_invoiced"], 2),
        "invoice_count": int(row["invoice_count"]),
        "outstanding_balance": round(row["outstanding_balance"], 2),
        "avg_invoice_amount": round(row["avg_invoice_amount"], 2)
    })

treemap_options = {
    "tooltip": {
        "formatter": """
            <b>{b}</b><br/>
            Total Invoiced: ${c}
        """
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
            }
        }
    },
    "series": [
        {
            "name": "Service Category",
            "type": "treemap",
            "data": treemap_data,
            "roam": False,
            "nodeClick": False,
            "breadcrumb": {
                "show": False
            },
            "label": {
                "show": True,
                "formatter": "{b}",
                "fontSize": 14
            },
            "upperLabel": {
                "show": True,
                "height": 30
            },
            "itemStyle": {
                "borderColor": "#ffffff",
                "borderWidth": 2,
                "gapWidth": 2
            },
            "levels": [
                {
                    "itemStyle": {
                        "borderColor": "#ffffff",
                        "borderWidth": 2,
                        "gapWidth": 2
                    }
                }
            ]
        }
    ]
}

# -----------------------------
# Top 10 Revenue by Country and Service Category
# -----------------------------

# Top 10 countries by total invoiced amount
top_countries = (
    country_service_df
    .groupby("country", as_index=False)["total_invoiced"]
    .sum()
    .sort_values("total_invoiced", ascending=False)
    .head(10)["country"]
    .tolist()
)

top_country_service_df = country_service_df[
    country_service_df["country"].isin(top_countries)
].copy()

# Pivot: rows = countries, columns = services
country_service_pivot = top_country_service_df.pivot_table(
    index="country",
    columns="service",
    values="total_invoiced",
    aggfunc="sum",
    fill_value=0
)

# Keep country order as Top 
country_service_pivot = country_service_pivot.reindex(top_countries)

countries = country_service_pivot.index.tolist()
services = country_service_pivot.columns.tolist()

country_service_series = []

for service in services:
    country_service_series.append({
        "name": service,
        "type": "bar",
        "stack": "total",
        "emphasis": {
            "focus": "series"
        },
        "data": country_service_pivot[service].round(2).tolist()
    })

country_service_options = {
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "shadow"
        }
    },
    "legend": {
        "top": 0,
        "type": "scroll"
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
            }
        }
    },
    "grid": {
        "left": "10%",
        "right": "8%",
        "bottom": "8%",
        "top": "18%",
        "containLabel": True
    },
    "xAxis": {
        "type": "value",
        "name": "Total Invoiced",
        "axisLabel": {
            "formatter": "${value}"
        }
    },
    "yAxis": {
        "type": "category",
        "data": countries,
        "inverse": True
    },
    "series": country_service_series
}


# -----------------------------
# Invoice Interactive Charts
# -----------------------------

st.markdown("""
<div class="hero-banner">
    <h1>Invoice related interactive charts</h1>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Row 1: Two charts side by side
# -----------------------------
with st.container():
    left_col, right_col = st.columns([1.4, 1])

    with left_col:
        st.markdown(
            "<h3 style='color:#1F4E79;'>Invoice Amount & Outstanding Balance Trend</h3>",
            unsafe_allow_html=True
        )
        st_echarts(
            options=trend_options,
            height="550px",
            key="invoice_trend_chart"
        )

    with right_col:
        st.markdown(
            "<h3 style='color:#1F4E79;'>Outstanding Balance by Vendor</h3>",
            unsafe_allow_html=True
        )
        st_echarts(
            options=vendor_options,
            height="550px",
            key="vendor_balance_chart"
        )


# Add spacing between chart rows
st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# Row 2: Treemap + table
# -----------------------------
with st.container():
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown(
            "<h3 style='color:#1F4E79;'>Service Category Treemap</h3>",
            unsafe_allow_html=True
        )
        st_echarts(
            options=treemap_options,
            height="550px",
            key="service_category_treemap"
        )

    with right_col:
        st.markdown(
            "<h3 style='color:#1F4E79;'>Top 10 Revenue by Country</h3>",
            unsafe_allow_html=True
        )

        st_echarts(
            options=country_service_options,
            height="500px",
            key="top_country_Service_revenue_chart"
        )


# -----------------------------
# Data table
# -----------------------------
with st.expander("🧾 Cleanded data preview", expanded=False):
    st.dataframe(
        raw_df,
        use_container_width=True,
        height=500
    )

# -----------------------------
# Budget vs Actual Interactive Charts
# -----------------------------

st.markdown("""
<div class="hero-banner">
    <h1>Annual payment related interactive charts</h1>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Prepare annual bubble chart data
# -----------------------------

annual_deep_df = annual_budget_df.copy()

annual_deep_df["department_name"] = annual_deep_df["department_name"].astype(str)
annual_deep_df["budget_annual_amount"] = annual_deep_df["budget_annual_amount"].fillna(0)
annual_deep_df["annual_actual_pay"] = annual_deep_df["annual_actual_pay"].fillna(0)
annual_deep_df["variance"] = annual_deep_df["variance"].fillna(0)

# Recalculate true variance %
annual_deep_df["variance_pct_true"] = annual_deep_df.apply(
    lambda row: (row["variance"] / row["budget_annual_amount"] * 100)
    if row["budget_annual_amount"] != 0 else 0,
    axis=1
)

# Cap only for chart display
annual_deep_df["variance_pct_chart"] = annual_deep_df["variance_pct_true"].clip(-100, 300)

top_deep_df = (
    annual_deep_df
    .sort_values("annual_actual_pay", ascending=False)
    .head(25)
    .copy()
)

bubble_data = []

for _, row in top_deep_df.iterrows():
    bubble_data.append({
        "name": row["department_name"],
        "value": [
            round(row["budget_annual_amount"], 2),   # x-axis
            round(row["variance_pct_chart"], 2),     # y-axis capped
            round(row["annual_actual_pay"], 2),      # bubble size reference
            round(row["variance"], 2),               # tooltip
            round(row["variance_pct_true"], 2)       # tooltip true %
        ]
    })


budget_bubble_options = {
    "tooltip": {
        "trigger": "item",
        "formatter": """
            function(params) {
                var v = params.value;
                return '<b>' + params.name + '</b><br/>' +
                       'Annual Budget: $' + v[0].toLocaleString() + '<br/>' +
                       'Annual Actual Pay: $' + v[2].toLocaleString() + '<br/>' +
                       'Variance: $' + v[3].toLocaleString() + '<br/>' +
                       'True Variance %: ' + v[4].toLocaleString() + '%';
            }
        """
    },
    "toolbox": {
        "show": True,
        "right": 20,
        "feature": {
            "saveAsImage": {"show": True, "title": "Save as Image"},
            "restore": {"show": True, "title": "Restore"},
            "dataView": {"show": True, "readOnly": True, "title": "View Data"}
        }
    },
    "grid": {
        "left": "12%",
        "right": "8%",
        "bottom": "14%",
        "top": "12%",
        "containLabel": True
    },
    "xAxis": {
        "type": "value",
        "name": "Annual Budget",
        "nameLocation": "middle",
        "nameGap": 35,
        "axisLabel": {
            "formatter": "${value}"
        },
        "splitLine": {"show": True}
    },
    "yAxis": {
        "type": "value",
        "name": "Variance %",
        "nameLocation": "middle",
        "nameGap": 55,
        "min": -100,
        "max": 300,
        "axisLabel": {
            "formatter": "{value}%"
        },
        "splitLine": {"show": True}
    },
    "series": [
        {
            "name": "Department",
            "type": "scatter",
            "data": bubble_data,
            "symbolSize": 22,
            "itemStyle": {
                "opacity": 0.75
            },
            "emphasis": {
                "focus": "self",
                "label": {
                    "show": True,
                    "formatter": "{b}",
                    "position": "top"
                }
            }
        }
    ]
}

st.write(top_deep_df[[
    "department_name",
    "budget_annual_amount",
    "annual_actual_pay",
    "variance",
    "variance_pct_true",
    "variance_pct_chart"
]])


# -----------------------------
# Click event
# -----------------------------

department_click_event = {
    "click": """
        function(params) {
            return params.name;
        }
    """
}


def extract_department_from_click(clicked_value):
    if clicked_value is None:
        return None

    if isinstance(clicked_value, dict):
        chart_event = clicked_value.get("chart_event")

        if chart_event is None:
            return None

        if isinstance(chart_event, str):
            return chart_event

        if isinstance(chart_event, dict):
            return chart_event.get("name")

    if isinstance(clicked_value, str):
        return clicked_value

    return None


# -----------------------------
# Default department before click
# -----------------------------

if "selected_budget_department" not in st.session_state:
    st.session_state["selected_budget_department"] = str(top_deep_df.iloc[0]["department_name"])


# -----------------------------
# Layout: Bubble chart + monthly trend chart
# -----------------------------

left_col, right_col = st.columns([1, 1.25])

with left_col:
    st.markdown(
        "<h3 style='color:#1F4E79; text-align:center;'>Annual Budget vs Actual Variance</h3>",
        unsafe_allow_html=True
    )

    clicked_result = st_echarts(
        options=budget_bubble_options,
        height="520px",
        key="budget_deep_dive_bubble_chart",
        events=department_click_event
    )

    clicked_department = extract_department_from_click(clicked_result)

    if clicked_department:
        st.session_state["selected_budget_department"] = clicked_department

with right_col:
    selected_department = str(st.session_state["selected_budget_department"])

    st.markdown(
        f"<h3 style='color:#1F4E79; text-align:center;'>{selected_department} — Monthly Trend</h3>",
        unsafe_allow_html=True
    )

    dept_monthly_df = monthly_budget_df[
        monthly_budget_df["department_name"].astype(str) == selected_department
    ].copy()

    dept_monthly_df = dept_monthly_df.sort_values("month")

    # Convert dollar amounts to millions for chart readability
    dept_monthly_df["budget_m"] = dept_monthly_df["budget_amount"].fillna(0) / 1_000_000
    dept_monthly_df["actual_m"] = dept_monthly_df["monthly_actual_pay"].fillna(0) / 1_000_000
    dept_monthly_df["variance_m"] = dept_monthly_df["variance"].fillna(0) / 1_000_000

    deep_months = dept_monthly_df["month"].astype(str).tolist()
    deep_budget = dept_monthly_df["budget_m"].round(2).tolist()
    deep_actual = dept_monthly_df["actual_m"].round(2).tolist()
    deep_variance = dept_monthly_df["variance_m"].round(2).tolist()

    monthly_deep_options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross"
            }
        },
        "legend": {
            "data": ["Monthly Budget", "Monthly Actual", "Variance"],
            "bottom": 0
        },
        "toolbox": {
            "show": True,
            "right": 20,
            "feature": {
                "saveAsImage": {"show": True, "title": "Save as Image"},
                "restore": {"show": True, "title": "Restore"},
                "dataView": {"show": True, "readOnly": True, "title": "View Data"}
            }
        },
        "grid": {
            "left": "10%",
            "right": "8%",
            "bottom": "18%",
            "top": "12%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": deep_months,
            "axisLabel": {
                "rotate": 45
            }
        },
        "yAxis": [
            {
                "type": "value",
                "name": "Budget / Actual ($M)",
                "axisLabel": {
                    "formatter": "${value}M"
                }
            },
            {
                "type": "value",
                "name": "Variance ($M)",
                "axisLabel": {
                    "formatter": "${value}M"
                }
            }
        ],
        "series": [
            {
                "name": "Monthly Budget",
                "type": "bar",
                "data": deep_budget,
                "barWidth": "45%"
            },
            {
                "name": "Monthly Actual",
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 8,
                "data": deep_actual
            },
            {
                "name": "Variance",
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 7,
                "yAxisIndex": 1,
                "data": deep_variance
            }
        ]
    }

    st_echarts(
        options=monthly_deep_options,
        height="520px",
        key="monthly_deep_dive_chart"
    )

    st.info(
    "Note: Monthly budget is synthetic data. Annual budget was divided evenly by 12 "
    "to simulate monthly budget phasing for dashboard demonstration purposes. "
    "Monthly budget variance should not be interpreted as actual approved monthly budget performance."
    )

# -----------------------------
# Selected department detail table
# -----------------------------

with st.expander("View selected department budget vs actual data", expanded=False):
    st.dataframe(
        dept_monthly_df,
        use_container_width=True,
        height=350
    )
