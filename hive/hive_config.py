import os
import sys

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.check_hive import check_hive_availability
from scripts.check_hdfs import check_hdfs_availability

# Hive Analytics Configuration

HIVE_ENABLED = os.environ.get("HIVE_ENABLED", "false").lower() == "true"
HIVE_DATABASE = os.environ.get("HIVE_DATABASE", "retail_bda")
HIVE_TABLE = os.environ.get("HIVE_TABLE", "retail_transactions")

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HIVE_SCRIPT_DIRECTORY = os.path.join(_project_root, "hive")
HIVE_OUTPUT_DIRECTORY = os.path.join(_project_root, "output", "hive")

LOCAL_ANALYTICS_OUTPUT_DIRECTORY = os.path.join(_project_root, "output", "hive")
LOCAL_DATASET = os.path.join(_project_root, "data", "retail_logs.csv")

def get_analytics_mode():
    hive_status = check_hive_availability()
    hdfs_available = check_hdfs_availability()
    
    if hive_status["connection"] and hdfs_available and HIVE_ENABLED:
        return "HIVE"
    return "LOCAL_FALLBACK"

MODE = get_analytics_mode()
