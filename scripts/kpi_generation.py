from pathlib import Path

import pandas as pd

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_DIR = DATA_DIR


# ==========================================================
# Helper Functions
# ==========================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)


def print_success(msg):
    print(f"✓ {msg}")


def load_tables():
    print_section("Loading Tables")

    fact = pd.read_csv(DATA_DIR / "supply_chain_features.csv")
    product = pd.read_csv(DATA_DIR / "product_metrics.csv")
    customer = pd.read_csv(DATA_DIR / "customer_metrics.csv")
    category = pd.read_csv(DATA_DIR / "category_metrics.csv")
    market = pd.read_csv(DATA_DIR / "market_metrics.csv")

    print_success("All tables loaded")

    return fact, product, customer, category, market


def create_kpi_table(kpis):
    return pd.DataFrame({
        "kpi_name": list(kpis.keys()),
        "kpi_value": list(kpis.values())
    })


def save_table(df, filename):
    df.to_csv(OUTPUT_DIR / filename, index=False)

    print_success(f"{filename} saved")


# ==========================================================
# Executive KPIs
# ==========================================================

def create_executive_kpis(fact, product, customer):
    total_revenue = fact["sales"].sum()

    total_profit = fact["benefit_per_order"].sum()

    total_orders = fact["order_id"].nunique()

    total_customers = customer.shape[0]

    total_products = product.shape[0]

    avg_order_value = (total_revenue / total_orders)

    avg_selling_price = (fact["average_selling_price"].mean())

    avg_discount = (fact["discount_pct"].mean())

    avg_margin = (fact["profit_margin_pct"].mean())

    on_time_pct = (fact["on_time_delivery"].mean() * 100)

    avg_delay = (fact["shipping_delay_days"].mean())

    loss_orders = (fact["loss_making_order"].mean() * 100)

    kpis = {
        "Total Revenue": round(total_revenue, 2),
        "Total Profit": round(total_profit, 2),
        "Profit Margin %": round(avg_margin, 2),
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Total Products": total_products,
        "Average Order Value": round(avg_order_value, 2),
        "Average Selling Price": round(avg_selling_price, 2),
        "Average Discount %": round(avg_discount, 2),
        "On-Time Delivery %": round(on_time_pct, 2),
        "Average Shipping Delay": round(avg_delay, 2),
        "Loss Making Orders %": round(loss_orders, 2)
    }

    return create_kpi_table(kpis)


# ==========================================================
# Logistics KPIs
# ==========================================================

def create_logistics_kpis(fact):
    total_orders = len(fact)

    late_pct = (fact["late_delivery"].mean() * 100)

    early_pct = (fact["early_delivery"].mean() * 100)

    sla_pct = ((fact["sla_compliance"] == "Met").mean() * 100)

    fast_pct = ((fact["processing_speed"] == "Fast").mean() * 100)

    slow_pct = ((fact["processing_speed"] == "Slow").mean() * 100)

    severe_delay = ((fact["delay_severity"] == "4+ Days Late").sum())

    avg_processing = (fact["order_processing_days"].mean())

    avg_delay = (fact["shipping_delay_days"].mean())

    avg_delay_pct = (fact["delay_pct"].mean())

    kpis = {
        "Total Orders": total_orders,
        "Late Deliveries %": round(late_pct, 2),
        "Early Deliveries %": round(early_pct, 2),
        "SLA Compliance %": round(sla_pct, 2),
        "Fast Processing %": round(fast_pct, 2),
        "Slow Processing %": round(slow_pct, 2),
        "Average Processing Days": round(avg_processing, 2),
        "Average Shipping Delay": round(avg_delay, 2),
        "Average Delay %": round(avg_delay_pct, 2),
        "Severe Delay Orders": int(severe_delay)
    }

    return create_kpi_table(kpis)

# ==========================================================
# Inventory KPIs
# ==========================================================

