# Presentation Outline

This document provides a 12-slide structure for presenting the Retail BDA Analytics Platform during an academic evaluation.

### Slide 1: Title Slide
- **Title:** Retail BDA Analytics Platform
- **Subtitle:** An end-to-end Big Data Analytics Pipeline
- **Details:** Your Name, Roll Number, Course, Date

### Slide 2: Problem Statement
- **Context:** Modern retail produces massive volumes of transactional data.
- **Problem:** Traditional relational databases struggle to process and aggregate this data at scale.
- **Solution:** A scalable Big Data architecture to extract actionable insights (trends, top products, category performance).

### Slide 3: Objectives
- Generate a realistic synthetic retail dataset.
- Implement MapReduce logic to aggregate massive data.
- Design HiveQL data warehousing scripts.
- Develop a REST API to serve analytics.
- Build an interactive React dashboard for visualization.

### Slide 4: System Architecture
- *Include a visual diagram of the architecture.*
- Explain the flow: CSV → HDFS → MapReduce → Hive → FastAPI → React Dashboard.

### Slide 5: The Dataset
- **Source:** Synthetic deterministic generation (5,000 records).
- **Structure:** 13 columns including Transaction ID, Category, Quantity, Price, City, Channel.
- **Goal:** Provide a stable, verifiable baseline for analytical output validation.

### Slide 6: HDFS + MapReduce
- **HDFS:** The distributed storage layer intended to hold the raw CSV across commodity hardware.
- **MapReduce:** 
  - **Mapper:** Extracts specific keys (e.g., Category).
  - **Reducer:** Aggregates values (e.g., sums revenue).
  - Designed to process data in parallel chunks.

### Slide 7: Hive & Data Warehousing
- **Concept:** Schema-on-read over the raw HDFS files.
- **Implementation:** HiveQL scripts mapping the CSV to an external table.
- **Analytics:** Performing complex grouping (daily trends, top performing products) using SQL-like syntax.

### Slide 8: The Local Fallback Engine
- **Academic Context:** Running a full Hadoop/Hive cluster locally on Windows is often unfeasible.
- **Solution:** The platform detects missing infrastructure and automatically switches to a Python-based execution engine.
- **Benefit:** Allows the end-to-end integration (Data → API → Dashboard) to be demonstrated and validated locally without fabricating execution claims.

### Slide 9: FastAPI Backend
- **Role:** The Serving Layer.
- **Tech:** Python, FastAPI, Pydantic.
- **Function:** Safely parses the TSV outputs from the analytics engine and serves them as strictly typed, validated JSON over REST endpoints.

### Slide 10: React Analytics Dashboard
- **Role:** The Presentation Layer.
- **Tech:** React, Vite, Recharts, Axios.
- **Features:** KPI cards, interactive Line/Bar/Pie charts, Responsive UI.
- **Highlight:** Real-time fetching of data from FastAPI.

### Slide 11: Results
- **Dataset:** 5,000 rows generated successfully.
- **Total Revenue Processed:** ₹18,044,188.70 matching exactly across MapReduce, Hive, and Dashboard layers.
- **Integration:** 100% end-to-end integration achieved.

### Slide 12: Limitations & Future Scope
- **Limitations:** Current execution relies on a local fallback engine; it is limited by single-machine memory constraints.
- **Future Scope:** 
  - Deploy to AWS EMR or Dockerized Hadoop cluster.
  - Implement real-time streaming via Apache Kafka.
  - Apply Machine Learning for predictive analytics.
