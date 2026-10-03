import sys
from decimal import Decimal

def main():
    total_revenue = Decimal('0.0')
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        key, value = parts
        if key == "TOTAL_REVENUE":
            try:
                total_revenue += Decimal(value)
            except:
                pass
    
    total_revenue = total_revenue.quantize(Decimal('0.01'))
    print(f"TOTAL_REVENUE\t{total_revenue}")

if __name__ == "__main__":
    main()
