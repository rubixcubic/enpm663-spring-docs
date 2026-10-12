#!/usr/bin/env bash
# Runs every L8 example and writes its output to ../outputs/.
# env -i drops this shell's ROS and Python paths. The orchestrator,
# validator and token examples use the system Python (jsonschema
# 4.10.3). The MCP example needs the mcp package, which is not
# installed system-wide: set VENV to a virtualenv that has it
# (python3 -m venv venv && venv/bin/pip install mcp).
set -euo pipefail
cd "$(dirname "$0")"
VENV=${VENV:-$HOME/l8-venv}
SYS=(env -i HOME="$HOME" PATH=/usr/bin:/bin /usr/bin/python3)
MCP=(env -i HOME="$HOME" PATH=/usr/bin:/bin "$VENV/bin/python")
OUT=../outputs
{
  "${SYS[@]}" -c "import sys; from importlib.metadata import version; print('system Python', sys.version.split()[0], 'jsonschema', version('jsonschema'))"
  "${MCP[@]}" -c "import sys; from importlib.metadata import version; print('venv Python', sys.version.split()[0], 'mcp', version('mcp'), 'pydantic', version('pydantic'))"
  echo "run on $(date +%Y-%m-%d)"
} > $OUT/versions.txt
"${SYS[@]}" orchestrator.py > $OUT/orchestrator.txt 2>&1
"${SYS[@]}" validator.py > $OUT/validator.txt 2>&1
"${SYS[@]}" token_growth.py > $OUT/token_growth.txt 2>&1
# The server's log lines go to stderr; keep them apart from the output.
"${MCP[@]}" agv_mcp_client.py > $OUT/mcp_demo.txt 2> $OUT/mcp_demo_stderr.txt
"${MCP[@]}" -c "from mcp.server.fastmcp import FastMCP" \
  > $OUT/fastmcp_import.txt 2>&1 || true
cat $OUT/versions.txt
