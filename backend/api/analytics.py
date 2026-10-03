import os
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from hive.hive_config import MODE, LOCAL_ANALYTICS_OUTPUT_DIRECTORY
    from scripts.check_hive import check_hive_availability
    from scripts.check_hdfs import check_hdfs_availability
except ImportError:
    MODE = "LOCAL_FALLBACK"
    LOCAL_ANALYTICS_OUTPUT_DIRECTORY = os.path.join(root_dir, "output", "hive")

    def check_hive_availability():
        return {"command": False, "connection": False}

    def check_hdfs_availability():
        return False

# Pydantic Models
class AnalyticsStatus(BaseModel):
    phase: str
    analytics_engine: str
    hive_available: bool
    hdfs_available: bool
    analytics_available: bool

class AnalyticsSummary(BaseModel):
    total_revenue: float
    total_transactions: int
    total_quantity: int
    average_transaction_value: float
    analytics_engine: str

class CategoryRevenue(BaseModel):
    category: str
    revenue: float

class ProductRevenue(BaseModel):
    product_id: str
    product_name: str
    revenue: float

class PaymentAnalysis(BaseModel):
    payment_method: str
    transaction_count: int
    revenue: float

class CityAnalysis(BaseModel):
    city: str
    transaction_count: int
    revenue: float

class ChannelAnalysis(BaseModel):
    channel: str
    transaction_count: int
    revenue: float

class DailyRevenue(BaseModel):
    date: str
    revenue: float

class MonthlyRevenue(BaseModel):
    month: str
    revenue: float

def check_outputs_exist():
    if not os.path.exists(LOCAL_ANALYTICS_OUTPUT_DIRECTORY):
        raise HTTPException(status_code=404, detail="Analytics outputs not found. Please run Phase 05 analytics.")
    if not os.path.exists(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "total_revenue.txt")):
        raise HTTPException(status_code=404, detail="Analytics outputs not found. Please run Phase 05 analytics.")

@router.get("/status", response_model=AnalyticsStatus)
async def get_status():
    hive_status = check_hive_availability()
    hdfs_available = check_hdfs_availability()
    
    analytics_avail = os.path.exists(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "total_revenue.txt"))

    return AnalyticsStatus(
        phase="06",
        analytics_engine=MODE,
        hive_available=hive_status["connection"],
        hdfs_available=hdfs_available,
        analytics_available=analytics_avail
    )

@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary():
    check_outputs_exist()
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "total_revenue.txt"), "r") as f:
            total_rev = float(f.read().strip())
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "average_transaction_value.txt"), "r") as f:
            avg_txn = float(f.read().strip())
            
        # We need to compute total_transactions from payments or channels
        txns = 0
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "payment_analysis.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    txns += int(parts[1])
                    
        total_qty = 0
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "category_quantity.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    total_qty += int(parts[1])

        return AnalyticsSummary(
            total_revenue=total_rev,
            total_transactions=txns,
            total_quantity=total_qty,
            average_transaction_value=avg_txn,
            analytics_engine=MODE
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading analytics summary: {str(e)}")

@router.get("/categories", response_model=List[CategoryRevenue])
async def get_categories():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "category_revenue.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    res.append(CategoryRevenue(category=parts[0], revenue=float(parts[1])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sorted(res, key=lambda x: x.revenue, reverse=True)

@router.get("/products", response_model=List[ProductRevenue])
async def get_products(limit: Optional[int] = None):
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "product_revenue.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    res.append(ProductRevenue(product_id=parts[0], product_name=parts[1], revenue=float(parts[2])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    res = sorted(res, key=lambda x: x.revenue, reverse=True)
    if limit:
        res = res[:limit]
    return res

@router.get("/payments", response_model=List[PaymentAnalysis])
async def get_payments():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "payment_analysis.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    res.append(PaymentAnalysis(payment_method=parts[0], transaction_count=int(parts[1]), revenue=float(parts[2])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sorted(res, key=lambda x: x.revenue, reverse=True)

@router.get("/cities", response_model=List[CityAnalysis])
async def get_cities():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "city_analysis.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    res.append(CityAnalysis(city=parts[0], transaction_count=int(parts[1]), revenue=float(parts[2])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sorted(res, key=lambda x: x.revenue, reverse=True)

@router.get("/channels", response_model=List[ChannelAnalysis])
async def get_channels():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "channel_analysis.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    res.append(ChannelAnalysis(channel=parts[0], transaction_count=int(parts[1]), revenue=float(parts[2])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sorted(res, key=lambda x: x.revenue, reverse=True)

@router.get("/daily", response_model=List[DailyRevenue])
async def get_daily():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "daily_revenue.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    res.append(DailyRevenue(date=parts[0], revenue=float(parts[1])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res

@router.get("/monthly", response_model=List[MonthlyRevenue])
async def get_monthly():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "monthly_revenue.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    res.append(MonthlyRevenue(month=parts[0], revenue=float(parts[1])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res

@router.get("/top-products", response_model=List[ProductRevenue])
async def get_top_products():
    check_outputs_exist()
    res = []
    try:
        with open(os.path.join(LOCAL_ANALYTICS_OUTPUT_DIRECTORY, "top_products.tsv"), "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    res.append(ProductRevenue(product_id=parts[0], product_name=parts[1], revenue=float(parts[2])))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sorted(res, key=lambda x: x.revenue, reverse=True)
