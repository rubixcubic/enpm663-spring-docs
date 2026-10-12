"""Where is slot 1 of AGV 1's tray, seen from the AGV's base?

The offsets are ARIAC's own, from ariac_gz/models/agv/model.sdf (branch ariac2025):
  tray_link   is 0.35 m above base_link, turned -1.57 rad about z
  slot_1_link is at (-0.065, 0.05, 0.032) m in tray_link
ARIAC's TF publisher names these frames agv1_frame, agv1_tray_frame and agv1_slot1_frame
(ariac_plugins/src/tf_publisher_plugin.cpp). This script publishes the same two transforms
as static frames and asks TF2 for the chain.
"""

import math

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import (
    Buffer,
    StaticTransformBroadcaster,
    TransformListener,
)


def make_tf(node, parent, child, xyz, yaw):
    t = TransformStamped()
    t.header.stamp = node.get_clock().now().to_msg()
    t.header.frame_id, t.child_frame_id = parent, child
    (
        t.transform.translation.x,
        t.transform.translation.y,
        t.transform.translation.z,
    ) = xyz
    t.transform.rotation.z = math.sin(
        yaw / 2.0
    )  # a turn about z only
    t.transform.rotation.w = math.cos(yaw / 2.0)
    return t


def main():
    rclpy.init()
    node = Node("slot_lookup")
    broadcaster = StaticTransformBroadcaster(node)
    broadcaster.sendTransform([
        make_tf(node, "agv1_frame", "agv1_tray_frame",
                (0.0, 0.0, 0.35), -1.57),
        make_tf(node, "agv1_tray_frame", "agv1_slot1_frame",
                (-0.065, 0.05, 0.032), 0.0),
    ])
    buffer = Buffer()
    TransformListener(buffer, node)
    base, slot = "agv1_frame", "agv1_slot1_frame"
    while not buffer.can_transform(base, slot, Time()):
        rclpy.spin_once(node, timeout_sec=0.1)
    t = buffer.lookup_transform(base, slot, Time())
    p = t.transform.translation
    print(
        f"slot 1 in agv1_frame: x = {p.x:.4f} m, y = {p.y:.4f} m, z = {p.z:.4f} m"
    )
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
