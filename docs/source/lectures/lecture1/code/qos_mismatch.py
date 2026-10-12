"""Break beam QoS: a best-effort publisher and a subscriber with the default QoS.

ARIAC's break beam publishes <sensor>/change with rclcpp::SensorDataQoS()
(best effort; ariac_plugins/src/ray_sensor_plugin.cpp, lines 51 and 52).
std_msgs/Bool stands in for ariac_interfaces/BreakBeamStatus.

Run: python3 qos_mismatch.py         (subscriber uses the default QoS)
     python3 qos_mismatch.py --match (subscriber uses the sensor data QoS)
"""

import sys

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Bool


class BeamListener(Node):
    def __init__(self, match: bool):
        super().__init__("beam_listener")
        self.pub = self.create_publisher(
            Bool, "beam/change", qos_profile_sensor_data
        )
        sub_qos = qos_profile_sensor_data if match else 10
        self.sub = self.create_subscription(
            Bool, "beam/change", self.on_change, sub_qos
        )
        self.sent = 0
        self.received = 0
        self.create_timer(0.1, self.publish)

    def publish(self):
        self.pub.publish(Bool(data=True))
        self.sent += 1

    def on_change(self, msg: Bool):
        self.received += 1


def main():
    rclpy.init()
    node = BeamListener(match="--match" in sys.argv)
    end = node.get_clock().now().nanoseconds + 2_000_000_000
    while node.get_clock().now().nanoseconds < end:
        rclpy.spin_once(node, timeout_sec=0.05)
    print(f"sent {node.sent}, received {node.received}")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
