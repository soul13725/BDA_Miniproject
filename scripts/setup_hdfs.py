import sys
import os
import subprocess

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.hdfs_manager import manager
from hadoop import hdfs_config

def setup_hdfs():
    print("========================================")
    print("HDFS DIRECTORY SETUP")
    print("========================================")
    
    if not manager.is_hdfs_available():
        print("HDFS is unavailable on this machine.")
        print("HDFS setup was SKIPPED.")
        print("The local fallback mode remains available.")
        print("========================================")
        print("SETUP RESULT: SKIPPED")
        return
        
    directories = [
        hdfs_config.HDFS_BASE_DIR,
        hdfs_config.HDFS_RAW_DIR,
        hdfs_config.HDFS_MAPREDUCE_DIR,
        f"{hdfs_config.HDFS_MAPREDUCE_DIR}/input",
        f"{hdfs_config.HDFS_MAPREDUCE_DIR}/output",
        hdfs_config.HDFS_HIVE_DIR
    ]
    
    success = True
    for directory in directories:
        print(f"Creating directory: {directory}")
        try:
            result = subprocess.run(
                ["hdfs", "dfs", "-mkdir", "-p", directory],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                print(f"FAIL: {result.stderr.strip()}")
                success = False
            else:
                print("PASS")
        except Exception as e:
            print(f"ERROR: {str(e)}")
            success = False
            
    print("========================================")
    if success:
        print("SETUP RESULT: PASS")
    else:
        print("SETUP RESULT: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    setup_hdfs()
