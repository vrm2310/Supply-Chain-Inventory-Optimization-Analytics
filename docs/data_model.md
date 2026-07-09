# Data Model Documentation

## Overview

The project follows a dimensional modeling approach using a Star Schema to optimize analytical performance in Power BI.

The PostgreSQL database serves as the analytical data warehouse, with one central fact table connected to multiple dimension tables.

---

# Schema

Schema Name

```
supply_chain
```

---

# Star Schema

```
                 dim_products
                       │
                       │
dim_categories ───── fact_orders ───── dim_customers
                       │
                       │
                  dim_markets
```

---

# Fact Table

## fact_orders

The central transactional table containing order-level business data.

### Grain

One record represents one product purchased in one customer order.

### Measures

- Sales
- Profit
- Quantity
- Discount
- Shipping Delay
- Shipping Cost
- Delivery Days

### Foreign Keys

- product_name
- customer_id
- category_name
- market

---

# Dimension Tables

## dim_products

Contains product-level performance metrics.

### Attributes

- Product Name
- Category
- ABC Class
- Inventory Priority
- Revenue Rank
- Profit Rank
- Product Velocity
- Revenue Share
- Average Margin
- Average Discount

---

## dim_categories

Contains category-level aggregated metrics.

### Attributes

- Category Name
- Total Revenue
- Total Profit
- Revenue Share
- Product Count
- Average Margin

---

## dim_customers

Contains customer performance metrics.

### Attributes

- Customer Name
- Customer Value Tier
- Customer Rank
- Repeat Customer
- Average Order Value
- Average Margin
- First Order Date
- Last Order Date

---

## dim_markets

Contains market-level performance metrics.

### Attributes

- Market
- Revenue Share
- Market Rank
- Average Margin
- Total Customers
- Average Order Value

---

# KPI Tables

The project includes dedicated KPI tables for improving dashboard performance.

## kpi_executive

Executive dashboard KPIs.

---

## kpi_product

Product performance KPIs.

---

## kpi_customer

Customer analytics KPIs.

---

## kpi_inventory

Inventory management KPIs.

---

## kpi_logistics

Logistics and delivery KPIs.

---

# Relationships

The data model follows one-to-many relationships.

```
fact_orders.product_name
        │
        ▼
dim_products.product_name

fact_orders.customer_id
        │
        ▼
dim_customers.customer_id

fact_orders.category_name
        │
        ▼
dim_categories.category_name

fact_orders.market
        │
        ▼
dim_markets.market
```

All relationships use:

- Cardinality: One-to-Many
- Cross-filter Direction: Single
- Active Relationships

---

# Data Flow

```
Raw Dataset
      │
      ▼
Data Cleaning

      │
      ▼
Feature Engineering

      │
      ▼
Fact Table

      │
      ▼
Dimension Tables

      │
      ▼
KPI Tables

      │
      ▼
Power BI

      │
      ▼
Interactive Dashboard
```

---

# Design Decisions

The dimensional model was selected because it provides:

- Faster dashboard performance
- Simpler DAX calculations
- Easier scalability
- Better maintainability
- Reduced data redundancy
- Improved analytical querying

---

# Power BI Model

The Power BI model imports the PostgreSQL warehouse directly.

Model characteristics:

- Import Mode
- Star Schema
- Single-direction filtering
- Pre-aggregated KPI tables
- Optimized DAX measures

---

# Analytical Views

Several SQL analytical views were created to validate business logic before visualization.

Examples include:

- Executive Performance
- Product Performance
- Customer Performance
- Logistics Performance
- Market Performance
- Inventory Analysis
- Profitability Analysis

These views were primarily used for SQL analysis and validation before developing the Power BI dashboard.