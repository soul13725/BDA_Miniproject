import sys
import os

# Ensure backend module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from services.infrastructure_service import infrastructure_service

def check_hdfs_availability():
    status = infrastructure_service.check_status()
    return status["hdfs"] == "ONLINE"

if __name__ == "__main__":
    if check_hdfs_availability():
        print("HDFS AVAILABLE")
        sys.exit(0)
    else:
        print("HDFS UNAVAILABLE")
        sys.exit(1)
