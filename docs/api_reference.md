# FastAPI Reference Guide

The backend FastAPI application acts as the Serving Layer for the Big Data Analytics platform. It securely parses processed TSV files from the Hive/Local Analytics engine and serves them as typed JSON responses.

**Base URL:** `http://127.0.0.1:8000`

---

### `GET /`
- **Purpose:** Project identification and simple connection test.
- **Response:** Basic metadata including project name and execution status.

### `GET /api/health`
- **Purpose:** Backend health-check endpoint.
- **Response:** Current Phase and boolean indicating if the CSV dataset exists.

### `GET /api/storage`
- **Purpose:** Checks HDFS vs Local storage mode.
- **Response:** JSON detailing if HDFS is connected or if local mode is active.

### `GET /api/analytics/status`
- **Purpose:** Evaluates the availability of Hadoop/Hive infrastructure.
- **Response:** JSON with `analytics_engine` (e.g., `LOCAL_FALLBACK`) and infrastructure boolean flags.
- **Dashboard Usage:** Displayed in the header badge.

### `GET /api/analytics/summary`
- **Purpose:** High-level Key Performance Indicators (KPIs).
- **Response:** JSON containing `total_revenue`, `total_transactions`, `total_quantity`, and `average_transaction_value`.
- **Dashboard Usage:** Powers the top KPI Cards.

### `GET /api/analytics/categories`
- **Purpose:** Revenue breakdown grouped by product category.
- **Response:** Array of `{category, revenue}` objects, sorted descending.
- **Dashboard Usage:** Powers the Category Pie Chart.

### `GET /api/analytics/products`
- **Purpose:** Revenue breakdown by individual product.
- **Response:** Array of `{product_id, product_name, revenue}` objects.

### `GET /api/analytics/payments`
- **Purpose:** Breakdown of payment methods utilized by customers.
- **Response:** Array of `{payment_method, transaction_count, revenue}` objects.
- **Dashboard Usage:** Powers the horizontal Payment Chart.

### `GET /api/analytics/cities`
- **Purpose:** Geographical revenue distribution.
- **Response:** Array of `{city, transaction_count, revenue}` objects.
- **Dashboard Usage:** Powers the City Bar Chart.

### `GET /api/analytics/channels`
- **Purpose:** Online vs. Store performance.
- **Response:** Array of `{channel, transaction_count, revenue}` objects.
- **Dashboard Usage:** Powers the Sales Channel Pie Chart.

### `GET /api/analytics/daily`
- **Purpose:** Time-series data of daily revenue.
- **Response:** Array of `{date, revenue}` objects for plotting over time.
- **Dashboard Usage:** Powers the main Revenue Trend Line Chart.

### `GET /api/analytics/monthly`
- **Purpose:** Aggregated monthly revenue.
- **Response:** Array of `{month, revenue}` objects.
- **Dashboard Usage:** Powers the Monthly Revenue Bar Chart.

### `GET /api/analytics/top-products`
- **Purpose:** Retrieves the top 5 highest-grossing products.
- **Response:** Array of the top 5 `{product_id, product_name, revenue}` objects.
- **Dashboard Usage:** Powers the Bottom Analytical Table.
