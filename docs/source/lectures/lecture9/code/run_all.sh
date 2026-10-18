#!/usr/bin/env bash
# Runs the offline L9 parts and writes their outputs to ../outputs/:
# the scripted VLM check, the tests, the slide listings and versions.txt.
# env -i drops this shell's ROS and Python paths; the system Python has jsonschema 4.10.3.
# The closed loop and the live VLM check need ARIAC and the Gemini API: they run through
# run_sim_demo.sh (closed_loop_dry, closed_loop_replan_rec<N>, closed_loop_wait_rec<N>).
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

write $OUT/vlm_check.txt "${SYS[@]}" vlm_check.py
# the tests import L8's orchestrator, skill_tools and fake_tools
env -i HOME="$HOME" PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../lecture8/code \
  /usr/bin/python3 -m pytest -q -p no:cacheprovider tests
"${SYS[@]}" ../../lecture8/code/listings.py build listings_l9.json
# every listing in the deck must equal its file in ../outputs/listings, byte for byte
"${SYS[@]}" ../../lecture8/code/listings.py check ../ENPM663-L9-v1.0.tex $OUT/listings
cat $OUT/versions.txt
