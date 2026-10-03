from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Real-Time Retail Big Data Analytics Platform",
)

from api.analytics import router as analytics_router
from api.live import router as live_router
from api.catalog import router as catalog_router

app.include_router(analytics_router)
app.include_router(live_router)
app.include_router(catalog_router)
# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------------------------
@app.get("/")
async def root():
    """Project identification endpoint."""
    return {
        "project": settings.app_name,
        "status": "running",
        "phase": settings.phase,
    }


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/api/health")
async def health_check():
    """Simple health-check endpoint consumed by the React frontend."""
    return {
        "status": "healthy",
        "backend": "FastAPI",
        "phase": "05",
        "dataset_exists": settings.dataset_path.exists(),
    }

# ---------------------------------------------------------------------------
# Storage Status
# ---------------------------------------------------------------------------
@app.get("/api/storage")
async def storage_status():
    """Returns the storage mode and dataset availability."""
    import sys
    import os
    # Add project root to path if needed to import hdfs_status
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
        
    try:
        from scripts.hdfs_status import get_status
        return get_status()
    except Exception as e:
        return {
            "mode": "local",
            "dataset_available": settings.dataset_path.exists(),
            "hdfs_available": False,
            "error": str(e)
        }


