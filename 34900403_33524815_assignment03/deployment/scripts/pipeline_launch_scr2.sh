#!/bin/bash

echo "Booting up stream producer notebook..."
# Executes the producer notebook cell-by-cell in the background
jupyter nbconvert --to notebook --execute "../../src/34900403_33524815_producer_a_b_c.ipynb" &

echo "Submitting PySpark Structured Streaming notebook..."
# Executes the streaming notebook cell-by-cell
jupyter nbconvert --to notebook --execute "../../src/34900403_33524815_data_design_streaming.ipynb"