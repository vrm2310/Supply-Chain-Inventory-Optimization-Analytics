from pathlib import Path

import numpy as np
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "supply_chain_features.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

# ==========================================================
# Helper Functions
# ==========================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)


def print_success(msg):
    print(f"✓ {msg}")


def print_info(msg):
    print(f"• {msg}")


# ==========================================================
# Load Dataset
# ==========================================================

def load_data():

    print_section("Loading Feature Dataset")

    df = pd.read_csv(
        INPUT_DATA,
        parse_dates=[
            "order_date_dateorders",
            "shipping_date_dateorders"
        ]
    )

    print_success("Dataset Loaded")
    print_info(f"Rows : {len(df):,}")
    print_info(f"Columns : {df.shape[1]}")

    return df


# ==========================================================
# Save Tables
# ==========================================================

def save_table(df, filename):

    filepath = OUTPUT_DIR / filename

    df.to_csv(
        filepath,
        index=False
    )

    print_success(f"{filename} saved")


# ==========================================================
# Validation
# ==========================================================

def validate_table(df, table_name):

    print_section(table_name)

    print_info(f"Rows : {len(df):,}")

    print_info(f"Columns : {df.shape[1]}")

    print_info(
        f"Missing Values : {df.isnull().sum().sum():,}"
    )

    print_info(
        f"Duplicate Rows : {df.duplicated().sum():,}"
    )

# ==========================================================
# Product Metrics
# ==========================================================

