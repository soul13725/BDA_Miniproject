# HDFS Integration Commands

> **Note:** Hadoop and HDFS are currently unavailable on this Windows machine. The execution defaults to the LOCAL FALLBACK MODE to allow Phase 04 testing to pass. The commands below document the actual verification tools available right now, as well as the Hadoop commands to be used when HDFS is deployed.

## 1. Actual Verified Commands (Run locally)

These commands do not require Hadoop and can be executed natively in Windows PowerShell.

**Check HDFS availability:**
```powershell
python scripts/check_hdfs.py
```

**Verify storage mode (Local Fallback):**
```powershell
python scripts/verify_storage.py
```

**Setup HDFS (Gracefully skips if unavailable):**
```powershell
python scripts/setup_hdfs.py
```

**Upload to HDFS (Gracefully skips if unavailable):**
```powershell
python scripts/upload_to_hdfs.py
```

**Verify HDFS (Gracefully reports unavailable if missing):**
```powershell
python scripts/verify_hdfs.py
```

## 2. HDFS Architecture

```
HDFS
│
└── /retail_bda
    │
    ├── raw
    │   └── retail_logs.csv
    │
    ├── mapreduce
    │   ├── input
    │   └── output
    │
    └── hive
```

## 3. Commands To Run When Hadoop is Available

The scripts implement subprocess wrappers around the following Hadoop commands. If running manually, here is the reference.

**Creating directories:**
```bash
hdfs dfs -mkdir -p /retail_bda/raw
hdfs dfs -mkdir -p /retail_bda/mapreduce/input
hdfs dfs -mkdir -p /retail_bda/mapreduce/output
hdfs dfs -mkdir -p /retail_bda/hive
```

**Uploading dataset:**
```bash
hdfs dfs -put -f data/retail_logs.csv /retail_bda/raw/retail_logs.csv
```

**Listing files:**
```bash
hdfs dfs -ls /retail_bda/raw
```

**Verifying dataset:**
```bash
hdfs dfs -test -e /retail_bda/raw/retail_logs.csv
hdfs dfs -du -h /retail_bda/raw/retail_logs.csv
```

**Removing old MapReduce output:**
```bash
hdfs dfs -rm -r -skipTrash /retail_bda/mapreduce/output/total_revenue
```

**Downloading output:**
```bash
hdfs dfs -get /retail_bda/mapreduce/output/total_revenue/part-00000 output/mapreduce/total_revenue.txt
```

### Required Hadoop Environment

When HDFS becomes available, ensure:
1. `HADOOP_HOME` is set.
2. `hadoop/bin` is in the PATH.
3. Hadoop cluster (NameNode and DataNode) is started via `start-dfs.sh` or `start-dfs.cmd` on Windows.
