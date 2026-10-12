"""Build a PointCloud2, read it back, move it to the world frame.

The points are one SYNTHETIC scan of lidar_a (synth.py), with the
cell right in front of it. A ray that hits nothing is a row of inf
here; row 0 is set to NaN by hand to show what skip_nans does.
"""
import numpy as np
import rclpy.time
import tf2_ros
from geometry_msgs.msg import TransformStamped
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header
import synth as S

lidar = S.two_lidars()[0]
pts = S.scan(lidar, 1.0, [], np.random.default_rng(0))
pts[0] = np.nan

# Build the message, as the ARIAC lidar plugin would publish it
header = Header(frame_id="lidar_a_frame")
msg = point_cloud2.create_cloud_xyz32(header, pts)
print(f"height {msg.height}, width {msg.width}, point_step "
      f"{msg.point_step}, row_step {msg.row_step}, "
      f"{len(msg.data)} bytes")
for f in msg.fields:
    print(f"  field {f.name}: offset {f.offset}, datatype "
          f"{f.datatype} (7 = FLOAT32)")

# Read it back into an N x 3 array
xyz = point_cloud2.read_points_numpy(
    msg, field_names=["x", "y", "z"], skip_nans=True)
bad = ~np.all(np.isfinite(xyz), axis=1)
print(f"read back {xyz.shape}, {bad.sum()} rows still not finite")
xyz = xyz[~bad]
print(f"after np.isfinite: {xyz.shape}")

# Stand-in for ARIAC's static transform from world to the lidar
t = TransformStamped()
t.header.frame_id, t.child_frame_id = "world", "lidar_a_frame"
(t.transform.translation.x, t.transform.translation.y,
 t.transform.translation.z) = lidar.xyz
t.transform.rotation.z = np.sin(lidar.yaw / 2)
t.transform.rotation.w = np.cos(lidar.yaw / 2)
buf = tf2_ros.Buffer()
buf.set_transform_static(t, "l5_demo")

# The lookup: target frame world, source frame lidar_a_frame
tf = buf.lookup_transform("world", "lidar_a_frame", rclpy.time.Time())
q, p = tf.transform.rotation, tf.transform.translation
x, y, z, w = q.x, q.y, q.z, q.w
m = np.eye(4)
m[:3, :3] = [                       # rotation matrix of q
    [1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)],
    [2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)],
    [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)]]
m[:3, 3] = [p.x, p.y, p.z]
world = (np.c_[xyz, np.ones(len(xyz))] @ m.T)[:, :3]  # all at once
on_cell = world[:, 2] > S.BELT_Z + 0.001
print(f"world frame: {on_cell.sum()} points on the cell, "
      f"{(~on_cell).sum()} on the belt")
print(f"first point, lidar frame: {np.round(xyz[0], 4)}")
print(f"first point, world frame: {np.round(world[0], 4)}")
