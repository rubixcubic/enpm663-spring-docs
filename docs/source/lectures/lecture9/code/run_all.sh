#!/usr/bin/env bash
# Runs every L9 example and writes its output to ../outputs/.
# Plain Python, no ROS and no model: env -i drops this shell's ROS and
# Python paths, so the system Python and its jsonschema are used.
set -euo pipefail
cd "$(dirname "$0")"
run() { env -i HOME="$HOME" PATH=/usr/bin:/bin /usr/bin/python3 "$@"; }
run -c "import sys; from importlib.metadata import version; \
print('Python', sys.version.split()[0], 'jsonschema', version('jsonschema'))" \
  > ../outputs/versions.txt
run closed_loop.py > ../outputs/closed_loop.txt 2>&1
run closed_loop.py --wait > ../outputs/closed_loop_wait.txt 2>&1
run vlm_check.py > ../outputs/vlm_check.txt 2>&1
head -n 1 ../outputs/*.txt
