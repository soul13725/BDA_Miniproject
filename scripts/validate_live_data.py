import os
import csv
from datetime import datetime

LIVE_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'live', 'retail_live_transactions.csv')

def validate_live_data():
    if not os.path.exists(LIVE_CSV):
        print("FAIL: Live CSV does not exist.")
        return False
        
    with open(LIVE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    if len(rows) == 0:
        print("LIVE DATA VALIDATION: PASS (File exists, empty)")
        return True
        
    ids = set()
    for row in rows:
        tid = row["transaction_id"]
        if tid in ids:
            print(f"FAIL: Duplicate transaction ID: {tid}")
            return False
        ids.add(tid)
        
        try:
            qty = int(row["quantity"])
            price = float(row["unit_price"])
            discount = float(row["discount_percent"])
            total = float(row["total_amount"])
            
            expected_total = qty * price * (1 - discount/100)
            if abs(total - expected_total) > 0.05:
                print(f"FAIL: Total amount mismatch for {tid}: expected {expected_total}, got {total}")
                return False
                
            datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            print(f"FAIL: Exception parsing row {tid}: {e}")
            return False
            
    print("LIVE DATA VALIDATION: PASS")
    return True

if __name__ == "__main__":
    validate_live_data()
