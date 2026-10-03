import sys
import subprocess
import shutil

def check_hdfs_availability():
    """Detects whether HDFS command is available on the system."""
    hdfs_executable = shutil.which("hdfs")
    
    if not hdfs_executable:
        return False
        
    try:
        # Safe test to check if hdfs is properly configured
        result = subprocess.run(["hdfs", "dfs", "-help"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        return False
    except Exception:
        return False

if __name__ == "__main__":
    if check_hdfs_availability():
        print("HDFS AVAILABLE")
        sys.exit(0)
    else:
        print("HDFS UNAVAILABLE")
        sys.exit(1)
