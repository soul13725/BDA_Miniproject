import os
import json
from services.infrastructure_service import run_wsl_command, infrastructure_service

def setup_hive_table():
    status = infrastructure_service.check_status()
    if status["hive"] != "ONLINE" or status["hdfs"] != "ONLINE":
        return {"success": False, "reason": "Hive/HDFS not ONLINE"}
        
    query = """
    CREATE DATABASE IF NOT EXISTS retail_bda;
    USE retail_bda;
    CREATE EXTERNAL TABLE IF NOT EXISTS retail_logs (
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
    LOCATION '/retail_bda/raw'
    TBLPROPERTIES ('skip.header.line.count'='1');
    """
    
    cmd = f'hive -e "{query}"'
    res = run_wsl_command(cmd, timeout=30)
    return {"success": res["success"], "reason": res["stderr"]}

def run_hive_query(query):
    status = infrastructure_service.check_status()
    if status["hive"] != "ONLINE":
        return {"success": False, "reason": "Hive not ONLINE"}
        
    full_query = f"USE retail_bda; {query}"
    # Remove newlines to pass safely as a bash argument
    full_query = full_query.replace('\n', ' ')
    cmd = f'hive -e "{full_query}"'
    res = run_wsl_command(cmd, timeout=60)
    if res["success"]:
        return {"success": True, "output": res["stdout"]}
    return {"success": False, "reason": res["stderr"]}
