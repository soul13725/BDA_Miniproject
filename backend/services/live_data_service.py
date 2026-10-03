import os
import csv
import json
import threading
from datetime import datetime
from collections import defaultdict

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LIVE_DIR = os.path.join(ROOT_DIR, "data", "live")
LIVE_CSV = os.path.join(LIVE_DIR, "retail_live_transactions.csv")

HEADERS = [
    "transaction_id", "timestamp", "customer_id", "product_id", "product_name",
    "category", "quantity", "unit_price", "discount_percent", "total_amount",
    "payment_method", "city", "channel"
]

class LiveDataService:
    def __init__(self):
        self.lock = threading.Lock()
        self._ensure_setup()
        
        # In-memory aggregations for fast real-time read
        self.transactions = []
        self.transaction_count = 0
        self.total_revenue = 0.0
        self.total_quantity = 0
        self.category_revenue = defaultdict(float)
        self.product_revenue = defaultdict(float)
        self.product_quantity = defaultdict(int)
        self.product_txns = defaultdict(int)
        self.product_metadata = {} # id -> {name, category, price}
        self.payment_revenue = defaultdict(float)
        self.payment_txns = defaultdict(int)
        self.city_revenue = defaultdict(float)
        self.city_txns = defaultdict(int)
        self.city_quantity = defaultdict(int)
        self.channel_revenue = defaultdict(float)
        self.channel_txns = defaultdict(int)
        self.channel_quantity = defaultdict(int)
        self.revenue_trend = defaultdict(float) # minute-level trend
        
        self.latest_timestamp = None
        self.is_running = False
        
        self._load_existing_csv()

    def _ensure_setup(self):
        if not os.path.exists(LIVE_DIR):
            os.makedirs(LIVE_DIR)
        if not os.path.exists(LIVE_CSV):
            with open(LIVE_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)

    def _load_existing_csv(self):
        if not os.path.exists(LIVE_CSV):
            return
            
        with self.lock:
            with open(LIVE_CSV, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self._process_row_in_memory(row)
                    self.transactions.append(row)

    def _process_row_in_memory(self, row):
        try:
            qty = int(row["quantity"])
            total = float(row["total_amount"])
            pid = row["product_id"]
            
            self.transaction_count += 1
            self.total_revenue += total
            self.total_quantity += qty
            self.category_revenue[row["category"]] += total
            
            self.product_revenue[pid] += total
            self.product_quantity[pid] += qty
            self.product_txns[pid] += 1
            if pid not in self.product_metadata:
                self.product_metadata[pid] = {
                    "name": row["product_name"],
                    "category": row["category"],
                    "price": float(row["unit_price"])
                }
                
            self.payment_revenue[row["payment_method"]] += total
            self.payment_txns[row["payment_method"]] += 1
            
            self.city_revenue[row["city"]] += total
            self.city_txns[row["city"]] += 1
            self.city_quantity[row["city"]] += qty
            
            self.channel_revenue[row["channel"]] += total
            self.channel_txns[row["channel"]] += 1
            self.channel_quantity[row["channel"]] += qty
            
            # Minute level trend
            dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            trend_key = dt.strftime("%H:%M")
            self.revenue_trend[trend_key] += total
            
            self.latest_timestamp = row["timestamp"]
        except Exception as e:
            pass # Skip invalid rows

    def append_transaction(self, txn_dict):
        # Validate
        expected = set(HEADERS)
        if not all(k in txn_dict for k in expected):
            return False
            
        qty = int(txn_dict["quantity"])
        price = float(txn_dict["unit_price"])
        discount = float(txn_dict["discount_percent"])
        expected_total = qty * price * (1 - discount/100)
        
        if abs(float(txn_dict["total_amount"]) - expected_total) > 0.05:
            txn_dict["total_amount"] = round(expected_total, 2)

        with self.lock:
            # Write to CSV
            with open(LIVE_CSV, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=HEADERS)
                writer.writerow(txn_dict)
            
            # Update memory
            self._process_row_in_memory(txn_dict)
            self.transactions.append(txn_dict)
            # Keep max 1000 in memory to avoid huge memory leak if running forever
            if len(self.transactions) > 1000:
                self.transactions.pop(0)

        return True

    def reset_live_data(self):
        with self.lock:
            with open(LIVE_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)
            
            self.transactions.clear()
            self.transaction_count = 0
            self.total_revenue = 0.0
            self.total_quantity = 0
            self.category_revenue.clear()
            self.product_revenue.clear()
            self.product_quantity.clear()
            self.product_txns.clear()
            self.payment_revenue.clear()
            self.payment_txns.clear()
            self.city_revenue.clear()
            self.city_txns.clear()
            self.city_quantity.clear()
            self.channel_revenue.clear()
            self.channel_txns.clear()
            self.channel_quantity.clear()
            self.revenue_trend.clear()
            self.latest_timestamp = None
        return True

    def get_summary(self):
        with self.lock:
            avg = self.total_revenue / self.transaction_count if self.transaction_count > 0 else 0.0
            return {
                "transaction_count": self.transaction_count,
                "total_revenue": round(self.total_revenue, 2),
                "total_quantity": self.total_quantity,
                "average_transaction_value": round(avg, 2),
                "latest_timestamp": self.latest_timestamp,
                "data_source": "LIVE_SIMULATED_RETAIL_DATA",
                "is_running": self.is_running
            }

    def get_transactions(self, limit=100):
        with self.lock:
            return list(reversed(self.transactions))[:limit]

    def get_products(self):
        with self.lock:
            res = []
            for pid, meta in self.product_metadata.items():
                res.append({
                    "product_id": pid,
                    "product_name": meta["name"],
                    "category": meta["category"],
                    "revenue": round(self.product_revenue[pid], 2),
                    "quantity": self.product_quantity[pid],
                    "transaction_count": self.product_txns[pid],
                    "average_price": meta["price"]
                })
            return sorted(res, key=lambda x: x["revenue"], reverse=True)

    def get_categories(self):
        with self.lock:
            res = [{"category": k, "revenue": round(v, 2)} for k, v in self.category_revenue.items()]
            return sorted(res, key=lambda x: x["revenue"], reverse=True)

    def get_payments(self):
        with self.lock:
            res = [{"payment_method": k, "transaction_count": self.payment_txns[k], "revenue": round(v, 2)} 
                   for k, v in self.payment_revenue.items()]
            return sorted(res, key=lambda x: x["revenue"], reverse=True)

    def get_cities(self):
        with self.lock:
            res = [{"city": k, "transaction_count": self.city_txns[k], "quantity": self.city_quantity[k], "revenue": round(v, 2)} 
                   for k, v in self.city_revenue.items()]
            return sorted(res, key=lambda x: x["revenue"], reverse=True)

    def get_channels(self):
        with self.lock:
            res = [{"channel": k, "transaction_count": self.channel_txns[k], "quantity": self.channel_quantity[k], "revenue": round(v, 2)} 
                   for k, v in self.channel_revenue.items()]
            return sorted(res, key=lambda x: x["revenue"], reverse=True)

    def get_revenue_trend(self):
        with self.lock:
            # Sort chronologically
            sorted_keys = sorted(self.revenue_trend.keys())
            # Return last 30 minutes to avoid huge charts
            recent = sorted_keys[-30:]
            return [{"date": k, "revenue": round(self.revenue_trend[k], 2)} for k in recent]

# Singleton instance
live_data_service = LiveDataService()
