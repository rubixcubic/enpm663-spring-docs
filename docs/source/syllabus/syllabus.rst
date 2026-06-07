Syllabus
========

Grade Breakdown
---------------

.. list-table::
   :header-rows: 1
   :widths: 60 20
   :class: compact-table

   * - Component
     - Percentage
   * - RWAs (3) + GPs (3)
     - 70%
   * - Quizzes (5)
     - 25%
   * - Participation/Engagement
     - 5%
   * - **Total**
     - **100%**

.. note::

   **Participation** is earned by actively engaging in class discussions
   or by submitting weekly exercise solutions on Canvas.


.. _course-schedule:

Course Schedule
---------------

.. list-table::
   :header-rows: 1
   :widths: 10 54 36
   :class: compact-table

   * - Week
     - Topic
     - Deliverable
   * - Week 1
     - Course Introduction, Linux Shell, VSCode, CMake
     -
   * - Week 2
     - Introduction to C++ (Variables, Types, Constants, Namespaces)
     -
   * - Week 3
     - Pointers and Memory Management (Stack, Heap, References)
     - RWA1 Posted
   * - Week 4
     - STL Containers (Strings, Arrays, Vectors, Iterators)
     - Quiz 1
   * - Week 5
     - Functions -- Basics (Declarations, Parameters, Overloading, Recursion)
     - RWA1 Due, RWA2 Posted
   * - Week 6
     - Functions -- Advanced (Templates, Lambdas, Functors, ``std::function``)
     - Quiz 2
   * - Week 7
     - Smart Pointers and Move Semantics (``unique_ptr``, ``shared_ptr``, ``weak_ptr``)
     - RWA2 Due
   * - Week 8
     - OOP Basics (Classes, Objects, Encapsulation, Constructors)
     - Quiz 3
   * - Week 9
     - OOP Advanced (Inheritance, Polymorphism, Abstraction)
     - RWA3 Posted
   * - Week 10
     - ROS 2 -- Foundations (Publisher, Subscriber, Custom Interfaces)
     - Quiz 4
   * - Week 11
     - ROS 2 -- Configuration and Orchestration (Parameters, Launch Files, Executors)
     - RWA3 Due, GP1 Posted
   * - Week 12
     - **THANKSGIVING BREAK**
     -
   * - Week 13
     - ROS 2 -- Communication Patterns (Services, Actions)
     - GP1 Due, GP2 Posted, Quiz 5
   * - Week 14
     - ROS 2 -- Advanced Topics (Frames, Lifecycle Nodes)
     - GP2 Due, GP3 Posted
   * - Week 15
     - No class
     - GP3 Due

.. note::

   This is a tentative schedule, and subject to change as necessary.
   Monitor ELMS-Canvas for current deadlines.


Real-World Applications (RWAs)
------------------------------

The three RWAs are **cumulative** individual assignments that progressively
build a C++ application using robotics-themed use cases. Each RWA refactors
and extends the previous one, demonstrating why each new C++ feature
improves the codebase:

.. list-table::
   :header-rows: 1
   :widths: 40 12 12 12
   :class: compact-table

   * - Assignment
     - Posted
     - Due
     - Duration
   * - RWA1: C++ Fundamentals (Variables, Types, Pointers)
     - Week 3
     - Week 5
     - 2 weeks
   * - RWA2: STL Containers and Functions
     - Week 5
     - Week 7
     - 2 weeks
   * - RWA3: Smart Pointers and OOP
     - Week 9
     - Week 11
     - 2 weeks


Group Projects (GPs)
--------------------

The three GPs are **cumulative** team-based projects that progressively
build a ROS 2 application with a mobile robot in Gazebo. Each GP extends
the previous deliverable:

.. list-table::
   :header-rows: 1
   :widths: 40 12 12 12
   :class: compact-table

   * - Project
     - Posted
     - Due
     - Duration
   * - GP1: ROS 2 Pub/Sub with Gazebo
     - Week 11
     - Week 13
     - 2 weeks
   * - GP2: Services, Actions, and Robot Inheritance
     - Week 13
     - Week 14
     - 1 week
   * - GP3: Coordinate Frames and Lifecycle Nodes
     - Week 14
     - Week 15
     - 1 week

.. tip::

   Start assignments early. RWAs and GPs are cumulative — a strong
   foundation in each deliverable makes the next one easier.


Reading Material
----------------

The following topics are provided as pre-recorded videos on Canvas.
Students are expected to watch these outside of class by the recommended
deadline:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30
   :class: compact-table

   * - Topic
     - Description
     - When to Watch
   * - Version Control (Git and GitHub)
     - Distributed version control, branching, merging, pull requests, and the fork workflow.
     - **Before the semester starts**
   * - Flow Control and Operations
     - Conditionals, loops, and operators.
     - **Before Week 3** (before RWA1 is posted)
   * - Exception Handling
     - Exception handling with ``try``, ``catch``, ``throw``, standard and custom exception classes, and RAII.
     - **Before Week 7** (before Smart Pointers)
