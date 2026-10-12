#!/usr/bin/env python3
"""L11 demo: check an LLM's action list before it reaches a robot.

The "model" here is a scripted stand-in: a fixed list of replies.
A real model's answers vary. Tool names, cell ids and the world
state are chosen for this example; the AGV count (3) and the four
tray slots come from ARIAC 2025.

Five layers, cheapest first; a reply stops at the first layer it
fails:
  1 syntax         the reply parses as JSON
  2 schema         it matches the JSON schema
  3 tools          every tool is on the allowed list
  4 objects        every cell, tester and AGV exists in the world
  5 preconditions  each action can run in the current state
"""
import json

from jsonschema import Draft7Validator

TOOLS = {"pick_cell", "place_cell", "move_agv"}

SLOT = {"type": "integer", "minimum": 1, "maximum": 4}
AGV = {"type": "integer", "minimum": 1, "maximum": 3}
ACTION = {
    "type": "object",
    "required": ["tool", "args"],
    "properties": {
        "tool": {"type": "string"},
        "args": {"type": "object", "properties": {
            "agv": AGV, "slot": SLOT, "tester": {"enum": [1, 2]}}},
    },
}
SCHEMA = {"type": "object", "required": ["actions"],
          "properties": {"actions": {"type": "array",
                                     "items": ACTION}}}

# The world state the executor keeps (values chosen for this example)
WORLD = {
    "cells": {"c7": "tester_1", "c8": "conveyor"},
    "agv_station": {1: "INSPECTION", 2: "INSPECTION", 3: "SHIPPING"},
    "free_slots": {1: [3, 4], 2: [1, 2, 3, 4], 3: []},
}


def check(reply):
    """Return (layer, message) of the first failed check, or None."""
    try:
        plan = json.loads(reply)
    except json.JSONDecodeError as err:
        return 1, f"not JSON: {err.msg}"
    errors = sorted(Draft7Validator(SCHEMA).iter_errors(plan),
                    key=lambda e: list(e.absolute_path))
    if errors:
        e = errors[0]
        where = ".".join(map(str, e.absolute_path))
        return 2, f"{where}: {e.message}"
    for a in plan["actions"]:
        if a["tool"] not in TOOLS:
            return 3, f"unknown tool '{a['tool']}'"
    for a in plan["actions"]:
        cell = a["args"].get("cell")
        if cell is not None and cell not in WORLD["cells"]:
            return 4, f"cell '{cell}' is not in the world state"
    for a in plan["actions"]:
        args = a["args"]
        if a["tool"] == "place_cell" and "agv" in args:
            agv, slot = args["agv"], args["slot"]
            if WORLD["agv_station"][agv] != "INSPECTION":
                return 5, f"agv {agv} is not at INSPECTION"
            if slot not in WORLD["free_slots"][agv]:
                return 5, f"agv {agv} slot {slot} is not free"
    return None


def reply(*steps):
    """Write tool calls as the JSON text a model would return."""
    return json.dumps({"actions": [
        {"tool": t, "args": a} for t, a in steps]})


REPLIES = {
    "A good plan": reply(
        ("pick_cell", {"cell": "c7", "tester": 1}),
        ("place_cell", {"cell": "c7", "agv": 1, "slot": 3})),
    "B fifth slot": reply(
        ("place_cell", {"cell": "c7", "agv": 1, "slot": 5})),
    "C made-up tool": reply(("test_voltage", {"cell": "c8"})),
    "D made-up cell": reply(
        ("pick_cell", {"cell": "c9", "tester": 2})),
}

NAMES = {1: "syntax", 2: "schema", 3: "tools", 4: "objects",
         5: "preconditions"}


def decide(scripted, max_tries=2):
    """Ask, check, re-prompt once with the error, then fall back.

    scripted[k] is the stand-in model's reply to request k + 1;
    request 2 is the first request plus the error message."""
    for n in range(1, max_tries + 1):
        reply = scripted[n - 1]
        result = check(reply)
        if result is None:
            print(f"  try {n}: accepted, sent to the executor")
            return reply
        layer, msg = result
        print(f"  try {n}: rejected at layer {layer}"
              f" ({NAMES[layer]})")
        print(f"    {msg}")
        if n < max_tries:
            print("  re-prompt: the same request plus that error")
    print("  fall back: hold the cell, keep the classical plan")
    return None


if __name__ == "__main__":
    for label, reply in REPLIES.items():
        result = check(reply)
        if result is None:
            print(f"{label}: accepted")
        else:
            layer, msg = result
            print(f"{label}: rejected at layer {layer}"
                  f" ({NAMES[layer]})")
            print(f"    {msg}")
    print()
    print("Policy run 1: bad reply, then a fixed one")
    decide([REPLIES["B fifth slot"], REPLIES["A good plan"]])
    print("Policy run 2: two bad replies in a row")
    decide([REPLIES["B fifth slot"], REPLIES["D made-up cell"]])
