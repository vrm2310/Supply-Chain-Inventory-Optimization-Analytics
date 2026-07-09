# Dashboard Design Document

## Project

Supply Chain & Inventory Analytics Dashboard

---

# Dashboard Objective

The objective of this dashboard is to provide executives and business stakeholders with an interactive analytics solution for monitoring sales performance, inventory efficiency, customer behavior, logistics operations, and profitability.

The dashboard is designed to answer operational and strategic business questions through a five-page analytical report built in Power BI using a PostgreSQL data warehouse.

---

# Dashboard Structure

The dashboard consists of five analytical pages.

---

## Page 1 — Executive Summary

### Purpose

Provide a high-level overview of overall business performance.

### KPIs

- Total Revenue
- Total Profit
- Profit Margin %
- Total Orders
- On-Time Delivery %

### Visuals

- Monthly Revenue Trend
- Revenue by Market
- Revenue Share by Market
- Top Products by Revenue
- Category Performance Matrix

### Business Questions

- How is the business performing overall?
- Which markets generate the highest revenue?
- Which products contribute most to sales?
- Is delivery performance meeting expectations?

---

## Page 2 — Product Analytics

### Purpose

Analyze product and inventory performance.

### KPIs

- Total Products
- Average Selling Price
- Average Discount %
- Average Margin %
- High Discount Orders

### Visuals

- Top Products by Revenue
- Category Revenue vs Profit
- Revenue by ABC Class
- Revenue by Inventory Priority
- Revenue vs Margin

### Business Questions

- Which products drive revenue?
- Which inventory requires immediate attention?
- Are discounts affecting profitability?
- Which categories generate the highest margins?

---

## Page 3 — Customer Analytics

### Purpose

Understand customer purchasing behavior and value.

### KPIs

- Total Customers
- Repeat Customers
- Average Order Value
- Revenue per Customer
- Average Customer Margin

### Visuals

- Top Customers by Revenue
- Customer Value Tier
- Revenue by Customer Segment
- Average Order Value by Segment
- Customer Revenue vs Profit
- Top States by Revenue

### Business Questions

- Who are the highest value customers?
- Which customer segments generate the most revenue?
- Which states contribute the most sales?
- What is the average customer value?

---

## Page 4 — Logistics Analytics

### Purpose

Evaluate delivery performance and shipping efficiency.

### KPIs

- Average Shipping Delay
- On-Time Delivery %
- Late Deliveries
- Average Delivery Days
- Early Deliveries %

### Visuals

- Delivery Status Distribution
- Shipping Delay by Shipping Mode
- On-Time Delivery by Market
- Average Delay by Market
- Scheduled vs Actual Delivery
- SLA Compliance by Market

### Business Questions

- Which shipping modes perform best?
- Which markets experience delivery delays?
- What percentage of deliveries meet SLA?
- How can logistics efficiency be improved?

---

## Page 5 — Profitability Analytics

### Purpose

Analyze the relationship between revenue, discounts, and profitability.

### KPIs

- Total Profit
- Profit Margin %
- Average Discount %
- High Discount Orders
- Revenue per Customer

### Visuals

- Top Categories by Profit
- Discount vs Profit
- Profit Margin by Market
- Top Profitable Products
- Revenue vs Profit
- Bottom Products by Profit

### Business Questions

- Which categories generate the highest profit?
- Which products are loss-making?
- Do higher discounts reduce margins?
- Which markets are most profitable?

---

# Dashboard Design Principles

The dashboard follows several design principles.

## Consistency

- Consistent KPI card layout
- Uniform spacing
- Standardized color palette
- Common typography
- Consistent shadows and borders

---

## Business Storytelling

The dashboard progresses from:

Overall Business

↓

Products

↓

Customers

↓

Logistics

↓

Profitability

allowing executives to move from high-level performance to detailed operational insights.

---

## Interactivity

The dashboard supports:

- Cross-filtering
- Interactive visuals
- Tooltips
- Dynamic KPIs
- Responsive filtering across pages

---

# Target Users

- Business Analysts
- Supply Chain Managers
- Operations Managers
- Inventory Planners
- Senior Leadership
- Executive Management

---

# Expected Business Outcomes

The dashboard enables stakeholders to:

- Monitor business performance
- Identify high-value products
- Improve inventory allocation
- Optimize discount strategy
- Reduce delivery delays
- Improve customer retention
- Increase profitability