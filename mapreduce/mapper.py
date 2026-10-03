import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or len(row) < 13:
            continue
        if row[0] == "transaction_id":
            continue
        
        try:
            total_amount = float(row[9])
            print(f"TOTAL_REVENUE\t{total_amount}")
        except ValueError:
            pass

if __name__ == "__main__":
    main()
