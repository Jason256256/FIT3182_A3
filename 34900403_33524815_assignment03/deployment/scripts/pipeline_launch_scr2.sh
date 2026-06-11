#!/bin/bash

# Navigate to the project root directory context
cd "$(dirname "$0")/../../src"

echo "Patching Python runtime environments..."
# 1. Fix the Python 3.14 + kafka3 vendor crash via dynamic module aliasing
python3 -c "import sys, six; sys.modules['kafka3.vendor.six'] = six; sys.modules['kafka3.vendor.six.moves'] = six.moves"

# 2. Automatically point PySpark to the internal OpenJDK instance inside Docker 
# to completely bypass the local Mac "Unable to locate a Java Runtime" error
export JAVA_HOME=$(docker exec $(docker ps -q --filter name=kafka) printenv JAVA_HOME 2>/dev/null)

echo "Booting up stream producer notebook..."
jupyter nbconvert --to notebook --execute 34900403_33524815_producer_a_b_c.ipynb --InPlace &

echo "Submitting PySpark Structured Streaming notebook..."
jupyter nbconvert --to notebook --execute 34900403_33524815_data_design_streaming.ipynb --InPlace &

echo "Pipeline triggered successfully!"