#!/bin/bash

# Resolve the running jupyter-pyspark container
JUPYTER_CONTAINER=$(docker ps -q --filter name=jupyter-pyspark --filter status=running)

if [ -z "$JUPYTER_CONTAINER" ]; then
  echo "ERROR: jupyter-pyspark container is not running."
  echo "Please run start_infra_scr1.sh first, then retry."
  exit 1
fi

echo "=== Pipeline execution starting inside container: $JUPYTER_CONTAINER ==="
echo ""

# The kafka3/six vendor fix is already applied automatically via PYTHONSTARTUP
# inside the container — no host-side Python call needed here.

# Notebooks live at /home/jovyan/work/ inside the container,
# which maps to ./src/ on your host (defined in docker-compose.yml volumes).

echo "[1/2] Executing PySpark Structured Streaming notebook..."
docker exec "$JUPYTER_CONTAINER" \
  papermill \
  /home/jovyan/work/src/34900403_33524815_data_design_streaming.ipynb \
  /home/jovyan/work/src/34900403_33524815_data_design_streaming.ipynb \
  --execution-timeout 600 &
STREAMING_PID=$!

echo "Waiting 15 seconds for Spark to initialize before starting producer..."
sleep 15

echo "[2/2] Executing stream producer notebook..."
docker exec "$JUPYTER_CONTAINER" \
  papermill \
  /home/jovyan/work/src/34900403_33524815_producer_a_b_c.ipynb \
  /home/jovyan/work/src/34900403_33524815_producer_a_b_c.ipynb \
  --execution-timeout 300 &
PRODUCER_PID=$!

# Wait for both to finish
wait $STREAMING_PID
STREAMING_EXIT=$?
wait $PRODUCER_PID
PRODUCER_EXIT=$?

echo ""
echo "=== Pipeline execution complete ==="

# Report outcome of each notebook clearly
if [ $PRODUCER_EXIT -eq 0 ]; then
  echo "  [OK]  producer_a_b_c notebook finished successfully"
else
  echo "  [FAIL] producer_a_b_c notebook exited with code $PRODUCER_EXIT"
  echo "         Check the notebook for error cells, or run:"
  echo "         docker logs $JUPYTER_CONTAINER"
fi

if [ $STREAMING_EXIT -eq 0 ]; then
  echo "  [OK]  data_design_streaming notebook finished successfully"
else
  echo "  [FAIL] data_design_streaming notebook exited with code $STREAMING_EXIT"
  echo "         Check the notebook for error cells, or run:"
  echo "         docker logs $JUPYTER_CONTAINER"
fi

# Exit with failure if either notebook failed
if [ $PRODUCER_EXIT -ne 0 ] || [ $STREAMING_EXIT -ne 0 ]; then
  exit 1
fi
