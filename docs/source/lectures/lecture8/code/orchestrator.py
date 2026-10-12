"""L8 demo: an orchestrator loop around a scripted stand-in model.

No LLM is called. ScriptedModel returns fixed replies, one per call,
in place of a real model; a real model's answers vary. The tool is a
stand-in for ARIAC's /agvN/move action (stub_agv.py). The reply format
is simplified: a provider API returns a tool call as a structured
block (Anthropic: a tool_use block with a name and an input).

Run: python3 orchestrator.py
"""

import json

from stub_agv import STATIONS, example_factory, move_agv

MAX_STEPS = 6      # step limit, chosen for this example
MAX_INVALID = 2    # invalid outputs in a row, chosen for this example

SYSTEM = ("You plan AGV moves for an ARIAC kitting cell. "
          "Use only the listed tools. Reply 'done' when finished.")

TOOLS = [{
    "name": "move-agv",
    "description": "Move one AGV to a station (ARIAC /agvN/move). "
                   "Only a full tray (4 cells) may go to SHIPPING.",
    "input_schema": {
        "type": "object",
        "required": ["agv", "station"],
        "additionalProperties": False,
        "properties": {
            "agv": {"type": "integer", "minimum": 1, "maximum": 3},
            "station": {"enum": list(STATIONS)},
        },
    },
}]


class ScriptedModel:
    """Stand-in for an LLM: returns the next scripted reply."""

    def __init__(self, replies):
        self.replies = list(replies)

    def __call__(self, system, messages, tools):
        return self.replies.pop(0)


def guard(call, factory):
    """The orchestrator's checks before a tool runs."""
    if call.get("tool") != "move-agv":
        return f"unknown tool {call.get('tool')!r}"
    agv, station = call["args"]["agv"], call["args"]["station"]
    if agv not in factory or station not in STATIONS:
        return "agv or station not in the factory"
    cells = factory[agv]["cells"]
    if station == "SHIPPING" and cells != 4:
        return f"agv{agv} holds {cells} of 4 cells"
    return None


def run(model, factory, goal_check):
    state = {f"agv{n}": f"{a['station']}, {a['cells']} cells"
             for n, a in factory.items()}
    goal = {"goal": "ship the kit on agv1", "state": state}
    messages = [{"role": "user", "content": json.dumps(goal)}]
    print(f"  user:   {messages[0]['content']}")
    invalid = 0
    for step in range(1, MAX_STEPS + 1):
        sent = [SYSTEM, TOOLS, messages]
        size = sum(len(json.dumps(part)) for part in sent)
        print(f"call {step}: {len(messages)} messages, {size} chars")
        reply = model(SYSTEM, messages, TOOLS)
        print(f"  model:  {json.dumps(reply)}")
        messages.append({"role": "assistant", "content": reply})
        if "tool" not in reply:
            if goal_check(factory):
                return "goal reached"
            result = {"error": "goal not reached"}
        elif (error := guard(reply, factory)) is not None:
            invalid += 1
            result = {"error": f"guard: {error}"}
            if invalid == MAX_INVALID:
                print(f"  orch:   {json.dumps(result)}")
                return f"{invalid} invalid outputs in a row"
        else:
            invalid = 0
            result = move_agv(factory, **reply["args"])
        print(f"  orch:   {json.dumps(result)}")
        messages.append({"role": "user", "content": result})
    return "step limit"


def shipped(factory):
    """Goal for this demo, checked in code: agv1 at SHIPPING."""
    return factory[1]["station"] == "SHIPPING"


def move(agv, station):
    return {"tool": "move-agv",
            "args": {"agv": agv, "station": station}}


if __name__ == "__main__":
    print("=== Run 1 ===")
    model = ScriptedModel([move(2, "SHIPPING"), move(1, "SHIPPING"),
                           {"text": "done"}])
    print("stop:", run(model, example_factory(), shipped))
    print("=== Run 2 ===")
    model = ScriptedModel([move(2, "SHIPPING"), move(2, "SHIPPING")])
    print("stop:", run(model, example_factory(), shipped))
