# Hive Analytics Integration

This directory contains the HiveQL scripts required to create databases, external tables, and perform various analytics queries on the retail dataset.

## Architecture

1. **Hive Database**: `retail_bda`
2. **Hive Table**: `retail_transactions` (External Table)
3. **Schema**: 13 columns (Matches Phase 02 CSV exact format).
4. **HDFS Source Path**: `/retail_bda/raw/`

## HiveQL Scripts
- `create_database.hql`: Creates the database context.
- `create_tables.hql`: Registers the external table against HDFS data.
- `analytics.hql`: Performs 11 distinct SQL aggregations and overwrites local directories with TSV files.

## Analytics Queries Implemented
1. Total Revenue
2. Revenue By Category
3. Revenue By Product
4. Quantity By Category
5. Average Transaction Value
6. Payment Method Analysis
7. City Analysis
8. Sales Channel Analysis
9. Daily Revenue
10. Monthly Revenue
11. Top 5 Products

## Infrastructure Limitations (Local Fallback)
Currently, Hive and HDFS are **UNAVAILABLE** on this machine.
Therefore, `scripts/run_hive.py` acts as a seamless **LOCAL_FALLBACK**. It avoids executing the `.hql` files through the absent `hive` runtime and instead uses native Python logic to generate the exact same analytical outputs under `output/hive/`. 

This local simulation ensures that frontend APIs and future phases can still consume these analytical datasets without blocking on heavy cluster provisioning.
