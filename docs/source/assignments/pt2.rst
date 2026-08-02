====================================================
PT2: Perception Pipeline
====================================================

.. list-table::
   :widths: 25 25 25 25
   :class: compact-table

   * - **Hand out:** Week 5
     - **Due:** Week 7
     - **Weight:** 10%
     - **Tools:** OpenCV, TF2

Goal
----

Detect ARIAC parts in camera images and publish their 3D poses to a TF-aware
ROS 2 topic; then wire PT1's behavior tree to consume real perception output
instead of hard-coded poses.

ARIAC Tie-in
------------

ARIAC's overhead RGB-D cameras above the supply bins are the input. The part
types (batteries, sensors, regulators, pumps) in their color variants define
the detection classes. The world-frame poses your pipeline publishes are what
PT3's planner and executor will act on.

Deliverable
-----------

- A perception package (color segmentation, contour and centroid extraction,
  pixel-to-3D via camera intrinsics and depth, camera-frame to world-frame via
  TF2).
- A comparison of detected vs. ground-truth poses on at least 5 ARIAC scenes,
  with error metrics.
- The updated PT1 behavior tree that consumes the perception topic.

Relevant Lectures
-----------------

- Week 5: Sensing and Perception for Robotic Systems.
