#!/usr/bin/env bash
# Run one L8 or L9 demo in the skills container and copy its outputs back.
#
#   run_sim_demo.sh --lecture 8 --name agent_rec1 \
#       --sim config/l8_trial.yaml config/l8_user_config.yaml 1800 --key -- orchestrator.py --runs 2,1
#   run_sim_demo.sh --lecture 8 --name structured_live --key -- structured_live.py
#   run_sim_demo.sh --preflight-only
#
# --sim: demo_inner.sh starts ARIAC with the trial file and user config (paths relative
#   to the lecture's code folder), starts the skills server, runs the demo with a wall
#   limit of LIMIT_S seconds, and stops every process it started.
# --limit LIMIT_S: the wall limit of a demo without --sim (default 600 s). Both paths run
#   the demo under the same three stops in demo_inner.sh, so LIMIT_S must be over 60.
# --key: the Gemini key goes from ~/.config/enpm663/gemini_key to /dev/shm in the
#   container (memory only) through stdin, never a command line. This script removes any
#   old copy before the run, demo_inner.sh removes it when the demo ends, and this
#   script removes it again when it ends. Only a --key run gets GEMINI_KEY_FILE.
# NAME: letters, digits and underscores.
# Writes lectureN/outputs/NAME.txt (header, the demo's log, the exit status) and
# lectureN/outputs/raw/NAME/; the ARIAC and skills logs go to $LOGS/NAME/.
set -euo pipefail
DOCKER=${DOCKER:-docker}
C=enpm663_skills_dev
V=/opt/enpm663_lecture_venv
KEY="$HOME/.config/enpm663/gemini_key"
SHM=/dev/shm/enpm663_gemini_key
HERE=$(cd "$(dirname "$0")" && pwd)
LECTURES=${DEMO_LECTURES:-$(cd "$HERE/../.." && pwd)}   # DEMO_LECTURES: for tests/test_run_sim_demo.sh
# SKILLS_REPO: the skills package clone. The default is its place in the instructor's
# folders, six folders above this script's folder in the slides repo; set it for any other layout.
SKILLS_REPO=${SKILLS_REPO:-$HERE/../../../../../../workspace/enpm663_ws/src/enpm663-spring-2027-skills}
# The demos record on the skills code of v0.2.0. The preflight accepts a later commit when
# its code outside sim_tests/ (the package's own probes and logs) matches this commit's.
SKILLS_BASE=${SKILLS_BASE:-6fa0563}
LOGS=${DEMO_LOGS:-$HOME/.cache/enpm663-demo-logs}
MIN_FREE_KB=$((2 * 1024 * 1024))   # 2 GB free on the host's /, chosen; the smoke test's logs measured 272 KB
PLAIN_LIMIT=600   # wall s for a demo without --sim, chosen: far above a few model calls of
                  # 0.8 to 1.5 wall s each (measured by gemini_model.py --probe, 2026-10-17)

die() { echo "run_sim_demo: $*" >&2; exit 2; }

busy() { "$DOCKER" exec "$C" bash -c 'ps -eo pid,cmd | grep -E "gz sim|ariac|skills_server|/lecture_demos/|enpm663_lecture_venv" | grep -v grep' || true; }

SKILLS_NOTE=""   # set by preflight: the skills commit used, for the header
preflight() {
  local free dirty b changed head
  free=$(df --output=avail -k / | tail -1)
  (( free >= MIN_FREE_KB )) || die "only $((free / 1024)) MB free on /"
  b=$(busy)
  [[ -z "$b" ]] || die "another simulation runs in $C: $b"
  # The container runs the mounted working tree, so every file outside sim_tests/ must be
  # committed. Untracked files in sim_tests/ (the package's own probes) are allowed.
  dirty=$(git -C "$SKILLS_REPO" status --porcelain -- . ':!sim_tests')
  [[ -z "$dirty" ]] || die "the skills package has uncommitted changes: $dirty"
  git -C "$SKILLS_REPO" rev-parse -q --verify "$SKILLS_BASE^{commit}" > /dev/null \
    || die "base commit $SKILLS_BASE not found in $SKILLS_REPO"
  changed=$(git -C "$SKILLS_REPO" diff --name-only "$SKILLS_BASE" HEAD -- . ':!sim_tests')
  [[ -z "$changed" ]] || die "the skills code outside sim_tests/ changed since $SKILLS_BASE: $changed"
  head=$(git -C "$SKILLS_REPO" rev-parse --short HEAD)
  SKILLS_NOTE="$head on $(git -C "$SKILLS_REPO" branch --show-current)"
  SKILLS_NOTE+="; code outside sim_tests/ identical to $SKILLS_BASE (git diff $SKILLS_BASE $head is empty there)"
}

