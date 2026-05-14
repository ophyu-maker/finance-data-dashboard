import sqlite3
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
DB_PATH = "database/workforce_analytics.db"  

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
# Show raw data first
# -----------------------------
st.subheader("Vendor Balance Summary")
st.dataframe(df, use_container_width=True)

# -----------------------------
# KPI cards
# -----------------------------
total_outstanding = df["outstanding_balance"].sum()
total_invoice_amount = df["total_invoice_amount"].sum()
invoice_count = df["invoice_count"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Outstanding Balance", f"${total_outstanding:,.2f}")
col2.metric("Total Invoice Amount", f"${total_invoice_amount:,.2f}")
col3.metric("Invoice Count", f"{invoice_count:,.0f}")

# -----------------------------
# Simple bar chart
# -----------------------------
st.subheader("Outstanding Balance by Vendor")

fig = px.bar(
    df,
    x="client",
    y="outstanding_balance",
    title="Outstanding Balance by Vendor",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)
