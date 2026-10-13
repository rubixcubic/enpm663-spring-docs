====================================================
Final Project
====================================================

Overview
--------

The final project is the capstone of ENPM663. Your team builds an
**agentic system for the ARIAC 2025 factory**: an LLM agent, grounded by a
vision-language model, that decides what the robots do next while a
behavior tree and classical robot skills carry it out. Working in teams of 3
students, you build it through four cumulative group projects. For the final
demo, the instructor runs your system's Docker image on an ARIAC trial your
team has never seen.

The project spans **14 weeks**, from GP1 in Week 2 to the final demo in
Week 15. Each group project builds on the previous one.

.. note::

   All four group projects and the final demo are on this site. Each one
   opens for work in the week the syllabus gives: GP1 in Week 2, GP2 in
   Week 5, GP3 in Week 7, GP4 in Week 10 and the final demo in Week 12. See
   the :doc:`syllabus </syllabus/index>` for the full schedule and weights.


Project Weight
--------------

The final project accounts for **60% of your overall course grade**:

.. list-table::
   :header-rows: 1
   :widths: 40 15 20 25
   :class: compact-table

   * - Component
     - % of course grade
     - Duration
     - Lectures
   * - :doc:`GP1: Behavior Tree for One Kit <gp1>`
     - 10%
     - Week 2 to Week 5
     - L1 to L4
   * - :doc:`GP2: Cell Inspection <gp2>`
     - 10%
     - Week 5 to Week 7
     - L5
   * - :doc:`GP3: PDDL Planner and BT Executor <gp3>`
     - 10%
     - Week 7 to Week 10
     - L6 and L7
   * - :doc:`GP4: LLM Agent with VLM Grounding <gp4>`
     - 10%
     - Week 10 to Week 13
     - L8 and L9
   * - :doc:`Final demo <final_demo>`
     - 20%
     - Week 12 to Week 15
     - L10 to L13


Pipeline Progression
--------------------

Each group project extends your team's system from the previous one:

.. code-block:: text

   GP1: Behavior tree      ->  One kit built and shipped by a py_trees_ros tree
       |
   GP2: Inspection         ->  Lidar, defect detection, inspection reports
       |
   GP3: PDDL + executor    ->  Plans for Task 1, run by a plan-to-BT executor
       |
   GP4: LLM agent + VLM    ->  An agent in place of the planner, handling the
       |                       ARIAC challenges
   Final demo              ->  Task 1 and Task 2 on an unseen trial

.. important::

   After GP1, every project builds on your previous submission. You extend
   the system your team builds in GP1, not replace it.


The Course Skills Package
-------------------------

ARIAC 2025 gives each robot a joint trajectory action and a gripper action,
but no pick or place skills. The course provides them: a Python ROS 2
package, built on MoveIt 2, with skills such as picking a cell and placing
it. Its page is :doc:`Course Skills Package </ariac/skills>`. Your team moves the AGVs with ARIAC's own AGV
move action.

- In GP1 to GP3, your behavior tree calls the skills.
- In GP4, your LLM agent calls the same skills as tools.
- L10 opens the package and shows how each skill becomes a trajectory.


Learning Objectives
-------------------

By completing the final project, you will be able to:

- Build behavior trees in ``py_trees_ros`` that run robot skills and recover
  from failures.
- Detect defects on battery cells from lidar point clouds and report
  inspection results through ROS 2.
- Write a PDDL domain for a factory task and execute its plans through a
  behavior tree.
- Build an LLM agent that calls robot skills as tools and returns structured
  output checked against a JSON schema.
- Ground the agent's decisions in VLM descriptions of the camera images.
- Use a hosted embodied-reasoning model to judge cell defects from camera
  images, and measure it against your lidar detector.
- Evaluate an agentic system with the ARIAC scoring formula and your own
  metrics.
- Package a ROS 2 solution in a Dockerfile.


Team Formation
--------------

**Timeline**: Form teams in **Week 2**.

**Team Size**: 3 students per team.

**Process**:

1. Form a team with complementary skills (ROS 2 and behavior trees,
   perception, planning and LLMs, integration).
2. Submit the team roster on Canvas.
3. Post your team charter on ELMS before L3 (see the
   :doc:`syllabus </syllabus/index>`).
4. Set up one shared Git repository for the whole project.

.. tip::

   Agree on a recurring weekly team meeting in Week 2, before GP1 starts
   taking time.


.. _final-demo:

Final Demo (Weeks 12 to 15)
---------------------------

**Weight:** 20% of the course grade.

The final demo specification is posted in **Week 12** and the demo is in
**Week 15** (May 5). Your team integrates GP1 to GP4 into one system that
runs a full ARIAC 2025 trial, Task 1 (inspection and kit building) and
Task 2 (module construction), and handles the ARIAC challenges:

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - Challenge
     - What happens (ARIAC 2025 documentation)
   * - Conveyor malfunction
     - The inspection conveyor stops operating.
   * - Voltage tester malfunction
     - One or both voltage testers stop providing data. (In the ARIAC 2025
       code, a tester keeps publishing a voltage of -1 with the status
       MALFUNCTIONING.)
   * - Vacuum tool malfunction
     - The vacuum gripper fails to grasp objects.
   * - High-priority order
     - An urgent kit request arrives with a time constraint.

**Final Deliverables:**

1. **Integrated system:** GP1 to GP4 running end to end from a Dockerfile.
2. **Physical AI step:** a hosted embodied-reasoning model judges cell
   defects from camera images over the inspection conveyor, scored with
   precision and recall on the same cells as your GP2 lidar detector.
3. **Evaluation run:** before the Week 15 class, the instructor runs your
   Docker image, built from your code-freeze tag, on a trial no team has
   seen, on the same machine as every other team, and the run is scored.
4. **Presentation (5 to 6 minutes):** architecture, design decisions, failure
   modes you met and how you handled them.
5. **Peer evaluation:** individual contribution assessment.

The run rules, the tasks and the rubric are on the :doc:`final demo page
<final_demo>`.


Academic Integrity
------------------

.. warning::

   **AI Usage Policy**

   AI tools are **required** in GP4 and the final demo, because the system
   you build calls an LLM and a VLM. On every project you may also use AI
   tools to clarify concepts or look up syntax.

   **Not permitted**:

   - Submitting AI-generated code that your team cannot explain
   - Using AI tools during quizzes
   - Sharing code between teams

   Any team member may be asked to explain any part of the submission.
   Violations are treated as academic dishonesty.

**Peer Reviews**: Required after every group project and after the final
demo. They make up the 15% peer-review contribution; the form and how the
score is computed are in :ref:`peer-evaluation`.


Support Resources
-----------------

- **Instructor office hours**: By appointment (email zeidk@umd.edu)
- **ARIAC documentation**: https://pages.nist.gov/ARIAC_docs/en/latest/
- **ROS 2 documentation**: https://docs.ros.org/en/jazzy/
- **MoveIt 2 documentation**: https://moveit.picknik.ai/main/
- **Canvas discussions**: For clarification and troubleshooting


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   gp1
   gp2
   gp3
   gp4
   final_demo
