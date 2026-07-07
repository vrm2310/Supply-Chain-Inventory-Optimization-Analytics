SET search_path TO supply_chain;

-------------------------------------------------------------
-- FACT TABLE
-------------------------------------------------------------

CREATE TABLE fact_orders (
    order_item_id                 INTEGER PRIMARY KEY,
    type                          TEXT,
    days_for_shipping_real        INTEGER,
    days_for_shipment_scheduled   INTEGER,
    benefit_per_order             NUMERIC(12,2),
    sales_per_customer            NUMERIC(12,2),
    delivery_status               TEXT,
    late_delivery_risk            INTEGER,
    category_id                   INTEGER,
    category_name                 TEXT,
    customer_city                 TEXT,
    customer_country              TEXT,
    customer_fname                TEXT,
    customer_id                   INTEGER,
    customer_lname                TEXT,
    customer_segment              TEXT,
    customer_state                TEXT,
    customer_street               TEXT,
    customer_zipcode              TEXT,
    department_id                 INTEGER,
    department_name               TEXT,
    latitude                      DOUBLE PRECISION,
    longitude                     DOUBLE PRECISION,
    market                        TEXT,
    order_city                    TEXT,
    order_country                 TEXT,
    order_date_dateorders         DATE,
    order_id                      INTEGER,
    order_item_cardprod_id        INTEGER,
    order_item_discount           NUMERIC(12,2),
    order_item_discount_rate      NUMERIC(6,4),
    order_item_product_price      NUMERIC(12,2),
    order_item_profit_ratio       NUMERIC(8,4),
    order_item_quantity           INTEGER,
    sales                         NUMERIC(12,2),
    order_region                  TEXT,
    order_state                   TEXT,
    order_status                  TEXT,
    product_image                 TEXT,
    product_name                  TEXT,
    shipping_date_dateorders      DATE,
    shipping_mode                 TEXT,
    order_year                    INTEGER,
    order_quarter                 TEXT,
    order_month                   TEXT,
    month_number                  INTEGER,
    order_week                    INTEGER,
    day_of_week                   TEXT,
    day_number                    INTEGER,
    is_weekend                    BOOLEAN,
    shipping_delay_days           INTEGER,
    on_time_delivery              BOOLEAN,
    early_delivery                BOOLEAN,
    late_delivery                 BOOLEAN,
    delay_severity                TEXT,
    sla_compliance                TEXT,
    delay_pct                     NUMERIC(8,2),
    fulfillment_speed             TEXT,
    profit_margin_pct             NUMERIC(8,2),
    discount_pct                  NUMERIC(8,2),
    average_selling_price         NUMERIC(12,2),
    effective_sale_price          NUMERIC(12,2),
    profit_per_unit               NUMERIC(12,2),
    loss_making_order             BOOLEAN,
    high_discount_order           BOOLEAN,
    profitability_tier            TEXT,
    order_size_band               TEXT,
    multi_item_order              BOOLEAN,
    order_processing_days         INTEGER,
    processing_speed              TEXT
);

-------------------------------------------------------------
-- PRODUCT DIMENSION
-------------------------------------------------------------

CREATE TABLE dim_products (
    product_name                  TEXT PRIMARY KEY,
    category_name                 TEXT,
    total_sales                   NUMERIC(14,2),
    total_profit                  NUMERIC(14,2),
    total_orders                  INTEGER,
    total_quantity                INTEGER,
    avg_selling_price             NUMERIC(10,2),
    avg_discount_pct              NUMERIC(6,2),
    avg_margin_pct                NUMERIC(6,2),
    revenue_rank                  INTEGER,
    profit_rank                   INTEGER,
    revenue_share_pct             NUMERIC(8,2),
    cumulative_revenue_pct        NUMERIC(8,2),
    abc_class                     CHAR(1),
    product_velocity              TEXT,
    inventory_priority            TEXT,
    last_order_date               DATE
);

-------------------------------------------------------------
-- CATEGORY DIMENSION
-------------------------------------------------------------

CREATE TABLE dim_categories (
    category_name                 TEXT PRIMARY KEY,
    total_sales                   NUMERIC(14,2),
    total_profit                  NUMERIC(14,2),
    total_orders                  INTEGER,
    total_quantity                INTEGER,
    avg_margin_pct                NUMERIC(6,2),
    revenue_share_pct             NUMERIC(8,2),
    category_rank                 INTEGER,
    product_count                 INTEGER
);

-------------------------------------------------------------
-- CUSTOMER DIMENSION
-------------------------------------------------------------

CREATE TABLE dim_customers (
    customer_id                   INTEGER PRIMARY KEY,
    customer_name                 TEXT,
    total_sales                   NUMERIC(14,2),
    total_profit                  NUMERIC(14,2),
    total_orders                  INTEGER,
    avg_margin_pct                NUMERIC(6,2),
    avg_order_value               NUMERIC(12,2),
    repeat_customer               BOOLEAN,
    customer_rank                 INTEGER,
    customer_value_tier           TEXT,
    first_order_date              DATE,
    last_order_date               DATE
);

-------------------------------------------------------------
-- MARKET DIMENSION
-------------------------------------------------------------

CREATE TABLE dim_markets (
    market                        TEXT PRIMARY KEY,
    total_sales                   NUMERIC(14,2),
    total_profit                  NUMERIC(14,2),
    total_orders                  INTEGER,
    total_customers               INTEGER,
    avg_margin_pct                NUMERIC(6,2),
    avg_order_value               NUMERIC(12,2),
    revenue_share_pct             NUMERIC(8,2),
    market_rank                   INTEGER,
    market_tier                   TEXT,
    first_order_date              DATE,
    last_order_date               DATE
);

-------------------------------------------------------------
-- KPI TABLES
-------------------------------------------------------------

CREATE TABLE kpi_executive (
    kpi_name                      TEXT PRIMARY KEY,
    kpi_value                     NUMERIC(18,2)
);

CREATE TABLE kpi_inventory (
    kpi_name                      TEXT PRIMARY KEY,
    kpi_value                     NUMERIC(18,2)
);

CREATE TABLE kpi_logistics (
    kpi_name                      TEXT PRIMARY KEY,
    kpi_value                     NUMERIC(18,2)
);

CREATE TABLE kpi_customer (
    kpi_name                      TEXT PRIMARY KEY,
    kpi_value                     NUMERIC(18,2)
);

CREATE TABLE kpi_product (
    kpi_name                      TEXT PRIMARY KEY,
    kpi_value                     NUMERIC(18,2)
);