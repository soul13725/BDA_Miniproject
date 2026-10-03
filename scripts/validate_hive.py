import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hive.hive_config import LOCAL_ANALYTICS_OUTPUT_DIRECTORY

def validate_hive():
    print("========================================")
    print("HIVE ANALYTICS VALIDATION")
    print("========================================")
    
    mode_file = os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "MODE.txt")
    if os.path.exists(mode_file):
        with open(mode_file, "r") as f:
            engine = f.read().strip()
    else:
        engine = "UNKNOWN"
        
    print(f"Validation against: {engine}\n")
    
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "total_revenue.txt"), "r") as f:
            tot_str = f.read().strip()
            total_rev = Decimal(tot_str)
            print(f"Total revenue validation: PASS ({total_rev})")
    except Exception as e:
        print(f"Total revenue validation: FAIL ({str(e)})")
        sys.exit(1)
        
    try:
        cat_sum = Decimal('0.0')
        cat_count = 0
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "category_revenue.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    cat_sum += Decimal(parts[-1])
                    cat_count += 1
        
        diff = abs(total_rev - cat_sum)
        if diff <= Decimal('0.01'):
            print(f"Category sum validation: PASS (diff: {diff})")
        else:
            print(f"Category sum validation: FAIL (diff: {diff})")
            sys.exit(1)
            
    except Exception as e:
        print(f"Category sum validation: FAIL ({str(e)})")
        sys.exit(1)
        
    try:
        prod_sum = Decimal('0.0')
        prod_count = 0
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "product_revenue.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    prod_sum += Decimal(parts[-1])
                    prod_count += 1
        
        diff = abs(total_rev - prod_sum)
        if diff <= Decimal('0.01'):
            print(f"Product sum validation: PASS (diff: {diff})")
        else:
            print(f"Product sum validation: FAIL (diff: {diff})")
            sys.exit(1)
            
    except Exception as e:
        print(f"Product sum validation: FAIL ({str(e)})")
        sys.exit(1)
        
    expected_categories = 4
    expected_cities = 6
    expected_payments = 4
    expected_channels = 2
    
    if cat_count == expected_categories:
        print("Analytical groups validation: PASS")
    else:
        print("Analytical groups validation: FAIL")
        sys.exit(1)
        
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "daily_revenue.tsv"), "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                print("Daily revenue validation: PASS")
            else:
                print("Daily revenue validation: FAIL")
                sys.exit(1)
    except:
        print("Daily revenue validation: FAIL")
        sys.exit(1)
        
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "monthly_revenue.tsv"), "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                print("Monthly revenue validation: PASS")
            else:
                print("Monthly revenue validation: FAIL")
                sys.exit(1)
    except:
        print("Monthly revenue validation: FAIL")
        sys.exit(1)
        
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "top_products.tsv"), "r") as f:
            lines = f.readlines()
            if len(lines) == 5:
                print("Top products validation: PASS")
            else:
                print("Top products validation: FAIL")
                sys.exit(1)
    except:
        print("Top products validation: FAIL")
        sys.exit(1)

    print("========================================")
    print("VALIDATION RESULT: PASS")
    print("========================================")

if __name__ == "__main__":
    validate_hive()
