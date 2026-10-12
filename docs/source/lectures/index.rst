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

The lectures open here one at a time, as their slides are finished; the
table shows the plan. Dates are in the :ref:`course schedule
<course-schedule>`.

.. list-table::
   :widths: 8 40 52
   :header-rows: 1
   :class: compact-table

   * - Lecture
     - Topic
     - Key Concepts
   * - L1
     - Course Overview and ROS 2 Refresher
     - Physical AI and agents, the ARIAC 2025 EV battery factory and what
       its score rewards, QoS, executors, actions, TF2, diagnostic quiz
   * - L2
     - System Architectures for AI-Augmented Robotics
     - Reactive, behavior-based and three-layer architectures; where an LLM
       agent and a VLM plug in; the course skills package; end-to-end VLA
       models; multi-robot coordination
   * - L3
     - Knowledge Representation for AI-Augmented Robotics
     - Frames, ontologies; a world model per layer and errors that move up
       (from 4D/RCS); one model for PDDL, an LLM and a VLM
   * - L4
     - Behavior Trees for Task Execution
     - Sequence, selector, parallel, decorators; ticks and status;
       blackboards; ``py_trees_ros``
   * - L5
     - Sensing and Perception for Robotic Systems
     - Sensor choice and budget, lidar point clouds and defect detection,
       TF2 in a perception pipeline, inspection reports, precision and recall
   * - L6
     - Task-Level Planning with PDDL
     - Domains and problems, Fast Downward and the Unified Planning
       Framework, plan validity, where PDDL strains (numbers)
   * - L7
     - Plan Execution Patterns with Behavior Trees
     - Plan-to-BT factory, retry and timeout, replanning triggers,
       ``BehaviorTree.CPP``
   * - L8
     - LLM Agents I: Agent Loops, Tool Use, and Structured Output
     - The orchestrator loop, plan-and-execute and ReAct, JSON schemas and
       validation, tool calling, MCP, context and cost
   * - L9
     - LLM Agents II: VLM Grounding and Agentic Replanning
     - VLM scene descriptions, embodied-reasoning models, closed-loop
       replanning, when PDDL is the better tool
   * - L10
     - Frames, Transforms, and Motion Planning
     - TF2 in depth, the pinhole camera model, MoveIt 2, sampling-based
       planners, parameterized grasps, inside the course skills package
   * - L11
     - Recovery, Robustness, and Failure Handling for AI-Driven Systems
     - Failure taxonomy, BT recovery structures, LLM and VLM output checks,
       the ARIAC 2025 challenges
   * - L12
     - Evaluation and Measurement Science for AI-Augmented Systems
     - Plan, perception and execution metrics; controlled comparisons;
       the ARIAC 2025 scoring formula
   * - L13
     - The Physical AI Frontier: VLAs, Robot Foundation Models, and World
       Models
     - VLA models, two-system designs, world models and simulation, cost of
       learned policies, agentic manufacturing in industry

.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

..
   Hidden until each deck is finished (see HIDDEN_LECTURES in conf.py).
   To open a lecture, move its line into the toctree above.
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
