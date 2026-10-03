import time
import random
import threading
import json
from datetime import datetime
from pathlib import Path
from services.live_data_service import live_data_service

# Load catalog globally
catalog_dir = Path("../data/catalog")
# For the backend, the CWD is usually `e:\CODING\BDA PROJECT\backend`
# so the path to catalog is `../data/catalog`
catalog_dir = Path("..") / "data" / "catalog"
if not catalog_dir.exists():
    catalog_dir = Path("data/catalog") # Fallback if run from root

products = []
cities = []

try:
    with open(catalog_dir / "products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    with open(catalog_dir / "cities.json", "r", encoding="utf-8") as f:
        cities = json.load(f)
except Exception as e:
    print(f"Error loading catalog for live generator: {e}")

product_weights = [p.get("demand_weight", 1) for p in products] if products else []
city_weights = [c.get("demand_weight", 1) for c in cities] if cities else []
city_names = [c["city_name"] for c in cities] if cities else []

def transaction_generator_thread():
    payments = ["Card", "UPI", "Wallet", "Cash"]
    channels = ["Online", "Store"]

    while True:
        if live_data_service.is_running and products and cities:
            try:
                prod = random.choices(products, weights=product_weights, k=1)[0]
                qty = random.randint(1, 5)
                discount = random.choice([0, 5, 10])
                total = round((prod["unit_price"] * qty) * (1 - discount/100), 2)
                
                txn = {
                    "transaction_id": f"LVTXN{int(time.time() * 1000)}{random.randint(10,99)}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "customer_id": f"CUST{random.randint(1000, 9999)}",
                    "product_id": prod["product_id"],
                    "product_name": prod["product_name"],
                    "category": prod["category"],
                    "quantity": qty,
                    "unit_price": prod["unit_price"],
                    "discount_percent": discount,
                    "total_amount": total,
                    "payment_method": random.choice(payments),
                    "city": random.choices(city_names, weights=city_weights, k=1)[0],
                    "channel": random.choice(channels)
                }
                
                live_data_service.append_transaction(txn)
            except Exception as e:
                print(f"Generator error: {e}")
                
        # Interval: 2-5 seconds (configurable concept)
        time.sleep(random.uniform(2.0, 5.0))

generator_thread = threading.Thread(target=transaction_generator_thread, daemon=True)
generator_thread.start()

def start_generator():
    live_data_service.is_running = True

def stop_generator():
    live_data_service.is_running = False

def add_live_transaction(txn):
    live_data_service.append_transaction(txn)
