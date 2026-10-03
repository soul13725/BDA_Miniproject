# Submission Screenshot & Demo Checklist

Before submitting the final academic report, ensure you have captured screenshots or recorded demonstrations of the following key components.

## 1. Codebase & Structure
- [ ] Screenshot of the root directory structure (showing `backend`, `frontend`, `hadoop`, `hive`, `mapreduce`).
- [ ] Screenshot of `.gitignore` proving clean dependency management.

## 2. Dataset Generation
- [ ] Screenshot of `data/retail_logs.csv` open in a text editor showing the headers and first few rows.
- [ ] Terminal screenshot running `python scripts/validate_data.py` showing `PASS`.

## 3. Big Data Execution
- [ ] Terminal screenshot running `python scripts/run_mapreduce.py` and `validate_mapreduce.py`.
- [ ] Screenshot of the MapReduce output file `output/mapreduce/category_revenue.tsv`.
- [ ] Terminal screenshot running `python scripts/check_hdfs.py` (proving the architecture handles infrastructure states dynamically).
- [ ] Screenshot of `hive/analytics.hql` showing the SQL-like query structure.
- [ ] Terminal screenshot running `python scripts/run_hive.py` showing successful Local Fallback execution.

## 4. API & Backend
- [ ] Terminal screenshot showing `uvicorn main:app` running successfully on port 8000.
- [ ] Browser screenshot of `http://localhost:8000/docs` (Swagger UI) showing the list of available `/api/analytics/` endpoints.
- [ ] Browser screenshot showing raw JSON output from `http://localhost:8000/api/analytics/summary`.

## 5. React Dashboard
- [ ] Browser screenshot of the full Dashboard UI loaded at `http://localhost:5173`.
- [ ] Close-up screenshot of the KPI Cards (highlighting Total Revenue).
- [ ] Close-up screenshot of the "Revenue Trend" Line Chart.
- [ ] Close-up screenshot of the Category Pie Chart.
- [ ] Close-up screenshot of the Top Products data table.
- [ ] Close-up screenshot of the "Analytics Engine: LOCAL FALLBACK" status badge.

## 6. Final Validation
- [ ] Terminal screenshot running `python scripts/final_validation.py` showing the `OVERALL PROJECT STATUS: PASS` at the end.
