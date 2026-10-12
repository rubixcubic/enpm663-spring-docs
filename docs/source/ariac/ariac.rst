=====================================
ARIAC Testbed
=====================================

ARIAC (Agile Robotics for Industrial Automation Competition) is a NIST
competition and simulator for factory robotics. This course uses **ARIAC
2025**: a simulated EV battery factory with two inspection robots, two
assembly robots, a gantry welder and three AGVs. Teams inspect battery cells,
build kits of four cells, and assemble and weld battery modules.

.. note::
   **Installation Options**

   NIST recommends running ARIAC in **Docker**, where every dependency is
   already in the image. A **native** install is also possible and requires
   Ubuntu 24.04. Both are described in the
   :doc:`ARIAC and robotics tools <ariac_setup>` page. The final ARIAC
   evaluation requires a Dockerfile for your solution, so plan to use Docker
   by the final demo either way.

.. important::
   **Why ARIAC?**

   - **A real factory problem:** inspection, kitting, assembly and welding,
     with malfunctions and urgent orders that a fixed script cannot handle.
   - **Scored runs:** every trial produces a score, so you can compare a
     PDDL planner with an LLM agent on the same trial.
   - **Unseen trials:** a trial is a configuration file, so the final demo
     can run a trial your team has never seen.
   - **ROS 2 throughout:** every robot, sensor and conveyor is a ROS 2
     topic, service or action.

.. toctree::
   :hidden:
   :caption: Operating System

   Ubuntu 24.04 <ubuntu_setup>

.. toctree::
   :hidden:
   :caption: Middleware and Simulator

   ROS 2 Jazzy and Gazebo <ros_setup>

.. toctree::
   :hidden:
   :caption: ARIAC and Tools

   ARIAC and Robotics Tools <ariac_setup>

.. toctree::
   :hidden:
   :caption: AI Access

   LLMs and VLMs <ai_setup>

Course Configuration
--------------------

.. list-table::
   :widths: 40 60
   :class: compact-table

   * - **Course**
     - ENPM663: Agentic Physical AI for Manufacturing Robotics
   * - **Ubuntu Version**
     - :bdg-success:`24.04` (Noble Numbat)
   * - **ROS 2**
     - :bdg-primary:`Jazzy` Jalisco
   * - **Simulator**
     - Gazebo Harmonic
   * - **ARIAC Version**
     - :bdg-warning:`2025`
   * - **Installation Method**
     - Docker (recommended by NIST) or native

Setup Order
-----------

1. :doc:`Ubuntu 24.04 <ubuntu_setup>`: dual boot is recommended. NIST
   notes that running ARIAC without a dedicated GPU gives worse
   performance.
2. :doc:`ROS 2 Jazzy and Gazebo Harmonic <ros_setup>`: needed from L1.
3. :doc:`ARIAC and robotics tools <ariac_setup>`: ARIAC 2025, MoveIt 2,
   ``py_trees_ros``, OpenCV and a PDDL planner. Needed from GP1.
4. :doc:`LLMs and VLMs <ai_setup>`: a hosted API or local models. Needed
   from L8 and GP4.
