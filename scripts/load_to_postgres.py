from pathlib import Path
from urllib.parse import quote_plus
import os

import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv

# ==========================================================
# Configuration
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (BASE_DIR/"data"/"processed")

SCHEMA_NAME = "supply_chain"

load_dotenv(BASE_DIR/".env")

# ==========================================================
# Table Mapping
# ==========================================================

TABLE_MAPPING = {
    "fact_orders": "supply_chain_features.csv",
    "dim_products": "product_metrics.csv",
    "dim_categories": "category_metrics.csv",
    "dim_customers": "customer_metrics.csv",
    "dim_markets": "market_metrics.csv",
    "kpi_executive": "executive_kpis.csv",
    "kpi_inventory": "inventory_kpis.csv",
    "kpi_logistics": "logistics_kpis.csv",
    "kpi_customer": "customer_kpis.csv",
    "kpi_product": "product_kpis.csv"
}

# ==========================================================
# Helper Functions
# ==========================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)


def print_success(msg):
    print(f"[SUCCESS] {msg}")


def print_info(msg):
    print(f"[INFO] {msg}")


# ==========================================================
# PostgreSQL Connection
# ==========================================================

def create_database_engine():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")

    password = quote_plus(os.getenv("DB_PASSWORD"))

    database_url = (
        f"postgresql+psycopg2://"
        f"{user}:{password}"
        f"@{host}:{port}/{database}"
    )

    engine = create_engine(database_url, future=True)

    return engine


# ==========================================================
# Connection Test
# ==========================================================

def test_connection(engine):
    print_section("Testing PostgreSQL Connection")

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        print_success("Connection successful")

    except SQLAlchemyError as e:
        raise RuntimeError(f"Database connection failed.\n{e}")


# ==========================================================
# Read CSV
# ==========================================================

def load_csv(filename):
    filepath = DATA_DIR / filename

    df = pd.read_csv(filepath)

    return df


# ==========================================================
# Truncate Table
# ==========================================================

def truncate_table(engine, table_name):
    with engine.begin() as conn:
        conn.execute(
            text(
                f"""
                TRUNCATE TABLE
                {SCHEMA_NAME}.{table_name}
                RESTART IDENTITY;
                """
            )
        )


# ==========================================================
# Load Single Table
# ==========================================================

def load_table(engine, table_name, filename):
    df = load_csv(filename)

    truncate_table(
        engine,
        table_name
    )

    df.to_sql(
        table_name,
        con=engine,
        schema=SCHEMA_NAME,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000
    )

    return len(df)

# ==========================================================
# Verify Table Load
# ==========================================================

def verify_table(engine, table_name, expected_rows):
    query = text(
        f"""
        SELECT COUNT(*)
        FROM {SCHEMA_NAME}.{table_name};
        """
    )

    with engine.connect() as conn:
        actual_rows = conn.execute(query).scalar()

    if actual_rows != expected_rows:

        raise ValueError(
            f"{table_name}: Expected "
            f"{expected_rows:,} rows "
            f"but found "
            f"{actual_rows:,}"
        )

    print_success(
        f"{table_name:<20} "
        f"{actual_rows:,} rows"
    )


# ==========================================================
# Load All Tables
# ==========================================================

def load_all_tables(engine):

    print_section("Loading Tables")

    load_order = [
        "fact_orders",
        "dim_products",
        "dim_categories",
        "dim_customers",
        "dim_markets",
        "kpi_executive",
        "kpi_inventory",
        "kpi_logistics",
        "kpi_customer",
        "kpi_product"
    ]

    total_rows = 0

    for table_name in load_order:

        filename = TABLE_MAPPING[table_name]

        rows = load_table(engine, table_name, filename)

        verify_table(engine, table_name, rows)

        total_rows += rows

    return total_rows


# ==========================================================
# Pipeline Summary
# ==========================================================

def print_summary(total_rows):
    print_section("Pipeline Summary")

    print_success("All tables loaded successfully")

    print_info(f"Tables Loaded : {len(TABLE_MAPPING)}")

    print_info(f"Rows Imported : {total_rows:,}")


# ==========================================================
# Main
# ==========================================================

def main():
    print_section("PostgreSQL Loader")

    engine = create_database_engine()

    test_connection(engine)

    total_rows = load_all_tables(engine)

    print_summary(total_rows)


if __name__ == "__main__":
    main()