"""
===========================================================
Supply Chain & Inventory Optimization Analytics Platform
Data Cleaning & Data Profiling
===========================================================

Author: Vyom Mangtani
Project: Supply Chain & Inventory Optimization Analytics Platform

Description:
This script performs initial data profiling and cleaning on the
DataCo Supply Chain dataset before feature engineering.

Outputs:
    data/processed/cleaned_supply_chain.csv
===========================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re

# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "DataCoSupplyChainDataset.csv"
OUTPUT_DATA = BASE_DIR / "data" / "processed" / "cleaned_supply_chain.csv"

# ----------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def load_data(filepath):
    """Load CSV dataset."""
    try:
        df = pd.read_csv(filepath, encoding="latin1")
        print(f"Dataset loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading dataset:\n{e}")
        raise


def basic_info(df):
    """Display basic dataset information."""

    print_section("DATASET OVERVIEW")

    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")
    print(f"Memory  : {df.memory_usage(deep=True).sum()/1024**2:.2f} MB")


def data_types(df):

    print_section("COLUMN DATA TYPES")

    summary = pd.DataFrame({
        "Data Type": df.dtypes,
        "Missing Values": df.isnull().sum(),
        "Missing %": round(df.isnull().mean()*100,2),
        "Unique Values": df.nunique()
    })

    print(summary)


def duplicate_report(df):

    print_section("DUPLICATE ANALYSIS")

    duplicates = df.duplicated().sum()

    print(f"Duplicate Rows : {duplicates:,}")
    print(f"Duplicate %    : {(duplicates/len(df))*100:.2f}%")


def missing_report(df):

    print_section("MISSING VALUE REPORT")

    missing = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing %": round(df.isnull().mean()*100,2)
    })

    missing = missing[missing["Missing Count"] > 0]

    if missing.empty:
        print("No missing values.")
    else:
        print(missing.sort_values("Missing %", ascending=False))


def numeric_summary(df):

    print_section("NUMERIC SUMMARY")

    print(df.describe().T)


def categorical_summary(df):

    print_section("CATEGORICAL SUMMARY")

    categorical_cols = df.select_dtypes(include=["object", "string", "category"]).columns

    summary = []

    for col in categorical_cols:

        summary.append({
            "Column": col,
            "Unique Values": df[col].nunique(),
            "Top Value": df[col].mode(dropna=False)[0],
            "Frequency": df[col].value_counts(dropna=False).iloc[0]
        })

    print(pd.DataFrame(summary))


def date_analysis(df):

    print_section("DATE ANALYSIS")

    date_columns = [
        "order date (DateOrders)",
        "shipping date (DateOrders)"
    ]

    for col in date_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(df[col], errors="coerce")

            print(f"\n{col}")

            print(f"Earliest : {df[col].min()}")

            print(f"Latest   : {df[col].max()}")

            print(f"Missing  : {df[col].isnull().sum()}")


def cardinality_report(df):

    print_section("HIGH CARDINALITY COLUMNS")

    cardinality = df.nunique().sort_values(ascending=False)

    print(cardinality.head(20))


def business_validation(df):

    print_section("BUSINESS VALIDATION")

    if "Sales" in df.columns:
        print(f"Negative Sales : {(df['Sales'] < 0).sum()}")

    if "Order Item Quantity" in df.columns:
        print(f"Negative Quantity : {(df['Order Item Quantity'] < 0).sum()}")

    if "Order Profit Per Order" in df.columns:
        print(f"Negative Profit Orders : {(df['Order Profit Per Order'] < 0).sum()}")

    if "Benefit per order" in df.columns:
        print(f"Negative Benefit : {(df['Benefit per order'] < 0).sum()}")


def clean_data(df):

    df = drop_irrelevant_columns(df)

    df = rename_columns(df)

    df = convert_data_types(df)

    df = standardize_text(df)

    df = handle_missing_values(df)

    df, verified = verify_duplicate_columns(df)

    df = remove_duplicate_columns(df, verified)

    df = optimize_memory(df)

    df = validate_dataset(df)

    return df


def drop_irrelevant_columns(df):

    print_section("DROPPING IRRELEVANT COLUMNS")

    columns_to_drop = [
        "Product Description",
        "Order Zipcode",
        "Customer Email",
        "Customer Password",
        "Product Status"
    ]

    existing = [col for col in columns_to_drop if col in df.columns]

    df = df.drop(columns=existing)

    print(f"Dropped {len(existing)} columns.")

    return df


def rename_columns(df):

    print_section("RENAMING COLUMNS")

    new_columns = {}

    for col in df.columns:

        new_name = (
            col.lower()
            .replace("(", "")
            .replace(")", "")
            .replace("/", "_")
            .replace("-", "_")
            .replace("%", "percent")
            .replace(".", "")
        )

        new_name = re.sub(r"[^a-z0-9]+", "_", new_name)
        new_name = re.sub(r"_+", "_", new_name)
        new_name = new_name.strip("_")

        new_columns[col] = new_name

    df = df.rename(columns=new_columns)

    print("Column names converted to snake_case.")

    return df


def convert_data_types(df):

    print_section("CONVERTING DATA TYPES")

    date_columns = [
        "order_date_dateorders",
        "shipping_date_dateorders"
    ]

    for col in date_columns:

        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    print("Date columns converted.")

    return df


def standardize_text(df):

    print_section("STANDARDIZING TEXT")

    text_columns = df.select_dtypes(include=["object", "string"]).columns

    for col in text_columns:

        df[col] = df[col].astype(str).str.strip()

    print("Whitespace removed.")

    return df


def handle_missing_values(df):

    print_section("HANDLING MISSING VALUES")

    if "customer_lname" in df.columns:
        df["customer_lname"] = df["customer_lname"].fillna("Unknown")

    if "customer_zipcode" in df.columns:
        df["customer_zipcode"] = (
            df["customer_zipcode"]
            .fillna(-1)
            .astype("Int64")
        )

    print(f"Remaining Missing Values: {df.isnull().sum().sum()}")

    return df


def verify_duplicate_columns(df):

    print_section("VERIFYING DUPLICATE COLUMNS")

    duplicate_pairs = [
        ("customer_id", "order_customer_id"),
        ("category_id", "product_category_id"),
        ("benefit_per_order", "order_profit_per_order"),
        ("order_item_product_price", "product_price"),
        ("sales_per_customer", "order_item_total"),
        ("order_item_cardprod_id", "product_card_id")
    ]

    verified = []

    for col1, col2 in duplicate_pairs:

        if col1 in df.columns and col2 in df.columns:

            identical = df[col1].fillna("__NA__").astype(str).equals(
                df[col2].fillna("__NA__").astype(str)
            )

            print(f"{col1} == {col2}: {identical}")

            if identical:
                verified.append(col2)

    return df, verified


def remove_duplicate_columns(df, verified):

    print_section("REMOVING DUPLICATE COLUMNS")

    df = df.drop(columns=verified)

    print(f"Dropped {len(verified)} duplicate columns.")

    return df


def optimize_memory(df):

    print_section("OPTIMIZING MEMORY")

    categorical_cols = [
        "type",
        "delivery_status",
        "customer_segment",
        "market",
        "shipping_mode",
        "order_status",
        "department_name",
        "category_name"
    ]

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    print(
        f"Memory Usage: "
        f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
    )

    return df


def validate_dataset(df):

    print_section("FINAL VALIDATION")

    print(f"Rows : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    print(f"Missing Values : {df.isnull().sum().sum():,}")

    print("Validation complete.")

    return df


def save_data(df, filepath):

    filepath.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(filepath, index=False)

    print_section("OUTPUT")

    print(f"Cleaned dataset saved to:\n{filepath}")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():

    print_section("SUPPLY CHAIN DATA CLEANING & PROFILING")

    df = load_data(RAW_DATA)

    basic_info(df)

    data_types(df)

    duplicate_report(df)

    missing_report(df)

    numeric_summary(df)

    categorical_summary(df)

    date_analysis(df)

    cardinality_report(df)

    business_validation(df)

    df = clean_data(df)

    save_data(df, OUTPUT_DATA)


if __name__ == "__main__":
    main()