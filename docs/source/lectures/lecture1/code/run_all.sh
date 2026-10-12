#!/usr/bin/env bash
# Runs every L1 example and writes its output to ../outputs/.
# env -i drops this shell's ROS and Python paths; ROS_DOMAIN_ID=77 keeps the
# examples away from any simulation running on domain 0.
set -euo pipefail
cd "$(dirname "$0")"
run() {
  local out=$1; shift
  env -i HOME="$HOME" PATH=/usr/bin:/bin ROS_DOMAIN_ID=77 \
    bash -c "source /opt/ros/jazzy/setup.bash && $*" > "../outputs/$out" 2>&1
  echo "== $out"; cat "../outputs/$out"
}
run qos_default.txt     /usr/bin/python3 qos_mismatch.py
run qos_match.txt       /usr/bin/python3 qos_mismatch.py --match
run executor_single.txt /usr/bin/python3 executor_blocking.py single
run executor_multi.txt  /usr/bin/python3 executor_blocking.py multi
run action_gripper.txt  /usr/bin/python3 action_gripper.py
run tf_slot.txt         /usr/bin/python3 tf_slot_lookup.py
