#!/usr/bin/env bash
# Runs every L5 example and writes its output to ../outputs/.
# env -i drops this shell's ROS and Python paths, so the system Python
# with ROS 2 Jazzy's packages is the one used. ROS_DOMAIN_ID=85 keeps
# the ROS example away from any simulation running on domain 0.
# Every data set here is SYNTHETIC (made in NumPy), except the mesh
# depths, which are read from the ARIAC 2025 source in $ARIAC_SRC.
set -euo pipefail
cd "$(dirname "$0")"
ARIAC_SRC=${ARIAC_SRC:?set ARIAC_SRC to your ARIAC 2025 source folder}
py() {
  local out=$1; shift
  env -i HOME="$HOME" PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$@" \
    > "../outputs/$out" 2>&1
  echo "== $out"; cat "../outputs/$out"
}
ros() {
  local out=$1; shift
  env -i HOME="$HOME" PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 ROS_DOMAIN_ID=85 \
    bash -c "source /opt/ros/jazzy/setup.bash && /usr/bin/python3 $*" \
    > "../outputs/$out" 2>&1
  echo "== $out"; cat "../outputs/$out"
}
env -i HOME="$HOME" PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c \
  "import sys, numpy, yaml; print('Python', sys.version.split()[0], \
'numpy', numpy.__version__, 'PyYAML', yaml.__version__)" \
  > ../outputs/versions.txt
echo "ROS 2 $(env -i bash -c 'source /opt/ros/jazzy/setup.bash \
  && echo $ROS_DISTRO')" >> ../outputs/versions.txt
cat ../outputs/versions.txt
ros pc2_roundtrip.txt     pc2_roundtrip.py
py  point_count.txt       point_count.py
py  calibrate.txt         calibrate.py
py  detect_one.txt        detect_one.py ../outputs/residuals.csv
py  precision_recall.txt  precision_recall.py
py  voltage_average.txt   voltage_average.py
py  mesh_depths.txt       mesh_depths.py "$ARIAC_SRC"
