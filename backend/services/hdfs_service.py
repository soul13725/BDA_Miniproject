import os
from services.infrastructure_service import run_wsl_command

def sync_dataset_to_hdfs():
    """Uploads the local retail_logs.csv to HDFS /retail_bda/raw/retail_logs.csv"""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    dataset_path = os.path.join(root_dir, 'data', 'retail_logs.csv')
    
    if not os.path.exists(dataset_path):
        return {"success": False, "reason": "Local dataset not found"}
        
    # Check HDFS
    check = run_wsl_command("hdfs dfs -ls /")
    if not check["success"]:
        return {"success": False, "reason": "HDFS not available"}
        
    # Convert windows path to WSL path (mnt/e/...)
    # We can just use the absolute path within WSL by translating E:\ -> /mnt/e/
    wsl_path = dataset_path.replace("\\", "/").replace("e:/", "/mnt/e/").replace("E:/", "/mnt/e/")
    
    # Create directories
    run_wsl_command("hdfs dfs -mkdir -p /retail_bda/raw")
    run_wsl_command("hdfs dfs -mkdir -p /retail_bda/mapreduce/input")
    run_wsl_command("hdfs dfs -mkdir -p /retail_bda/mapreduce/output")
    run_wsl_command("hdfs dfs -mkdir -p /retail_bda/hive")
    
    # Upload
    upload_cmd = f"hdfs dfs -put -f '{wsl_path}' /retail_bda/raw/retail_logs.csv"
    res = run_wsl_command(upload_cmd, timeout=30)
    
    if res["success"]:
        return {"success": True, "reason": "Uploaded successfully"}
    else:
        return {"success": False, "reason": res["stderr"]}
