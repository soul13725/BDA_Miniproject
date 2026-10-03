import subprocess
import json
import os

def run_wsl_command(command, timeout=10):
    try:
        # We run the command through wsl. We don't assume a specific distribution, 
        # wsl will use the default one. 
        # Need to source environment or just run the command if it's in PATH.
        # To be safe, we invoke bash -ic to load profiles so hadoop/hive are in PATH
        cmd = ["wsl", "bash", "-ic", command]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }

class InfrastructureService:
    def __init__(self):
        # We cache the detection results to avoid slow WSL invocations on every API call.
        # In a real app, this might be periodically refreshed.
        self._status = None

    def check_status(self, force_refresh=False):
        if self._status and not force_refresh:
            return self._status

        status = {
            "python": "ONLINE",
            "fastapi": "ONLINE",
            "react": "ONLINE",
            "historical_dataset": "OFFLINE",
            "hadoop": "OFFLINE",
            "hdfs": "OFFLINE",
            "yarn": "OFFLINE",
            "mapreduce": "LOCAL_FALLBACK",
            "mapreduce_output": "LOCAL OUTPUT",
            "hive": "OFFLINE",
            "hive_server": "OFFLINE",
            "hiveql": "LOCAL_FALLBACK",
            "analytics_engine": "LOCAL_FALLBACK"
        }

        # Check Historical Dataset
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        dataset_path = os.path.join(root_dir, 'data', 'retail_logs.csv')
        if os.path.exists(dataset_path):
            status["historical_dataset"] = "ONLINE"

        # Check WSL availability
        wsl_check = run_wsl_command("echo wsl_works", timeout=5)
        if not wsl_check["success"]:
            self._status = status
            return status

        # Check Hadoop
        hadoop_check = run_wsl_command("hadoop version", timeout=10)
        if hadoop_check["success"] and "Hadoop" in hadoop_check["stdout"]:
            status["hadoop"] = "ONLINE"
        else:
            self._status = status
            return status # if hadoop is offline, others are too

        # Check HDFS
        hdfs_check = run_wsl_command("hdfs dfs -ls /", timeout=10)
        if hdfs_check["success"]:
            status["hdfs"] = "ONLINE"

        # Check YARN
        yarn_check = run_wsl_command("yarn version", timeout=10)
        if yarn_check["success"]:
            status["yarn"] = "ONLINE"

        # Check Hive
        hive_check = run_wsl_command("hive --version", timeout=15)
        if hive_check["success"] and "Hive" in hive_check["stdout"]:
            status["hive"] = "ONLINE"
            
        # Check HiveServer2 (Optional heuristic, checking if port 10000 is listening)
        # Using netstat or ss in WSL
        hs2_check = run_wsl_command("ss -tln | grep 10000", timeout=5)
        if hs2_check["success"] and "10000" in hs2_check["stdout"]:
            status["hive_server"] = "ONLINE"

        self._status = status
        return status

infrastructure_service = InfrastructureService()
