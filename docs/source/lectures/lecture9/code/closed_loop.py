"""L9 demo: a closed agent loop meets two ARIAC 2025 malfunctions.

Plain Python. No simulator and no model run here:
- Factory is a stand-in for the ARIAC topics and the skills. Its
  payloads copy ARIAC 2025: a malfunctioning voltage tester keeps
  publishing voltage -1 with operation_status 2 (MALFUNCTIONING),
  as in ariac_plugins/src/voltage_tester_plugin.cpp.
- stand_in_model() is a scripted stand-in for the LLM. It returns
  canned JSON replies in order; a real model's answers vary.
Durations, voltages and malfunction times are chosen for this
example. The malfunction keys are those of an ARIAC trial file.
"""
import json
import sys

from jsonschema import Draft7Validator

OPERATIONAL, MALFUNCTIONING = 1, 2          # OperationStates.msg
NAME = {OPERATIONAL: "OPERATIONAL",
        MALFUNCTIONING: "MALFUNCTIONING"}
CELL_MIN, CELL_MAX = 3.4, 3.8               # 3.6 V +/- 0.2 V
KIT_MIN, KIT_MAX = 14.25, 14.55             # 4 x 3.6 V +/- 0.15 V
RETRY_CAP = 2                               # chosen for this example
# --wait: never replan around a broken tester, wait for it instead
POLICY = "wait" if "--wait" in sys.argv else "replan"

# Challenges (keys as in an ARIAC trial file; times chosen here)
CONVEYOR_MALFUNCTION = {"START_TIME": 90, "DURATION": 30}
TESTER_MALFUNCTION = {"START_TIME": 140, "DURATION": 45, "TESTER": 1}
SECONDS = {"load_tester": 25, "unload_to_tray": 20, "move_agv": 15}

STEP = {
    "type": "object",
    "required": ["action"],
    "additionalProperties": False,
    "properties": {
        "action": {"enum": ["load_tester", "unload_to_tray",
                            "move_agv"]},
        "cell": {"type": "string"},
        "tester": {"enum": [1, 2]},
        "slot": {"type": "integer", "minimum": 1, "maximum": 4},
        "station": {"enum": ["SHIPPING"]},
    },
}
PLAN = {"type": "object", "required": ["steps"],
        "properties": {"steps": {"type": "array", "items": STEP,
                                 "minItems": 1, "maxItems": 12}}}


def load(cell, tester):
    return {"action": "load_tester", "cell": cell, "tester": tester}


def unload(tester, slot):
    return {"action": "unload_to_tray", "tester": tester,
            "slot": slot}


SHIP = {"action": "move_agv", "station": "SHIPPING"}
REPLIES = [  # what the stand-in model returns, call by call
    json.dumps({"steps": [load("c1", 1), unload(1, 1),
                          load("c2", 2), unload(2, 2),
                          load("c3", 1), unload(1, 3),
                          load("c4", 2), unload(2, 4), SHIP]}),
    json.dumps({"steps": [load("c4", 1), unload(1, 3), SHIP]}),
    json.dumps({"steps": [load("c4", 2), unload(2, 3),
                          unload(1, 4), SHIP]}),
]


def stand_in_model(prompt):
    """Scripted stand-in for the LLM: ignores the prompt."""
    return REPLIES.pop(0)


class Factory:
    """Stand-in for the ARIAC topics and the course skills."""

    def __init__(self):
        self.t = 0
        self.on_tester = {1: None, 2: None}
        self.tray = [False, False, False, False]
        self.volts = {"c1": 3.58, "c2": 3.61, "c3": 3.55, "c4": 3.63}
        self.grasp_fails = {"c4": 1}      # c4's first unload fails

    def down(self, challenge):
        start = challenge["START_TIME"]
        return start <= self.t < start + challenge["DURATION"]

    def conveyor_status(self):        # /inspection_conveyor/status
        bad = self.down(CONVEYOR_MALFUNCTION)
        return {"operating_status": MALFUNCTIONING if bad
                else OPERATIONAL}

    def tester(self, n):              # /voltage_tester_n/voltage
        if n == TESTER_MALFUNCTION["TESTER"] and self.down(
                TESTER_MALFUNCTION):
            return {"voltage": -1.0,
                    "operation_status": MALFUNCTIONING}
        cell = self.on_tester[n]
        volts = self.volts[cell] if cell else 0.0
        return {"voltage": volts, "operation_status": OPERATIONAL}

    def slot_occupied(self, slot):    # /agv1/tray_status
        return self.tray[slot - 1]

    def run(self, step):              # a skill or an ARIAC action
        self.t += SECONDS[step["action"]]
        if step["action"] == "load_tester":
            self.on_tester[step["tester"]] = step["cell"]
        elif step["action"] == "unload_to_tray":
            cell = self.on_tester[step["tester"]]
            if self.grasp_fails.get(cell, 0) > 0:
                self.grasp_fails[cell] -= 1
                return {"success": False, "message": "grasp lost"}
            self.on_tester[step["tester"]] = None
            self.tray[step["slot"] - 1] = True
        return {"success": True, "message": ""}


RECORD = {}   # orchestrator's record: tester -> (cell, volts)
KIT = {}      # orchestrator's record: slot -> (cell, volts)


def log(f, text):
    print(f"t={f.t:>3}  {text}")


def decide(goal_changed, device_down, alternative, world_matches,
           retries):
    """The retry-or-replan chart, in code."""
    if goal_changed:
        return "REPLAN"
    if device_down:
        return "REPLAN" if alternative else "WAIT"
    if world_matches and retries < RETRY_CAP:
        return "RETRY"
    return "REPLAN"


