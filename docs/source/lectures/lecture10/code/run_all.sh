#!/usr/bin/env bash
# Runs every L10 example and writes its output to ../outputs/.
# env -i drops this shell's ROS and Python paths; ROS_DOMAIN_ID=90 keeps
# the ROS examples away from any simulation running on domain 0.
set -euo pipefail
cd "$(dirname "$0")"
ros() {
  local out=$1; shift
  env -i HOME="$HOME" PATH=/usr/bin:/bin ROS_DOMAIN_ID=90 \
    bash -c "source /opt/ros/jazzy/setup.bash && $*" > "../outputs/$out" 2>&1
  echo "== $out"; cat "../outputs/$out"
}
py() {
  local out=$1; shift
  env -i HOME="$HOME" PATH=/usr/bin:/bin /usr/bin/python3 "$@" \
    > "../outputs/$out" 2>&1
  echo "== $out"; cat "../outputs/$out"
}
ros tf_agv_moves.txt       /usr/bin/python3 tf_agv_moves.py
ros tf_failures.txt        /usr/bin/python3 tf_failures.py
ros pixel_to_table.txt     /usr/bin/python3 pixel_to_table.py
py  conveyor_intercept.txt conveyor_intercept.py
py  rrt_connect.txt        rrt_connect_toy.py ../outputs/rrt_seed1.json
{
  echo "python: $(/usr/bin/python3 --version 2>&1)"
  echo "numpy: $(/usr/bin/python3 -c 'import numpy; print(numpy.__version__)')"
  echo "ROS 2: $(env -i HOME="$HOME" PATH=/usr/bin:/bin bash -c \
    'source /opt/ros/jazzy/setup.bash && echo $ROS_DISTRO')"
} > ../outputs/versions.txt
echo "== versions.txt"; cat ../outputs/versions.txt
