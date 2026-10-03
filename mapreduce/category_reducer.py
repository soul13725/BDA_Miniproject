import sys
from decimal import Decimal

def main():
    current_category = None
    current_revenue = Decimal('0.0')
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) != 2:
            continue
            
        category, value_str = parts
        try:
            value = Decimal(value_str)
        except:
            continue
            
        if current_category == category:
            current_revenue += value
        else:
            if current_category:
                print(f"{current_category}\t{current_revenue.quantize(Decimal('0.01'))}")
            current_category = category
            current_revenue = value
            
    if current_category:
        print(f"{current_category}\t{current_revenue.quantize(Decimal('0.01'))}")

if __name__ == "__main__":
    main()
