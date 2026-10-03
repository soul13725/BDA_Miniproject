import sys
import os
import subprocess

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.hdfs_manager import manager
from hadoop import hdfs_config

def upload_to_hdfs():
    print("========================================")
    print("HDFS DATASET UPLOAD")
    print("========================================")
    
    local_path = manager.get_local_dataset_path()
    hdfs_path = manager.get_hdfs_dataset_path()
    
    if not manager.is_hdfs_available():
        print("HDFS is unavailable on this machine.")
        print("Upload was not performed.")
        print("Upload skipped because HDFS is unavailable.")
        print("Local dataset remains available.")
        print("========================================")
        print("UPLOAD RESULT: SKIPPED")
        return
        
    if not os.path.exists(local_path):
        print(f"ERROR: Local dataset '{local_path}' does not exist.")
        print("UPLOAD RESULT: FAIL")
        sys.exit(1)
        
    print(f"Uploading {local_path} -> {hdfs_path}")
    try:
        # Create parent directory first
        subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_config.HDFS_RAW_DIR], check=False)
        
        # Upload file
        result = subprocess.run(
            ["hdfs", "dfs", "-put", "-f", local_path, hdfs_path],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print(f"FAIL: {result.stderr.strip()}")
            print("========================================")
            print("UPLOAD RESULT: FAIL")
            sys.exit(1)
            
        # Verify file exists and get size
        du_result = subprocess.run(
            ["hdfs", "dfs", "-du", "-h", hdfs_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        if du_result.returncode == 0:
            size_info = du_result.stdout.strip().split()[0]
            print(f"Upload successful. HDFS file size: {size_info}")
        else:
            print("Upload successful.")
            
        print("========================================")
        print("UPLOAD RESULT: PASS")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("========================================")
        print("UPLOAD RESULT: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    upload_to_hdfs()
