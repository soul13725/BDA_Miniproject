import argparse
import csv
import random
import json
from datetime import datetime, timedelta
from pathlib import Path

PAYMENT_METHODS = ["UPI", "Card", "Cash", "Wallet"]
CHANNELS = ["Online", "Store"]
DISCOUNTS = [0, 5, 10, 15, 20, 25]

def generate_data(num_records, output_path):
    random.seed(42)
    
    # Load catalog
    catalog_dir = Path("data/catalog")
    with open(catalog_dir / "products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    with open(catalog_dir / "cities.json", "r", encoding="utf-8") as f:
        cities = json.load(f)

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31, 23, 59, 59)
    time_diff = end_date - start_date
    
    num_customers = max(10, num_records // 10)
    customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
    
    # Pre-calculate weighted choices
    product_weights = [p.get("demand_weight", 1) for p in products]
    city_weights = [c.get("demand_weight", 1) for c in cities]
    city_names = [c["city_name"] for c in cities]
    
    records = []
    
    total_revenue = 0.0
    unique_customers = set()
    unique_products = set()
    categories = set()
    
    min_date = None
    max_date = None
    
    for i in range(1, num_records + 1):
        txn_id = f"TXN{str(i).zfill(6)}"
        
        random_seconds = random.randint(0, int(time_diff.total_seconds()))
        txn_date = start_date + timedelta(seconds=random_seconds)
        
        if min_date is None or txn_date < min_date:
            min_date = txn_date
        if max_date is None or txn_date > max_date:
            max_date = txn_date
            
        timestamp_str = txn_date.strftime("%Y-%m-%d %H:%M:%S")
        
        customer_id = random.choice(customer_ids)
        product = random.choices(products, weights=product_weights, k=1)[0]
        
        quantity = random.randint(1, 5)
        discount_percent = random.choice(DISCOUNTS)
        
        gross_amount = quantity * product["unit_price"]
        discount_amount = gross_amount * (discount_percent / 100.0)
        total_amount = round(gross_amount - discount_amount, 2)
        
        payment_method = random.choice(PAYMENT_METHODS)
        city = random.choices(city_names, weights=city_weights, k=1)[0]
        channel = random.choice(CHANNELS)
        
        records.append([
            txn_id, timestamp_str, customer_id, product["product_id"], product["product_name"], product["category"], 
            quantity, product["unit_price"], discount_percent, total_amount, payment_method, city, channel
        ])
        
        total_revenue += total_amount
        unique_customers.add(customer_id)
        unique_products.add(product["product_id"])
        categories.add(product["category"])
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "transaction_id", "timestamp", "customer_id", "product_id", "product_name", 
            "category", "quantity", "unit_price", "discount_percent", "total_amount", 
            "payment_method", "city", "channel"
        ])
        writer.writerows(records)
        
    print("Dataset generated successfully.")
    print(f"Records: {num_records}")
    print("Columns: 13")
    print(f"Output: {output_path}")
    print()
    if records:
        print(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
        print(f"Number of unique customers: {len(unique_customers)}")
        print(f"Number of unique products: {len(unique_products)}")
        print(f"Number of categories: {len(categories)}")
        print(f"Total revenue: {total_revenue:.2f}")
        print(f"Average transaction value: {(total_revenue / num_records):.2f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate retail transaction data.")
    parser.add_argument('--records', type=int, default=5000, help='Number of records to generate.')
    args = parser.parse_args()
    
    output_file = Path("data/retail_logs.csv")
    generate_data(args.records, output_file)
