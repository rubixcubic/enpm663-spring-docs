"""Where is slot 1 of AGV 1 in the world, before and after a move?

Frames and offsets are ARIAC's own (branch ariac2025, commit 0c3e722):
  tf_publisher_plugin.cpp: world -> agv1_frame goes on the moving
    (dynamic) broadcaster: the AGV model has <static>false</static>;
    agv1_frame -> agv1_tray_frame -> agv1_slot1_frame are static.
  ariac_gz/models/agv/model.sdf: tray 0.35 m above the base, turned
    -1.57 rad about z; slot 1 at (-0.065, 0.05, 0.032) m in the tray.
  AGV 1 at the inspection station: (2.15, 1.5, 0.005) m, yaw 1.57 rad
    (ariac_gz/world/ariac.world).
  AGV at the assembly station: (5.0, 4.5) m, yaw 0 rad
    (ariac_plugins/include/ariac_plugins/agv_motion_plugin.hpp);
    z kept at 0.005 m.
This script stands in for ARIAC: it publishes the same transforms.
"""

import math

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import (
    Buffer,
    StaticTransformBroadcaster,
    TransformBroadcaster,
    TransformListener,
)


def make_tf(stamp, parent, child, xyz, yaw):
    t = TransformStamped()
    t.header.stamp = stamp
    t.header.frame_id, t.child_frame_id = parent, child
    tr = t.transform.translation
    tr.x, tr.y, tr.z = xyz
    t.transform.rotation.z = math.sin(yaw / 2.0)  # turn about z
    t.transform.rotation.w = math.cos(yaw / 2.0)
    return t


def lookup_at(node, buffer, target, source, stamp):
    """Spin until TF2 can answer for this time, then look up."""
    while not buffer.can_transform(target, source, stamp):
        rclpy.spin_once(node, timeout_sec=0.05)
    return buffer.lookup_transform(target, source, stamp)


def show(label, t):
    p = t.transform.translation
    print(f"{label}: x = {p.x:.3f}, y = {p.y:.3f}, z = {p.z:.3f}")
    return p


def main():
    rclpy.init()
    node = Node("agv_slot_lookup")
    static = StaticTransformBroadcaster(node)
    moving = TransformBroadcaster(node)
    buffer = Buffer()
    TransformListener(buffer, node)
    now = node.get_clock().now().to_msg()
    static.sendTransform([
        make_tf(now, "agv1_frame", "agv1_tray_frame",
                (0.0, 0.0, 0.35), -1.57),
        make_tf(now, "agv1_tray_frame", "agv1_slot1_frame",
                (-0.065, 0.05, 0.032), 0.0),
    ])
    stations = [
        ("inspection", (2.15, 1.5, 0.005), 1.57),
        ("assembly", (5.0, 4.5, 0.005), 0.0),
    ]
    print("slot 1 of AGV 1, in meters")
    found = []
    for name, xyz, yaw in stations:
        stamp = node.get_clock().now()
        moving.sendTransform(
            make_tf(stamp.to_msg(), "world", "agv1_frame", xyz, yaw))
        t = lookup_at(node, buffer, "world", "agv1_slot1_frame",
                      stamp)
        found.append(show(f"in world, AGV at {name:10s}", t))
    t = buffer.lookup_transform("agv1_frame", "agv1_slot1_frame",
                                Time())
    show("in agv1_frame, any station ", t)
    a, b = found
    gap = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))
    print(f"a pose cached at inspection is {gap:.3f} m off")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
