====================================================
L10: Frames, Transforms, and Motion Planning
====================================================

Overview
--------

This lecture opens up the motion layer: TF2 in depth, the pinhole camera
model that turns a camera pixel into a robot target, the MoveIt 2
architecture, the motion planning pipeline (sampling, collision checking,
trajectory optimization) and parameterized grasps. It also shows how the
course skills package that you have called since GP1 is built on MoveIt 2,
so you can tune it or debug it for the final demo.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Build and reason about a TF2 frame chain for an ARIAC robot cell.
- Convert a camera pixel on a known plane to a world position with the
  pinhole camera model, the camera intrinsics and TF2.
- Describe the MoveIt 2 architecture: ``move_group``, the planning scene, the
  planners.
- Plan a motion with MoveIt 2 from Python.
- Specify grasp poses as parameterized targets relative to a part frame (no
  learned grasp model).
- Explain how the course skills package turns a MoveIt 2 plan into an ARIAC
  joint trajectory and a gripper or vacuum command.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- TF2 in depth: static and dynamic transforms, frame conventions, lookup
  failures.
- The pinhole camera model: intrinsics and extrinsics; locating an object on
  a known plane without a depth camera (the Task 2 top shell on the assembly
  table).
- MoveIt 2 architecture: ``move_group``, planning scene, planning pipeline,
  controllers.
- Sampling-based planners (RRT-Connect, PRM) and when each fits.
- Trajectory optimization (CHOMP, STOMP) at a high level.
- Parameterized grasps: a grasp pose defined relative to a part frame.
- Inside the course skills package: from a skill call to a trajectory on an
  ARIAC robot.


ARIAC Tie-in
------------

ARIAC 2025 gives each robot a joint trajectory action and a gripper action,
plus vacuum tools and a tool changer on assembly robot 2. Its example team
includes a MoveIt demo that moves all five robots. The course skills package
builds pick and place skills on top of these, and this lecture shows how.


Starting References
-------------------

- OpenCV documentation (camera images): https://docs.opencv.org/4.x/
- MoveIt 2 documentation: https://moveit.picknik.ai/main/
- ROS 2 TF2 tutorials: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/
- ARIAC 2025 ROS API: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
- ARIAC 2025 demos: https://pages.nist.gov/ARIAC_docs/en/latest/pages/demos.html
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Continue GP4; it is due in Week 13.
- In the next lecture, we will cover **recovery and robustness**; Quiz 5 is at
  the start of class.
