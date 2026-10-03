import sys
from decimal import Decimal

def main():
    current_product = None
    current_revenue = Decimal('0.0')
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split('\t')
        if len(parts) != 2:
            continue
            
        product_key, value_str = parts
        try:
            value = Decimal(value_str)
        except:
            continue
            
        if current_product == product_key:
            current_revenue += value
        else:
            if current_product:
                prod_id, prod_name = current_product.split('|')
                print(f"{prod_id}\t{prod_name}\t{current_revenue.quantize(Decimal('0.01'))}")
            current_product = product_key
            current_revenue = value
            
    if current_product:
        prod_id, prod_name = current_product.split('|')
        print(f"{prod_id}\t{prod_name}\t{current_revenue.quantize(Decimal('0.01'))}")

if __name__ == "__main__":
    main()
