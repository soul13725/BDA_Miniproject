# Big Data Analytics Concepts Mapping

This document explains how core Big Data Analytics concepts from the academic syllabus map directly to the technical implementation of the Retail BDA Analytics Platform.

| BDA Concept | Project Implementation | Status |
|---|---|---|
| **Dataset Generation** | `retail_logs.csv` (Synthetic generation) | Executed |
| **Distributed Storage (HDFS)** | HDFS directory configurations (`hadoop/`) | Documented / Unavailable |
| **Data Ingestion** | Local storage extraction | Executed |
| **MapReduce Paradigm** | `mapper.py` and `reducer.py` logic | Executed locally |
| **Map Phase** | Tokenizing transactions by key | Executed locally |
| **Reduce Phase** | Aggregating metrics (sums, counts) | Executed locally |
| **Data Warehousing (Hive)** | External tables defined in `hiveQL` | Implemented / Unavailable |
| **Analytical Querying** | Equivalent analytical aggregations | Executed (via Fallback) |
| **REST APIs for Analytics** | FastAPI endpoints | Executed |
| **Data Visualization** | React dashboard with Recharts | Executed |

## Detailed Concept Breakdown

### 1. The Dataset
Big data begins with volume. The project generates 5,000 transaction records deterministically (using a fixed random seed). This ensures that while the data mimics real-world noise, the analytics outputs are consistently verifiable against a known baseline.

### 2. Distributed Storage (HDFS)
While unavailable in the current execution environment, the project implements the conceptual framework for HDFS. The scripts define HDFS interaction logic, expecting to upload the CSV to a raw zone (e.g., `/retail_bda/raw/`) from which MapReduce and Hive can consume it.

### 3. Processing (MapReduce)
The core of the analytics logic demonstrates the MapReduce paradigm:
- **Mappers** read lines, parse the schema, and yield key-value pairs (e.g., `Category \t Revenue`).
- **Shuffle & Sort** is handled conceptually by the environment before passing to the reducer.
- **Reducers** sum the values for each key to produce aggregate datasets.

### 4. Querying and Warehousing (Hive)
The project demonstrates schema-on-read principles through Hive. HiveQL scripts define an external table mapped directly over the CSV structure. Complex analytical queries (e.g., aggregating daily revenue trends) are drafted. A robust local fallback engine mimics this exactly to keep the pipeline intact.

### 5. Consumption Layer (FastAPI & React)
In modern architectures, Big Data insights must be accessible. The project builds a FastAPI backend to serve as the gateway, pulling the generated analytical TSVs into structured JSON payloads. The React frontend visualizes these JSON payloads to provide decision-makers with actionable insights.
