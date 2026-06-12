# fix_kafka3.py
# Place this file next to docker-compose.yml on your host.
# It is loaded automatically inside the jupyter-pyspark container via the
# PYTHONSTARTUP environment variable, which means EVERY Python process in
# the container (including notebook kernels) gets this patch applied —
# not just a single python3 -c call.
#
# This fixes the kafka3.vendor.six crash that affects Python 3.10+.
import sys
try:
    import six
    sys.modules.setdefault('kafka.vendor.six', six)
    sys.modules.setdefault('kafka.vendor.six.moves', six.moves)
except ImportError:
    pass  # six not available; kafka pip install will handle it
