-- ==========================================================
-- SUPPLY CHAIN ANALYTICS
-- BUSINESS SQL QUERIES
-- ==========================================================

SET search_path TO supply_chain;

-- ==========================================================
-- SECTION 1
-- EXECUTIVE ANALYTICS
-- ==========================================================

-------------------------------------------------------------
-- Q1
-- What are the company's overall business KPIs?
-------------------------------------------------------------

SELECT *
FROM vw_executive_summary;

-------------------------------------------------------------
-- Q2
-- Which markets generate the highest revenue?
-------------------------------------------------------------

SELECT market, total_sales, total_profit, revenue_share_pct, market_rank
FROM vw_market_performance
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q3
-- Which product categories contribute the most revenue?
-------------------------------------------------------------

SELECT category_name, total_sales, total_profit, revenue_share_pct, category_rank
FROM vw_category_performance
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q4
-- Which markets generate the highest profit margin?
-------------------------------------------------------------

SELECT market, avg_margin_pct, total_profit, total_sales
FROM vw_market_performance
ORDER BY avg_margin_pct DESC;

-------------------------------------------------------------
-- Q5
-- Which categories have high revenue but weak profitability?
-------------------------------------------------------------

SELECT category_name, total_sales, total_profit, avg_margin_pct
FROM vw_category_performance
WHERE avg_margin_pct < (
    SELECT AVG(avg_margin_pct)
    FROM vw_category_performance
)
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q6
-- Compare revenue contribution across markets.
-------------------------------------------------------------

SELECT market, revenue_share_pct
FROM vw_market_performance
ORDER BY revenue_share_pct DESC;

-------------------------------------------------------------
-- Q7
-- Which markets have the highest average order value?
-------------------------------------------------------------

SELECT market, avg_order_value, total_orders
FROM vw_market_performance
ORDER BY avg_order_value DESC;

-- ==========================================================
-- SECTION 2
-- PRODUCT ANALYTICS
-- ==========================================================

-------------------------------------------------------------
-- Q8
-- Which products generate the highest revenue?
-------------------------------------------------------------

SELECT product_name, category_name, total_sales, revenue_rank
FROM vw_product_performance
ORDER BY total_sales DESC
LIMIT 10;

-------------------------------------------------------------
-- Q9
-- Which products generate the highest profit?
-------------------------------------------------------------

SELECT product_name, category_name, total_profit, profit_rank
FROM vw_product_performance
ORDER BY total_profit DESC
LIMIT 10;

-------------------------------------------------------------
-- Q10
-- Which products have the highest profit margin?
-------------------------------------------------------------

SELECT product_name, category_name, avg_margin_pct, total_sales
FROM vw_product_performance
ORDER BY avg_margin_pct DESC
LIMIT 10;

-------------------------------------------------------------
-- Q11
-- Which products rely heavily on discounts?
-------------------------------------------------------------

SELECT product_name, avg_discount_pct, avg_margin_pct, total_sales
FROM vw_product_performance
ORDER BY avg_discount_pct DESC
LIMIT 10;

-------------------------------------------------------------
-- Q12
-- Which products contribute the largest share of company revenue?
-------------------------------------------------------------

SELECT product_name, revenue_share_pct, cumulative_revenue_pct, abc_class
FROM vw_product_performance
ORDER BY revenue_share_pct DESC;

SELECT *
FROM supply_chain.dim_products
LIMIT 1;

SELECT *
FROM supply_chain.vw_product_performance
LIMIT 1;

-------------------------------------------------------------
-- Q13
-- Which products generate high sales but relatively low margins?
-------------------------------------------------------------

SELECT product_name, total_sales, avg_margin_pct, total_profit
FROM vw_product_performance
WHERE total_sales >
    (
        SELECT AVG(total_sales)
        FROM vw_product_performance
    )
AND avg_margin_pct <
    (
        SELECT AVG(avg_margin_pct)
        FROM vw_product_performance
    )
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q14
-- Which categories have the largest product portfolio?
-------------------------------------------------------------

SELECT category_name, product_count, total_sales, total_profit
FROM vw_category_performance
ORDER BY product_count DESC;

-- ==========================================================
-- SECTION 3
-- CUSTOMER ANALYTICS
-- ==========================================================

-------------------------------------------------------------
-- Q15
-- Who are the highest revenue generating customers?
-------------------------------------------------------------

SELECT customer_id, customer_name, total_sales, total_profit, customer_rank
FROM vw_customer_performance
ORDER BY total_sales DESC
LIMIT 10;

-------------------------------------------------------------
-- Q16
-- Which customers generate the highest profit?
-------------------------------------------------------------

SELECT customer_id, customer_name, total_profit, total_sales
FROM vw_customer_performance
ORDER BY total_profit DESC
LIMIT 10;

-------------------------------------------------------------
-- Q17
-- How are customers distributed across value tiers?
-------------------------------------------------------------

