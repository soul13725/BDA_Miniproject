# RetailPulse

## Real-Time Retail Big Data Analytics Platform

> A modular Big Data Analytics platform for retail, built as an academic project.  
> **Current Phase:** Phase 12 — Branding & Polish

---

## 1. Project Overview

RetailPulse is a real-time retail Big Data analytics platform that ingests a continuously generated simulated retail transaction stream, performs live analytics, exposes analytics through FastAPI, and visualizes insights through an interactive React dashboard.

Because the current development environment does not have Hadoop, HDFS, or Hive installed, the system provides a validated local fallback execution path. The project retains HDFS and Hive integration artifacts so the same analytical architecture can be executed on a Hadoop/Hive environment later.

## 2. Problem Statement

Retail businesses generate massive amounts of transactional data. Analyzing this data to extract insights (such as revenue trends, category performance, and top-selling products) requires a scalable Big Data architecture that can process data efficiently and present it in an accessible format for decision-makers.

## 3. Objectives

- Generate a deterministic and realistic synthetic retail dataset.
- Implement Hadoop MapReduce jobs to calculate revenue aggregations.
- Design HiveQL scripts for advanced querying and data summarization.
- Provide a robust local fallback mechanism for environments lacking Big Data infrastructure.
- Develop a REST API using FastAPI to serve the analytical results.
- Build a responsive React dashboard to visualize the data with interactive charts.
- Maintain academic honesty by accurately reporting the execution engine.

## 4. Technology Stack

- **Frontend**: React 18, Vite 5, React Router 6, Recharts
- **Backend**: Python 3, FastAPI, Uvicorn, Pydantic
- **Big Data Engine (Intended)**: Hadoop HDFS, MapReduce, Hive
- **Big Data Engine (Current)**: Python Local Simulation (Pandas/CSV)

## 5. Architecture

```
                 RETAIL BDA ANALYTICS PLATFORM

               Live Simulated Retail Transaction Stream
                           │
                           ▼
             Live Dataset (retail_live_transactions.csv)
                           │
                           ▼
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
       MapReduce/HDFS               Hive / HiveQL  (Future)
            │                             │
            └──────────────┬──────────────┘
                           ▼
                 Live Analytics Engine
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                    React + Vite
                           │
                           ▼
                 Interactive Dashboard

* Note: Historical dataset (retail_logs.csv) is retained for baseline comparison.
```

## 6. Dataset

The project relies on a continuously generated live transaction stream (`data/live/retail_live_transactions.csv`) for real-time analytics. The platform also maintains a historical 5,000-record CSV file (`data/retail_logs.csv`) containing simulated retail transactions for baseline validation and comparison.

## 7. Hadoop/HDFS

Hadoop Distributed File System (HDFS) is intended for distributed storage of the dataset. Currently, HDFS is unavailable in the environment. The system gracefully falls back to local storage while preserving all HDFS setup scripts, configuration artifacts, and intended cluster paths (`/retail_bda/raw/`).

## 8. MapReduce

MapReduce logic is implemented to compute total revenue, category revenue, and product revenue. The mapper extracts keys and values from the dataset, the shuffle phase groups them, and the reducer aggregates the metrics. A local simulator validates the exact output that Hadoop Streaming would produce.

## 9. Hive/HiveQL

Hive provides a SQL-like interface for querying the data. External tables and analytics queries (e.g., daily trends, top products) are fully defined in `hive/`. As Hive is currently unavailable, a local fallback script uses Python to generate the identical aggregated TSV files.

## 10. FastAPI

FastAPI serves as the backend bridge. It securely reads the generated TSV outputs from the analytical pipeline and serves them as JSON using strict Pydantic models. It is completely aware of the infrastructure state and dynamically reports whether the data comes from Hive or the local fallback.

## 11. React Dashboard

A Vite + React application provides an interactive UI. It fetches data from the FastAPI endpoints using Axios and visualizes it using Recharts (Line, Bar, Pie charts). It features KPI cards, a top products table, and prominently displays the active analytics engine (e.g., `LOCAL_FALLBACK`).

## 12. Current Execution Mode

```text
Hadoop: UNAVAILABLE
HDFS: UNAVAILABLE
Hive: UNAVAILABLE
Analytics Engine: LOCAL_FALLBACK
```

## 13. Installation

Ensure you have **Python 3.10+** and **Node.js 18+**.

**Backend Setup:**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend Setup:**
```powershell
cd frontend
npm install
```

