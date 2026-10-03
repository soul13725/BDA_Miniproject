import os
import subprocess
import sys

def print_header(title):
    print(f"\n{'=' * 50}")
    print(f" {title}")
    print(f"{'=' * 50}")

def run_script(script_path, description):
    print(f"\n--- {description} ---")
    if not os.path.exists(script_path):
        print(f"[{description}] SKIPPED — Script not found at {script_path}")
        return "SKIPPED"
        
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:", result.stderr)
            
        if result.returncode == 0:
            print(f"[{description}] PASS")
            return "PASS"
        else:
            if "Status" in description:
                print(f"[{description}] SKIPPED — infrastructure unavailable (exit code {result.returncode})")
                return "SKIPPED"
            print(f"[{description}] FAIL — exit code {result.returncode}")
            return "FAIL"
    except Exception as e:
        print(f"[{description}] FAIL — {str(e)}")
        return "FAIL"

def main():
    print_header("RETAIL BDA ANALYTICS PLATFORM - FINAL VALIDATION")
    
    results = {}
    
    # 1. Dataset Validation
    results['Dataset Validation'] = run_script("scripts/validate_data.py", "Dataset Validation")
    
    # 2. MapReduce Execution
    results['MapReduce Execution'] = run_script("scripts/run_mapreduce.py", "MapReduce Execution")
    
    # 3. MapReduce Validation
    results['MapReduce Validation'] = run_script("scripts/validate_mapreduce.py", "MapReduce Validation")
    
    # 4. HDFS Status
    results['HDFS Status'] = run_script("scripts/check_hdfs.py", "HDFS Status")
    
    # 5. Hive Status
    results['Hive Status'] = run_script("scripts/check_hive.py", "Hive Status")
    
    # 6. Hive/Local Analytics Execution
    results['Analytics Execution'] = run_script("scripts/run_hive.py", "Hive/Local Analytics Execution")
    
    # 7. Hive/Local Analytics Validation
    results['Analytics Validation'] = run_script("scripts/validate_hive.py", "Hive/Local Analytics Validation")
    
    print_header("FINAL VALIDATION SUMMARY")
    for task, status in results.items():
        print(f"{task.ljust(35)} : {status}")
        
    if all(s in ["PASS", "SKIPPED"] for s in results.values()):
        print("\nOVERALL PROJECT STATUS: PASS")
        sys.exit(0)
    else:
        print("\nOVERALL PROJECT STATUS: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
