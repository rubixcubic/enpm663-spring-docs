"""L13: score the embodied-reasoning answers against GP2 lidar.

Three labels per cell, all chosen for this example:
  TRUTH  what the cell really has. In a practice run, ARIAC prints it
         to the Gazebo log when launched with log_cell_info:=true.
  LIDAR  the defect type in the team's GP2 inspection report.
  ER     the defect type from er_demo.py (a scripted stand-in).
Each defective cell in this example has one defect.

Only cells where both detectors gave a valid answer are scored, so
both are scored on the same cells.

Run: python3 score_er.py   (needs google-genai and jsonschema)
"""

from er_demo import ask_all

TRUTH = {"c01": None, "c02": "DENT", "c03": None, "c04": "SCRATCH",
         "c05": None, "c06": "BULGE", "c07": "DENT", "c08": None,
         "c09": "SCRATCH", "c10": None, "c11": "BULGE", "c12": None}
LIDAR = {"c01": None, "c02": "DENT", "c03": None, "c04": "SCRATCH",
         "c05": None, "c06": "BULGE", "c07": "DENT", "c08": None,
         "c09": None, "c10": None, "c11": "BULGE", "c12": None}
TYPES = ["DENT", "SCRATCH", "BULGE"]


def er_labels(results):
    """One label per cell with a valid answer; None if no defect."""
    labels, rejected = {}, []
    for cell, (_, answer, errors) in results.items():
        if errors:
            rejected.append(cell)
            continue
        kinds = [d["type"] for d in answer["defects"]]
        labels[cell] = kinds[0] if kinds else None
    return labels, rejected


def counts(pred, cells, kind):
    """True positives, false positives, false negatives for a kind."""
    tp = sum(pred[c] == kind and TRUTH[c] == kind for c in cells)
    fp = sum(pred[c] == kind and TRUTH[c] != kind for c in cells)
    fn = sum(pred[c] != kind and TRUTH[c] == kind for c in cells)
    return tp, fp, fn


def ratio(num, den):
    return f"{num}/{den} = {num / den:.2f}" if den else "no calls"


def row(name, pred, cells, kind):
    tp, fp, fn = counts(pred, cells, kind)
    print(f"  {name:6} TP {tp}  FP {fp}  FN {fn}   "
          f"precision {ratio(tp, tp + fp):12}  "
          f"recall {ratio(tp, tp + fn)}")


def main():
    _, results = ask_all()
    er, rejected = er_labels(results)
    cells = [c for c in TRUTH if c in er]
    print(f"Cells used: {len(cells)} of {len(TRUTH)}")
    print(f"  rejected by the schema: {', '.join(rejected)}")
    for kind in TYPES:
        print(f"{kind}")
        row("lidar", LIDAR, cells, kind)
        row("ER", er, cells, kind)
    same = sum(er[c] == LIDAR[c] for c in cells)
    print(f"ER and lidar give the same label: {same} of {len(cells)}")
    print("Latency and cost per call: not measured (stand-in)")


if __name__ == "__main__":
    main()