def problems(f, plan):
    """Schema errors, then checks against the observed state."""
    errors = [e.message for e in
              Draft7Validator(PLAN).iter_errors(plan)]
    for k, step in enumerate(plan.get("steps", []), start=1):
        n = step.get("tester")
        if (step["action"] == "load_tester" and n and
                f.tester(n)["operation_status"] == MALFUNCTIONING):
            errors.append(f"step {k} uses tester {n}, MALFUNCTIONING")
    return errors


def get_plan(f, reason, calls):
    error = None
    for _ in range(2):                # one re-prompt, then stop
        calls[0] += 1
        prompt = {"reason": reason, "error": error}
        plan = json.loads(stand_in_model(json.dumps(prompt)))
        errors = problems(f, plan)
        if not errors:
            log(f, f"model call {calls[0]}: "
                   f"{len(plan['steps'])} steps, valid")
            return plan["steps"]
        error = errors[0]
        log(f, f"model call {calls[0]} rejected: {error}")
    raise SystemExit("no valid plan after one re-prompt: stop")


def show(step):
    args = [str(v) for k, v in step.items() if k != "action"]
    return f"{step['action']}({', '.join(args)})"


def before(f, step, quiet=False):
    """Precondition check. Returns a decision, or None to go on."""
    say = (lambda text: None) if quiet else (lambda t: log(f, t))
    if step["action"] == "load_tester":
        conv = f.conveyor_status()["operating_status"]
        if conv == MALFUNCTIONING:
            say("check /inspection_conveyor/status: "
                "MALFUNCTIONING -> MISMATCH")
            say("      expected OPERATIONAL; no other conveyor")
            return decide(False, True, alternative=False,
                          world_matches=True, retries=0)
    if step["action"] == "unload_to_tray":
        n = step["tester"]
        obs = f.tester(n)
        if obs["operation_status"] == MALFUNCTIONING:
            say(f"check tester {n}: MALFUNCTIONING -> MISMATCH")
            say(f"      expected OPERATIONAL; the cell is on it")
            return decide(False, True, alternative=False,
                          world_matches=True, retries=0)
        if n not in RECORD:           # this cell was never read
            ok = CELL_MIN <= obs["voltage"] <= CELL_MAX
            say(f"check tester {n}: {obs['voltage']:.2f} V -> "
                f"{'match' if ok else 'MISMATCH'}")
            if ok and not quiet:
                RECORD[n] = (f.on_tester[n], obs["voltage"])
    if step["action"] == "move_agv":
        total = sum(v for _, v in KIT.values())
        ok = KIT_MIN <= total <= KIT_MAX
        say(f"check kit total {total:.2f} V, window {KIT_MIN} "
            f"to {KIT_MAX} V -> {'match' if ok else 'MISMATCH'}")
    return None


def after(f, step, result, retries):
    """Compare the expected effect with a fresh observation."""
    n = step.get("tester")
    if step["action"] == "load_tester":
        obs = f.tester(n)
        state = NAME[obs["operation_status"]]
        ok = (obs["operation_status"] == OPERATIONAL
              and CELL_MIN <= obs["voltage"] <= CELL_MAX)
        log(f, f"observe tester {n}: {obs['voltage']:.2f} V, {state}"
               f" -> {'match' if ok else 'MISMATCH'}")
        if ok:
            RECORD[n] = (step["cell"], obs["voltage"])
            return None
        log(f, f"      expected {CELL_MIN} to {CELL_MAX} V, "
               f"OPERATIONAL")
        other = 2 if n == 1 else 1
        free = f.on_tester[other] is None and POLICY == "replan"
        return decide(False, True, alternative=free,
                      world_matches=False, retries=retries)
    if step["action"] == "unload_to_tray":
        slot = step["slot"]
        filled = f.slot_occupied(slot)
        volts = f.tester(n)["voltage"]
        what = "success" if result["success"] else (
            f"'{result['message']}'")
        verdict = "match" if filled else "MISMATCH"
        log(f, f"result {what}; slot {slot} "
               f"{'occupied' if filled else 'empty'}, tester {n} "
               f"{volts:.2f} V -> {verdict}")
        if filled:
            KIT[slot] = RECORD.pop(n)
            return None
        on_tester = CELL_MIN <= volts <= CELL_MAX
        log(f, f"      expected slot {slot} occupied; cell still "
               f"on tester {n}: {on_tester}")
        return decide(False, False, alternative=False,
                      world_matches=on_tester, retries=retries)
    return None


def main():
    f = Factory()
    calls = [0]
    print("Stand-ins: factory and model (real answers vary); "
          f"policy {POLICY}")
    steps = get_plan(f, "start: Li-Ion kit on agv1", calls)
    retries = 0
    while steps:
        step = steps[0]
        if before(f, step) == "WAIT":
            log(f, "decision WAIT: keep the plan, watch the status")
            while before(f, step, quiet=True) == "WAIT":
                f.t += 5                  # poll every 5 s
            log(f, "check again: OPERATIONAL -> resume the plan")
            continue
        log(f, f"act {show(step)}")
        result = f.run(step)
        decision = after(f, step, result, retries)
        if decision is None:
            steps.pop(0)
            retries = 0
        elif decision == "WAIT":
            log(f, "decision WAIT: keep the plan (policy --wait)")
            steps.pop(0)
        elif decision == "RETRY":
            retries += 1
            log(f, f"decision RETRY ({retries} of {RETRY_CAP}): "
                   f"the plan still holds")
        elif decision == "REPLAN":
            n = step["tester"]
            log(f, f"decision REPLAN: tester {n} is down, the other "
                   f"is free")
            steps = get_plan(f, f"tester {n} MALFUNCTIONING", calls)
    word = "call" if calls[0] == 1 else "calls"
    log(f, f"done: agv1 at SHIPPING after {calls[0]} model {word}")


if __name__ == "__main__":
    main()
