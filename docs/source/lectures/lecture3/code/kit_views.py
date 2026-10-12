"""One kit state, three views: PDDL facts, a JSON record checked
against a JSON schema, and a text description.

The kit values are chosen for this example. The limits come from
ARIAC 2025: three AGVs, four stations (AgvStations.msg), four tray
slots, and the Li-Ion voltages in CellTypes.msg.

Run: python3 kit_views.py   (needs the jsonschema package)
"""

import copy

from jsonschema import Draft7Validator

KIT = {
    "agv": 1,
    "station": "INSPECTION",
    "cell_type": "LI_ION",
    "slots": [
        {"slot": 1, "cell": {"id": "c1", "voltage": 3.55}},
        {"slot": 2, "cell": {"id": "c2", "voltage": 3.62}},
        {"slot": 3, "cell": {"id": "c3", "voltage": 3.70}},
        {"slot": 4, "cell": None},
    ],
}

CELL = {
    "type": ["object", "null"],
    "required": ["id", "voltage"],
    "properties": {
        "id": {"type": "string"},
        "voltage": {"type": "number"},
    },
}
SCHEMA = {
    "type": "object",
    "required": ["agv", "station", "cell_type", "slots"],
    "properties": {
        "agv": {"type": "integer", "minimum": 1, "maximum": 3},
        "station": {
            "enum": ["INSPECTION", "ASSEMBLY", "SHIPPING", "RECYCLING"]
        },
        "cell_type": {"enum": ["LI_ION", "NIMH"]},
        "slots": {
            "type": "array",
            "minItems": 4,
            "maxItems": 4,
            "items": {
                "type": "object",
                "required": ["slot", "cell"],
                "properties": {
                    "slot": {
                        "type": "integer", "minimum": 1, "maximum": 4
                    },
                    "cell": CELL,
                },
            },
        },
    },
}


def pddl_facts(kit):
    agv = f"agv{kit['agv']}"
    facts = [f"(at {agv} {kit['station'].lower()})"]
    for s in kit["slots"]:
        slot = f"s{s['slot']}"
        if s["cell"] is None:
            facts.append(f"(slot-empty {agv} {slot})")
        else:
            c = s["cell"]["id"]
            facts += [f"(in-slot {c} {agv} {slot})", f"(passed {c})"]
    return facts


def text_view(kit):
    full = [s for s in kit["slots"] if s["cell"]]
    empty = [s["slot"] for s in kit["slots"] if not s["cell"]]
    volts = [f"{s['cell']['voltage']:.2f} V" for s in full]
    kind = "Li-Ion" if kit["cell_type"] == "LI_ION" else "Ni-MH"
    return (
        f"AGV {kit['agv']} is at the {kit['station'].lower()} "
        f"station. Kit type {kind}. Slots {full[0]['slot']} to "
        f"{full[-1]['slot']} hold cells at {', '.join(volts[:-1])} "
        f"and {volts[-1]}. Slot {empty[0]} is empty."
    )


def check(name, record):
    found = Draft7Validator(SCHEMA).iter_errors(record)
    errors = sorted(
        f"{'.'.join(map(str, e.absolute_path))}: "
        f"{e.validator} {e.validator_value}"
        for e in found
    )
    print(f"  {name}: {'valid' if not errors else 'rejected'}")
    for error in errors:
        print(f"    {error}")


def fourth_cell_range(kit, nominal=3.6, cell_tol=0.2, kit_tol=0.15):
    total = sum(s["cell"]["voltage"] for s in kit["slots"] if s["cell"])
    low = max(4 * nominal - kit_tol - total, nominal - cell_tol)
    high = min(4 * nominal + kit_tol - total, nominal + cell_tol)
    return total, low, high


def main():
    print("PDDL facts:")
    for fact in pddl_facts(KIT):
        print(f"  {fact}")
    print("Text:")
    print(f"  {text_view(KIT)}")
    print("JSON schema checks:")
    check("the kit", KIT)
    bad_agv = copy.deepcopy(KIT)
    bad_agv["agv"] = 5
    check("agv 5", bad_agv)
    five_slots = copy.deepcopy(KIT)
    five_slots["slots"].append({"slot": 5, "cell": None})
    check("five slots", five_slots)
    total, low, high = fourth_cell_range(KIT)
    print(f"Three cells total {total:.2f} V.")
    print(f"The fourth cell must be from {low:.2f} V to {high:.2f} V.")


if __name__ == "__main__":
    main()
