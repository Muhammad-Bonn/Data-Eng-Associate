# Brazilian E-commerce Data Warehouse & Analytics Project

## Overview

This project builds a **Data Warehouse (DWH)** for the [Brazilian E-commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).  
The goal is to design a clean and well-structured **data modeling and transformation workflow** that converts raw CSV data into analytical tables suitable for reporting and business intelligence.

### Key Design Choices
- Only **core business attributes** were kept — focusing on customers, sellers, products, orders, payments, and reviews.  
- **Timing fields**, **delivery durations**, and **geospatial coordinates (lat/lng)** were intentionally **excluded** to simplify the model.  
- Brazilian **cities and states** were retained for geographical insights.  
- The workflow is divided into multiple stages — each represented by a numbered SQL script — forming a full ELT pipeline with visual ERDs.

---

## Project Files

| No. | File | Description |
|-----|------|-------------|
| **1** | `1. Creating Tables and Schemas.sql` | Creates the main base tables from the Olist dataset, defines the `raw` and `staging` schemas, and prepares data for cleaning. |
| **2** | `2. Adding Keys.sql` | Adds primary and foreign key constraints, and computes derived columns like `total_value`. |
| **3** | `3. Staging ERD.sql` | Visual representation (ERD) of the staging schema showing relationships between core entities. |
| **4** | `4. Fact and Dim Tables.sql` | Builds the `prefact` and `dwh` layers — aggregates payments, merges product categories, and creates the main fact and dimension tables. |
| **5** | `5. Fact and Dimensions ERD.sql` | Entity Relationship Diagram for the final Data Warehouse layer, illustrating the **star schema** between fact and dimension tables. |
| **6** | `6. Sales and Reviews Analysis` | Exploratory Data Analysis for Sales and Reviews. |

---

## Data Source

- **Dataset:** [Brazilian E-commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
- **Provider:** Olist (via Kaggle)  
- **Period:** 2016–2018  
- **Description:** A comprehensive dataset containing thousands of e-commerce orders from multiple Brazilian marketplaces, including customer, seller, product, payment, and review data.

---

## Workflow Summary

**1. Raw Layer (`raw`):**  
Unprocessed data copied from the `public` schema, which was copied directly from CSV files.

**2. Staging Layer (`staging`):**  
Cleans and validates data while preserving structural relationships.  
- Adds `total_value = price + freight_value`  
- Removes duplicates  
- Defines PKs and FKs  
- The ERD (File 3) visually documents these relationships.

**3. Prefact Layer (`prefact`):**  
Intermediate summarized data:
- Order payments aggregated into one record per order  
- Products enriched with English category names  
- Orders joined with reviews for analysis readiness  

**4. DWH Layer (`dwh`):**  
Final star schema:
- **Fact table** integrates order items with payments, reviews, and customer info.  
- **Dimension tables** for customers and sellers.  
- The ERD (File 5) shows final model relationships clearly.

---

## Example Analytical Queries

```sql
-- Top product categories by revenue
SELECT product_category, SUM(total_value) AS total_sales
FROM dwh.fact
GROUP BY product_category
ORDER BY total_sales DESC
LIMIT 10;

-- Average review score per Brazilian state
SELECT c.customer_state, ROUND(AVG(f.review_score), 2) AS avg_review
FROM dwh.fact AS f
JOIN dwh.dim_customers AS c
ON f.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY avg_review DESC;


