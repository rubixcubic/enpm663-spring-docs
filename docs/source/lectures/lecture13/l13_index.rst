====================================================
L13: ROS 2 -- Advanced Topics
====================================================

Overview
--------

This is the final ROS 2 lecture in the course. It covers two essential
capabilities for building robust robotic systems: **coordinate frame
management with TF2** and **managed lifecycle nodes**. TF2 provides the
framework for tracking and transforming between coordinate frames --
critical when your robot has multiple sensors, links, and reference
frames. Lifecycle nodes give you deterministic control over node
startup, shutdown, and error recovery, enabling coordinated system
bringup. Both topics are essential for **GP3**.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Understand what coordinate frames are and why they are essential in robotics.
   - Use TF2 to broadcast and listen for transforms between coordinate frames.
   - Distinguish between static and dynamic transforms and know when to use each.
   - Understand the lifecycle node state machine and its states (Unconfigured, Inactive, Active, Finalized).
   - Implement a lifecycle node by inheriting from ``rclcpp_lifecycle::LifecycleNode``.
   - Use lifecycle transition callbacks (``on_configure``, ``on_activate``, ``on_deactivate``, ``on_cleanup``, ``on_shutdown``).
   - Manage lifecycle nodes using ``ros2 lifecycle`` CLI commands and programmatic transitions.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l13_lecture
   l13_exercises
   l13_quiz
   l13_references

Next Steps
----------

- This is the **final lecture** in the course. You now have all the tools
  and knowledge needed for the remaining assignments.

- **GP3** uses the concepts from this lecture extensively:

  - TF2 for managing coordinate frames between the robot, its sensors,
    and the world.
  - Lifecycle nodes for coordinated startup and shutdown of system
    components.

- Complete the C++ exercises on TF2 and lifecycle nodes, and take the
  quiz to solidify your understanding before starting GP3.
