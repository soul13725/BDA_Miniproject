# Hadoop MapReduce Commands

> **Note:** Hadoop is currently unavailable in the local development environment (Windows). The commands documented below represent the conceptual Hadoop Streaming execution pattern that will be used when the Hadoop environment is available in later phases. For now, the MapReduce logic is executed and verified through a local Python simulation (`scripts/run_mapreduce.py`).

## 1. Create HDFS Input Directory
```bash
hdfs dfs -mkdir -p /user/bda/retail/input
hdfs dfs -mkdir -p /user/bda/retail/output
```

## 2. Upload Dataset to HDFS
```bash
hdfs dfs -put data/retail_logs.csv /user/bda/retail/input/
```

## 3. Running Total Revenue MapReduce
```bash
hadoop jar /path/to/hadoop-streaming.jar \
  -input /user/bda/retail/input/retail_logs.csv \
  -output /user/bda/retail/output/total_revenue \
  -mapper "python3 mapreduce/mapper.py" \
  -reducer "python3 mapreduce/reducer.py" \
  -file mapreduce/mapper.py \
  -file mapreduce/reducer.py
```

## 4. Running Category Revenue MapReduce
```bash
hadoop jar /path/to/hadoop-streaming.jar \
  -input /user/bda/retail/input/retail_logs.csv \
  -output /user/bda/retail/output/category_revenue \
  -mapper "python3 mapreduce/category_mapper.py" \
  -reducer "python3 mapreduce/category_reducer.py" \
  -file mapreduce/category_mapper.py \
  -file mapreduce/category_reducer.py
```

## 5. Running Product Revenue MapReduce
```bash
hadoop jar /path/to/hadoop-streaming.jar \
  -input /user/bda/retail/input/retail_logs.csv \
  -output /user/bda/retail/output/product_revenue \
  -mapper "python3 mapreduce/product_mapper.py" \
  -reducer "python3 mapreduce/product_reducer.py" \
  -file mapreduce/product_mapper.py \
  -file mapreduce/product_reducer.py
```

## 6. Viewing Output
```bash
hdfs dfs -cat /user/bda/retail/output/total_revenue/part-*
hdfs dfs -cat /user/bda/retail/output/category_revenue/part-*
hdfs dfs -cat /user/bda/retail/output/product_revenue/part-*
```

## 7. Downloading Output
```bash
hdfs dfs -get /user/bda/retail/output/total_revenue/part-00000 output/mapreduce/total_revenue.txt
hdfs dfs -get /user/bda/retail/output/category_revenue/part-00000 output/mapreduce/category_revenue.tsv
hdfs dfs -get /user/bda/retail/output/product_revenue/part-00000 output/mapreduce/product_revenue.tsv
```
