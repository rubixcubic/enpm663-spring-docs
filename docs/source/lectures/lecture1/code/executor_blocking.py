"""A slow callback blocks a fast one unless the executor and callback groups allow both.

The slow timer stands in for a callback that waits on a robot skill (1 s).
The fast timer stands in for reading a status topic at 10 Hz.

Run: python3 executor_blocking.py single  (SingleThreadedExecutor, one group)
     python3 executor_blocking.py multi   (MultiThreadedExecutor, two groups)
"""

import sys
import threading
import time

import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import (
    MultiThreadedExecutor,
    SingleThreadedExecutor,
)
from rclpy.node import Node


class Cell(Node):
    def __init__(self, two_groups: bool):
        super().__init__("cell")
        slow = MutuallyExclusiveCallbackGroup() if two_groups else None
        fast = MutuallyExclusiveCallbackGroup() if two_groups else None
        self.create_timer(1.0, self.wait_on_skill, callback_group=slow)
        self.create_timer(0.1, self.read_status, callback_group=fast)
        self.status_reads = 0

    def wait_on_skill(self):
        time.sleep(1.0)  # stands in for waiting on a skill's result

    def read_status(self):
        self.status_reads += 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "single"
    rclpy.init()
    node = Cell(two_groups=(mode == "multi"))
    executor = (
        MultiThreadedExecutor()
        if mode == "multi"
        else SingleThreadedExecutor()
    )
    executor.add_node(node)
    spinner = threading.Thread(target=executor.spin)
    spinner.start()
    time.sleep(5.0)
    executor.shutdown()  # stops spin() and waits for running callbacks
    spinner.join()
    print(
        f"{mode}: {node.status_reads} status reads in 5 s (50 expected at 10 Hz)"
    )
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