lecture="" name="" sim=0 key=0 trial="" user="" limit="" plain_limit=""
while (( $# )); do
  case $1 in
    --preflight-only) preflight; echo "preflight ok: skills package $SKILLS_NOTE"; exit 0 ;;
    --lecture) lecture=$2; shift 2 ;;
    --name) name=$2; shift 2 ;;
    --sim) sim=1 trial=$2 user=$3 limit=$4; shift 4 ;;
    --limit) plain_limit=$2; shift 2 ;;
    --key) key=1; shift ;;
    --) shift; break ;;
    *) die "unknown argument $1" ;;
  esac
done
[[ -n "$lecture" && -n "$name" && $# -gt 0 ]] || die "usage: see the comment at the top"
[[ $name =~ ^[A-Za-z0-9_]+$ ]] || die "NAME '$name' may hold only letters, digits and underscores"
if (( sim )); then
  [[ -z "$plain_limit" ]] || die "--limit is for a demo without --sim; --sim takes its own LIMIT_S"
else
  limit=${plain_limit:-$PLAIN_LIMIT}
fi
# The watchdog fires at LIMIT_S - 60 s; at 60 or less DEMO_DEADLINE <= 0 turns it off.
# No leading zero: bash arithmetic reads 0100 as octal (64).
[[ $limit =~ ^[1-9][0-9]*$ ]] && (( limit > 60 )) || die "the wall limit must be a whole number over 60 s, not '$limit'"
preflight
OUT="$LECTURES/lecture$lecture/outputs"
[[ ! -e "$OUT/$name.txt" ]] || die "$OUT/$name.txt exists; every recording keeps its own name"
mkdir -p "$OUT/raw/$name" "$LOGS/$name"
CO=/lecture_demos/out/$name
cleanup() { "$DOCKER" exec "$C" rm -f "$SHM" || true; }
trap cleanup EXIT
# A run killed by SIGKILL never runs its EXIT trap, so remove an old key copy first.
"$DOCKER" exec "$C" rm -f "$SHM"

"$DOCKER" exec "$C" bash -c "rm -rf /lecture_demos/lecture8 /lecture_demos/lecture9 $CO && mkdir -p /lecture_demos/lecture8 /lecture_demos/lecture9 $CO/raw"
for n in 8 9; do "$DOCKER" cp "$LECTURES/lecture$n/code" "$C:/lecture_demos/lecture$n/code"; done
if (( key )); then
  [[ -f "$KEY" ]] || die "no key file at $KEY"
  [[ $(stat -c %a "$KEY") == 600 ]] || die "$KEY must be mode 600"
  "$DOCKER" exec -i "$C" sh -c "umask 077 && cat > $SHM" < "$KEY"
fi
WD=/lecture_demos/lecture$lecture/code
ENVS=(-e "DEMO_OUT_DIR=$CO" -e "DEMO_RAW_DIR=$CO/raw" -e PYTHONUNBUFFERED=1)
if (( key )); then ENVS+=(-e "GEMINI_KEY_FILE=$SHM"); fi
if (( sim )); then
  cmd=(bash /lecture_demos/lecture8/code/demo_inner.sh "$WD/$trial" "$WD/$user" "$limit" "$CO/$name" "$@")
else
  cmd=(bash /lecture_demos/lecture8/code/demo_inner.sh --no-sim "$limit" "$@")
fi
status=0
"$DOCKER" exec -w "$WD" "${ENVS[@]}" "$C" "${cmd[@]}" > "$LOGS/$name/body.txt" 2> "$LOGS/$name/stderr.txt" || status=$?
"$DOCKER" cp "$C:$CO/." "$LOGS/$name/out"
/bin/cp -rf "$LOGS/$name/out/." "$OUT/raw/$name/"
rm -f "$OUT/raw/$name/${name}_ariac.log" "$OUT/raw/$name/${name}_skills.log"
reported=$(/usr/bin/python3 "$HERE/gemini_model.py" --reported-model "$OUT/raw/$name/raw" 2>/dev/null || echo "none (no API call)")
{
  echo "date: $(date '+%Y-%m-%d %H:%M %Z')"
  echo "demo: $name (lecture $lecture): $*"
  if (( sim )); then echo "trial file: $trial; user config: $user; wall limit: $limit s"; else echo "wall limit: $limit s"; fi
  echo "model (as the API reports it): $reported"
  echo "venv: $("$DOCKER" exec "$C" "$V/bin/python" -c 'import sys, importlib.metadata as m; print("Python", sys.version.split()[0], "| google-genai", m.version("google-genai"), "| mcp", m.version("mcp"))')"
  echo "image: $("$DOCKER" inspect "$C" --format '{{.Config.Image}}'), $(grep -m1 '^FROM' "$SKILLS_REPO/Dockerfile")"
  echo "ARIAC source: $("$DOCKER" exec "$C" git -C /ariac_ws/src log -1 --format='%h %s')"
  echo "skills package: $SKILLS_NOTE"
  echo "---"
  cat "$LOGS/$name/body.txt"
  echo "--- exit status $status"
} > "$OUT/$name.txt"
b=$(busy)
[[ -z "$b" ]] || echo "run_sim_demo: WARNING: still running after the demo: $b" >&2
echo "wrote $OUT/$name.txt (exit status $status)"
exit "$status"
