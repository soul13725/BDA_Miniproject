import os

# HDFS Integration Configuration

HDFS_ENABLED = os.environ.get("HDFS_ENABLED", "false").lower() == "true"
HDFS_NAMENODE = os.environ.get("HDFS_NAMENODE", "hdfs://localhost")
HDFS_PORT = os.environ.get("HDFS_PORT", "9000")

HDFS_BASE_DIR = "/retail_bda"
HDFS_RAW_DIR = f"{HDFS_BASE_DIR}/raw"
HDFS_MAPREDUCE_DIR = f"{HDFS_BASE_DIR}/mapreduce"
HDFS_HIVE_DIR = f"{HDFS_BASE_DIR}/hive"

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOCAL_DATASET = os.path.join(_project_root, "data", "retail_logs.csv")
