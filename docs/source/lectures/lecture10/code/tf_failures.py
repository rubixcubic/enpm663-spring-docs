"""Three TF2 lookup failures, and the exception each one raises.

The frames stand in for ARIAC's: agv1_frame under world, as
tf_publisher_plugin.cpp publishes it. "wrld" is a typo on purpose.
"""

import textwrap

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.duration import Duration
from rclpy.node import Node
from tf2_ros import (
    Buffer,
    StaticTransformBroadcaster,
    TransformBroadcaster,
    TransformException,
    TransformListener,
)


def make_tf(stamp, parent, child):
    t = TransformStamped()
    t.header.stamp = stamp
    t.header.frame_id, t.child_frame_id = parent, child
    t.transform.rotation.w = 1.0
    return t


def attempt(label, buffer, target, source, when):
    print(label)
    try:
        buffer.lookup_transform(target, source, when)
        print("  found")
    except TransformException as e:
        print(f"  {type(e).__name__}")
        for row in textwrap.wrap(str(e), 60):
            print(f"    {row}")


def main():
    rclpy.init()
    node = Node("lookup_failures")
    buffer = Buffer()
    TransformListener(buffer, node)
    moving = TransformBroadcaster(node)
    static = StaticTransformBroadcaster(node)
    now = node.get_clock().now()
    moving.sendTransform(make_tf(now.to_msg(), "world", "agv1_frame"))
    static.sendTransform(
        make_tf(now.to_msg(), "wrld", "top_camera_frame"))
    while not (buffer.can_transform("world", "agv1_frame", now)
               and buffer.can_transform("wrld", "top_camera_frame",
                                        now)):
        rclpy.spin_once(node, timeout_sec=0.05)
    attempt("1. a frame nobody publishes", buffer,
            "world", "agv9_frame", now)
    later = now + Duration(seconds=5.0)
    attempt("2. a time newer than the newest transform", buffer,
            "world", "agv1_frame", later)
    attempt("3. two trees that never connect", buffer,
            "world", "top_camera_frame", now)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
