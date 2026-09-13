"""
Sales Data Analysis - Internship Task
--------------------------------------
Task: Analyze business sales data to identify revenue trends, top-selling
products, high-value categories, and regional performance.

HOW TO RUN:
1. Put this file in the same folder as sales_data.csv
2. Run: python analyze_sales.py
3. Charts will be saved in a "charts" folder next to this script
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# 1. Load the data
# ---------------------------------------------------------
df = pd.read_csv("sales_data.csv")
df["date"] = pd.to_datetime(df["date"])

# make a folder to save charts into
os.makedirs("charts", exist_ok=True)

print("Data loaded:", len(df), "rows")
print(df.head())
print()

# ---------------------------------------------------------
# 2. Revenue Trends (monthly)
# ---------------------------------------------------------
df["month"] = df["date"].dt.to_period("M")
monthly_revenue = df.groupby("month")["revenue"].sum()

print("----- Monthly Revenue -----")
print(monthly_revenue)
print()

monthly_revenue.plot(kind="line", marker="o", figsize=(10, 5), title="Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("charts/monthly_revenue_trend.png")
plt.close()

# ---------------------------------------------------------
# 3. Top-Selling Products
# ---------------------------------------------------------
top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10)

print("----- Top 10 Products by Revenue -----")
print(top_products)
print()

top_products.plot(kind="barh", figsize=(10, 6), title="Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.gca().invert_yaxis()  # highest at the top
plt.tight_layout()
plt.savefig("charts/top_products.png")
plt.close()

# ---------------------------------------------------------
# 4. High-Value Categories
# ---------------------------------------------------------
category_revenue = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

print("----- Revenue by Category -----")
print(category_revenue)
print()

category_revenue.plot(kind="pie", autopct="%1.1f%%", figsize=(7, 7), title="Revenue Share by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/category_share.png")
plt.close()

# ---------------------------------------------------------
# 5. Regional Performance
# ---------------------------------------------------------
region_revenue = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

print("----- Revenue by Region -----")
print(region_revenue)
print()

region_revenue.plot(kind="bar", figsize=(8, 5), title="Revenue by Region", color="steelblue")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/region_revenue.png")
plt.close()

# ---------------------------------------------------------
# 6. Quick summary / insights
# ---------------------------------------------------------
total_revenue = df["revenue"].sum()
total_orders = len(df)
best_month = monthly_revenue.idxmax()
top_product = top_products.index[0]
top_category = category_revenue.index[0]
top_region = region_revenue.index[0]

print("===== SUMMARY =====")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Best Month: {best_month}")
print(f"Top Product: {top_product}")
print(f"Top Category: {top_category}")
print(f"Top Region: {top_region}")

print("\nAll charts saved in the 'charts' folder.")
