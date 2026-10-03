# RetailPulse — Real-Time Retail Big Data Analytics Platform — Phase Roadmap

> Each phase builds on the previous one.  
> Only **Phase 01** is currently implemented.

---

## PHASE 01 — Project Foundation
**Status:** ✅ COMPLETE

Establish the full-stack project scaffold:
- FastAPI backend with health-check endpoints and CORS
- React + Vite frontend with professional dark-theme UI
- Centralised configuration (pydantic-settings, pathlib)
- Axios API service with `VITE_API_BASE_URL` support
- Project directory structure for all future phases
- README, PHASES.md, .gitignore

---

## PHASE 02 — Dataset Generation and Validation
**Status:** ✅ COMPLETE

- Generate a realistic synthetic retail CSV dataset
- Validate schema, data types, and integrity
- Store dataset in the `data/` directory
- Expose a dataset-info endpoint in FastAPI

---

## PHASE 03 — Hadoop MapReduce Analytics
**Status:** ✅ COMPLETE

- Implement Hadoop MapReduce jobs for:
  - Sales aggregation by category
  - Revenue totals by store/region
  - Top-selling products
- Store mapper and reducer scripts in `mapreduce/`
- Run jobs locally using Hadoop Streaming

---

## PHASE 04 — HDFS Integration
**Status:** ✅ COMPLETE

- Upload retail dataset to HDFS
- Configure HDFS input/output directories
- Integrate MapReduce jobs with HDFS
- Store Hadoop configuration in `hadoop/`
- Implemented Local Fallback mechanism (Windows compatibility)

---

## PHASE 05 — Hive Analytics
**Status:** ✅ COMPLETE

- Create Hive external tables over HDFS data
- Write HiveQL queries for analytical reporting
- Store queries and schema DDL in `hive/`
- Export Hive query results to `output/`
- Provide `LOCAL_FALLBACK` equivalent processing

---

## PHASE 06 — Analytics API & Dashboard
**Status:** ✅ COMPLETE

- Expose Phase 05 analytics through FastAPI endpoints
- Create robust Pydantic response models
- Build Interactive React Dashboard
- Add KPI Cards and Charts using `recharts`
- Combine API and Dashboard into a single end-to-end integration

## PHASE 07 — Final Integration & Testing
**Status:** ✅ COMPLETE

- End-to-end integration testing
- Final documentation and academic report
- Submission readiness validation
- Final validation scripts

## PHASE 08 — Presentation & Viva Packaging
**Status:** ✅ COMPLETE
- Optimize project for academic demonstration.

## PHASE 09 & 10 — Real Infrastructure Audit & Live Ingestion
**Status:** ✅ COMPLETE
- Audit WSL/Hadoop/Hive infrastructure availability.
- Introduce live transaction generation and streaming APIs.

## PHASE 11 — Live-First Dataset & Real-Time Analytics
**Status:** ✅ COMPLETE
- Convert architecture to Live-First ingestion.
- Store real-time events in `data/live/retail_live_transactions.csv`.
- Create live analytical endpoints.
- Update React Dashboard to track real-time analytics by default.
- Retain historical data for baseline comparison.

---
*(End of Roadmap)*
