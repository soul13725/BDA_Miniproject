import time
import random
import threading
from datetime import datetime
from services.live_data_service import live_data_service

def transaction_generator_thread():
    categories = ["Electronics", "Fashion", "Home", "Stationery"]
    products = [
        {"id": "P001", "name": "Wireless Mouse", "category": "Electronics", "price": 599.00},
        {"id": "P005", "name": "Smartphone", "category": "Electronics", "price": 24995.00},
        {"id": "P008", "name": "T-Shirt", "category": "Fashion", "price": 799.00},
        {"id": "P011", "name": "Chair", "category": "Home", "price": 4500.00},
        {"id": "P002", "name": "Notebook", "category": "Stationery", "price": 150.00}
    ]
    cities = ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad", "Chennai"]
    payments = ["Card", "UPI", "Wallet", "Cash"]
    channels = ["Online", "Store"]

    while True:
        if live_data_service.is_running:
            try:
                prod = random.choice(products)
                qty = random.randint(1, 5)
                discount = random.choice([0, 5, 10])
                total = round((prod["price"] * qty) * (1 - discount/100), 2)
                
                txn = {
                    "transaction_id": f"LVTXN{int(time.time() * 1000)}{random.randint(10,99)}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "customer_id": f"CUST{random.randint(1000, 9999)}",
                    "product_id": prod["id"],
                    "product_name": prod["name"],
                    "category": prod["category"],
                    "quantity": qty,
                    "unit_price": prod["price"],
                    "discount_percent": discount,
                    "total_amount": total,
                    "payment_method": random.choice(payments),
                    "city": random.choice(cities),
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
