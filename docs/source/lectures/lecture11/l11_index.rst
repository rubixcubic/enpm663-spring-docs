====================================================
L11: ROS 2 -- Configuration and Orchestration
====================================================

Overview
--------

This lecture covers the tools and techniques for configuring, launching, and
orchestrating ROS 2 systems. We begin with **parameters** -- node-specific
configuration values that allow you to change a node's behavior without
recompiling. Next, we explore **launch files**, which let you start multiple
nodes, pass parameters, remap topics, and set up complex systems with a
single command. We then examine **executors** -- the mechanism that controls
how callbacks are dispatched -- including single-threaded and multi-threaded
executors with their associated callback groups. The lecture also covers
**YAML configuration files** for externalizing parameter values and the
**ROS 2 CLI tools** for inspecting and modifying parameters at runtime.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Declare, get, and set parameters on ROS 2 nodes using ``rclcpp``.
   - Use parameter callbacks to respond dynamically when parameters change at runtime.
   - Write Python launch files to start multiple nodes with parameters, remappings, and arguments.
   - Use launch arguments (``DeclareLaunchArgument``, ``LaunchConfiguration``) to create reusable launch files.
   - Structure YAML configuration files and load them from launch files.
   - Distinguish between single-threaded and multi-threaded executors and choose the appropriate one.
   - Use callback groups (mutually exclusive and reentrant) to control concurrency in multi-threaded executors.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l11_lecture
   l11_exercises
   l11_quiz
   l11_references

Next Steps
----------

- In the next lecture (**L12: ROS 2 -- Services and Actions**), we will cover:

  - ROS 2 services: synchronous request/reply communication.
  - Writing service servers and clients in C++.
  - ROS 2 actions: long-running tasks with feedback.
  - Writing action servers and clients.
  - Choosing between topics, services, and actions.

- Before next class: complete the C++ exercises on parameters, launch files,
  and executors, and take the quiz.