## 14. Quick Demo Workflow

1. Start FastAPI (`python -m uvicorn main:app --port 8000`)
2. Start React (`npm run dev`)
3. Open RetailPulse in browser
4. Click "Start" in the Live Data Control section
5. Observe live KPIs updating in real-time
6. Observe charts reacting to new data
7. Open Products page to see live analytics per product
8. Open Transactions page to see the raw event stream
9. Open BDA Pipeline page to review architecture
10. Explain HDFS/Hive fallback for historical processing

> **Note:** RetailPulse currently uses a simulated live retail transaction stream. The historical dataset is retained for MapReduce/Hive/BDA demonstration and regression testing.

## 15. Validation Commands

A single master validation script checks the entire pipeline:
```powershell
python scripts/final_validation.py
```

To run validations individually:
```powershell
python scripts/validate_data.py
python scripts/run_mapreduce.py
python scripts/validate_mapreduce.py
python scripts/check_hdfs.py
python scripts/check_hive.py
python scripts/run_hive.py
python scripts/validate_hive.py
```

## 16. API Endpoints

| Endpoint | Expected HTTP Status |
|---|---|
| `GET /` | 200 |
| `GET /api/health` | 200 |
| `GET /api/storage` | 200 |
| `GET /api/analytics/status` | 200 |
| `GET /api/analytics/summary` | 200 |
| `GET /api/analytics/categories` | 200 |
| `GET /api/analytics/products` | 200 |
| `GET /api/analytics/payments` | 200 |
| `GET /api/analytics/cities` | 200 |
| `GET /api/analytics/channels` | 200 |
| `GET /api/analytics/daily` | 200 |
| `GET /api/analytics/monthly` | 200 |
| `GET /api/analytics/top-products` | 200 |

## 17. Dashboard Features

- KPI Cards (Revenue, Transactions, Quantity, Avg Value)
- Revenue Trend (Line Chart)
- Monthly Revenue (Bar Chart)
- Category & Channel Analysis (Pie Charts)
- Payment & City Analysis (Bar Charts)
- Top Products Table
- Active Analytics Engine Badge
- Refresh Button and Error Handling

## 18. Results

- **Dataset Validation:** PASS (5,000 rows, 13 columns)
- **MapReduce Simulation:** PASS
- **Hive Fallback Execution:** PASS
- **Data Consistency:** PASS (Total Revenue matches across all layers: ₹18,044,188.70)
- **End-to-End Integration:** PASS

## 19. Current Limitations

- **Hadoop:** Not installed.
- **HDFS:** Not available (Local storage fallback is active).
- **Hive:** Not installed (HiveQL scripts are parsed by a local equivalent engine).
- **Dashboard:** Fully functional, but operating entirely on local fallback analytics.

## 20. Future Enhancements

- Deployment on an actual Hadoop cluster.
- Actual HDFS storage execution and Hive cluster integration.
- Real-time ingestion via Kafka.
- Spark Streaming for live analytics.
- Machine Learning for predictive sales forecasting.
- Customer segmentation and recommendation systems.

## 21. BDA Concepts Demonstrated

- **Distributed Storage Concept:** Designing directories and partition structures intended for HDFS.
- **MapReduce Paradigm:** Structuring logic into distinct Map, Shuffle/Sort, and Reduce phases.
- **Analytical Querying:** Modeling external tables over raw data for HiveQL aggregation.
- **Data Pipeline Integration:** Ensuring downstream systems (API/UI) consume aggregated datasets seamlessly, regardless of the compute engine.

## 22. Viva-Ready Project Workflow

```text
User opens dashboard
        ↓
React requests analytics from FastAPI
        ↓
FastAPI reads validated analytical outputs
        ↓
Outputs originated from local fallback analytics
        ↓
Local fallback reproduces Hive analytical operations
        ↓
HiveQL definitions are available for actual Hive infrastructure
        ↓
Dashboard renders KPIs and charts
```

## 23. Project Structure

```
Retail-BDA-Analytics/
├── backend/          ← FastAPI application
├── frontend/         ← React + Vite application
├── data/             ← CSV dataset
├── hadoop/           ← HDFS config & shell commands
├── mapreduce/        ← Mapper & Reducer scripts
├── hive/             ← HiveQL definitions & config
├── scripts/          ← Validation and generation scripts
├── output/           ← Processed analytics outputs
├── README.md         ← Project documentation
├── PHASES.md         ← Phase roadmap
└── .gitignore
```