def create_inventory_kpis(product):

    total_products = len(product)

    abc_a = (product["abc_class"] == "A").sum()
    abc_b = (product["abc_class"] == "B").sum()
    abc_c = (product["abc_class"] == "C").sum()

    critical = (product["inventory_priority"] == "Critical").sum()
    high = (product["inventory_priority"] == "High").sum()
    medium = (product["inventory_priority"] == "Medium").sum()
    low = (product["inventory_priority"] == "Low").sum()

    fast = (product["product_velocity"] == "Fast").sum()
    medium_velocity = (product["product_velocity"] == "Medium").sum()
    slow = (product["product_velocity"] == "Slow").sum()

    kpis = {
        "Total Products": total_products,
        "ABC Class A Products": abc_a,
        "ABC Class B Products": abc_b,
        "ABC Class C Products": abc_c,
        "Critical Priority Products": critical,
        "High Priority Products": high,
        "Medium Priority Products": medium,
        "Low Priority Products": low,
        "Fast Moving Products": fast,
        "Medium Moving Products": medium_velocity,
        "Slow Moving Products": slow
    }

    return create_kpi_table(kpis)


# ==========================================================
# Customer KPIs
# ==========================================================

def create_customer_kpis(customer):

    total_customers = len(customer)

    repeat = customer["repeat_customer"].sum()

    repeat_rate = (repeat / total_customers * 100)

    vip = (customer["customer_value_tier"] == "VIP").sum()

    high = (customer["customer_value_tier"] == "High Value").sum()

    standard = (customer["customer_value_tier"] == "Standard").sum()

    low = (customer["customer_value_tier"] == "Low Value").sum()

    avg_revenue = (customer["total_sales"].mean())

    avg_profit = (customer["total_profit"].mean())

    avg_orders = (customer["total_orders"].mean())

    kpis = {
        "Total Customers": total_customers,
        "Repeat Customers": int(repeat),
        "Repeat Customer Rate %": round(repeat_rate,2),
        "VIP Customers": int(vip),
        "High Value Customers": int(high),
        "Standard Customers": int(standard),
        "Low Value Customers": int(low),
        "Average Customer Revenue": round(avg_revenue,2),
        "Average Customer Profit": round(avg_profit,2),
        "Average Orders Per Customer": round(avg_orders,2)
    }

    return create_kpi_table(kpis)


# ==========================================================
# Product KPIs
# ==========================================================

def create_product_kpis(product):

    avg_revenue = product["total_sales"].mean()

    avg_profit = product["total_profit"].mean()

    avg_margin = product["avg_margin_pct"].mean()

    above_avg = (product["total_sales"] > avg_revenue).sum()

    below_avg = (product["total_sales"] <= avg_revenue).sum()

    top_revenue = (product["total_sales"].max())

    top_profit = (product["total_profit"].max())

    highest_share = (product["revenue_share_pct"].max())

    avg_discount = (product["avg_discount_pct"].mean())

    kpis = {
        "Average Product Revenue": round(avg_revenue,2),
        "Average Product Profit": round(avg_profit,2),
        "Average Product Margin %": round(avg_margin,2),
        "Average Product Discount %": round(avg_discount,2),
        "Highest Product Revenue": round(top_revenue,2),
        "Highest Product Profit": round(top_profit,2),
        "Highest Revenue Share %": round(highest_share,2),
        "Products Above Average Revenue": int(above_avg),
        "Products Below Average Revenue": int(below_avg),
        "Average Revenue Share %": round(product["revenue_share_pct"].mean(),2)
    }

    return create_kpi_table(kpis)


# ==========================================================
# Main
# ==========================================================

def main():

    print_section("KPI Generation Pipeline")

    fact, product, customer, category, market = load_tables()

    executive = create_executive_kpis(fact, product, customer)
    logistics = create_logistics_kpis(fact)
    inventory = create_inventory_kpis(product)
    customer_kpis = create_customer_kpis(customer)
    product_kpis = create_product_kpis(product)

    save_table(executive, "executive_kpis.csv")
    save_table(logistics, "logistics_kpis.csv")
    save_table(inventory, "inventory_kpis.csv")
    save_table(customer_kpis, "customer_kpis.csv")
    save_table(product_kpis, "product_kpis.csv")

    print_section("Pipeline Completed")

    print_success("KPI tables generated successfully")


if __name__ == "__main__":
    main()