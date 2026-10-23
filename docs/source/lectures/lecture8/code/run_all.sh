#!/usr/bin/env bash
# Runs the offline L8 parts and writes their outputs to ../outputs/:
# the validator, the token growth table, the system message, the tests and the slide listings.
# env -i drops this shell's ROS and Python paths; the system Python has jsonschema 4.10.3.
# The demos that need ARIAC or the Gemini API run through run_sim_demo.sh (see l8_code docs).
set -euo pipefail
cd "$(dirname "$0")"
SYS=(env -i HOME="$HOME" PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3)
OUT=../outputs

# write OUTPUT_FILE from a command: to a .tmp file first, moved into place only on
# success, so a failed run keeps the last good output and set -e stops the script
write() {
  local file=$1; shift
  "$@" > "$file.tmp" 2>&1 || { cat "$file.tmp" >&2; rm -f "$file.tmp"; return 1; }
  mv "$file.tmp" "$file"
}

# versions.txt: the venv line comes from the container. When docker exec fails,
# print its error, keep the last recorded venv line, and say on which day it was read.
VENV_CMD="import sys; from importlib.metadata import version; print('lecture venv Python', sys.version.split()[0], 'google-genai', version('google-genai'), 'mcp', version('mcp'))"
kept=""
if ! venv_line=$(docker exec enpm663_skills_dev /opt/enpm663_lecture_venv/bin/python -c "$VENV_CMD" 2>&1); then
  echo "lecture venv not read, docker exec failed: $venv_line" >&2
  venv_line=$(grep '^lecture venv Python ' $OUT/versions.txt || echo "lecture venv: never recorded")
  read_on=$(sed -n 's/^lecture venv line kept from the run of \([0-9-]*\).*/\1/p' $OUT/versions.txt)
  [ -n "$read_on" ] || read_on=$(sed -n 's/^run on //p' $OUT/versions.txt)
  kept="lecture venv line kept from the run of $read_on: the container was not reached"
fi
{
  "${SYS[@]}" -c "import sys; from importlib.metadata import version; print('system Python', sys.version.split()[0], 'jsonschema', version('jsonschema'))"
  echo "$venv_line"
  echo "run on $(date +%Y-%m-%d)"
  [ -z "$kept" ] || echo "$kept"
} > $OUT/versions.txt.tmp
mv $OUT/versions.txt.tmp $OUT/versions.txt

write $OUT/validator.txt "${SYS[@]}" validator.py
write $OUT/token_growth.txt "${SYS[@]}" token_growth.py
write $OUT/system_message.txt "${SYS[@]}" -c "from structured_live import SYSTEM; print(SYSTEM)"
"${SYS[@]}" -m pytest -q -p no:cacheprovider tests
bash tests/test_run_sim_demo.sh
"${SYS[@]}" listings.py build listings_l8.json
"${SYS[@]}" listings.py check ../L8-ENPM663-v1.0.tex $OUT/listings
cat $OUT/versions.txt
