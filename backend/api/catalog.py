from fastapi import APIRouter, Query
from typing import Optional, List
import json
from pathlib import Path
from pydantic import BaseModel
import os

router = APIRouter(prefix="/api/catalog", tags=["catalog"])

catalog_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'catalog')))

# Load catalog in memory
products = []
categories = []
try:
    with open(catalog_dir / "products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    with open(catalog_dir / "categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)
except Exception as e:
    print(f"Error loading catalog in API: {e}")

from services.live_data_service import live_data_service

class ProductResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int

@router.get("/products", response_model=ProductResponse)
def get_catalog_products(
    page: int = 1,
    page_size: int = 50,
    search: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    product_class: Optional[str] = None,
    brand: Optional[str] = None,
    sort_by: Optional[str] = "revenue",
    sort_order: Optional[str] = "desc"
):
    # Join with live stats
    enriched = []
    
    # We need to lock while reading live stats to be thread-safe
    with live_data_service.lock:
        live_rev = dict(live_data_service.product_revenue)
        live_qty = dict(live_data_service.product_quantity)
        live_txns = dict(live_data_service.product_txns)

    for p in products:
        pid = p["product_id"]
        p_copy = p.copy()
        p_copy["revenue"] = live_rev.get(pid, 0.0)
        p_copy["quantity"] = live_qty.get(pid, 0)
        p_copy["transaction_count"] = live_txns.get(pid, 0)
        enriched.append(p_copy)

    # Filtering
    if search:
        search_lower = search.lower()
        enriched = [p for p in enriched if search_lower in p["product_name"].lower() or search_lower in p["product_id"].lower()]
    
    if category and category != "All":
        enriched = [p for p in enriched if p["category"] == category]
        
    if subcategory and subcategory != "All":
        enriched = [p for p in enriched if p["subcategory"] == subcategory]
        
    if product_class and product_class != "All":
        enriched = [p for p in enriched if p.get("product_class") == product_class]
        
    if brand and brand != "All":
        enriched = [p for p in enriched if p.get("brand") == brand]
        
    # Sorting
    if sort_by in ["unit_price", "revenue", "quantity", "transaction_count"]:
        reverse = sort_order == "desc"
        enriched = sorted(enriched, key=lambda x: x[sort_by], reverse=reverse)

    total = len(enriched)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "items": enriched[start:end],
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/filters")
def get_filters():
    cats = list(set(p["category"] for p in products))
    subcats = list(set(p["subcategory"] for p in products))
    pclasses = list(set(p.get("product_class", "Shopping") for p in products))
    brands = list(set(p.get("brand", "Generic") for p in products))
    
    return {
        "categories": sorted(cats),
        "subcategories": sorted(subcats),
        "product_classes": sorted(pclasses),
        "brands": sorted(brands)
    }