def create_product_metrics(df):

    print_section("Creating Product Metrics")

    product = (
        df.groupby(["product_name", "category_name"], as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("benefit_per_order", "sum"),
            total_orders=("order_id", "nunique"),
            total_quantity=("order_item_quantity", "sum"),
            avg_selling_price=("average_selling_price", "mean"),
            avg_discount_pct=("discount_pct", "mean"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            last_order_date=("order_date_dateorders", "max")
        )
    )

    # ----------------------------------------
    # Rounding
    # ----------------------------------------

    numeric_cols = [
        "total_sales",
        "total_profit",
        "avg_selling_price",
        "avg_discount_pct",
        "avg_margin_pct"
    ]

    product[numeric_cols] = (product[numeric_cols].round(2))

    # ----------------------------------------
    # Revenue Rank
    # ----------------------------------------

    product["revenue_rank"] = (
        product["total_sales"].rank(ascending=False, method="dense").astype(int)
    )

    # ----------------------------------------
    # Profit Rank
    # ----------------------------------------

    product["profit_rank"] = (
        product["total_profit"].rank(ascending=False, method="dense").astype(int)
    )

    # ----------------------------------------
    # Revenue Share
    # ----------------------------------------

    total_revenue = product["total_sales"].sum()

    product["revenue_share_pct"] = (product["total_sales"] / total_revenue * 100).round(2)

    # ----------------------------------------
    # Sort for Pareto
    # ----------------------------------------

    product = (
        product
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )

    # ----------------------------------------
    # Cumulative Revenue
    # ----------------------------------------

    product["cumulative_revenue_pct"] = (
        product["revenue_share_pct"]
        .cumsum()
        .round(2)
    )

    # ----------------------------------------
    # ABC Classification
    # ----------------------------------------

    product["abc_class"] = np.where(
        product["cumulative_revenue_pct"] <= 80,
        "A",
        np.where(
            product["cumulative_revenue_pct"] <= 95,
            "B",
            "C"
        )
    )

    # ----------------------------------------
    # Product Velocity
    # ----------------------------------------

    q1 = product["total_quantity"].quantile(0.33)

    q2 = product["total_quantity"].quantile(0.66)

    conditions = [
        product["total_quantity"] >= q2,
        product["total_quantity"].between(q1, q2),
        product["total_quantity"] < q1
    ]

    labels = [
        "Fast",
        "Medium",
        "Slow"
    ]

    product["product_velocity"] = np.select(
        conditions,
        labels,
        default="Medium"
    )

    # ----------------------------------------
    # Inventory Priority
    # ----------------------------------------

    conditions = [
        (product["abc_class"] == "A") & (product["product_velocity"] == "Fast"),
        (product["abc_class"] == "A"),
        (product["abc_class"] == "B")
    ]

    labels = [
        "Critical",
        "High",
        "Medium"
    ]

    product["inventory_priority"] = np.select(
        conditions,
        labels,
        default="Low"
    )

    product = product.sort_values("revenue_rank").reset_index(drop=True)
    
    validate_table(
        product,
        "Product Metrics"
    )

    return product

# ==========================================================
# Category Metrics
# ==========================================================

def create_category_metrics(df):

    print_section("Creating Category Metrics")

    category = (
        df.groupby("category_name", as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("benefit_per_order", "sum"),
            total_orders=("order_id", "nunique"),
            total_quantity=("order_item_quantity", "sum"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            product_count=("product_name", "nunique")
        )
    )

    category["total_sales"] = category["total_sales"].round(2)

    category["total_profit"] = category["total_profit"].round(2)

    category["avg_margin_pct"] = category["avg_margin_pct"].round(2)

    total_sales = category["total_sales"].sum()

    category["revenue_share_pct"] = (category["total_sales"] / total_sales * 100).round(2)

    category["category_rank"] = (category["total_sales"].rank(ascending=False, method="dense").astype(int))

    category = category.sort_values("category_rank").reset_index(drop=True)
    
    validate_table(category,"Category Metrics")

    return category


# ==========================================================
# Customer Metrics
# ==========================================================

def create_customer_metrics(df):

    print_section("Creating Customer Metrics")

    customer_df = df.copy()

    customer_df["customer_name"] = (
        customer_df["customer_fname"].fillna("").str.strip()+ " "
        +
        customer_df["customer_lname"].fillna("").str.strip()).str.strip()

    customer = (
        customer_df.groupby(["customer_id", "customer_name"],as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("benefit_per_order", "sum"),
            total_orders=("order_id", "nunique"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            first_order_date=("order_date_dateorders", "min"),
            last_order_date=("order_date_dateorders", "max")
        )
    )

    customer["avg_order_value"] = (customer["total_sales"] / customer["total_orders"]).round(2)

    customer["repeat_customer"] = (customer["total_orders"] > 1)

    customer["customer_rank"] = (customer["total_sales"].rank(ascending=False, method="dense").astype(int))

    q1 = customer["total_sales"].quantile(0.25)

    q2 = customer["total_sales"].quantile(0.50)

    q3 = customer["total_sales"].quantile(0.75)

    conditions = [
        customer["total_sales"] >= q3,
        customer["total_sales"] >= q2,
        customer["total_sales"] >= q1
    ]

    labels = [
        "VIP",
        "High Value",
        "Standard"
    ]

    customer["customer_value_tier"] = np.select(
        conditions,
        labels,
        default="Low Value"
    )

    round_cols = [
        "total_sales",
        "total_profit",
        "avg_margin_pct"
    ]

    customer[round_cols] = (customer[round_cols].round(2))

    customer = customer.sort_values("customer_rank").reset_index(drop=True)
    
    validate_table(customer, "Customer Metrics")

    return customer


# ==========================================================
# Market Metrics
# ==========================================================

def create_market_metrics(df):

    print_section("Creating Market Metrics")

    market = (
        df.groupby("market", as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("benefit_per_order", "sum"),
            total_orders=("order_id", "nunique"),
            total_customers=("customer_id", "nunique"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            first_order_date=("order_date_dateorders", "min"),
            last_order_date=("order_date_dateorders", "max")
        )
    )

    market["avg_order_value"] = (market["total_sales"] / market["total_orders"]).round(2)

    total_sales = market["total_sales"].sum()

    market["revenue_share_pct"] = (market["total_sales"] / total_sales * 100).round(2)

    market["market_rank"] = (market["total_sales"].rank(ascending=False, method="dense").astype(int))

    q1 = market["total_sales"].quantile(0.33)

    q2 = market["total_sales"].quantile(0.66)

    conditions = [
        market["total_sales"] >= q2,
        market["total_sales"] >= q1
    ]

    labels = [
        "Tier 1",
        "Tier 2"
    ]

    market["market_tier"] = np.select(conditions, labels, default="Tier 3")

    round_cols = [
        "total_sales",
        "total_profit",
        "avg_margin_pct"
    ]

    market[round_cols] = (market[round_cols].round(2))

    market = market.sort_values("market_rank").reset_index(drop=True)
    
    validate_table(market, "Market Metrics")

    return market


# ==========================================================
# Main
# ==========================================================

def main():

    print_section("Business Metrics Pipeline")

    df = load_data()

    product_metrics = create_product_metrics(df)
    category_metrics = create_category_metrics(df)
    customer_metrics = create_customer_metrics(df)
    market_metrics = create_market_metrics(df)

    save_table(
        product_metrics,
        "product_metrics.csv"
    )

    save_table(
        category_metrics,
        "category_metrics.csv"
    )

    save_table(
        customer_metrics,
        "customer_metrics.csv"
    )

    save_table(
        market_metrics,
        "market_metrics.csv"
    )

    print_section("Pipeline Completed")

    print_success("Business metrics generated successfully")


if __name__ == "__main__":
    main()