SELECT
    customer_value_tier,
    COUNT(*) AS total_customers,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS customer_pct
FROM vw_customer_performance
GROUP BY customer_value_tier
ORDER BY total_customers DESC;

-------------------------------------------------------------
-- Q18
-- What percentage of customers are repeat customers?
-------------------------------------------------------------

SELECT
    repeat_customer,
    COUNT(*) AS total_customers,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS customer_pct
FROM vw_customer_performance
GROUP BY repeat_customer;

-------------------------------------------------------------
-- Q19
-- Which customer value tier generates the highest revenue?
-------------------------------------------------------------

SELECT
    customer_value_tier,
    COUNT(*) AS customers,
    ROUND(SUM(total_sales),2) AS total_revenue,
    ROUND(SUM(total_profit),2) AS total_profit,
    ROUND(AVG(avg_order_value),2) AS avg_order_value
FROM vw_customer_performance
GROUP BY customer_value_tier
ORDER BY total_revenue DESC;

-------------------------------------------------------------
-- Q20
-- Which repeat customers have the highest lifetime value?
-------------------------------------------------------------

SELECT customer_id, customer_name, total_sales, total_profit, total_orders, avg_order_value
FROM vw_customer_performance
WHERE repeat_customer = TRUE
ORDER BY total_sales DESC
LIMIT 10;

-- ==========================================================
-- SECTION 4
-- INVENTORY ANALYTICS
-- ==========================================================

-------------------------------------------------------------
-- Q21
-- How are products distributed across ABC inventory classes?
-------------------------------------------------------------

SELECT
    abc_class,
    COUNT(*) AS total_products,
    ROUND(SUM(total_sales),2) AS total_revenue,
    ROUND(SUM(total_profit),2) AS total_profit
FROM vw_inventory_analysis
GROUP BY abc_class
ORDER BY abc_class;

-------------------------------------------------------------
-- Q22
-- Which products require the highest inventory attention?
-------------------------------------------------------------

SELECT product_name, category_name, inventory_priority, product_velocity, total_sales, total_quantity
FROM vw_inventory_analysis
WHERE inventory_priority = 'Critical'
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q23
-- Which fast-moving products contribute the most revenue?
-------------------------------------------------------------

SELECT product_name, category_name, total_sales, total_quantity, abc_class
FROM vw_inventory_analysis
WHERE product_velocity = 'Fast'
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q24
-- Which slow-moving products should be reviewed?
-------------------------------------------------------------

SELECT product_name, category_name, total_sales, total_quantity, inventory_priority
FROM vw_inventory_analysis
WHERE product_velocity = 'Slow'
ORDER BY total_sales ASC;

-------------------------------------------------------------
-- Q25
-- Which products generate high revenue but have low inventory priority?
-------------------------------------------------------------

SELECT product_name, category_name, total_sales, inventory_priority, product_velocity
FROM vw_inventory_analysis
WHERE total_sales >
    (
        SELECT AVG(total_sales)
        FROM vw_inventory_analysis
    )
AND inventory_priority IN ('Medium','Low')
ORDER BY total_sales DESC;

-------------------------------------------------------------
-- Q26
-- Inventory recommendation summary by action category.
-------------------------------------------------------------

SELECT
    inventory_action,
    COUNT(*) AS total_products,
    ROUND(SUM(total_sales),2) AS total_revenue,
    ROUND(SUM(total_profit),2) AS total_profit
FROM vw_inventory_analysis
GROUP BY inventory_action
ORDER BY total_revenue DESC;

-- ==========================================================
-- SECTION 5
-- LOGISTICS ANALYTICS
-- ==========================================================

-------------------------------------------------------------
-- Q27
-- Which shipping modes have the highest average delay?
-------------------------------------------------------------

SELECT
    shipping_mode,
    ROUND(AVG(shipping_delay_days),2) AS avg_delay,
    ROUND(AVG(delay_pct),2) AS avg_delay_pct,
    COUNT(*) AS total_orders
FROM vw_logistics_performance
GROUP BY shipping_mode
ORDER BY avg_delay DESC;

-------------------------------------------------------------
-- Q28
-- Which markets experience the most delivery delays?
-------------------------------------------------------------

SELECT
    market,
    ROUND(AVG(shipping_delay_days),2) AS avg_delay,
    ROUND(
        AVG(
            CASE
                WHEN late_delivery THEN 1
                ELSE 0
            END
        ) * 100,
        2
    ) AS late_delivery_pct
FROM vw_logistics_performance
GROUP BY market
ORDER BY avg_delay DESC;

-------------------------------------------------------------
-- Q29
-- How does SLA compliance vary across shipping modes?
-------------------------------------------------------------

SELECT shipping_mode, sla_compliance, COUNT(*) AS total_orders
FROM vw_logistics_performance
GROUP BY shipping_mode, sla_compliance
ORDER BY shipping_mode, total_orders DESC;

-------------------------------------------------------------
-- Q30
-- Which regions have the highest late delivery rate?
-------------------------------------------------------------

