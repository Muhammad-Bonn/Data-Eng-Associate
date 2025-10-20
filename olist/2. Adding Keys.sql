-- Explore
SELECT * FROM staging.stag_customers LIMIT 5;
SELECT COUNT(*) FROM staging.stag_order_payments WHERE order_id IS NULL;

SELECT customer_unique_id, COUNT(*)
FROM staging.stag_customers
GROUP BY customer_unique_id
HAVING COUNT(*) > 1;

SELECT MAX(price), Round(AVG(price),2),MIN(price)
FROM staging.stag_order_items;

-- Derived Column
ALTER TABLE staging.stag_order_items ADD COLUMN total_value numeric(12,2);
UPDATE staging.stag_order_items
SET total_value = price + freight_value;

SELECT MAX(total_value), Round(AVG(total_value),2),MIN(total_value)
FROM staging.stag_order_items;

-- Adding Primary Keys
ALTER TABLE staging.stag_customers
ADD CONSTRAINT pk_stag_customers PRIMARY KEY (customer_id);

ALTER TABLE staging.stag_sellers
ADD CONSTRAINT pk_stag_sellers PRIMARY KEY (seller_id);

ALTER TABLE staging.stag_products
ADD CONSTRAINT pk_stag_products PRIMARY KEY (product_id);

ALTER TABLE staging.stag_orders
ADD CONSTRAINT pk_stag_orders PRIMARY KEY (order_id);

ALTER TABLE staging.stag_order_payments
ADD CONSTRAINT pk_stag_order_payments PRIMARY KEY (order_id, payment_sequential);

ALTER TABLE staging.stag_product_category_name_translation
ADD CONSTRAINT pk_stag_product_category PRIMARY KEY (product_category_name);

ALTER TABLE staging.stag_order_items
ADD CONSTRAINT pk_stag_order_items PRIMARY KEY (order_id, order_item_id);

ALTER TABLE staging.stag_geolocation
ADD COLUMN pk_stag_geolocation SERIAL PRIMARY KEY;

-- Removing Duplicated from order_reviews
DELETE FROM staging.stag_order_reviews AS a
USING staging.stag_order_reviews As b
WHERE a.review_id = b.review_id
AND a.ctid > b.ctid;

ALTER TABLE staging.stag_order_reviews
ADD CONSTRAINT pk_stag_order_reviews PRIMARY KEY (review_id);

-- Adding Foreign Keys
ALTER TABLE staging.stag_orders
ADD CONSTRAINT fk_stag_orders_customer
FOREIGN KEY (customer_id)
REFERENCES staging.stag_customers (customer_id);

ALTER TABLE staging.stag_order_reviews
ADD CONSTRAINT fk_stag_order_reviews_order
FOREIGN KEY (order_id)
REFERENCES staging.stag_orders (order_id);

ALTER TABLE staging.stag_order_items
ADD CONSTRAINT fk_stag_order_items_order
FOREIGN KEY (order_id)
REFERENCES staging.stag_orders (order_id);

ALTER TABLE staging.stag_order_payments
ADD CONSTRAINT fk_stag_order_payments_order
FOREIGN KEY (order_id)
REFERENCES staging.stag_orders (order_id);

ALTER TABLE staging.stag_order_items
ADD CONSTRAINT fk_stag_order_items_seller
FOREIGN KEY (seller_id)
REFERENCES staging.stag_sellers (seller_id);

ALTER TABLE staging.stag_order_items
ADD CONSTRAINT fk_stag_order_items_product
FOREIGN KEY (product_id)
REFERENCES staging.stag_products (product_id);


