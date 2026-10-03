# RetailPulse Architecture

## 1. System Architecture
RetailPulse is a Real-Time Retail Big Data Analytics Platform. It uses a dual-pipeline architecture to process both live simulated transactions and batch historical records, merging them seamlessly into a unified React dashboard.

## 2. Data Flow
```text
                         RETAILPULSE
                              |
              +---------------+---------------+
              |                               |
        HISTORICAL DATA                  LIVE DATA
              |                               |
      Canonical Catalog                Canonical Catalog
              |                               |
      Historical Generator             Live Generator
              |                               |
      retail_logs.csv              live_transactions.csv
              |                               |
              v                               v
             HDFS                       Live Analytics
              |
              v
         MapReduce
              |
              v
      MapReduce Output
              |
              v
            Hive
              |
              v
           HiveQL
              |
              +---------------+
                              |
                              v
                           FastAPI
                              |
                              v
                         React + Vite
                              |
                              v
                       RetailPulse UI
```

### Fallback Architecture
If Hadoop, HDFS, or Hive are offline, the system automatically routes to:
```text
Local CSV -> Pandas Analytics -> FastAPI -> React
```

## 3. Catalog Architecture
A canonical JSON catalog (`data/catalog/`) acts as the single source of truth, removing hardcoded logic from code.
- `products.json`
- `categories.json`
- `cities.json`

## 4. Historical Pipeline
Python scripts generate a `retail_logs.csv` by sampling the catalog with demand weights.

## 5. Live Pipeline
A background thread in the FastAPI backend (`backend/services/live_transaction_generator.py`) generates transactions continuously from the same catalog.

## 6. HDFS Architecture
If configured, data is loaded into `/retail_bda/raw/retail_logs.csv`.

## 7. MapReduce Architecture
Hadoop streaming or local python simulation runs mappers and reducers (`scripts/run_mapreduce.py`) over the dataset.

## 8. Hive Architecture
HiveQL creates external tables and runs queries over MapReduce output.

## 9. FastAPI Architecture
Serves live memory aggregates, historical MapReduce/Hive results, and paginated dynamic catalog data.

## 10. React Architecture
Vite + React SPA providing dashboards, transaction viewers, product catalogs, and pipeline visualizers.

## 11. Fallback Architecture
Handled via `scripts/check_hdfs.py` and `scripts/check_hive.py`. If absent, analytics fall back to reading simulated MapReduce local outputs.

## 12. Infrastructure Requirements
- Node.js >= 18
- Python >= 3.8
- Optional: Hadoop 3.3.6, Hive 4.0.1 (WSL2 / Linux recommended)

## 13. Startup Instructions
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 14. Validation Instructions
Run `python scripts/final_validation.py` to assert data integrity against catalog logic.

## 15. Troubleshooting
If the dashboard appears blank, ensure port 8000 is free and the FastAPI backend is running.
