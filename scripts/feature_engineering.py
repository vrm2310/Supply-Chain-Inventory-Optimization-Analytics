# ==========================================================
# Imports
# ==========================================================

from pathlib import Path

import numpy as np
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

PROJECT_NAME = "Supply Chain & Inventory Optimization Analytics Platform"

DATE_COLUMNS = [
    "order_date_dateorders",
    "shipping_date_dateorders"
]

SHIPPING_SCORE_PENALTY = 10

REVENUE_BAND_LABELS = [
    "Low",
    "Medium",
    "High",
    "Premium"
]

ORDER_SIZE_LABELS = [
    "Small",
    "Medium",
    "Large",
    "Bulk"
]

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_supply_chain.csv"
)

OUTPUT_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "supply_chain_features.csv"
)

# ==========================================================
# Helper Functions
# ==========================================================

def print_section(title: str) -> None:
    """Print section heading."""

    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)


def print_success(message: str) -> None:
    """Print success message."""

    print(f"✓ {message}")


def print_info(message: str) -> None:
    """Print informational message."""

    print(f"• {message}")


# ==========================================================
# Load Dataset
# ==========================================================

def load_data(filepath: Path) -> pd.DataFrame:
    """
    Load cleaned supply chain dataset.
    """

    print_section("Loading Dataset")

    try:

        df = pd.read_csv(
            filepath,
            parse_dates=DATE_COLUMNS
        )

        print_success("Dataset loaded successfully")

        print_info(f"Rows    : {len(df):,}")
        print_info(f"Columns : {df.shape[1]}")

        return df

    except Exception as e:

        raise RuntimeError(
            f"Unable to load dataset.\n{e}"
        )


# ==========================================================
# Validation
# ==========================================================

def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Ensure required columns exist before
    feature engineering starts.
    """

    print_section("Validating Dataset")

    required_columns = [

        # Dates
        "order_date_dateorders",
        "shipping_date_dateorders",

        # Shipping
        "days_for_shipping_real",
        "days_for_shipment_scheduled",

        # Finance
        "benefit_per_order",
        "sales",
        "order_item_discount",

        # Order
        "order_item_quantity",

        # Category
        "category_name",

        # Product
        "product_name"

    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing required columns:\n{missing}"
        )

    print_success("All required columns found")


# ==========================================================
# Dataset Snapshot
# ==========================================================

def dataset_snapshot(df: pd.DataFrame) -> None:
    """
    Display dataset overview before
    feature engineering.
    """

    print_section("Dataset Snapshot")

    print_info(f"Rows : {len(df):,}")
    print_info(f"Columns : {df.shape[1]}")

    memory = (
        df.memory_usage(deep=True).sum()
        / 1024 ** 2
    )

    print_info(f"Memory : {memory:.2f} MB")

    print_info(
        f"Missing Values : {df.isnull().sum().sum():,}"
    )


# ==========================================================
# Feature Validation
# ==========================================================

def validate_features(
    df: pd.DataFrame,
    original_columns: int
) -> pd.DataFrame:
    """
    Validate engineered dataset and
    generate ETL summary.
    """

    print_section("Feature Engineering Summary")

    new_columns = df.shape[1]

    new_features = new_columns - original_columns

    print("\nInput Dataset")
    print("-" * 30)

    print(f"Rows               : {len(df):,}")
    print(f"Columns Before     : {original_columns}")

    print("\nOutput Dataset")
    print("-" * 30)

    print(f"Columns After      : {new_columns}")
    print(f"New Features       : {new_features}")

    print("\nData Quality")
    print("-" * 30)

    missing = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()

    infinite = (
        np.isinf(
            df.select_dtypes(include=np.number)
        ).sum().sum()
    )

    print(f"Missing Values     : {missing:,}")

    print(f"Duplicate Rows     : {duplicate_rows:,}")

    print(f"Infinite Values    : {infinite:,}")

    memory = (
        df.memory_usage(deep=True).sum()
        / 1024**2
    )

    print(f"Memory Usage       : {memory:.2f} MB")

    if missing == 0:
        print_success("No missing values")

    if duplicate_rows == 0:
        print_success("No duplicate rows")

    if infinite == 0:
        print_success("No infinite values")

    print_success("Feature engineering completed")

    return df


# ==========================================================
# Save Dataset
# ==========================================================

def save_data(
    df: pd.DataFrame,
    filepath: Path
):

    print_section("Saving Dataset")

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        filepath,
        index=False
    )

    print_success("Dataset exported successfully")

    print_info(filepath)

    print()

    print("=" * 60)

    print("FEATURE ENGINEERING PIPELINE COMPLETED")

    print("=" * 60)


# ==========================================================
# Time Intelligence Features
# ==========================================================

def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create calendar and time-based analytical features.
    """

    print_section("Time Intelligence Features")

    order_date = df["order_date_dateorders"]

    df["order_year"] = order_date.dt.year

    df["order_quarter"] = (
        "Q" + order_date.dt.quarter.astype(str)
    )

    df["order_month"] = order_date.dt.month_name()

    df["month_number"] = order_date.dt.month

    df["order_week"] = (
        order_date.dt.isocalendar()
        .week
        .astype(int)
    )

    df["day_of_week"] = order_date.dt.day_name()

    df["day_number"] = order_date.dt.day

    df["is_weekend"] = (
        order_date.dt.dayofweek >= 5
    )

    print_success("Created 8 time intelligence features")

    return df


