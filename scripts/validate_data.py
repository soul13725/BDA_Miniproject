import csv
import sys
from pathlib import Path
from datetime import datetime

REQUIRED_COLUMNS = [
    "transaction_id", "timestamp", "customer_id", "product_id", "product_name",
    "category", "quantity", "unit_price", "discount_percent", "total_amount",
    "payment_method", "city", "channel"
]

VALID_CATEGORIES = {"Electronics", "Stationery", "Fashion", "Home"}
VALID_PAYMENTS = {"UPI", "Card", "Cash", "Wallet"}
VALID_CITIES = {"Mumbai", "Pune", "Delhi", "Bengaluru", "Hyderabad", "Chennai"}
VALID_CHANNELS = {"Online", "Store"}

def validate_data(file_path):
    print("========================================")
    print("RETAIL DATASET VALIDATION")
    print("========================================")
    print(f"File:\n{file_path}\n")
    
    if not file_path.exists():
        print("File exists:\nFAIL")
        print("========================================")
        print("VALIDATION RESULT: FAIL")
        print("========================================")
        return False
        
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            rows = list(reader)
    except Exception as e:
        print(f"CSV loading:\nFAIL ({str(e)})")
        print("========================================")
        print("VALIDATION RESULT: FAIL")
        print("========================================")
        return False
        
    num_rows = len(rows)
    print(f"Rows:\n{num_rows}\n")
    
    if num_rows == 0:
        print("Rows:\nFAIL (No rows)")
        return False
        
    num_cols = len(headers) if headers else 0
    print(f"Columns:\n{num_cols}\n")
    
    schema_pass = True
    if num_cols != 13:
        schema_pass = False
    elif headers != REQUIRED_COLUMNS:
        schema_pass = False
        
    print(f"Schema:\n{'PASS' if schema_pass else 'FAIL'}\n")
    
    if not schema_pass:
        print("========================================")
        print("VALIDATION RESULT: FAIL")
        print("========================================")
        return False
        
    txn_ids = set()
    txn_id_pass = True
    null_pass = True
    quantity_pass = True
    price_pass = True
    discount_pass = True
    amount_pass = True
    category_pass = True
    payment_pass = True
    city_pass = True
    channel_pass = True
    timestamp_pass = True
    
    invalid_examples = {}
    
    # Stats
    unique_customers = set()
    unique_products = set()
    total_revenue = 0.0
    total_quantity = 0
    min_val = None
    max_val = None
    category_counts = {}
    payment_counts = {}
    city_counts = {}
    channel_counts = {}
    min_date = None
    max_date = None
    
    for idx, row in enumerate(rows):
        # null check
        if len(row) != 13 or any(val is None or val.strip() == '' for val in row):
            null_pass = False
            
        if len(row) != 13:
            continue
            
        txn_id = row[0]
        ts_str = row[1]
        cust_id = row[2]
        prod_id = row[3]
        cat = row[5]
        qty_str = row[6]
        price_str = row[7]
        disc_str = row[8]
        amount_str = row[9]
        pay = row[10]
        city = row[11]
        channel = row[12]
        
        # Transaction ID
        if txn_id in txn_ids:
            txn_id_pass = False
            invalid_examples['Duplicate TXN'] = txn_id
        txn_ids.add(txn_id)
        
        # Quantity
        try:
            qty = int(qty_str)
            if qty <= 0:
                quantity_pass = False
                invalid_examples['Quantity'] = qty
        except:
            quantity_pass = False
            invalid_examples['Quantity format'] = qty_str
            
        # Price
        try:
            price = float(price_str)
            if price <= 0:
                price_pass = False
                invalid_examples['Price'] = price
        except:
            price_pass = False
            invalid_examples['Price format'] = price_str
            
        # Discount
        try:
            disc = float(disc_str)
            if disc < 0 or disc > 100:
                discount_pass = False
                invalid_examples['Discount'] = disc
        except:
            discount_pass = False
            invalid_examples['Discount format'] = disc_str
            
        # Total Amount
        try:
            amount = float(amount_str)
            if amount < 0:
                amount_pass = False
                invalid_examples['Amount'] = amount
            else:
                if 'qty' in locals() and 'price' in locals() and 'disc' in locals():
                    expected_gross = qty * price
                    expected_disc = expected_gross * (disc / 100.0)
                    expected_amount = round(expected_gross - expected_disc, 2)
                    if abs(amount - expected_amount) > 0.01:
                        amount_pass = False
                        invalid_examples['Amount math'] = f"Expected {expected_amount}, got {amount}"
        except:
            amount_pass = False
            invalid_examples['Amount format'] = amount_str
            
        # Enum checks
        if cat not in VALID_CATEGORIES:
            category_pass = False
            invalid_examples['Category'] = cat
        if pay not in VALID_PAYMENTS:
            payment_pass = False
            invalid_examples['Payment'] = pay
        if city not in VALID_CITIES:
            city_pass = False
            invalid_examples['City'] = city
        if channel not in VALID_CHANNELS:
            channel_pass = False
            invalid_examples['Channel'] = channel
            
        # Timestamp
        try:
            dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            if min_date is None or dt < min_date:
                min_date = dt
            if max_date is None or dt > max_date:
                max_date = dt
        except:
            timestamp_pass = False
            invalid_examples['Timestamp format'] = ts_str
            
        # Gather stats
        if 'amount' in locals():
            total_revenue += amount
            if min_val is None or amount < min_val:
                min_val = amount
            if max_val is None or amount > max_val:
                max_val = amount
        if 'qty' in locals():
            total_quantity += qty
            
        unique_customers.add(cust_id)
        unique_products.add(prod_id)
        
        category_counts[cat] = category_counts.get(cat, 0) + 1
        payment_counts[pay] = payment_counts.get(pay, 0) + 1
        city_counts[city] = city_counts.get(city, 0) + 1
        channel_counts[channel] = channel_counts.get(channel, 0) + 1

    print(f"Transaction IDs:\n{'PASS' if txn_id_pass else 'FAIL'}\n")
    print(f"Null values:\n{'PASS' if null_pass else 'FAIL'}\n")
    print(f"Quantity:\n{'PASS' if quantity_pass else 'FAIL'}\n")
    print(f"Unit price:\n{'PASS' if price_pass else 'FAIL'}\n")
    print(f"Discount:\n{'PASS' if discount_pass else 'FAIL'}\n")
    print(f"Total amount:\n{'PASS' if amount_pass else 'FAIL'}\n")
    print(f"Categories:\n{'PASS' if category_pass else 'FAIL'}\n")
    print(f"Payment methods:\n{'PASS' if payment_pass else 'FAIL'}\n")
    print(f"Cities:\n{'PASS' if city_pass else 'FAIL'}\n")
    print(f"Channels:\n{'PASS' if channel_pass else 'FAIL'}\n")
    print(f"Timestamps:\n{'PASS' if timestamp_pass else 'FAIL'}\n")
    
    if invalid_examples:
        print("Examples of failures:")
        for k, v in invalid_examples.items():
            print(f"- {k}: {v}")
        print()

    print("----------------------------------------")
    print("DATASET STATISTICS")
    print("----------------------------------------")
    print(f"Total records: {num_rows}")
    print(f"Unique customers: {len(unique_customers)}")
    print(f"Unique products: {len(unique_products)}")
    print(f"Total revenue: {total_revenue:.2f}")
    if num_rows > 0:
        print(f"Average transaction value: {(total_revenue / num_rows):.2f}")
    print(f"Minimum transaction value: {min_val:.2f}" if min_val is not None else "Minimum transaction value: N/A")
    print(f"Maximum transaction value: {max_val:.2f}" if max_val is not None else "Maximum transaction value: N/A")
    print(f"Total quantity sold: {total_quantity}")
    
    print("\nCategory counts:")
    for k, v in category_counts.items(): print(f"  {k}: {v}")
    
    print("\nPayment method counts:")
    for k, v in payment_counts.items(): print(f"  {k}: {v}")
        
    print("\nCity counts:")
    for k, v in city_counts.items(): print(f"  {k}: {v}")
        
    print("\nChannel counts:")
    for k, v in channel_counts.items(): print(f"  {k}: {v}")
        
    if min_date and max_date:
        print(f"\nDate range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
        
    all_pass = all([
        schema_pass, txn_id_pass, null_pass, quantity_pass, price_pass,
        discount_pass, amount_pass, category_pass, payment_pass, city_pass,
        channel_pass, timestamp_pass
    ])
    
    print("========================================")
    print(f"VALIDATION RESULT: {'PASS' if all_pass else 'FAIL'}")
    print("========================================")
    
    return all_pass

if __name__ == '__main__':
    file_path = Path("data/retail_logs.csv")
    if validate_data(file_path):
        sys.exit(0)
    else:
        sys.exit(1)
