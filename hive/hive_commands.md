# Hive Commands

> **Note:** The `hive` runtime and HDFS are currently **UNAVAILABLE** on this local machine. Analytics run seamlessly through a `LOCAL_FALLBACK` Python script.

## 1. Commands Actually Verified

These commands are run natively without Hive to check the environment and execute fallback logic.

**Check Hive Availability:**
```powershell
python scripts/check_hive.py
```

**Run Analytics (Uses Fallback):**
```powershell
python scripts/run_hive.py
```

**Validate Analytics:**
```powershell
python scripts/validate_hive.py
```

## 2. Commands To Run When Hive Is Installed

When Hadoop and Hive are properly provisioned, execute these commands sequentially to ingest and query the dataset.

**Initialize Database:**
```powershell
hive -f hive/create_database.hql
```

**Create External Table:**
```powershell
hive -f hive/create_tables.hql
```

**Execute Analytics:**
```powershell
hive -f hive/analytics.hql
```
