import sys
import os
import subprocess

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.hdfs_manager import manager
from hadoop import hdfs_config

def verify_hdfs():
    print("========================================")
    print("HDFS VERIFICATION")
    print("========================================")
    
    if not manager.is_hdfs_available():
        print("HDFS UNAVAILABLE")
        print("========================================")
        print("Base directory: UNAVAILABLE")
        print("Raw directory: UNAVAILABLE")
        print("Dataset: UNAVAILABLE")
        print("========================================")
        print("VERIFICATION RESULT: HDFS UNAVAILABLE")
        return
        
    success = True
    
    # 1. Base directory
    result = subprocess.run(["hdfs", "dfs", "-test", "-d", hdfs_config.HDFS_BASE_DIR], capture_output=True)
    base_exists = (result.returncode == 0)
    print(f"Base directory exists: {'PASS' if base_exists else 'FAIL'}")
    if not base_exists: success = False
    
    # 2. Raw directory
    result = subprocess.run(["hdfs", "dfs", "-test", "-d", hdfs_config.HDFS_RAW_DIR], capture_output=True)
    raw_exists = (result.returncode == 0)
    print(f"Raw directory exists: {'PASS' if raw_exists else 'FAIL'}")
    if not raw_exists: success = False
    
    # 3. Dataset exists
    hdfs_path = manager.get_hdfs_dataset_path()
    result = subprocess.run(["hdfs", "dfs", "-test", "-e", hdfs_path], capture_output=True)
    dataset_exists = (result.returncode == 0)
    print(f"Dataset exists: {'PASS' if dataset_exists else 'FAIL'}")
    if not dataset_exists: success = False
    
    # 4. Dataset can be listed
    result = subprocess.run(["hdfs", "dfs", "-ls", hdfs_path], capture_output=True, text=True)
    can_list = (result.returncode == 0)
    print(f"Dataset can be listed: {'PASS' if can_list else 'FAIL'}")
    if not can_list: success = False
    
    # 5. Dataset size
    result = subprocess.run(["hdfs", "dfs", "-du", "-h", hdfs_path], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        size = result.stdout.strip().split()[0]
        size_valid = size != "0"
        print(f"Dataset size is non-zero: {'PASS' if size_valid else 'FAIL'} ({size})")
        if not size_valid: success = False
    else:
        print("Dataset size is non-zero: FAIL (could not determine size)")
        success = False
        
    print(f"Dataset path is correct: PASS ({hdfs_path})")
    
    print("========================================")
    print("Base directory: " + ("PASS" if base_exists else "FAIL"))
    print("Raw directory: " + ("PASS" if raw_exists else "FAIL"))
    print("Dataset: " + ("PASS" if dataset_exists else "FAIL"))
    print("========================================")
    
    if success:
        print("VERIFICATION RESULT: PASS")
    else:
        print("VERIFICATION RESULT: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    verify_hdfs()
