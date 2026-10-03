import os
import sys
import json
import subprocess

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.hdfs_manager import manager
from hadoop import hdfs_config

def get_status():
    local_dataset_exists = os.path.exists(manager.get_local_dataset_path())
    hdfs_dataset_exists = False
    
    if manager.is_hdfs_available():
        try:
            result = subprocess.run(
                ["hdfs", "dfs", "-test", "-e", manager.get_hdfs_dataset_path()],
                capture_output=True,
                check=False
            )
            hdfs_dataset_exists = (result.returncode == 0)
        except Exception:
            hdfs_dataset_exists = False
            
    status = {
        "mode": manager.get_mode(),
        "hdfs_command_available": manager.is_hdfs_available(),
        "hdfs_connection_available": manager.is_hdfs_available(),
        "dataset_available": local_dataset_exists,
        "hdfs_dataset_available": hdfs_dataset_exists
    }
    
    return status

if __name__ == "__main__":
    status = get_status()
    print(json.dumps(status, indent=4))
