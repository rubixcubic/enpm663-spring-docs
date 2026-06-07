====================================================
L9: OOP Advanced
====================================================

Overview
--------

This lecture covers advanced object-oriented programming concepts in C++.
Building on the OOP fundamentals from L8, we explore how classes relate to
each other through association, aggregation, composition, and inheritance.
The lecture then introduces polymorphism -- both compile-time and runtime --
showing how ``virtual`` methods, ``override``, and ``= default`` enable
flexible, extensible designs. We examine why virtual destructors are
essential for polymorphic hierarchies, how to define abstract classes with
pure virtual methods, and how concrete classes fulfill those contracts.
The lecture concludes with the ``final`` keyword for locking class
hierarchies and method implementations.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Understand class relationships: association, aggregation, composition, and inheritance.
   - Distinguish compile-time vs. runtime polymorphism and use ``virtual`` methods.
   - Apply ``override``, ``= default``, and ``final`` keywords correctly.
   - Choose between ``auto`` and explicit base types for polymorphic objects.
   - Implement ``virtual`` destructors to prevent resource leaks.
   - Create abstract classes with pure ``virtual`` methods and concrete implementations.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l9_lecture
   l9_shell
   l9_exercises
   l9_quiz
   l9_references

Next Steps
----------

- In the next lecture (**L10: ROS 2 Foundations**), we will cover:

  - Introduction to ROS 2 and its architecture.
  - Publisher/Subscriber communication pattern.
  - Custom interfaces (messages and services).
  - Creating ROS 2 packages and nodes that inherit from ``rclcpp::Node``.

- Before next class: complete the shell exercises (this is the final set
  before we transition to ROS 2), the C++ exercises on inheritance and
  polymorphism, and the quiz.
- Make sure your ROS 2 installation is complete and working (see the
  ROS setup guide).
