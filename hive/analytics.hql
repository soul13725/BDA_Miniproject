USE retail_bda;

-- Query 1: Total Revenue
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/total_revenue'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT SUM(total_amount) AS total_revenue
FROM retail_transactions;

-- Query 2: Revenue By Category
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/category_revenue'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT category, SUM(total_amount) AS total_revenue
FROM retail_transactions
GROUP BY category;

-- Query 3: Revenue By Product
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/product_revenue'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT product_id, product_name, SUM(total_amount) AS total_revenue
FROM retail_transactions
GROUP BY product_id, product_name
ORDER BY total_revenue DESC;

-- Query 4: Quantity By Category
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/category_quantity'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT category, SUM(quantity) AS total_quantity
FROM retail_transactions
GROUP BY category;

-- Query 5: Average Transaction Value
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/average_transaction_value'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT AVG(total_amount) AS avg_transaction_value
FROM retail_transactions;

-- Query 6: Payment Method Analysis
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/payment_analysis'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT payment_method, COUNT(*) AS transaction_count, SUM(total_amount) AS total_revenue
FROM retail_transactions
GROUP BY payment_method;

-- Query 7: City Analysis
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/city_analysis'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT city, COUNT(*) AS transaction_count, SUM(total_amount) AS total_revenue
FROM retail_transactions
GROUP BY city;

-- Query 8: Sales Channel Analysis
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/channel_analysis'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT channel, COUNT(*) AS transaction_count, SUM(total_amount) AS total_revenue
FROM retail_transactions
GROUP BY channel;

-- Query 9: Daily Revenue
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/daily_revenue'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT SUBSTR(timestamp, 1, 10) AS date, SUM(total_amount) AS daily_revenue
FROM retail_transactions
GROUP BY SUBSTR(timestamp, 1, 10)
ORDER BY date;

-- Query 10: Monthly Revenue
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/monthly_revenue'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT SUBSTR(timestamp, 1, 7) AS month, SUM(total_amount) AS monthly_revenue
FROM retail_transactions
GROUP BY SUBSTR(timestamp, 1, 7)
ORDER BY month;

-- Query 11: Top 5 Products
INSERT OVERWRITE LOCAL DIRECTORY 'output/hive/top_products'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT product_id, product_name, SUM(total_amount) AS total_revenue
FROM retail_transactions
GROUP BY product_id, product_name
ORDER BY total_revenue DESC
LIMIT 5;
