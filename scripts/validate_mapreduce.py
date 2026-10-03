import sys
from pathlib import Path
from decimal import Decimal

def validate():
    output_dir = Path("output/mapreduce")
    
    total_file = output_dir / "total_revenue.txt"
    cat_file = output_dir / "category_revenue.tsv"
    prod_file = output_dir / "product_revenue.tsv"
    
    files_exist = total_file.exists() and cat_file.exists() and prod_file.exists()
    
    if not files_exist:
        print("Output existence: FAIL")
        return False
    else:
        print("Output existence: PASS")
        
    try:
        with open(total_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
            parts = lines[0].split('\t')
            total_rev = Decimal(parts[1])
            print("Total revenue numeric: PASS")
    except Exception as e:
        print(f"Total revenue numeric: FAIL ({e})")
        return False
        
    cat_sum = Decimal('0.0')
    cat_valid = True
    cat_names = set()
    dup_cats = False
    try:
        with open(cat_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                parts = line.strip().split('\t')
                cat = parts[0]
                val = Decimal(parts[1])
                cat_sum += val
                if cat in cat_names:
                    dup_cats = True
                cat_names.add(cat)
        print("Category output valid: PASS")
    except Exception as e:
        print(f"Category output valid: FAIL ({e})")
        cat_valid = False
        
    print(f"No duplicate categories: {'FAIL' if dup_cats else 'PASS'}")
    
    prod_sum = Decimal('0.0')
    prod_valid = True
    prod_ids = set()
    dup_prods = False
    try:
        with open(prod_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                parts = line.strip().split('\t')
                pid = parts[0]
                pname = parts[1]
                val = Decimal(parts[2])
                prod_sum += val
                if pid in prod_ids:
                    dup_prods = True
                prod_ids.add(pid)
        print("Product output valid: PASS")
    except Exception as e:
        print(f"Product output valid: FAIL ({e})")
        prod_valid = False
        
    print(f"No duplicate products: {'FAIL' if dup_prods else 'PASS'}")
    
    cat_diff = abs(total_rev - cat_sum)
    prod_diff = abs(total_rev - prod_sum)
    
    cat_match = cat_diff <= Decimal('0.01')
    prod_match = prod_diff <= Decimal('0.01')
    
    print(f"Category sum matches total: {'PASS' if cat_match else 'FAIL'} (diff: {cat_diff})")
    print(f"Product sum matches total: {'PASS' if prod_match else 'FAIL'} (diff: {prod_diff})")
    
    expected_cats = {"Electronics", "Stationery", "Fashion", "Home"}
    cats_exist = expected_cats.issubset(cat_names)
    print(f"Expected categories: {'PASS' if cats_exist else 'FAIL'} (found: {cat_names})")
    
    expected_prods = {"P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010", "P011", "P012"}
    prods_exist = expected_prods.issubset(prod_ids)
    print(f"Expected products: {'PASS' if prods_exist else 'FAIL'}")
    
    all_pass = files_exist and cat_valid and prod_valid and not dup_cats and not dup_prods and cat_match and prod_match and cats_exist and prods_exist
    return all_pass

if __name__ == "__main__":
    if validate():
        sys.exit(0)
    else:
        sys.exit(1)
