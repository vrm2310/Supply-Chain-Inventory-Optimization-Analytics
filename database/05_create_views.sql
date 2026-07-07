-- ==========================================================
-- Supply Chain Analytics Warehouse
-- Analytical Views
-- ==========================================================

SET search_path TO supply_chain;

-------------------------------------------------------------
-- Executive Summary
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_executive_summary AS

SELECT

    COUNT(DISTINCT order_id)                     AS total_orders,

    COUNT(DISTINCT customer_id)                  AS total_customers,

    COUNT(DISTINCT product_name)                 AS total_products,

    ROUND(SUM(sales),2)                          AS total_revenue,

    ROUND(SUM(benefit_per_order),2)              AS total_profit,

    ROUND(AVG(profit_margin_pct),2)              AS avg_profit_margin,

    ROUND(AVG(discount_pct),2)                   AS avg_discount,

    ROUND(AVG(shipping_delay_days),2)            AS avg_shipping_delay,

    ROUND(
        AVG(CASE WHEN on_time_delivery THEN 1 ELSE 0 END) * 100,
        2
    ) AS on_time_delivery_pct
FROM fact_orders;

-------------------------------------------------------------
-- Product Performance
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_product_performance AS

SELECT product_name, category_name, total_sales, total_profit, avg_margin_pct, avg_discount_pct, total_orders, total_quantity, revenue_share_pct, revenue_rank, profit_rank, abc_class, product_velocity, inventory_priority FROM dim_products;

-------------------------------------------------------------
-- Category Performance
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_category_performance AS

SELECT category_name, total_sales, total_profit, avg_margin_pct, total_orders, total_quantity, revenue_share_pct, category_rank, product_count FROM dim_categories;

-------------------------------------------------------------
-- Customer Performance
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_customer_performance AS
SELECT customer_id, customer_name, total_sales, total_profit, total_orders, avg_order_value, avg_margin_pct, repeat_customer, customer_rank, customer_value_tier, first_order_date, last_order_date
FROM dim_customers;

-------------------------------------------------------------
-- Market Performance
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_market_performance AS
SELECT market, total_sales, total_profit, total_orders, total_customers, avg_order_value, avg_margin_pct, revenue_share_pct, market_rank, market_tier, first_order_date, last_order_date
FROM dim_markets;

-------------------------------------------------------------
-- Inventory Analysis
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_inventory_analysis AS
SELECT product_name, category_name, abc_class, inventory_priority, product_velocity, total_sales, total_profit, total_quantity, avg_margin_pct, avg_discount_pct, revenue_share_pct, cumulative_revenue_pct, revenue_rank, profit_rank,
    CASE
        WHEN abc_class = 'A' AND product_velocity = 'Fast' THEN 'Highest Priority'
        WHEN abc_class = 'A' THEN 'High Priority'
        WHEN abc_class = 'B' THEN 'Medium Priority'
        ELSE 'Monitor'
    END AS inventory_action
FROM dim_products;

-------------------------------------------------------------
-- Logistics Performance
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_logistics_performance AS
SELECT order_id, order_date_dateorders, shipping_date_dateorders, market, order_region, order_country, order_state, order_city, shipping_mode, delivery_status, order_status, days_for_shipping_real, days_for_shipment_scheduled, shipping_delay_days, order_processing_days, delay_severity, fulfillment_speed, processing_speed, sla_compliance, on_time_delivery, early_delivery, late_delivery, delay_pct,
    CASE
        WHEN shipping_delay_days <= 0 THEN 'Excellent'
        WHEN shipping_delay_days <= 2 THEN 'Acceptable'
        ELSE 'Needs Attention'
    END AS logistics_health
FROM fact_orders;

-------------------------------------------------------------
-- Profitability Analysis
-------------------------------------------------------------

CREATE OR REPLACE VIEW vw_profitability_analysis AS
SELECT order_id, product_name, category_name, customer_id, market, sales, benefit_per_order, profit_per_unit, profit_margin_pct, discount_pct, average_selling_price, effective_sale_price, order_item_quantity, profitability_tier, loss_making_order, high_discount_order,
    
    CASE
        WHEN loss_making_order THEN 'Loss Making'
        WHEN profit_margin_pct >= 30 THEN 'High Margin'
        WHEN profit_margin_pct >= 15 THEN 'Healthy Margin'
        ELSE 'Low Margin'
    END AS profitability_status,

    CASE
        WHEN high_discount_order AND profit_margin_pct < 10 THEN 'Review Discount Strategy'
        WHEN high_discount_order THEN 'Promotional Discount'
        ELSE 'Normal Pricing'
    END AS pricing_strategy
FROM fact_orders;