SET search_path TO supply_chain;

-------------------------------------------------------------
-- FACT TABLE INDEXES
-------------------------------------------------------------

CREATE INDEX idx_fact_orders_product
ON fact_orders(product_name);

CREATE INDEX idx_fact_orders_category
ON fact_orders(category_name);

CREATE INDEX idx_fact_orders_customer
ON fact_orders(customer_id);

CREATE INDEX idx_fact_orders_market
ON fact_orders(market);

CREATE INDEX idx_fact_orders_order_date
ON fact_orders(order_date_dateorders);

CREATE INDEX idx_fact_orders_shipping_mode
ON fact_orders(shipping_mode);

CREATE INDEX idx_fact_orders_order_status
ON fact_orders(order_status);

-------------------------------------------------------------
-- DIMENSION TABLE INDEXES
-------------------------------------------------------------

CREATE INDEX idx_dim_products_abc
ON dim_products(abc_class);

CREATE INDEX idx_dim_products_priority
ON dim_products(inventory_priority);

CREATE INDEX idx_dim_products_velocity
ON dim_products(product_velocity);

CREATE INDEX idx_dim_customers_tier
ON dim_customers(customer_value_tier);

CREATE INDEX idx_dim_markets_tier
ON dim_markets(market_tier);

-------------------------------------------------------------
-- DATE INDEXES
-------------------------------------------------------------

CREATE INDEX idx_dim_products_last_order
ON dim_products(last_order_date);

CREATE INDEX idx_dim_customers_last_order
ON dim_customers(last_order_date);

CREATE INDEX idx_dim_markets_last_order
ON dim_markets(last_order_date);