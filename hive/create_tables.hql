USE retail_bda;

CREATE EXTERNAL TABLE IF NOT EXISTS retail_transactions (
    transaction_id STRING,
    timestamp STRING,
    customer_id STRING,
    product_id STRING,
    product_name STRING,
    category STRING,
    quantity INT,
    unit_price DOUBLE,
    discount_percent DOUBLE,
    total_amount DOUBLE,
    payment_method STRING,
    city STRING,
    channel STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/retail_bda/raw/'
TBLPROPERTIES ('skip.header.line.count'='1');
