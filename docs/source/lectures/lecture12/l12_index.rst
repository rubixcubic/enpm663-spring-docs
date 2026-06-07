====================================================
L12: ROS 2 -- Communication Patterns
====================================================

Overview
--------

This lecture extends the ROS 2 toolkit beyond publish-subscribe by
introducing two additional communication patterns: **services** and
**actions**. Services provide a synchronous request-response mechanism
suited to quick, one-off queries and commands, while actions support
long-running tasks that report incremental feedback and can be
preempted. Together with topics, these three patterns cover the vast
majority of inter-node communication needs in a ROS 2 system. Students
will define custom ``.srv`` and ``.action`` interfaces, implement
servers and clients in C++, and learn when each pattern is the
appropriate choice.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Distinguish the three core ROS 2 communication patterns: topics (publish-subscribe), services (request-response), and actions (goal-feedback-result).
   - Define custom service interfaces (``.srv`` files) and build them with ``ament_cmake``.
   - Implement a service server using ``create_service`` and handle requests in a callback.
   - Implement a service client using ``create_client`` and ``async_send_request``.
   - Define custom action interfaces (``.action`` files) and build them with ``ament_cmake``.
   - Implement an action server using ``rclcpp_action`` that publishes feedback and returns a result.
   - Implement an action client that sends goals, receives feedback, and processes results asynchronously.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l12_lecture
   l12_exercises
   l12_quiz
   l12_references

Next Steps
----------

- In the next lecture (**L13: Frames, Lifecycle Nodes**), we will cover:

  - The TF2 transform library and coordinate frames.
  - Broadcasting and listening to transforms.
  - Lifecycle (managed) nodes and their state machine.
  - Designing robust systems with managed transitions.

- Before next class: complete the C++ exercises on services and
  actions, and the quiz.
- Make sure you can build and run a service server/client pair and an
  action server/client pair in your ROS 2 workspace.
