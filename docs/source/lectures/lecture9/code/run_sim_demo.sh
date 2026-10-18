#!/usr/bin/env bash
# L9 demos: the L8 script with --lecture 9. Usage as ../../lecture8/code/run_sim_demo.sh,
# without --lecture; trial and user config paths are relative to this folder.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
# A trial file that still holds UNSET_START_TIME or UNSET_DURATION is a template: set both
# from the dry run's cycle times first. Refuse such a file here, before anything starts.
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
  [[ ${args[i]} == -- ]] && break
  if [[ ${args[i]} == --sim && $((i + 1)) -lt ${#args[@]} ]]; then
    trial=${args[i + 1]}
    [[ $trial == /* ]] || trial="$here/$trial"
    if [[ -f $trial ]] && grep -q UNSET_ "$trial"; then
      echo "run_sim_demo: ${args[i + 1]} still holds UNSET_ placeholders; set START_TIME and DURATION first, from the dry run's cycle times" >&2
      exit 2
    fi
  fi
done
exec "$here/../../lecture8/code/run_sim_demo.sh" --lecture 9 "$@"
