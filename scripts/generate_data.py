import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set up constraints and mappings
PRODUCTS = [
    ("P001", "Wireless Mouse", "Electronics", 599.00),
    ("P002", "Mechanical Keyboard", "Electronics", 3500.00),
    ("P003", "USB-C Cable", "Electronics", 299.00),
    ("P004", "Notebook", "Stationery", 150.00),
    ("P005", "Ball Pen Pack", "Stationery", 100.00),
    ("P006", "Backpack", "Fashion", 1200.00),
    ("P007", "Running Shoes", "Fashion", 2500.00),
    ("P008", "Coffee Mug", "Home", 250.00),
    ("P009", "Water Bottle", "Home", 450.00),
    ("P010", "Desk Lamp", "Home", 850.00),
    ("P011", "Smart Watch", "Electronics", 4999.00),
    ("P012", "Power Bank", "Electronics", 1500.00)
]

PAYMENT_METHODS = ["UPI", "Card", "Cash", "Wallet"]
CITIES = ["Mumbai", "Pune", "Delhi", "Bengaluru", "Hyderabad", "Chennai"]
CHANNELS = ["Online", "Store"]
DISCOUNTS = [0, 5, 10, 15, 20, 25]

def generate_data(num_records, output_path):
    random.seed(42)
    
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31, 23, 59, 59)
    time_diff = end_date - start_date
    
    # Pre-generate some customers
    num_customers = max(10, num_records // 10)
    customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
    
    records = []
    
    total_revenue = 0.0
    unique_customers = set()
    unique_products = set()
    categories = set()
    
    min_date = None
    max_date = None
    
    for i in range(1, num_records + 1):
        txn_id = f"TXN{str(i).zfill(6)}"
        
        # Random timestamp
        random_seconds = random.randint(0, int(time_diff.total_seconds()))
        txn_date = start_date + timedelta(seconds=random_seconds)
        
        if min_date is None or txn_date < min_date:
            min_date = txn_date
        if max_date is None or txn_date > max_date:
            max_date = txn_date
            
        timestamp_str = txn_date.strftime("%Y-%m-%d %H:%M:%S")
        
        customer_id = random.choice(customer_ids)
        product = random.choice(PRODUCTS)
        product_id, product_name, category, unit_price = product
        
        quantity = random.randint(1, 5)
        discount_percent = random.choice(DISCOUNTS)
        
        gross_amount = quantity * unit_price
        discount_amount = gross_amount * (discount_percent / 100.0)
        total_amount = round(gross_amount - discount_amount, 2)
        
        payment_method = random.choice(PAYMENT_METHODS)
        city = random.choice(CITIES)
        channel = random.choice(CHANNELS)
        
        records.append([
            txn_id, timestamp_str, customer_id, product_id, product_name, category, 
            quantity, unit_price, discount_percent, total_amount, payment_method, city, channel
        ])
        
        total_revenue += total_amount
        unique_customers.add(customer_id)
        unique_products.add(product_id)
        categories.add(category)
        
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
