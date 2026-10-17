====================================================
L1: Course Overview and ROS 2 Refresher
====================================================

Overview
--------

This lecture opens ENPM663. It starts with an ungraded **diagnostic quiz** on
your ROS 2 background, then walks through how the course runs: four group
projects and a final demo, five quizzes and a peer review. The full rules are
in the :doc:`syllabus </syllabus/index>`.

The first content block defines the words in the course title. **Physical
AI**, in NVIDIA's words, lets robots and other autonomous systems "perceive,
understand, reason, and perform or orchestrate complex actions in the physical
world." An **agent** is a program that runs a loop around a large language
model (LLM): it observes the world, asks the model what to do, calls a tool,
checks the result and repeats. In this course the agent decides what a factory
cell does next, and classical robot skills carry out each decision. The
course's title term, **agentic physical AI**, means a robot system in which an
AI agent decides what the robots do next, and robot skills carry out each
decision in the physical world: here, the ARIAC factory, simulated in Gazebo.

The second block introduces the testbed you use all semester: **ARIAC 2025**,
NIST's simulated EV battery factory. You see its two tasks (inspection and kit
building, then module construction), its robots, the sensors your team buys
from a budget, the four challenges and what a run's score rewards. A worked
example computes the **kit voltage window**: the range a kit's total voltage
must fall in.

The last block traces one battery cell through the ARIAC ROS 2 interfaces, then
refreshes the four ROS 2 topics the course uses most: **QoS profiles**,
**executors**, **actions** and **TF2**. Each one comes with a short script and
its measured output.

.. important::

   **ARIAC tie-in.** Every step of Task 1 is a ROS 2 topic, service or action.
   A cell rides the inspection conveyor, your node submits its inspection
   report before the inspection door, a robot places it in a voltage tester,
   another robot places it on an AGV tray, and the AGV takes the kit to
   shipping. The refresher topics are what make those interfaces work.

.. important::

   **Group project.** GP1, a behavior tree that builds one kit, is posted in
   L2. It needs a working ARIAC install, so install it this week.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the course structure: GP1 to GP4, the final demo, the grading
  weights, the quizzes and the AI policy.
- Explain what agentic physical AI means in this course, and which layer of a
  robot system it puts AI in.
- Describe the ARIAC 2025 factory: its two tasks, its robots, sensors and
  challenges, and what a run's score rewards.
- Compute a kit voltage window from a cell type's nominal voltage and the kit
  tolerance.
- Explain, from measured demonstrations, how QoS, executors, actions and TF2
  affect a node that works with ARIAC.
- Identify gaps in your own ROS 2 background with the diagnostic quiz.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l1_lecture
   l1_code
   l1_exercises
   l1_quiz
   l1_references


Next Steps
----------

- In the next lecture we cover **L2: System Architectures for Agentic
  Robotics**:

  - Classical robot architectures and the three-layer architecture.
  - Where an LLM agent and a VLM plug into a robot stack.
  - Teams form, and GP1 is posted.

- **Before next class:**

  - Install Ubuntu 24.04, ROS 2 Jazzy and ARIAC 2025 with the
    :doc:`ARIAC Testbed </ariac/ariac>` pages, and run the example trial.
  - Run the four L1 scripts (see :doc:`l1_code`) and compare your outputs
    with the ones in the notes.
  - Work through the :doc:`L1 exercises <l1_exercises>` and the
    :doc:`self-check quiz <l1_quiz>`.
  - Find two teammates. Teams form in L2.
