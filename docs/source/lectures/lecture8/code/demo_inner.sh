#!/usr/bin/env bash
# Inside the skills container: start ARIAC and the skills server, run one demo,
# and stop every process this script started. Called by run_sim_demo.sh.
# Usage: demo_inner.sh TRIAL USER_CONFIG LIMIT_S LOG_PREFIX SCRIPT [ARGS...]
#        demo_inner.sh --no-sim LIMIT_S SCRIPT [ARGS...]   (no ARIAC, no skills server)
#
# Three stops, as in the skills package's own simulation probes:
# the demo's watchdog at LIMIT - 60 s (DEMO_DEADLINE), timeout's SIGINT at LIMIT,
# and SIGKILL 60 s later (-k 60). Then the EXIT trap removes the key copy, stops the
# demo's process group and both launch groups, and stops every process left from the
# lecture venv, on every path.
set -eo pipefail
source /opt/ros/jazzy/setup.bash
source /ariac_ws/install/setup.bash
source /skills_ws/install/setup.bash
set -u
PY=/opt/enpm663_lecture_venv/bin/python
SHM=/dev/shm/enpm663_gemini_key   # run_sim_demo.sh writes the key here for a --key run
GROUP_STOP_WAIT=30   # s for a launch group to exit after SIGINT (sim_tests/harness.py GROUP_STOP_WAIT)
groups=()

stop_group() {   # SIGINT the whole group, wait, SIGKILL what is left (harness.py _stop)
  local g=$1 i
  kill -INT -- "-$g" 2>/dev/null || return 0
  for ((i = 0; i < GROUP_STOP_WAIT * 2; i++)); do
    kill -0 -- "-$g" 2>/dev/null || return 0
    sleep 0.5
  done
  kill -KILL -- "-$g" 2>/dev/null || true
}
# A child that the demo starts in a new session is in no group above. mcp 2.3.0 starts its
# stdio server that way (mcp/client/stdio.py:348, start_new_session=True) and stops it on a
# normal exit or a SIGINT, but not after the watchdog's os._exit or timeout's SIGKILL. Every
# such child runs on the lecture venv's Python, and only this demo uses that venv while it
# runs (run_sim_demo.sh refuses to start while one runs), so stop all of them.
stop_venv() {   # SIGINT, wait, SIGKILL what is left (as stop_group)
  local i
  pkill -INT -f "^$PY" || return 0
  for ((i = 0; i < GROUP_STOP_WAIT * 2; i++)); do
    pgrep -f "^$PY" > /dev/null || return 0
    sleep 0.5
  done
  pkill -KILL -f "^$PY" || true
}
cleanup() {   # the key copy first, so it does not wait for the stops below (up to about 90 s)
  local g
  rm -f "$SHM"
  for g in "${groups[@]}"; do stop_group "$g"; done
  stop_venv
}
trap cleanup EXIT

if [[ $1 == --no-sim ]]; then
  limit=$2
  shift 2
else
  trial=$1 user=$2 limit=$3 prefix=$4
  shift 4
  # setsid makes each launch the leader of its own group: ros2 launch exits on SIGINT
  # before Gazebo does, so the whole group is stopped, not only the launch (harness.py _stop).
  setsid ros2 launch ariac_gz ariac.launch.py trial_config:="$trial" user_config:="$user" \
    cheat_selection:=0 headless:=true > "${prefix}_ariac.log" 2>&1 &
  groups=("$!")
  "$PY" "$(dirname "$0")/sim_session.py" wait-ready   # absolute: L9 demos run in lecture9/code
  setsid ros2 launch enpm663_skills skills.launch.py > "${prefix}_skills.log" 2>&1 &
  groups=("$!" "${groups[@]}")   # the skills server stops first
fi
status=0
# timeout runs without --foreground, so it makes itself the leader of a new process group,
# and the demo and every child that stays in the demo's group belong to it. The cleanup
# stops that group first, on every path. A child in its own session (an MCP stdio server)
# leaves the group; stop_venv stops it.
DEMO_DEADLINE=$((limit - 60)) timeout -s INT -k 60 "$limit" "$PY" -u "$@" &
groups=("$!" "${groups[@]}")
wait "$!" || status=$?
exit "$status"
