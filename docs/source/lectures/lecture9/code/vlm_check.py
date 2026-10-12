"""L9 demo: check a VLM's tray record before a high-priority submit.

Plain Python, no simulator and no model run here:
- stand_in_vlm() is a scripted stand-in for a VLM. It returns canned
  replies in order, written to contain mistakes for the checker to
  find; a real model's answers vary.
- TRAY_STATUS stands in for one /agv1/tray_status message
  (AgvTrayStatus.msg: four booleans, no cell type).
- RECORD stands in for the orchestrator's own record: the voltage
  each cell read on a tester before it was placed. Values are
  chosen for this example.
"""
import json
import textwrap

from jsonschema import Draft7Validator

NIMH_MIN, NIMH_MAX = 1.0, 1.4       # 1.2 V +/- 0.2 V, CellTypes.msg
LI_MIN, LI_MAX = 3.4, 3.8           # 3.6 V +/- 0.2 V, CellTypes.msg

WEAK = "Describe this image."
STRUCTURED = (
    "This image is from a camera above the tray of agv1. The tray "
    "has four slots, numbered 1 to 4 from the left of the image. "
    "Return only JSON that matches the schema: one record per slot. "
    "Use UNKNOWN when you cannot see a value.")

SLOT = {
    "type": "object",
    "required": ["slot", "occupied", "cell_type", "damage",
                 "confidence"],
    "additionalProperties": False,
    "properties": {
        "slot": {"type": "integer", "minimum": 1, "maximum": 4},
        "occupied": {"type": "boolean"},
        "cell_type": {"enum": ["LI_ION", "NIMH", "UNKNOWN"]},
        "damage": {"enum": ["NONE", "DENT", "SCRATCH", "BULGE",
                            "UNKNOWN"]},
        "confidence": {"type": "number", "minimum": 0,
                       "maximum": 1},
    },
}
SCHEMA = {"type": "object", "required": ["slots"],
          "additionalProperties": False,
          "properties": {"slots": {"type": "array", "items": SLOT,
                                   "minItems": 4, "maxItems": 4}}}


def rec(slot, occupied, cell_type, damage, confidence):
    return {"slot": slot, "occupied": occupied,
            "cell_type": cell_type, "damage": damage,
            "confidence": confidence}


REPLIES = [  # what the stand-in VLM returns, call by call
    "The image shows a gray tray with four cylindrical battery "
    "cells. Most look the same. One near the right may be a "
    "different type.",
    json.dumps({"slots": [rec(k, True, "NIMH", "NONE", 0.9)
                          for k in range(0, 4)]}),
    json.dumps({"slots": [rec(1, True, "NIMH", "NONE", 0.9),
                          rec(2, True, "NIMH", "NONE", 0.85),
                          rec(3, True, "LI_ION", "NONE", 0.6),
                          rec(4, False, "UNKNOWN", "UNKNOWN", 0.7)]}),
]
TRAY_STATUS = {"slot_1_occupied": True, "slot_2_occupied": True,
               "slot_3_occupied": True, "slot_4_occupied": True}
RECORD = {1: 1.21, 2: 1.18, 3: 1.24, 4: 1.22}   # volts per slot


def stand_in_vlm(prompt, image="agv1_tray.png"):
    """Scripted stand-in for a VLM: ignores the prompt and image."""
    return REPLIES.pop(0)


def check(text):
    """Parse, then validate. Returns (record, list of errors)."""
    try:
        reply = json.loads(text)
    except json.JSONDecodeError as err:
        return None, [f"not JSON: {err.msg}"]
    errors = [f"{'.'.join(map(str, e.absolute_path))}: {e.message}"
              for e in Draft7Validator(SCHEMA).iter_errors(reply)]
    return reply, sorted(errors)


def ask(prompt):
    """One call, one re-prompt with the error, then stop."""
    for attempt in (1, 2):
        reply, errors = check(stand_in_vlm(prompt))
        print(f"  attempt {attempt}: "
              f"{'valid' if not errors else 'rejected'}")
        for error in errors[:2]:
            print(f"    {error}")
        if not errors:
            return reply
        prompt = f"{STRUCTURED}\nYour last reply failed: {errors[0]}"
        print("  re-prompt with: 'Your last reply failed: ...'")
    return None


def type_from_volts(volts):
    if NIMH_MIN <= volts <= NIMH_MAX:
        return "NIMH"
    return "LI_ION" if LI_MIN <= volts <= LI_MAX else "UNKNOWN"


def cross_check(reply):
    print("slot  vlm (conf.)       tray_status  record        "
          "verdict")
    flags = []
    for r in reply["slots"]:
        k = r["slot"]
        seen = "empty" if not r["occupied"] else r["cell_type"]
        topic = TRAY_STATUS[f"slot_{k}_occupied"]
        volts = RECORD[k]
        kind = type_from_volts(volts)
        verdict = "agree"
        if r["occupied"] != topic:
            verdict = "DISAGREE: occupancy"
        elif r["cell_type"] not in ("UNKNOWN", kind):
            verdict = "DISAGREE: type"
        if verdict != "agree":
            flags.append(k)
        seen = f"{seen} ({r['confidence']})"
        print(f"{k:<5} {seen:<17} "
              f"{'occupied' if topic else 'empty':<12} "
              f"{kind} {volts:.2f} V   {verdict}")
    return flags


def main():
    print("Scripted stand-in VLM (a real model's answers vary)")
    print(f"Weak prompt: {WEAK!r}")
    text = stand_in_vlm(WEAK)
    for row in textwrap.wrap(text, 64):
        print(f"  | {row}")
    _, errors = check(text)
    print(f"  check: {errors[0]}")
    print("Structured prompt with the schema:")
    reply = ask(STRUCTURED)
    if reply is None:
        print("no valid record: stop and report")
        return
    print("Cross-check before /submit_high_priority_order:")
    flags = cross_check(reply)
    if flags:
        names = " and ".join(map(str, flags))
        print(f"decision: do not submit; slots {names} disagree")
    else:
        print("decision: all four slots agree; submit")


if __name__ == "__main__":
    main()
