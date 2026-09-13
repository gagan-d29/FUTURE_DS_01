"""
Sales Dashboard (Streamlit) - Internship Task
-----------------------------------------------
An interactive dashboard for the same sales_data.csv used in analyze_sales.py.

HOW TO RUN:
1. Install streamlit (one-time):
       pip install streamlit
2. Put this file in the same folder as sales_data.csv
3. Run:
       streamlit run dashboard.py
4. It opens automatically in your browser (usually http://localhost:8501)
"""

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Performance Dashboard")

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
df = pd.read_csv("sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Region", options=sorted(df["region"].unique()), default=sorted(df["region"].unique())
)
categories = st.sidebar.multiselect(
    "Category", options=sorted(df["category"].unique()), default=sorted(df["category"].unique())
)

min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input("Date range", (min_date, max_date), min_value=min_date, max_value=max_date)

# apply filters
filtered = df[df["region"].isin(regions) & df["category"].isin(categories)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

# ---------------------------------------------------------
# KPI row
# ---------------------------------------------------------
total_revenue = filtered["revenue"].sum()
total_orders = len(filtered)
aov = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg. Order Value", f"₹{aov:,.0f}")

st.markdown("---")

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Monthly Revenue Trend")
    monthly = filtered.groupby("month")["revenue"].sum()
    st.line_chart(monthly)

with right:
    st.subheader("Revenue by Category")
    cat_rev = filtered.groupby("category")["revenue"].sum().sort_values(ascending=False)
    st.bar_chart(cat_rev)

left2, right2 = st.columns(2)

with left2:
    st.subheader("Top 10 Products by Revenue")
    top_products = filtered.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_products)

with right2:
    st.subheader("Revenue by Region")
    region_rev = filtered.groupby("region")["revenue"].sum().sort_values(ascending=False)
    st.bar_chart(region_rev)

# ---------------------------------------------------------
# Raw data (optional peek)
# ---------------------------------------------------------
st.markdown("---")
with st.expander("View filtered data"):
    st.dataframe(filtered)
