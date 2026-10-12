#!/usr/bin/env bash
# Runs every L4 example and writes its output to ../outputs/.
# env -i drops this shell's ROS and Python paths, so the system Python
# with ROS 2 Jazzy's py_trees and py_trees_ros is the one used.
# ROS_DOMAIN_ID=84 keeps the examples away from any simulation running
# on domain 0.
set -euo pipefail
cd "$(dirname "$0")"
run() {
  local out=$1; shift
  env -i HOME="$HOME" PATH=/usr/bin:/bin ROS_DOMAIN_ID=84 \
    bash -c "source /opt/ros/jazzy/setup.bash && $*" > "../outputs/$out" 2>&1
  echo "== $out"; cat "../outputs/$out"
}
run versions.txt /usr/bin/python3 -c "'import sys; \
from importlib.metadata import version as v; \
print(\"Python\", sys.version.split()[0], \"py_trees\", v(\"py_trees\"), \
\"py_trees_ros\", v(\"py_trees_ros\"))'"
run retry_demo.txt       /usr/bin/python3 retry_demo.py
run composite_status.txt /usr/bin/python3 composite_status.py
run parallel_watch.txt   /usr/bin/python3 parallel_watch.py
run blackboard_demo.txt  /usr/bin/python3 blackboard_demo.py
run ros_tree_ok.txt      /usr/bin/python3 ros_tree_demo.py ok
run ros_tree_timeout.txt /usr/bin/python3 ros_tree_demo.py timeout
run ros_tree_bad_kit.txt /usr/bin/python3 ros_tree_demo.py bad_kit
# Ten more runs of the two timed cases: how far the tick counts move.
run ros_tree_repeats.txt "for r in ok timeout; do for i in \$(seq 10); do \
echo -n \"\$r: \"; /usr/bin/python3 ros_tree_demo.py \$r 2>/dev/null \
| grep 'tree finished'; done; done"
