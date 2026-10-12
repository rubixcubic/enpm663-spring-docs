"""From a camera pixel to a point on the assembly table, with TF2.

Sources (ARIAC branch ariac2025, commit 0c3e722):
  Camera: 720p is 1280 x 720 (ariac_setup/structures.py); FOV 1.57 rad
    is the docs' example configuration (config_files.rst).
  Gazebo intrinsics with no lens block in the SDF (ARIAC sets none):
    fx = fy = (width / 2) / tan(FOV / 2), cx = width / 2,
    cy = height / 2 (gz-rendering Utils.cc,
    gz-sensors CameraSensor.cc).
  ARIAC publishes {name}_frame, the camera's link frame; a Gazebo
    camera looks along that frame's +x. ARIAC has no optical frame,
    so this script adds one (z forward, x right, y down, REP 103).
  Table top: z = 0.43 m (assembly_table/model.sdf: a 0.43 m box).
  Top shell: 0.023 m tall (collision mesh top_shell_vg_4.stl).
Chosen for this example: the camera "top_camera" at (3.85, 5.2, 1.43),
1.0 m above the table, RPY (0, pi/2, 0) so that it looks straight
down. (3.85, 5.2) is where ARIAC drops the top shell before its
random offset (shell_insertion_plugin.hpp).
"""

import math

import numpy as np
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo
from tf2_ros import Buffer, StaticTransformBroadcaster
from tf2_ros import TransformListener

W, H, FOV = 1280, 720, 1.57
TABLE_Z, SHELL_H = 0.43, 0.023
LINK, OPTICAL = "top_camera_frame", "top_camera_optical_frame"


def make_tf(stamp, parent, child, xyz, q):
    t = TransformStamped()
    t.header.stamp = stamp
    t.header.frame_id, t.child_frame_id = parent, child
    tr, r = t.transform.translation, t.transform.rotation
    tr.x, tr.y, tr.z = xyz
    r.x, r.y, r.z, r.w = q
    return t


def rot(q):
    """Rotation matrix of a quaternion (x, y, z, w)."""
    x, y, z, w = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w),
         2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z),
         2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w),
         1 - 2 * (x * x + y * y)],
    ])


def lookup(node, buffer, target, source):
    while not buffer.can_transform(target, source, Time()):
        rclpy.spin_once(node, timeout_sec=0.05)
    t = buffer.lookup_transform(target, source, Time()).transform
    r = t.rotation
    origin = np.array([t.translation.x, t.translation.y,
                       t.translation.z])
    return rot((r.x, r.y, r.z, r.w)), origin


def pixel_to_plane(u, v, k, R, origin, plane_z):
    fx, cx, fy, cy = k[0], k[2], k[4], k[5]
    ray = np.array([(u - cx) / fx, (v - cy) / fy, 1.0])  # Step 1
    ray_w = R @ ray                                      # Step 2
    t = (plane_z - origin[2]) / ray_w[2]                 # Step 3
    return origin + t * ray_w


def main():
    rclpy.init()
    node = Node("pixel_to_table")
    info = CameraInfo(width=W, height=H)
    fx = (W / 2) / math.tan(FOV / 2)
    info.k = [fx, 0.0, W / 2, 0.0, fx, H / 2, 0.0, 0.0, 1.0]
    k = info.k
    print(f"K: fx = fy = {k[0]:.1f}, cx = {k[2]:.0f}, "
          f"cy = {k[5]:.0f}")
    s = math.sin(math.pi / 4)
    down = (0.0, s, 0.0, s)             # RPY (0, pi/2, 0)
    optical = (-0.5, 0.5, -0.5, 0.5)    # optical axes in the link
    now = node.get_clock().now().to_msg()
    StaticTransformBroadcaster(node).sendTransform([
        make_tf(now, "world", LINK, (3.85, 5.2, 1.43), down),
        make_tf(now, LINK, OPTICAL, (0.0, 0.0, 0.0), optical),
    ])
    buffer = Buffer()
    TransformListener(buffer, node)
    R, _ = lookup(node, buffer, LINK, OPTICAL)
    p = R @ np.array([1.0, 2.0, 3.0])
    print(f"optical (1, 2, 3) is link ({p[0]:.0f}, {p[1]:.0f}, "
          f"{p[2]:.0f})")
    R, origin = lookup(node, buffer, "world", OPTICAL)
    for u, v in [(704, 360), (576, 296)]:
        x, y, z = pixel_to_plane(u, v, k, R, origin, TABLE_Z)
        print(f"pixel ({u}, {v}) on the table: "
              f"({x:.4f}, {y:.4f}, {z:.3f})")
    top = TABLE_Z + SHELL_H
    x, y, z = pixel_to_plane(704, 360, k, R, origin, top)
    print(f"pixel (704, 360) at z = {top:.3f}: "
          f"({x:.4f}, {y:.4f}, {z:.3f})")
    q = R.T @ (np.array([3.85, 5.10, TABLE_Z]) - origin)
    u, v = k[0] * q[0] / q[2] + k[2], k[4] * q[1] / q[2] + k[5]
    print(f"check: world (3.85, 5.10, 0.43) -> pixel "
          f"({u:.1f}, {v:.1f})")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
