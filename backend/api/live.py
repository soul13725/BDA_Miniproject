from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.live_transaction_generator import start_generator, stop_generator

router = APIRouter(prefix="/api/live", tags=["live"])

class TransactionEvent(BaseModel):
    transaction_id: str
    timestamp: str
    customer_id: str
    product_id: str
    product_name: str
    category: str
    quantity: int
    unit_price: float
    discount_percent: float
    total_amount: float
    payment_method: str
    city: str
    channel: str

from services.live_data_service import live_data_service

@router.get("/status")
def get_status():
    return {
        "status": "ONLINE",
        "is_running": live_data_service.is_running,
        "data_source": "LIVE SIMULATED RETAIL DATA"
    }

@router.post("/start")
def start_stream():
    start_generator()
    return {"status": "started"}

@router.post("/stop")
def stop_stream():
    stop_generator()
    return {"status": "stopped"}

@router.post("/reset")
def reset_stream():
    live_data_service.reset_live_data()
    return {"status": "reset"}

@router.get("/summary")
def get_summary():
    return live_data_service.get_summary()

@router.get("/transactions")
def get_transactions(limit: int = 100):
    return live_data_service.get_transactions(limit=limit)

@router.post("/transactions")
def ingest_transaction(event: TransactionEvent):
    success = live_data_service.append_transaction(event.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Invalid transaction data")
    return {"status": "ingested", "transaction_id": event.transaction_id}

@router.get("/products")
def get_products():
    return live_data_service.get_products()

@router.get("/categories")
def get_categories():
    return live_data_service.get_categories()

@router.get("/payments")
def get_payments():
    return live_data_service.get_payments()

@router.get("/cities")
def get_cities():
    return live_data_service.get_cities()

@router.get("/channels")
def get_channels():
    return live_data_service.get_channels()

@router.get("/revenue-trend")
def get_revenue_trend():
    return live_data_service.get_revenue_trend()