# ==========================================================
# Shipping & Logistics Features
# ==========================================================

def create_shipping_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create shipping performance metrics.
    """

    print_section("Shipping & Logistics Features")

    actual = df["days_for_shipping_real"]

    scheduled = df["days_for_shipment_scheduled"]

    # --------------------------------------
    # Shipping Delay
    # --------------------------------------

    df["shipping_delay_days"] = (
        actual - scheduled
    )

    # --------------------------------------
    # Delivery Status Flags
    # --------------------------------------

    df["on_time_delivery"] = (
        df["shipping_delay_days"] <= 0
    )

    df["early_delivery"] = (
        df["shipping_delay_days"] < 0
    )

    df["late_delivery"] = (
        df["shipping_delay_days"] > 0
    )

    # --------------------------------------
    # Delay Severity
    # --------------------------------------

    conditions = [
        df["shipping_delay_days"] < 0,
        df["shipping_delay_days"] == 0,
        df["shipping_delay_days"] == 1,
        df["shipping_delay_days"].between(2, 3),
        df["shipping_delay_days"] >= 4
    ]

    labels = [
        "Early",
        "On Time",
        "1 Day Late",
        "2-3 Days Late",
        "4+ Days Late"
    ]

    df["delay_severity"] = np.select(
        conditions,
        labels,
        default="Unknown"
    )

    # --------------------------------------
    # SLA Compliance
    # --------------------------------------

    df["sla_compliance"] = np.where(
        df["shipping_delay_days"] <= 0,
        "Met",
        "Breached"
    )

    # --------------------------------------
    # Delay Percentage
    # --------------------------------------

    df["delay_pct"] = (
        (
            df["shipping_delay_days"]
            / scheduled.replace(0, np.nan)
        )
        * 100
    ).round(2)

    df["delay_pct"] = (
        df["delay_pct"]
        .fillna(0)
    )

    # --------------------------------------
    # Fulfillment Speed
    # --------------------------------------

    df["fulfillment_speed"] = pd.cut(

        actual,

        bins=[0, 2, 4, np.inf],

        labels=[
            "Fast",
            "Standard",
            "Slow"
        ],

        include_lowest=True

    )

    print_success("Created 8 shipping features")

    return df


# ==========================================================
# Financial Analytics Features
# ==========================================================

def create_financial_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create financial and profitability features.
    """

    print_section("Financial Analytics Features")

    sales = df["sales"]

    profit = df["benefit_per_order"]

    quantity = df["order_item_quantity"]

    discount = df["order_item_discount"]

    # --------------------------------------------------
    # Profit Margin %
    # --------------------------------------------------

    df["profit_margin_pct"] = np.where(
        sales > 0,
        (profit / sales) * 100,
        0
    ).round(2)

    # --------------------------------------------------
    # Discount %
    # --------------------------------------------------

    df["discount_pct"] = np.where(
        sales > 0,
        (discount / sales) * 100,
        0
    ).round(2)

    # --------------------------------------------------
    # Average Selling Price
    # --------------------------------------------------

    df["average_selling_price"] = np.where(
        quantity > 0,
        sales / quantity,
        0
    ).round(2)

    # --------------------------------------------------
    # Effective Selling Price
    # --------------------------------------------------

    df["effective_sale_price"] = np.where(
        quantity > 0,
        (sales - discount) / quantity,
        0
    ).round(2)

    # --------------------------------------------------
    # Profit Per Unit
    # --------------------------------------------------

    df["profit_per_unit"] = np.where(
        quantity > 0,
        profit / quantity,
        0
    ).round(2)

    # --------------------------------------------------
    # Loss Making Order
    # --------------------------------------------------

    df["loss_making_order"] = (
        profit < 0
    )

    # --------------------------------------------------
    # High Discount Order
    # --------------------------------------------------

    HIGH_DISCOUNT_THRESHOLD = 20

    df["high_discount_order"] = (
        df["discount_pct"]
        >= HIGH_DISCOUNT_THRESHOLD
    )

    # --------------------------------------------------
    # Profitability Tier
    # --------------------------------------------------

    conditions = [
    df["profit_margin_pct"] < 0,
    df["profit_margin_pct"].between(0, 10, inclusive="left"),
    df["profit_margin_pct"].between(10, 20, inclusive="left"),
    df["profit_margin_pct"].between(20, 40, inclusive="left"),
    df["profit_margin_pct"] >= 40
    ]

    labels = [
    "Negative",
    "Low Margin",
    "Medium Margin",
    "High Margin",
    "Excellent Margin"
    ]

    df["profitability_tier"] = np.select(
        conditions,
        labels,
        default="Unknown"
    )

    print_success("Created 8 financial features")

    return df


