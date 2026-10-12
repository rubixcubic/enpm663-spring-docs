"""A py_trees_ros tree that moves one cell from tester to tray.

Everything ARIAC would provide is a stand-in in this process:
  - the tester publishes std_msgs/Float64 on /tester1/voltage
    every 0.1 s (ARIAC: VoltageReading on /voltage_tester_1/voltage);
  - pick_from_tester and place_in_slot are action servers of type
    control_msgs/GripperCommand (the course skills have their own
    types); each goal runs for a scripted time, then succeeds or
    aborts;
  - check_kit is a std_srvs/Trigger service (ARIAC:
    CheckKitQuality, which answers is_good).
Run:  python3 ros_tree_demo.py ok | timeout | bad_kit
"""
import sys
import threading
import time

import py_trees
import py_trees_ros
import rclpy
from control_msgs.action import GripperCommand
from py_trees.common import Access, Status
from rclpy.action import ActionServer, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Float64
from std_srvs.srv import Trigger

RUN = sys.argv[1]
# (seconds the goal runs, result) for each goal, in order
SCRIPT = {
    "pick_from_tester": [(0.4, "abort"), (0.4, "succeed")],
    "place_in_slot": [(5.0 if RUN == "timeout" else 0.6, "succeed")],
}
T0 = time.monotonic()


def stamp():
    return f"{time.monotonic() - T0:4.1f} s"


class StandIns(Node):
    """The tester, two skills and the kit check, all stand-ins."""

    def __init__(self):
        super().__init__("stand_ins")
        group = ReentrantCallbackGroup()
        self.pub = self.create_publisher(
            Float64, "tester1/voltage", qos_profile_sensor_data)
        self.create_timer(0.1, self.publish, callback_group=group)
        for name in SCRIPT:
            ActionServer(
                self, GripperCommand, name,
                lambda handle, n=name: self.execute(n, handle),
                cancel_callback=lambda goal: CancelResponse.ACCEPT,
                callback_group=group)
        self.create_service(Trigger, "check_kit", self.check_kit,
                            callback_group=group)
        self.goals = {name: 0 for name in SCRIPT}

    def publish(self):
        self.pub.publish(Float64(data=3.62))

    def execute(self, name, handle):
        seconds, result = SCRIPT[name][self.goals[name]]
        self.goals[name] += 1
        start = time.monotonic()
        while time.monotonic() - start < seconds:
            if handle.is_cancel_requested:
                handle.canceled()
                print(f"{stamp()}  [server] {name}: goal canceled")
                return GripperCommand.Result()
            time.sleep(0.05)
        print(f"{stamp()}  [server] {name}: goal {result}ed")
        handle.succeed() if result == "succeed" else handle.abort()
        return GripperCommand.Result()

    def check_kit(self, request, response):
        response.success = RUN != "bad_kit"
        response.message = "stand-in: kit rejected" \
            if RUN == "bad_kit" else "stand-in: kit accepted"
        return response


class KitIsGood(py_trees.behaviour.Behaviour):
    """Condition on the reply the check_kit leaf wrote."""

    def __init__(self):
        super().__init__("kit_is_good")
        self.bb = self.attach_blackboard_client(self.name)
        self.bb.register_key("/kit/check", Access.READ)

    def update(self):
        reply = self.bb.get("/kit/check")
        self.feedback_message = reply.message
        return Status.SUCCESS if reply.success else Status.FAILURE


def build():
    goal = GripperCommand.Goal()
    voltage = py_trees_ros.subscribers.ToBlackboard(
        name="read_voltage", topic_name="tester1/voltage",
        topic_type=Float64, qos_profile=qos_profile_sensor_data,
        blackboard_variables={"/tester1/voltage": "data"})
    pick = py_trees_ros.action_clients.FromConstant(
        name="pick_from_tester", action_type=GripperCommand,
        action_name="pick_from_tester", action_goal=goal)
    place = py_trees_ros.action_clients.FromConstant(
        name="place_in_slot", action_type=GripperCommand,
        action_name="place_in_slot", action_goal=goal)
    check = py_trees_ros.service_clients.FromConstant(
        name="check_kit", service_type=Trigger,
        service_name="check_kit", service_request=Trigger.Request(),
        key_response="/kit/check")
    return py_trees.composites.Sequence("move_cell", True, [
        voltage,
        py_trees.decorators.Retry("retry_pick", pick, num_failures=2),
        py_trees.decorators.Timeout("timeout_place", place,
                                    duration=2.0),
        check,
        KitIsGood(),
    ])


def main():
    rclpy.init()
    stand_ins = StandIns()
    tree = py_trees_ros.trees.BehaviourTree(build())
    tree.setup(node_name="gp1_tree", timeout=10.0)
    print(py_trees.display.ascii_tree(tree.root))
    heard = [0]  # voltage messages this node receives while ticking
    heard_at_end = []
    tree.node.create_subscription(
        Float64, "tester1/voltage",
        lambda msg: heard.__setitem__(0, heard[0] + 1),
        qos_profile_sensor_data)
    last = {node.name: Status.INVALID for node in tree.root.iterate()}

    def report(t):
        for node in t.root.iterate():
            if last[node.name] != node.status:
                last[node.name] = node.status
                print(f"{stamp()}  tick {t.count + 1:2d}: "
                      f"{node.name} {node.status.name}")
        if t.root.status in (Status.SUCCESS, Status.FAILURE):
            t.timer.cancel()  # stop ticking once the root is done
            heard_at_end.append(heard[0])

    executor = MultiThreadedExecutor()
    executor.add_node(stand_ins)
    executor.add_node(tree.node)
    global T0
    T0 = time.monotonic()
    tree.tick_tock(period_ms=100.0, post_tick_handler=report)
    spinner = threading.Thread(target=executor.spin, daemon=True)
    spinner.start()
    while tree.root.status in (Status.INVALID, Status.RUNNING):
        time.sleep(0.05)
    time.sleep(0.5)  # let a cancel reach the server
    reply = py_trees.blackboard.Blackboard.storage.get("/kit/check")
    if reply is not None:
        print(f"check_kit reply: success={reply.success},"
              f" message='{reply.message}'")
    print(f"tree finished: {tree.root.status.name} after"
          f" {tree.count} ticks; {heard_at_end[0]} voltage"
          f" messages heard")
    tree.shutdown()
    executor.shutdown()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
