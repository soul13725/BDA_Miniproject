import sys
import os

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.hdfs_manager import manager
from scripts.validate_data import validate_data
from pathlib import Path

def verify_storage():
    print("========================================")
    print("STORAGE STATUS VERIFICATION")
    print("========================================")
    
    mode = manager.get_mode().upper()
    print(f"Storage mode:\n{mode} MODE\n")
    
    if mode == "LOCAL":
        local_path = manager.get_local_dataset_path()
        dataset_exists = os.path.exists(local_path)
        
        print(f"Dataset available:\n{'YES' if dataset_exists else 'NO'}\n")
        print(f"Local dataset exists: {'PASS' if dataset_exists else 'FAIL'}")
        
        if dataset_exists:
            print("\nRunning dataset validation...")
            validation_success = validate_data(Path(local_path))
            print(f"Dataset validation: {'PASS' if validation_success else 'FAIL'}")
            
            if not validation_success:
                print("========================================")
                print("VERIFICATION RESULT: FAIL")
                sys.exit(1)
        else:
            print("========================================")
            print("VERIFICATION RESULT: FAIL")
            sys.exit(1)
            
    elif mode == "HDFS":
        hdfs_path = manager.get_hdfs_dataset_path()
        print(f"HDFS dataset path to verify: {hdfs_path}")
        print("Run scripts/verify_hdfs.py to fully verify HDFS dataset.")
        
    print("========================================")
    print("VERIFICATION RESULT: PASS")

if __name__ == "__main__":
    verify_storage()
