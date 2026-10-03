import os
from services.infrastructure_service import run_wsl_command, infrastructure_service

def run_real_mapreduce():
    """Executes the Hadoop Streaming MapReduce job via WSL"""
    status = infrastructure_service.check_status()
    if status["hadoop"] != "ONLINE" or status["hdfs"] != "ONLINE":
        return {"success": False, "reason": "Hadoop/HDFS not ONLINE"}
        
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    mapper_path = os.path.join(root_dir, 'mapreduce', 'mapper.py').replace("\\", "/").replace("e:/", "/mnt/e/").replace("E:/", "/mnt/e/")
    reducer_path = os.path.join(root_dir, 'mapreduce', 'reducer.py').replace("\\", "/").replace("e:/", "/mnt/e/").replace("E:/", "/mnt/e/")
    
    # Clean output dir
    run_wsl_command("hdfs dfs -rm -r -f /retail_bda/mapreduce/output")
    
    # Find hadoop streaming jar dynamically
    find_jar_cmd = "find $HADOOP_HOME/share/hadoop/tools/lib/ -name 'hadoop-streaming*.jar' | head -n 1"
    res_jar = run_wsl_command(find_jar_cmd)
    if not res_jar["success"] or not res_jar["stdout"]:
        return {"success": False, "reason": "Hadoop streaming jar not found"}
        
    jar_path = res_jar["stdout"]
    
    # Execute Hadoop Streaming
    cmd = (f"hadoop jar {jar_path} "
           f"-file '{mapper_path}' -mapper 'python3 mapper.py' "
           f"-file '{reducer_path}' -reducer 'python3 reducer.py' "
           f"-input /retail_bda/raw/retail_logs.csv "
           f"-output /retail_bda/mapreduce/output")
           
    res = run_wsl_command(cmd, timeout=120)
    
    if res["success"]:
        # Mark in infrastructure service that mapreduce output is ONLINE
        infrastructure_service._status["mapreduce"] = "ONLINE"
        infrastructure_service._status["mapreduce_output"] = "ONLINE"
        return {"success": True}
    else:
        return {"success": False, "reason": res["stderr"]}
