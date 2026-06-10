#!/bin/bash

echo "Booting up stream producer..."
# Adjust the python file name if yours is named differently (e.g., producer.py)
python3 "../../src/traffic_producer.py" &

echo "Submitting PySpark Structured Streaming cluster job..."
# Adjust the streaming script path to match your exact file name
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.mongodb.spark:mongo-spark-connector_2.12:10.2.0 "../../src/spark_streaming.py"