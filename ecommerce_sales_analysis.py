
# STEP 1: Import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# STEP 2: Read the CSV dataset

df = pd.read_csv("ecommerce_sales.csv")


# STEP 3: Display the data

print("First 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nDataset information:")
df.info()


# STEP 4: Check missing values and duplicates

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# STEP 5: Clean the data

df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)

df = df.drop_duplicates()

df = df.dropna(
    subset=[
        "OrderID",
        "OrderDate",
        "CustomerID",
        "Quantity",
        "UnitPrice"
    ]
)

df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] >= 0)
].copy()


# STEP 6: Create a Revenue column

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("\nData after cleaning:")
print(df.head())

print("\nRevenue column:")
print(df[["Product", "Quantity", "UnitPrice", "Revenue"]])


# STEP 7: Calculate key business metrics

total_revenue = df["Revenue"].sum()

total_orders = df["OrderID"].nunique()

total_customers = df["CustomerID"].nunique()

total_units_sold = df["Quantity"].sum()

average_order_value = total_revenue / total_orders

print("\n--- BUSINESS SUMMARY ---")

print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Unique Customers:", total_customers)
print("Units Sold:", total_units_sold)
print("Average Revenue per Order:", round(average_order_value, 2))


# STEP 8: Category-wise sales analysis

category_sales = (
    df.groupby("Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCategory-wise Revenue:")
print(category_sales)

best_category = category_sales.idxmax()

print("Best Performing Category:", best_category)


# STEP 9: Product-wise sales analysis

product_sales = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nProduct-wise Revenue:")
print(product_sales)


# STEP 10: Monthly sales analysis

df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\nMonthly Revenue:")
print(monthly_sales)


# STEP 11: Customer analysis

customer_sales = (
    df.groupby("CustomerID")
    .agg(
        Total_Spending=("Revenue", "sum"),
        Number_of_Orders=("OrderID", "nunique")
    )
    .sort_values("Total_Spending", ascending=False)
)

print("\nTop Customers:")
print(customer_sales.head(5))


# STEP 12: Create an output folder

import os

os.makedirs("outputs", exist_ok=True)


# STEP 13: Plot monthly revenue

monthly_sales.plot(
    kind="line",
    marker="o",
    title="Monthly Revenue Trend"
)

plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/monthly_sales.png")
plt.show()


# STEP 14: Plot category-wise revenue
print("Category graph code started")

category_sales.plot(
    kind="bar",
    title="Revenue by Product Category"
)

plt.xlabel("Category")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("outputs/category_sales.png")
plt.show()



# STEP 14.1: Top 5 Products by Revenue

top_products = product_sales.head(5)

plt.figure(figsize=(8, 5))

top_products.plot(kind="bar", color="purple")

plt.title("Top 5 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("outputs/top_products.png", dpi=300)
plt.close()

print("Top 5 Products graph saved successfully!")



# STEP 16: City-wise Sales Analysis

city_sales = (
    df.groupby("City")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCity-wise Revenue:")
print(city_sales)

plt.figure(figsize=(8, 5))

city_sales.plot(kind="bar", color="teal")

plt.title("City-wise Sales Analysis")
plt.xlabel("City")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("outputs/city_sales.png", dpi=300)
plt.close()

print("City-wise graph saved successfully!")

# Export city-wise sales
city_sales.to_csv("outputs/city_sales_summary.csv")




# STEP 15: Plot top 5 customers
print("Top customers graph code started")

top_customers = customer_sales.head(5)["Total_Spending"]

top_customers.plot(
    kind="bar",
    title="Top 5 Customers by Spending"
)

plt.xlabel("Customer ID")
plt.ylabel("Total Spending (Rs.)")
plt.tight_layout()

plt.savefig("outputs/top_customers.png")
plt.show()


# STEP 16: Export cleaned data and analysis

df.to_csv("outputs/cleaned_ecommerce_sales.csv", index=False)

category_sales.to_csv("outputs/category_sales_summary.csv")

monthly_sales.to_csv("outputs/monthly_sales_summary.csv")

customer_sales.to_csv("outputs/customer_sales_summary.csv")

print("\nProject completed successfully!")
print("Check the outputs folder for results.")
