"""Where and when the arm meets a cell on the moving conveyor.

ARIAC publishes no pose for a cell. The team's break beam fires when a
cell passes it; positions here are along the belt, in meters past the
beam, and times are in seconds after the beam fired.

From ARIAC (branch ariac2025): the largest conveyor speed a team may
set is 0.1 m/s (ariac_setup/config/user_config_schema.json), the
value in the docs' example configuration. A stopped belt reports
speed 0 (linear_conveyor_plugin.cpp, conveyor malfunction).
Chosen for this example: the delay before the arm starts (2.0 s), the
time the arm takes to reach the grasp (1.5 s), and the stretch of belt
the arm can reach (0.00 m to 0.45 m past the beam).
"""

REACH = (0.00, 0.45)
MOVE_TIME = 1.5


def distance(speeds, t_end):
    """Add up speed x time, piece by piece, from 0 to t_end.

    speeds: list of (start time, speed), the status topic's history.
    """
    total = 0.0
    for i, (t0, v) in enumerate(speeds):
        t1 = speeds[i + 1][0] if i + 1 < len(speeds) else t_end
        t1 = min(t1, t_end)
        if t1 > t0:
            total += v * (t1 - t0)
    return total


def plan(name, speeds, start):
    meet = start + MOVE_TIME
    at_start = distance(speeds, start)
    at_meet = distance(speeds, meet)
    ok = REACH[0] <= at_meet <= REACH[1]
    print(f"{name}")
    print(f"  arm starts at t = {start:.1f} s, "
          f"cell at {at_start:.2f} m")
    print(f"  arm meets it at t = {meet:.1f} s, "
          f"cell at {at_meet:.2f} m")
    print("  in reach: move" if ok else "  out of reach: refuse")


def main():
    plan("A. belt at 0.1 m/s, arm starts after 2.0 s",
         [(0.0, 0.1)], 2.0)
    plan("B. belt at 0.1 m/s, arm starts after 3.5 s",
         [(0.0, 0.1)], 3.5)
    plan("C. belt stops 1.0 s after the beam fires",
         [(0.0, 0.1), (1.0, 0.0)], 2.0)
    feed_rate = 0.1  # cells per second, docs' example configuration
    gap_t = 1 / feed_rate
    print(f"one cell every {gap_t:.0f} s at 0.1 m/s: "
          f"{0.1 * gap_t:.1f} m apart")


if __name__ == "__main__":
    main()
