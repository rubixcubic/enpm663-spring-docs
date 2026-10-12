#!/usr/bin/env bash
# Runs every L7 example and writes its output to ../outputs/.
# env -i drops this shell's paths; sourcing ROS 2 Jazzy gives
# py_trees 2.6.0 and BehaviorTree.CPP 4. No example uses ROS
# communication; ROS_DOMAIN_ID=87 keeps it off domain 0 anyway.
set -euo pipefail
cd "$(dirname "$0")"
OUT=../outputs
BUILD=$(mktemp -d)
trap 'rm -rf "$BUILD"' EXIT
ros() {
  env -i HOME="$HOME" PATH=/usr/bin:/bin ROS_DOMAIN_ID=87 \
    PYTHONDONTWRITEBYTECODE=1 \
    bash -c "source /opt/ros/jazzy/setup.bash && $*"
}
run() {
  local out=$1; shift
  ros "$@" > "$OUT/$out" 2>&1
  echo "== $out"; cat "$OUT/$out"
}
for mode in build tick trace unknown nomemory noguard; do
  run "factory_$mode.txt" /usr/bin/python3 demo_factory.py "$mode"
done
run retry_2.txt /usr/bin/python3 demo_retry.py 2
run retry_3.txt /usr/bin/python3 demo_retry.py 3
for mode in normal silent malfunction; do
  run "timeout_$mode.txt" /usr/bin/python3 demo_timeout.py "$mode"
done
run nesting_hang.txt /usr/bin/python3 demo_nesting.py hang --starts
run nesting_fail.txt /usr/bin/python3 demo_nesting.py fail
run replan.txt /usr/bin/python3 demo_replan.py
g++ -std=c++17 btcpp/place_cell.cpp -I/opt/ros/jazzy/include \
  -L/opt/ros/jazzy/lib -lbehaviortree_cpp \
  -Wl,-rpath,/opt/ros/jazzy/lib -o "$BUILD/place_cell"
for n in 1 3; do
  run "btcpp_$n.txt" "$BUILD/place_cell" btcpp/place_cell.xml "$n"
  run "pytrees_$n.txt" /usr/bin/python3 demo_place_cell.py "$n"
done
{
  echo "date: $(date +%F)"
  ros /usr/bin/python3 --version
  ros /usr/bin/python3 -c "'import py_trees.version as v; \
print(\"py_trees\", v.__version__)'"
  grep -m1 -o '<version>[^<]*' \
    /opt/ros/jazzy/share/behaviortree_cpp/package.xml \
    | sed 's/<version>/BehaviorTree.CPP /'
  g++ --version | head -1
} > "$OUT/versions.txt"
echo "== versions.txt"; cat "$OUT/versions.txt"
