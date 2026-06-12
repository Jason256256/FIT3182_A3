#!/bin/bash

echo "Starting containerized big data infrastructure (Kafka, MongoDB & Jupyter-PySpark)..."
# Launch all containers relative to where this script lives
docker-compose -f ../config/docker-compose.yml up -d

echo ""
echo "Waiting 15 seconds for Kafka broker initialization..."
echo "(jupyter-pyspark will start automatically once Kafka passes its health check)"
sleep 15

echo ""
echo "Creating Apache Kafka traffic event streaming topic..."
# Note: removed -it flag — it causes failures in non-TTY environments (Windows Git Bash, CI)
docker exec $(docker ps -q -f name=kafka) \
  kafka-topics --create \
  --topic awas-traffic \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1 2>/dev/null || echo "Topic already exists, continuing."

echo ""
echo "Waiting for jupyter-pyspark container to finish starting up..."
# Poll until the container is responsive (max ~60s)
for i in $(seq 1 12); do
  JUPYTER_ID=$(docker ps -q --filter name=jupyter-pyspark --filter status=running)
  if [ -n "$JUPYTER_ID" ]; then
    echo "jupyter-pyspark is ready."
    break
  fi
  echo "  Still waiting... ($((i * 5))s)"
  sleep 5
done

if [ -z "$JUPYTER_ID" ]; then
  echo "WARNING: jupyter-pyspark container did not start in time."
  echo "Check logs with: docker-compose -f ../config/docker-compose.yml logs jupyter-pyspark"
  exit 1
fi

echo ""
echo "=== Infrastructure is running successfully! ==="
echo "  Kafka broker : localhost:9092"
echo "  MongoDB      : localhost:27017"
echo "  Jupyter UI   : http://localhost:8888  (no token/password required)"
echo ""
echo "To execute notebooks headlessly, run: ./pipeline_launch_scr2.sh"
