import sys
import json
from pathlib import Path
from decimal import Decimal

def validate():
    output_dir = Path("output/mapreduce")
    catalog_dir = Path("data/catalog")
    
    with open(catalog_dir / "categories.json", "r", encoding="utf-8") as f:
        catalog_cats = json.load(f)
    with open(catalog_dir / "products.json", "r", encoding="utf-8") as f:
        catalog_prods = json.load(f)
        
    VALID_CATEGORIES = set(c["category_name"] for c in catalog_cats)
    VALID_PRODS = set(p["product_id"] for p in catalog_prods)
    
    
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
    
    cats_valid = cat_names.issubset(VALID_CATEGORIES)
    print(f"Categories valid: {'PASS' if cats_valid else 'FAIL'} (found: {len(cat_names)})")
    
    prods_valid = prod_ids.issubset(VALID_PRODS)
    print(f"Products valid: {'PASS' if prods_valid else 'FAIL'}")
    
    all_pass = files_exist and cat_valid and prod_valid and not dup_cats and not dup_prods and cat_match and prod_match and cats_valid and prods_valid
    return all_pass

if __name__ == "__main__":
    if validate():
        sys.exit(0)
    else:
        sys.exit(1)
