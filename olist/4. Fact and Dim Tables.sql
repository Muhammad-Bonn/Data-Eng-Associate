--
CREATE SCHEMA IF NOT EXISTS prefact;

CREATE TABLE prefact.order_payments_summary AS
SELECT 
    order_id,
    STRING_AGG(DISTINCT payment_type, ', ') AS payments,
    STRING_AGG(DISTINCT payment_installments::TEXT, ', ') AS installments,
    SUM(payment_value) AS total_payment_value
FROM staging.stag_order_payments
GROUP BY order_id;

--
CREATE TABLE prefact.products AS
SELECT 
    p.product_id,
    t.product_category_name_english AS product_category
FROM staging.stag_products AS p
LEFT JOIN staging.stag_product_category_name_translation AS t
    ON p.product_category_name = t.product_category_name;

--
CREATE TABLE prefact.fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    r.review_id,
    r.review_score,
    p.payments,
    p.installments,
    p.total_payment_value
FROM staging.stag_orders AS o
LEFT JOIN staging.stag_order_reviews AS r
    ON o.order_id = r.order_id
LEFT JOIN prefact.order_payments_summary AS p
    ON o.order_id = p.order_id;

CREATE TABLE prefact.cleaned_orders AS
SELECT DISTINCT *
FROM prefact.fact_orders;

-- 
CREATE TABLE prefact.fact_items AS
SELECT
    i.order_id,
    i.order_item_id,
    i.product_id,
    i.seller_id,
    i.price,
    i.freight_value,
	i.total_value,
    t.product_category,
FROM staging.stag_order_items AS i
LEFT JOIN prefact.products AS t
    ON i.product_id = t.product_id;

CREATE TABLE prefact.cleaned_items AS
SELECT DISTINCT *
FROM prefact.fact_items;

-- Fact Table
CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE dwh.fact AS
SELECT 
    i.*,
	o.customer_id,
    o.order_status,
    o.review_id,
    o.review_score,
    o.payments,
    o.installments,
	o.total_payment_value
FROM prefact.cleaned_items AS i
LEFT JOIN prefact.cleaned_orders AS o
    ON i.order_id = o.order_id;

-- Dim Tables
CREATE TABLE dwh.dim_sellers AS
SELECT DISTINCT *
FROM staging.stag_sellers;

CREATE TABLE dwh.dim_customers AS
SELECT DISTINCT *
FROM staging.stag_customers;

