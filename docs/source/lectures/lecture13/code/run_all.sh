#!/usr/bin/env bash
# Runs every L13 example and writes its output to ../outputs/.
# google-genai is not installed for the system Python, so the examples
# run in a venv (VENV, default below) with google-genai and jsonschema.
# env -i drops this shell's ROS and Python paths. No network is used:
# the model server is a scripted stand-in (see er_demo.py).
set -euo pipefail
cd "$(dirname "$0")"
VENV="${VENV:-$HOME/l13-venv}"
PY="$VENV/bin/python"
env -i HOME="$HOME" PATH=/usr/bin:/bin "$PY" -c \
  "import sys; from importlib.metadata import version as v; print('Python', sys.version.split()[0], 'google-genai', v('google-genai'), 'httpx', v('httpx'), 'jsonschema', v('jsonschema'))" \
  > ../outputs/versions.txt
env -i HOME="$HOME" PATH=/usr/bin:/bin "$PY" er_demo.py > ../outputs/er_demo.txt 2>&1
env -i HOME="$HOME" PATH=/usr/bin:/bin "$PY" score_er.py > ../outputs/score_er.txt 2>&1
cat ../outputs/versions.txt ../outputs/er_demo.txt ../outputs/score_er.txt
