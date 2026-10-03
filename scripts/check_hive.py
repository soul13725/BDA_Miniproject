import sys
import shutil
import subprocess
import os

# Ensure hadoop module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from scripts.check_hdfs import check_hdfs_availability
except ImportError:
    def check_hdfs_availability():
        return False

def check_hive_availability():
    """Detects whether Hive command is available on the system."""
    hive_executable = shutil.which("hive")
    
    if not hive_executable:
        return {"command": False, "executable": "NOT FOUND", "connection": False, "version": None}
        
    try:
        # Safe test to check if hive is properly configured
        result = subprocess.run(["hive", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            return {"command": True, "executable": hive_executable, "connection": True, "version": version}
        return {"command": True, "executable": hive_executable, "connection": False, "version": None}
    except Exception:
        return {"command": True, "executable": hive_executable, "connection": False, "version": None}

if __name__ == "__main__":
    print("Hive Availability")
    print("-----------------")
    
    hive_status = check_hive_availability()
    hdfs_available = check_hdfs_availability()
    
    if not hive_status["command"]:
        print("Hive command available: NO")
        print("Hive executable: NOT FOUND")
        print("Hive connection: UNAVAILABLE")
        print(f"HDFS available: {'YES' if hdfs_available else 'NO'}")
        print("Recommended analytics mode: LOCAL_FALLBACK")
        sys.exit(1)
    else:
        print("Hive command available: YES")
        print(f"Hive executable: {hive_status['executable']}")
        if hive_status["version"]:
            print(f"Hive version: {hive_status['version']}")
        print(f"Hive connection: {'AVAILABLE' if hive_status['connection'] else 'UNAVAILABLE'}")
        print(f"HDFS available: {'YES' if hdfs_available else 'NO'}")
        
        if hive_status['connection'] and hdfs_available:
            print("Recommended analytics mode: HIVE")
            sys.exit(0)
        else:
            print("Recommended analytics mode: LOCAL_FALLBACK")
            sys.exit(1)
