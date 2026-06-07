====================================================
L10: ROS 2 -- Foundations
====================================================

Overview
--------

This is the first ROS 2 lecture in ENPM702. Students learn the core
communication pattern in ROS 2: the publish-subscribe model. The lecture
covers creating ROS 2 packages with ``colcon``, writing publisher and
subscriber nodes in C++ using object-oriented programming (inheriting
from ``rclcpp::Node``), working with standard message types, and
defining custom interfaces (messages and services). By the end of this
lecture, students will be able to build, run, and inspect ROS 2 nodes
that communicate over topics.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Understand the ROS 2 architecture: nodes, topics, messages, and the computation graph.
   - Create ROS 2 packages using ``ros2 pkg create`` with ``ament_cmake``.
   - Build packages with ``colcon build`` and source the overlay workspace.
   - Write publisher nodes that inherit from ``rclcpp::Node`` and publish messages on topics.
   - Write subscriber nodes that inherit from ``rclcpp::Node`` and process incoming messages via callbacks.
   - Use standard message types (``std_msgs``, ``geometry_msgs``) in publisher/subscriber nodes.
   - Define custom message types (``.msg`` files) in a dedicated interface package.
   - Use ROS 2 CLI tools to inspect the system: ``ros2 topic list``, ``ros2 topic echo``, ``ros2 topic info``, ``ros2 node list``.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_exercises
   l10_quiz
   l10_references

Next Steps
----------

- In the next lecture (**L11: Parameters, Launch Files, Executors**), we will cover:

  - Declaring and using parameters in ROS 2 nodes.
  - Writing launch files to start multiple nodes.
  - Understanding executors and callback groups.
  - Configuring nodes at runtime without recompilation.

- Before next class: complete the C++ exercises on publishers,
  subscribers, and custom interfaces, and the quiz.
- Make sure you can build and run a basic publisher/subscriber pair in
  your ROS 2 workspace.