# ==========================================================
# Order Analytics Features
# ==========================================================

def create_order_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create order behaviour features.
    """

    print_section("Order Analytics Features")

    quantity = df["order_item_quantity"]

    # --------------------------------------------------
    # Order Size Band
    # --------------------------------------------------

    conditions = [
        quantity == 1,
        quantity.between(2, 3),
        quantity == 4,
        quantity >= 5
    ]

    labels = [
        "Single",
        "Small",
        "Medium",
        "Bulk"
    ]

    df["order_size_band"] = np.select(
        conditions,
        labels,
        default="Unknown"
    )

    # --------------------------------------------------
    # Multi Item Order
    # --------------------------------------------------

    df["multi_item_order"] = (
        quantity > 1
    )

    # --------------------------------------------------
    # Order Processing Time
    # --------------------------------------------------

    df["order_processing_days"] = (
        (
            df["shipping_date_dateorders"]
            - df["order_date_dateorders"]
        )
        .dt.days
    )

    # --------------------------------------------------
    # Processing Speed
    # --------------------------------------------------

    conditions = [
        df["order_processing_days"] <= 2,
        df["order_processing_days"].between(3, 5),
        df["order_processing_days"] > 5
    ]

    labels = [
        "Fast",
        "Standard",
        "Slow"
    ]

    df["processing_speed"] = np.select(
        conditions,
        labels,
        default="Unknown"
    )

    print_success("Created 4 order features")

    return df


# ==========================================================
# Main
# ==========================================================

def main():

    print_section(PROJECT_NAME)

    df = load_data(INPUT_DATA)

    validate_required_columns(df)

    dataset_snapshot(df)

    original_columns = df.shape[1]

    # -----------------------------------
    # Time Intelligence
    # -----------------------------------

    df = create_time_features(df)

    # -----------------------------------
    # Shipping
    # -----------------------------------

    df = create_shipping_features(df)

    # -----------------------------------
    # Financial
    # -----------------------------------

    df = create_financial_features(df)

    # -----------------------------------
    # Order Analytics
    # -----------------------------------

    df = create_order_features(df)

    validate_features(
        df,
        original_columns
    )

    save_data(
        df,
        OUTPUT_DATA
    )


if __name__ == "__main__":
    main()