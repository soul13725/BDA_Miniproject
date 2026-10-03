# RETAILPULSE — 5 MINUTE DEMO

1. Project Introduction
RetailPulse is a real-time retail Big Data analytics platform that ingests live simulated transactions and provides instantaneous analytical insights through an interactive dashboard.

2. Architecture
The system consists of a live Python transaction generator, a FastAPI backend serving real-time KPIs, and a React + Vite dashboard displaying interactive Recharts. A historical dataset and MapReduce/Hive fallback path are preserved for batch analytical regression testing.

3. Start Backend
Run `python -m uvicorn main:app --port 8000` from the `backend/` directory to start the FastAPI server.

4. Start Frontend
Run `npm run dev` from the `frontend/` directory to launch the Vite development server.

5. Start Live Stream
Open the RetailPulse dashboard (default: http://localhost:5173). Under the "Live Data Control" section, click the "Start" button to begin generating live simulated retail transactions.

6. Explain Live KPIs
Observe the "Live Revenue", "Live Transactions", "Live Quantity", and "Live Avg Transaction" KPI cards. These numbers increment in real-time as the data stream is processed by the backend.

7. Explain Products
Navigate to the "Products" page. Show the live product analytics table dynamically updating. Demonstrate the search functionality, category filtering, and sorting capabilities across live metrics.

8. Explain Transactions
Navigate to the "Transactions" page. Show the raw event stream flowing into the application in reverse chronological order, displaying the most recent transactions first.

9. Explain BDA Pipeline
Navigate to the "BDA Pipeline" page. Explain the two parallel architectures: the "Live Stream Architecture" powering the current demonstration, and the "Historical BDA Processing" pathway for batch analytics.

10. Explain HDFS/Hive
Discuss the intended use of Hadoop Distributed File System (HDFS) and Hive for large-scale distributed storage and SQL-like analytics on historical data.

11. Explain Local Fallback
Point out that because true HDFS/Hive infrastructure is unavailable in the current local Windows environment, the application intelligently routes historical queries through a Local Analytics Engine (Python/Pandas) that mimics HiveQL outputs exactly.

12. Explain Big Data Concepts
Highlight how the platform embodies core Big Data principles: Velocity (real-time stream), Volume (historical data processing capability), and Veracity (strict schema validation).

13. Conclusion
Summarize that RetailPulse successfully bridges the gap between high-velocity real-time event streaming and reliable historical batch processing, creating a comprehensive analytical platform.
