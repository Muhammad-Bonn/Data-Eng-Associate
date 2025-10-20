-- =========================================
-- Project: Olist E-Commerce Data Warehouse
-- Description: SQL script for creating and preparing raw + staging schemas in PostgreSQL
-- =========================================

-- Create Tables
CREATE TABLE customers (
  customer_id TEXT,
  customer_unique_id TEXT,
  customer_zip_code_prefix INTEGER,
  customer_city TEXT,
  customer_state TEXT
);

CREATE TABLE geolocation (
  geolocation_zip_code_prefix INTEGER,
  geolocation_lat NUMERIC,
  geolocation_lng NUMERIC,
  geolocation_city TEXT,
  geolocation_state TEXT
);

CREATE TABLE sellers (
  seller_id TEXT,
  seller_zip_code_prefix INTEGER,
  seller_city TEXT,
  seller_state TEXT
);

CREATE TABLE products (
  product_id TEXT,
  product_category_name TEXT,
  product_name_lenght INTEGER,
  product_description_lenght INTEGER,
  product_photos_qty INTEGER,
  product_weight_g NUMERIC,
  product_length_cm NUMERIC,
  product_height_cm NUMERIC,
  product_width_cm NUMERIC
);

CREATE TABLE orders (
  order_id TEXT,
  customer_id TEXT,
  order_status TEXT,
  order_purchase_timestamp TIMESTAMP,
  order_approved_at TIMESTAMP,
  order_delivered_carrier_date TIMESTAMP,
  order_delivered_customer_date TIMESTAMP,
  order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE order_items (
  order_id TEXT,
  order_item_id INTEGER,
  product_id TEXT,
  seller_id TEXT,
  shipping_limit_date TIMESTAMP,
  price NUMERIC(12,2),
  freight_value NUMERIC(12,2)
);

CREATE TABLE order_payments (
  order_id TEXT,
  payment_sequential INTEGER,
  payment_type TEXT,
  payment_installments INTEGER,
  payment_value NUMERIC(12,2)
);

CREATE TABLE order_reviews (
  review_id TEXT,
  order_id TEXT,
  review_score INTEGER,
  review_comment_title TEXT,
  review_comment_message TEXT,
  review_creation_date TIMESTAMP,
  review_answer_timestamp TIMESTAMP
);

CREATE TABLE product_category_name_translation (
  product_category_name TEXT,
  product_category_name_english TEXT
);

-- LOADING TABLES FROM CSV FILES Manually

-- Creating raw and staging
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;

-- Moving Tables from public to raw
ALTER TABLE public.customers SET SCHEMA raw;
ALTER TABLE public.geolocation SET SCHEMA raw;
ALTER TABLE public.order_items SET SCHEMA raw;
ALTER TABLE public.order_payments SET SCHEMA raw;
ALTER TABLE public.order_reviews SET SCHEMA raw;
ALTER TABLE public.orders SET SCHEMA raw;
ALTER TABLE public.product_category_name_translation SET SCHEMA raw;
ALTER TABLE public.sellers SET SCHEMA raw;
ALTER TABLE public.products SET SCHEMA raw;

-- Copy Entities from raw to staging
CREATE TABLE staging.stag_customers AS TABLE raw.customers;
CREATE TABLE staging.stag_geolocation AS TABLE raw.geolocation;
CREATE TABLE staging.stag_order_items AS TABLE raw.order_items;
CREATE TABLE staging.stag_order_payments AS TABLE raw.order_payments;
CREATE TABLE staging.stag_order_reviews AS TABLE raw.order_reviews;
CREATE TABLE staging.stag_orders AS TABLE raw.orders;
CREATE TABLE staging.stag_sellers AS TABLE raw.sellers;
CREATE TABLE staging.stag_product_category_name_translation AS TABLE raw.product_category_name_translation;
CREATE TABLE staging.stag_products AS TABLE raw.products;
