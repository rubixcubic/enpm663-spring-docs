====================================================
Lectures
====================================================

Overview
--------

The lectures in ENPM663 follow the layers of an agentic robot system. They
start with the course, the ARIAC 2025 factory and a ROS 2 refresher, then
build up the classical stack (architectures, knowledge representation,
behavior trees, perception, PDDL planning), replace the planner with an LLM
agent grounded by a VLM, and finish with motion, recovery, evaluation and the
physical AI frontier. Lectures are exposition: there are no in-class
exercises. Lecture materials are available on Canvas and on this site.

.. tip::

   Each group project builds on the previous one, and the final demo
   integrates all four. Read a lecture's page again when you start the
   group project that uses it.


Schedule
--------

Each lecture's page holds its notes, its code, take-home exercises and a
self-check quiz. Dates are in the :ref:`course schedule <course-schedule>`.

.. list-table::
   :widths: 8 40 52
   :header-rows: 1
   :class: compact-table

   * - Lecture
     - Topic
     - Key Concepts
   * - :doc:`L1 <lecture1/l1_index>`
     - Course Overview and ROS 2 Refresher
     - Physical AI and agents, the ARIAC 2025 EV battery factory and what
       its score rewards, QoS, executors, actions, TF2, diagnostic quiz
   * - :doc:`L2 <lecture2/l2_index>`
     - System Architectures for Agentic Robotics
     - Reactive, behavior-based and three-layer architectures; where an LLM
       agent and a VLM plug in; the course skills package; end-to-end VLA
       models; multi-robot coordination
   * - :doc:`L3 <lecture3/l3_index>`
     - Knowledge Representation for Agentic Robotics
     - Frames, ontologies; a world model per layer and status that moves up
       (from 4D/RCS); one kit state in three views for a PDDL planner, an LLM agent and an executor
   * - :doc:`L4 <lecture4/l4_index>`
     - Behavior Trees for Task Execution
     - Sequence, selector, parallel, decorators; ticks and status;
       blackboards; ``py_trees_ros``
   * - :doc:`L5 <lecture5/l5_index>`
     - Sensing and Perception for Robotic Systems
     - Sensor choice and budget, lidar point clouds and defect detection,
       TF2 in a perception pipeline, inspection reports, precision and recall
   * - :doc:`L6 <lecture6/l6_index>`
     - Task-Level Planning with PDDL
     - Domains and problems, Fast Downward through the Unified Planning
       Framework, plan validity, where PDDL strains (numbers)
   * - :doc:`L7 <lecture7/l7_index>`
     - Plan Execution Patterns with Behavior Trees
     - Plan-to-BT factory, retry and timeout, replanning triggers,
       ``BehaviorTree.CPP``
   * - :doc:`L8 <lecture8/l8_index>`
     - LLM Agents I: Agent Loops, Tool Use, and Structured Output
     - The orchestrator loop, plan-and-execute and ReAct, JSON schemas and
       validation, tool calling, MCP, context and cost
   * - :doc:`L9 <lecture9/l9_index>`
     - LLM Agents II: VLM Grounding and Agentic Replanning
     - VLM scene descriptions, embodied-reasoning models, closed-loop
       replanning, when PDDL is the better tool
   * - :doc:`L10 <lecture10/l10_index>`
     - Frames, Transforms, and Motion Planning
     - TF2 in depth, the pinhole camera model, MoveIt 2, sampling-based
       planners, parameterized grasps, inside the course skills package
   * - :doc:`L11 <lecture11/l11_index>`
     - Recovery, Robustness, and Failure Handling for Agentic Systems
     - Failure taxonomy, BT recovery structures, LLM and VLM output checks,
       the ARIAC 2025 challenges
   * - :doc:`L12 <lecture12/l12_index>`
     - Evaluation and Measurement Science for Agentic Systems
     - Plan, perception and execution metrics; controlled comparisons;
       the ARIAC 2025 scoring formula
   * - :doc:`L13 <lecture13/l13_index>`
     - The Physical AI Frontier: VLAs, Robot Foundation Models, and World
       Models
     - VLA models, two-system designs, world models and simulation, cost of
       learned policies, agentic manufacturing in industry

.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   lecture1/l1_index
   lecture2/l2_index
   lecture3/l3_index
   lecture4/l4_index
   lecture5/l5_index
   lecture6/l6_index
   lecture7/l7_index
   lecture8/l8_index
   lecture9/l9_index
   lecture10/l10_index
   lecture11/l11_index
   lecture12/l12_index
   lecture13/l13_index
