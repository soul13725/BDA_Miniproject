import argparse
import subprocess
import sys
from pathlib import Path

def run_job(name, input_file, mapper_script, reducer_script, output_file):
    # Read input
    with open(input_file, 'rb') as f:
        csv_data = f.read()
        
    # Mapper
    mapper_proc = subprocess.run(
        [sys.executable, str(mapper_script)],
        input=csv_data,
        capture_output=True,
        check=True
    )
    
    mapper_output = mapper_proc.stdout.decode('utf-8')
    
    # Shuffle (Sort)
    lines = mapper_output.strip().split('\n')
    lines = [line for line in lines if line]
    lines.sort()
    sorted_input = '\n'.join(lines) + '\n'
    
    # Reducer
    reducer_proc = subprocess.run(
        [sys.executable, str(reducer_script)],
        input=sorted_input.encode('utf-8'),
        capture_output=True,
        check=True
    )
    
    reducer_output = reducer_proc.stdout.decode('utf-8')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reducer_output)
        
    return reducer_output

def main():
    parser = argparse.ArgumentParser(description="Local MapReduce Simulation")
    parser.add_argument('--input', type=str, default="data/retail_logs.csv")
    parser.add_argument('--output', type=str, default="output/mapreduce")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)
        
    with open(input_path, 'r', encoding='utf-8') as f:
        records_processed = max(0, sum(1 for _ in f) - 1)
        
    print("========================================")
    print("LOCAL MAPREDUCE EXECUTION")
    print("========================================")
    print(f"Input:\n{input_path}\n")
    print(f"Records processed:\n{records_processed}\n")
    
    jobs = [
        {
            "id": 1,
            "name": "Total Revenue",
            "mapper": Path("mapreduce/mapper.py"),
            "reducer": Path("mapreduce/reducer.py"),
            "output": output_dir / "total_revenue.txt"
        },
        {
            "id": 2,
            "name": "Revenue by Category",
            "mapper": Path("mapreduce/category_mapper.py"),
            "reducer": Path("mapreduce/category_reducer.py"),
            "output": output_dir / "category_revenue.tsv"
        },
        {
            "id": 3,
            "name": "Revenue by Product",
            "mapper": Path("mapreduce/product_mapper.py"),
            "reducer": Path("mapreduce/product_reducer.py"),
            "output": output_dir / "product_revenue.tsv"
        }
    ]
    
    total_rev_str = ""
    categories_count = 0
    products_count = 0
    
    print("Jobs:")
    for job in jobs:
        print(f"{job['id']}. {job['name']}")
        try:
            out_content = run_job(
                job['name'], input_path, job['mapper'], job['reducer'], job['output']
            )
            
            lines = [l for l in out_content.strip().split('\n') if l]
            if job['id'] == 1:
                if lines:
                    total_rev_str = lines[0].split('\t')[1]
            elif job['id'] == 2:
                categories_count = len(lines)
            elif job['id'] == 3:
                products_count = len(lines)
                
        except Exception as e:
            print(f"Error running job {job['name']}: {e}")
            print("Execution Status:\nFAIL")
            print("========================================")
            sys.exit(1)
            
    print(f"\nOutput:\n{output_dir}/\n")
    print(f"Total Revenue:\n{total_rev_str}\n")
    print(f"Categories:\n{categories_count}\n")
    print(f"Products:\n{products_count}\n")
    print("Execution Status:\nPASS")
    print("========================================")

if __name__ == "__main__":
    main()
