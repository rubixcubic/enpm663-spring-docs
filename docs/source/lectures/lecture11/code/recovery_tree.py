#!/usr/bin/env python3
"""L11 demo: a recovery tree with injected failures (py_trees 2.6.0).

Inspection robot 1 must place a cell on a voltage tester. The same
tree runs three separate times, each with its own injected failure:

  A  the place on tester 1 fails once; Retry runs it again
  B  the place on tester 1 fails three times; the selector falls
     back to tester 2
  C  tester 1 reports MALFUNCTIONING while the place is running;
     the guard stops that branch and the selector falls back
  D  as B, with tester 1 still failing, but the selector has
     memory off: it goes back to tester 1 on every tick

No ROS and no simulator: each skill is a stub that follows a
script of outcomes chosen for this example.
"""
import py_trees
from py_trees.common import Status


def log(text):
    print(f"        {text}")


class StubSkill(py_trees.behaviour.Behaviour):
    """A stand-in for a skill. Script entry k sets attempt k:
    "fail" fails on the first tick; a number n runs for n ticks,
    then succeeds."""

    def __init__(self, name, script):
        super().__init__(name)
        self.script = list(script)
        self.attempt = 0
        self.ticks = 0

    def initialise(self):
        self.attempt += 1
        self.ticks = 0
        log(f"{self.name}: attempt {self.attempt} starts")

    def update(self):
        self.ticks += 1
        k = self.attempt - 1
        plan = self.script[k] if k < len(self.script) else 1
        if plan == "fail":
            log(f"{self.name}: attempt {self.attempt} FAILED"
                " (injected)")
            return Status.FAILURE
        if self.ticks < plan:
            return Status.RUNNING
        log(f"{self.name}: attempt {self.attempt} SUCCEEDED")
        return Status.SUCCESS

    def terminate(self, new_status):
        # self.status still holds the old status here
        if new_status == Status.INVALID and \
                self.status == Status.RUNNING:
            log(f"{self.name}: stopped by its parent")


class LoggedRetry(py_trees.decorators.Retry):
    """Retry that prints its feedback after each child failure."""

    def update(self):
        result = super().update()
        if self.decorated.status == Status.FAILURE:
            log(f"{self.name}: {self.feedback_message}")
        return result


class LoggedGuard(py_trees.decorators.EternalGuard):
    """EternalGuard that prints when it stops its branch."""

    def terminate(self, new_status):
        if new_status != Status.FAILURE:
            return
        if not self.condition():
            log(f"{self.name}: condition false, stops its branch")
        else:
            log(f"{self.name}: FAILURE, because its child failed")


def build(script_t1, status, memory=True):
    place_t1 = StubSkill("place_on_tester_1", script_t1)
    retry = LoggedRetry(
        "retry_3", place_t1, num_failures=3)
    guard = LoggedGuard(
        "tester_1_ok",
        retry,
        condition=lambda: status["tester_1"] == "OPERATIONAL",
    )
    place_t2 = StubSkill("place_on_tester_2", [2])
    hold = py_trees.behaviours.Running("hold_cell")
    root = py_trees.composites.Selector(
        "place_cell", memory=memory,
        children=[guard, place_t2, hold])
    return root


def run(title, script_t1, flip_at=None, ticks=5, memory=True):
    print(title)
    status = {"tester_1": "OPERATIONAL"}
    root = build(script_t1, status, memory)
    for n in range(1, ticks + 1):
        print(f"tick {n}")
        if n == flip_at:
            status["tester_1"] = "MALFUNCTIONING"
            log("tester 1 status is now MALFUNCTIONING")
        root.tick_once()
        if root.status != Status.RUNNING:
            log(f"place_cell: {root.status.name}"
                f" through {root.current_child.name}")
            break
    print()


if __name__ == "__main__":
    run("Run A: tester 1 place fails once", ["fail", 2])
    run("Run B: tester 1 place fails three times",
        ["fail", "fail", "fail"])
    run("Run C: tester 1 malfunctions during the place", [3],
        flip_at=2)
    run("Run D: as B, tester 1 keeps failing, memory off",
        ["fail"] * 6, ticks=4, memory=False)