SELECT
    order_region,
    ROUND(
        AVG(
            CASE
                WHEN late_delivery THEN 1
                ELSE 0
            END
        ) * 100,
        2
    ) AS late_delivery_pct,
    COUNT(*) AS total_orders
FROM vw_logistics_performance
GROUP BY order_region
ORDER BY late_delivery_pct DESC;

-------------------------------------------------------------
-- Q31
-- What is the distribution of logistics health?
-------------------------------------------------------------

SELECT
    logistics_health,
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER(),
        2
    ) AS order_pct
FROM vw_logistics_performance
GROUP BY logistics_health
ORDER BY total_orders DESC;

-------------------------------------------------------------
-- Q32
-- Which shipping modes process orders the fastest?
-------------------------------------------------------------

SELECT
    shipping_mode,
    ROUND(AVG(order_processing_days),2) AS avg_processing_days,
    ROUND(AVG(days_for_shipping_real),2) AS avg_shipping_days,
    COUNT(*) AS total_orders
FROM vw_logistics_performance
GROUP BY shipping_mode
ORDER BY avg_processing_days ASC;

-------------------------------------------------------------
-- Q33
-- Which markets require logistics improvement?
-------------------------------------------------------------

SELECT
    market,
    ROUND(AVG(shipping_delay_days),2) AS avg_delay,
    ROUND(
        AVG(
            CASE
                WHEN on_time_delivery THEN 1
                ELSE 0
            END
        ) * 100,
        2
    ) AS on_time_pct,
    COUNT(*) AS total_orders
FROM vw_logistics_performance
GROUP BY market
HAVING AVG(shipping_delay_days) > 0
ORDER BY avg_delay DESC;

-- ==========================================================
-- SECTION 6
-- PROFITABILITY ANALYTICS
-- ==========================================================

-------------------------------------------------------------
-- Q34
-- Which products generate the highest profit?
-------------------------------------------------------------

SELECT product_name, category_name, total_profit, total_sales, avg_margin_pct
FROM vw_product_performance
ORDER BY total_profit DESC
LIMIT 10;

-------------------------------------------------------------
-- Q35
-- Which products are loss making?
-------------------------------------------------------------

SELECT
    product_name,
    category_name,
    COUNT(*) AS loss_orders,
    ROUND(SUM(sales),2) AS revenue,
    ROUND(SUM(benefit_per_order),2) AS total_profit
FROM vw_profitability_analysis
WHERE loss_making_order = TRUE
GROUP BY product_name, category_name
ORDER BY loss_orders DESC, revenue DESC;

-------------------------------------------------------------
-- Q36
-- Which products depend heavily on discounts?
-------------------------------------------------------------

SELECT
    product_name,
    category_name,
    ROUND(AVG(discount_pct),2) AS avg_discount,
    ROUND(AVG(profit_margin_pct),2) AS avg_margin,
    ROUND(SUM(sales),2) AS revenue
FROM vw_profitability_analysis
GROUP BY product_name, category_name
ORDER BY avg_discount DESC
LIMIT 10;

-------------------------------------------------------------
-- Q37
-- How does profitability vary across categories?
-------------------------------------------------------------

SELECT
    category_name,
    ROUND(SUM(sales),2) AS revenue,
    ROUND(SUM(benefit_per_order),2) AS profit,
    ROUND(AVG(profit_margin_pct),2) AS avg_margin,
    COUNT(*) AS total_orders
FROM vw_profitability_analysis
GROUP BY category_name
ORDER BY profit DESC;

-------------------------------------------------------------
-- Q38
-- Which pricing strategies are most common?
-------------------------------------------------------------

SELECT
    pricing_strategy,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS revenue,
    ROUND(SUM(benefit_per_order),2) AS profit
FROM vw_profitability_analysis
GROUP BY pricing_strategy
ORDER BY revenue DESC;

-------------------------------------------------------------
-- Q39
-- Which profitability status contributes the most revenue?
-------------------------------------------------------------

SELECT
    profitability_status,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS revenue,
    ROUND(SUM(benefit_per_order),2) AS profit,
    ROUND(AVG(profit_margin_pct),2) AS avg_margin
FROM vw_profitability_analysis
GROUP BY profitability_status
ORDER BY revenue DESC;

-------------------------------------------------------------
-- Q40
-- Which products should management review immediately?
-------------------------------------------------------------

SELECT
    product_name,
    category_name,
    ROUND(SUM(sales),2) AS revenue,
    ROUND(SUM(benefit_per_order),2) AS profit,
    ROUND(AVG(discount_pct),2) AS avg_discount,
    ROUND(AVG(profit_margin_pct),2) AS avg_margin,
    COUNT(*) AS total_orders
FROM vw_profitability_analysis
WHERE high_discount_order = TRUE OR loss_making_order = TRUE
GROUP BY product_name, category_name
ORDER BY profit ASC, avg_discount DESC;