#!/usr/bin/env bash
# Create the lecture-only venv for the L8 and L9 demos in the skills container.
# It lives at /opt/enpm663_lecture_venv, outside the skills package, its image and
# the container's system Python. Rerun it after the container is recreated.
#
# --system-site-packages: the venv sees the container's PIL, numpy, jsonschema and
# PyYAML. --without-pip: the container's Python has no ensurepip; the system pip
# installs into the venv with --python.
set -euo pipefail
DOCKER=${DOCKER:-docker}
C=enpm663_skills_dev
V=/opt/enpm663_lecture_venv
HERE=$(cd "$(dirname "$0")" && pwd)
"$DOCKER" exec "$C" bash -c "test -x $V/bin/python || python3 -m venv --without-pip --system-site-packages $V"
"$DOCKER" cp "$HERE/lecture_requirements.txt" "$C:/tmp/lecture_requirements.txt"
"$DOCKER" exec "$C" python3 -m pip --python "$V/bin/python" install --no-cache-dir -r /tmp/lecture_requirements.txt
"$DOCKER" exec "$C" bash -c "source /opt/ros/jazzy/setup.bash && source /ariac_ws/install/setup.bash \
  && source /skills_ws/install/setup.bash && $V/bin/python -c 'import rclpy, ariac_interfaces.msg, \
enpm663_skills_interfaces.action, mcp, PIL, numpy, jsonschema, google.genai; print(\"imports ok\")'"
"$DOCKER" exec "$C" python3 -m pip --python "$V/bin/python" check
