import sys
import os

# Ensure backend module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from services.infrastructure_service import infrastructure_service

def check_hive_availability():
    status = infrastructure_service.check_status()
    return {
        "command": status["hive"] == "ONLINE",
        "connection": status["hive"] == "ONLINE"
    }

def check_hdfs_availability():
    status = infrastructure_service.check_status()
    return status["hdfs"] == "ONLINE"

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
        print("Hive connection: AVAILABLE")
        print(f"HDFS available: {'YES' if hdfs_available else 'NO'}")
        
        if hive_status['connection'] and hdfs_available:
            print("Recommended analytics mode: HIVE")
            sys.exit(0)
        else:
            print("Recommended analytics mode: LOCAL_FALLBACK")
            sys.exit(1)
