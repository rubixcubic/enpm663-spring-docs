====================================================
Lecture
====================================================

.. note::

   These notes follow the L1 slides shown in class, in the same order and
   with the same sections, so you can read them at home. The program outputs
   below come from the four L1 scripts, run on ROS 2 Jazzy. The scripts and
   how to run them are on the :doc:`code page <l1_code>`.


.. _l1-course-introduction:

Course Introduction
-------------------

Course Focus
~~~~~~~~~~~~

This course is about robot systems in which an **AI agent decides what a
factory cell does next**. Behavior trees, planners and motion planning carry
out each decision. You work in one testbed all
semester, the ARIAC 2025 EV battery factory from NIST, and your team builds
four group projects and a final demo on a trial no team has seen.

The rules of the course (grading, quizzes, late work, teams, peer review and
AI tools) are in the :doc:`syllabus </syllabus/index>`. This section only
lists what the first class covers, with links to the full text.


The Diagnostic Quiz
~~~~~~~~~~~~~~~~~~~

The first 20 minutes of L1 are an **ungraded** diagnostic quiz, closed notes,
on ELMS-Canvas or on paper. It covers the prerequisites in the syllabus:

- packages and workspaces;
- publishers, subscribers, services, action clients and servers in Python;
- launch files, parameters and the ``ros2`` command-line tools;
- reading C++ ROS 2 code;
- Git and GitHub: branches, merge conflicts and pull requests.

If you miss questions on a topic, read the ROS 2 Refresher in the
:doc:`Pre-Read </preread/index>` again and talk to the instructor this week.


Disclaimer
~~~~~~~~~~

.. admonition:: Disclaimer
   :class: warning

   The instructor teaches this course solely in his capacity as a lecturer at
   the University of Maryland.

   - He does **not** represent NIST in this course.
   - Opinions, findings, and recommendations expressed here are his own and
     do not necessarily reflect the views of NIST or the U.S. Department of
     Commerce.
   - Nothing stated in this course should be interpreted as an official NIST
     position, policy, or endorsement.
   - Course content, assignments, and grading are governed by UMD policy only.


The Instructor and His Research
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zeid Kootbally (zeidk@umd.edu, office hours by appointment) is a researcher
at the NIST Engineering Laboratory. Format email subjects as
``ENPM663 (Section): [Topic]``.

His research is on **robot agility**:

- How well can a robot adapt to task failures?
- How fast can a robot re-plan when it gets a new goal?
- How can robots be swapped without reprogramming them?
- How well can a robot respond to changing conditions around it?

The target audience is small and medium-sized manufacturers. They make many
kinds of products in small batches (high mix, low volume), so they need robots
that are easier to task and retask and that recover better from execution
failures. The outcomes include the
`IEEE P2940 standard <https://standards.ieee.org/ieee/2940/10411/>`_ (Standard
for Measuring Robot Agility), a validated framework (a digital twin), and
`ARIAC <https://pages.nist.gov/ARIAC_docs/en/latest/index.html>`_, the
testbed of this course.


How the Course Runs
~~~~~~~~~~~~~~~~~~~

- **Format.** One lecture a week, Wednesdays 7:00 to 9:40 pm, Jan 27 to May 5,
  2027, with no class on 03/17 (spring break). Section 0101 meets in person and
  section RO01 online. Lectures are exposition with demonstrations: there are
  **no in-class exercises and no labs**. All hands-on work happens in the
  group projects, outside class.
- **Workload.** Expect about 4 hours a week on group project work early on,
  and 6 to 8 hours a week per student for the later projects.
- **Grades.** Final project 60% (GP1 to GP4 at 10% each, final demo at 20%),
  five quizzes 25%, peer-review contribution 15%. There is no final exam.
  See :doc:`the syllabus </syllabus/index>`.
- **Quizzes.** Five quizzes at the start of class, 20 minutes each, closed
  notes, no AI. Quiz 1 is in Week 4 and covers L1 to L3. No quiz is dropped.
- **Late work.** 10% of the project grade per calendar day, up to 3 days.
  Work more than 3 days late earns zero.

.. list-table:: The final project: four group projects and a final demo
   :header-rows: 1
   :widths: 14 46 13 13 14
   :class: compact-table

   * - **Part**
     - **What your team builds**
     - **Posted**
     - **Due**
     - **Weight**
   * - GP1
     - Behavior tree that builds one kit
     - Week 2
     - Week 5
     - 10%
   * - GP2
     - Cell inspection from lidar point clouds
     - Week 5
     - Week 7
     - 10%
   * - GP3
     - PDDL planner and behavior-tree executor
     - Week 7
     - Week 10
     - 10%
   * - GP4
     - LLM agent with VLM grounding
     - Week 10
     - Week 13
     - 10%
   * - Final demo
     - Task 1 and Task 2 on an unseen trial
     - Week 12
     - Week 15
     - 20%

Each project extends the previous one: after GP1, your team builds on its own
earlier submission. GP1 comes with a starter tree. Weeks 2 and 3 go to setup,
and the tree work follows L4.

**How the final demo is graded.** Your team tags its code before the code
freeze, and the instructor runs every team's Docker image on the same unseen
ARIAC trial, on one machine, before the Week 15 class, so every run has the
same hardware. In class, each team presents its recorded run for 5 to 6 minutes.

**Teams and peer review.** Teams of three form in Week 2, when GP1 is posted,
and post a one-page team charter on ELMS before L3. After each project you rate
each teammate (see :ref:`peer-evaluation`).

**AI policy.** AI tools are **required** in GP4 and the final demo, because
the system your team builds calls an LLM and a VLM. You may not submit
AI-generated code your team cannot explain, and you may not use AI tools or
notes during a quiz. See :ref:`ai-disclosure`.

The week-by-week schedule is in the :ref:`course-schedule`.

**Software.** Ubuntu 24.04 LTS (native or a virtual machine), ROS 2 Jazzy
Jalisco, Gazebo Harmonic, ARIAC 2025 (Docker or native), MoveIt 2,
``py_trees_ros`` and a PDDL planner, and Visual Studio Code. From GP4 on, your
team uses its own free-tier Gemini API key while it develops; the course
Gemini key runs only the graded GP4 and final demo evaluations. The
:doc:`ARIAC Testbed </ariac/ariac>` pages give the install steps. GP1
needs a working install by Week 2.


.. _l1-physical-ai:

Physical AI and Agents
----------------------

This section answers three questions: what the words in the course title
mean, which part of a robot system this course builds with AI, and what it
leaves to classical robotics, and why.

Two Definitions
~~~~~~~~~~~~~~~

.. admonition:: Definition: physical AI
   :class: note

   "Physical AI lets autonomous systems like cameras, robots, and
   self-driving cars perceive, understand, reason, and perform or orchestrate
   complex actions in the physical world."
   (`NVIDIA glossary <https://www.nvidia.com/en-us/glossary/generative-physical-ai/>`_)

.. admonition:: Definition: agent
   :class: note

   An **agent** is a program that runs a loop around a large language model
   (LLM):

   1. it observes the state of the world;
   2. it asks the model what to do;
   3. it calls a **tool** (in this course, a robot skill);
   4. it checks the result, and repeats.

This course works on the "orchestrate" part of the NVIDIA definition. L8
and L9 cover agents in depth.

.. _l1-agentic-physical-ai:

Agentic Physical AI: What It Means in This Course
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: agentic physical AI
   :class: note

   The course's title term, **agentic physical AI**, means a robot system in
   which an AI agent decides what the robots do next, and robot skills carry
   out each decision in the physical world: here, the ARIAC factory,
   simulated in Gazebo.

**The three words.**

1. **Agentic:** the agent runs the loop from the agent definition above
   (observe, ask the model, call a skill, check the result, repeat). It picks
   each next step from what it observes.
2. **Physical:** each decision runs a robot skill. A wrong decision can make
   a robot drop a cell on the floor or hit a tray, and the ARIAC score charges
   a penalty for each.
3. **AI:** learned models make the decisions (the LLM agent, from GP4 on),
   describe what the cameras see (a vision-language model, or VLM, in GP4),
   and judge cell defects in one perception step (in the final demo, a hosted
   **embodied-reasoning model**: a VLM trained to answer spatial questions
   about a scene).


What Your Team Builds, Part by Part
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 82
   :class: compact-table

   * - **Part**
     - **What it is in this course**
   * - Perception
     - Sensors your team places: lidar point clouds for cell defects (GP2);
       cameras later, for the VLM in GP4 and the top shell in the final demo.
   * - Decision
     - A behavior tree (GP1), then a PDDL planner (GP3), then an LLM agent
       grounded by a vision-language model, or VLM (GP4).
   * - Motion
     - The **course skills package**: Python ROS 2 actions built on MoveIt 2,
       given to your team with GP1.

ARIAC gives its robots low-level controls only (listed in
:ref:`l1-robot-interfaces`): joint motion, and a gripper, vacuum tools or a
weld service. None of them picks or places a cell, so the course gives your
team the skills package, and you never write motion code.


What the Course Does Not Do, and Why
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Out of scope.** No policy training and no reinforcement learning, so the
course needs no GPU. Motion planning and grasping stay classical (MoveIt 2).

**Where learned models appear.** L13 surveys vision-language-action
models, robot foundation models and world models. In the final demo, a hosted
embodied-reasoning model judges cell defects from camera images, and your
team compares it with its GP2 lidar detector.

**Why keep AI at the decision layer.** An agent's decisions leave a trace a
person can read and grade: each tool call and its arguments. A learned motion
policy leaves no such trace of tool calls, and this course grades your system
on trials it has never seen.


.. _l1-ariac:

The ARIAC 2025 Factory
----------------------

**ARIAC** is the Agile Robotics for Industrial Automation Competition, run by
NIST. The 2025 edition simulates an EV battery factory in Gazebo. Every group
project and the final demo run in it.

.. figure:: /_static/images/l1/ariac_environment.png
   :alt: An elevated view of the ARIAC 2025 factory floor in Gazebo. In the foreground, an inspection conveyor, two robot arms, voltage testers, bins and three AGVs; in the back, a second area with two robot arms and a conveyor. Colored lines on the floor mark the AGV paths.
   :width: 90%
   :align: center

   The ARIAC 2025 factory. Credit: NIST,
   `ARIAC 2025 documentation <https://pages.nist.gov/ARIAC_docs/en/latest/index.html>`__.


Cells, Kits and Modules
~~~~~~~~~~~~~~~~~~~~~~~

The factory uses two **cell** types, defined in ``CellTypes.msg``:

- **Li-Ion**, nominal 3.6 V;
- **Ni-MH**, nominal 1.2 V.

The **nominal voltage** is the voltage a cell of that type is meant to have.
The factory makes two products:

- a **kit**: four cells on an AGV tray (Task 1);
- a **module**: four cells inside a bottom and a top shell, joined by six
  welds, four on top and two on the bottom (Task 2).

.. figure:: /_static/images/l1/ariac_module.png
   :alt: A finished ARIAC battery module: four blue cylindrical cells held between a bottom shell and a top shell, each shell marked with the NIST logo.
   :width: 45%
   :align: center

   A finished module. Credit: NIST,
   `ARIAC 2025 documentation <https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html>`__.


Task 1: Inspection and Kit Building
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l1/ariac_task1_environment.png
   :alt: The ARIAC Task 1 area with labels: the inspection conveyor and inspection door on the right, inspection robot 1 and the voltage testers in the middle, inspection bins 1 and 2 and the recycling bin, inspection robot 2 on the left, and three AGVs, AGV 1 to AGV 3, each with a kit tray.
   :width: 90%
   :align: center

   The Task 1 area. Credit: NIST,
   `ARIAC 2025 documentation <https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html>`__.
   Inspection Bin 1, beside the inspection door, is the **inspection bin**;
   Inspection Bin 2, at the end of the conveyor, is the **inspection conveyor
   bin**. These are their names in the ARIAC world file.

Task 1 has five steps, 1a to 1e.

**1a. Physical inspection.** The inspection conveyor carries the cells. Your team must
use **lidar point clouds** to rebuild each cell's shape and find defects: a
dent, a scratch or a bulge. On ARIAC's training cells these are 0.84 to
2.49 mm off the normal surface (L5 measures them). Your
team submits an **inspection report** for each cell: passed or not, with an
optional defect type and location.

.. admonition:: The inspection door
   :class: warning

   The inspection door lets a cell through only if your team submitted a
   passing report for it. A failing or missing report keeps the door closed,
   and the cell drops into the inspection bin. So from GP1 on, your system
   submits a report for every cell.

**1b. Conveyor pickup.** Inspection robot 1 (a UR3e with a Robotiq 2F-85
gripper) picks the cell off the moving conveyor and places it in one of two
voltage testers.

**1c. Voltage inspection.** The tester publishes noisy voltage readings, so
your team averages readings over a short window.

**1d. AGV placement.** Inspection robot 2 (a UR5e with a 2F-85) moves the
cell. A cell outside its nominal voltage plus or minus 0.2 V goes to the
recycling bin; a good cell goes on an AGV tray. The kit total must be within
4 × nominal plus or minus 0.15 V. Cells lock to the tray once placed. Your
team calls the check kit quality service before moving the AGV.

**1e. Move the AGV.** The AGV goes to the shipping station, and your team
calls the submit kit service.


.. _l1-kit-window:

Worked Example: The Kit Voltage Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **kit voltage window** is the range the total voltage of a kit's four
cells must fall in. Here it is for a Li-Ion kit, in numbered steps.

1. Four cells at 3.6 V nominal give a target total of 4 × 3.6 = 14.4 V.
2. The kit tolerance is plus or minus 0.15 V, so the total must fall between
   14.4 − 0.15 = 14.25 V and 14.4 + 0.15 = 14.55 V.
3. Each cell on its own may be anywhere from 3.4 V to 3.8 V (3.6 V plus or
   minus 0.2 V).
4. If all four cells were at 3.8 V, they would total 4 × 3.8 = 15.2 V, which
   is 0.8 V above 14.4 V and far outside the window.

.. important::

   Your system must choose which cells go together. Cells lock to the tray
   once placed, so it must choose before it places.

For Ni-MH, the same steps give 4 × 1.2 = 4.8 V, with a window of 4.65 V to
4.95 V.


Task 2: Module Construction (Final Demo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l1/ariac_task2_environment.png
   :alt: The ARIAC Task 2 area with labels: assembly robot 1 on the left, the assembly table with a tool stand holding the VG-2 and VG-4 vacuum tools, assembly robot 2, the assembly conveyor in three sections, the gantry welder and the module submission station.
   :width: 90%
   :align: center

   The Task 2 area. Credit: NIST,
   `ARIAC 2025 documentation <https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html>`__.

Task 2 appears only in the final demo. Its steps:

1. Assembly robot 1 places four cells in a bottom shell.
2. Assembly robot 2 changes to a vacuum tool and places the top shell. The top
   shell spawns at a random pose, so your team must find it with a sensor.
3. The gantry welder makes four top welds.
4. Assembly robot 2 flips the module.
5. The welder makes two bottom welds.


.. _l1-robot-interfaces:

What ARIAC Gives Each Robot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 32 44
   :class: compact-table

   * - **Robot**
     - **Motion**
     - **Grasping or tool**
   * - Inspection robots 1 and 2
     - A joint trajectory action
     - A gripper action (Robotiq 2F-85)
   * - Assembly robot 1
     - A joint trajectory action
     - A gripper action (Robotiq 2F-85)
   * - Assembly robot 2
     - A joint trajectory action
     - No gripper. Services to attach and detach a vacuum tool
       (``attach_tool``, ``detach_tool``), and the tool's ``grasp`` and
       ``release`` services
   * - Gantry welder
     - A joint trajectory action (three slide joints)
     - No gripper. A ``weld`` service

The table comes from each robot's controller file in
``ariac_description/config`` and from the tool changer, vacuum tool and
welder plugins in ``ariac_plugins``.

A joint trajectory action moves the joints through a list of joint positions
that you send. It does not plan a path to a cell or pick the cell up.


Sensors Your Team Buys
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - **Sensor**
     - **Cost by grade**
   * - Break beam
     - $400 (30 Hz), $200 (10 Hz)
   * - Distance
     - $600 (30 Hz), $300 (10 Hz)
   * - RGB camera
     - $800 (1080p), $500 (720p)
   * - Lidar
     - $1500 (20 Hz); otherwise $1250 (200 samples or more), $1000 (fewer)

- Your team places its sensors in its configuration file.
- Lidar may only sit in three bounding boxes around the inspection conveyor.
- There are no depth cameras and no logical cameras in ARIAC 2025.

The ARIAC scoring file sets a **sensor budget** of $9600. A cost under it
earns a bonus; a cost over it, a penalty. Your team picks its sensors in GP2.


The Four Challenges
~~~~~~~~~~~~~~~~~~~

A **challenge** is an event ARIAC injects during a trial to test whether your
system adapts.

- **Conveyor malfunction**: the inspection conveyor stops for a set time.
- **Voltage tester malfunction**: one or both testers stop giving valid
  readings. In the ARIAC 2025 code a tester keeps publishing, with a voltage
  of −1 and the status ``MALFUNCTIONING``.
- **Vacuum tool malfunction**: a vacuum gripper fails a given grasp attempt
  (Task 2).
- **High-priority order**: an order ID arrives; your team switches the feed
  to Ni-MH, builds and ships a Ni-MH kit, and submits it with that ID.

A trial can contain any of them, at times your team does not know in advance,
so a fixed script cannot handle them.


How ARIAC Scores a Run
~~~~~~~~~~~~~~~~~~~~~~

- **Base score**: the share of the desired kits and modules your team
  submitted.
- **Bonuses**: for speed, for sensor cost under the budget and for correct
  defect classification. They are paid only if every desired kit and module
  was submitted.
- **Penalties**: for good cells in the inspection bin, cells in the inspection
  conveyor bin, objects on invalid surfaces, AGV collisions, robot collisions,
  and sensor cost over the budget.

.. important::

   L12 covers the scoring formula and its weights.


How a Competition Run Goes
~~~~~~~~~~~~~~~~~~~~~~~~~~

A run moves through five competition states:

``PREPARING`` → ``READY`` → ``STARTED`` → ``ORDERS_COMPLETE`` → ``ENDED``

1. At ``READY``, your system connects to the robots and sensors.
2. Your system calls the start competition service; the state becomes
   ``STARTED``.
3. Your system builds the kits and modules the trial asks for.
4. The state becomes ``ORDERS_COMPLETE`` when every order is done, but not
   while a high-priority order is still to be announced.
5. The run ends at the time limit, or when your system calls the end
   competition service.


.. _l1-tracing:

Tracing One Cell
----------------

Every step of Task 1 is a ROS 2 topic, service or action.

Three Kinds of Interface
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 14 44 42
   :class: compact-table

   * - **Kind**
     - **What it does**
     - **ARIAC example**
   * - Topic
     - Streams data; no reply
     - A voltage tester's readings
   * - Service
     - One short request and one reply
     - Starting the competition
   * - Action
     - A long goal with feedback and a result
     - Moving an AGV to a station

Moving an AGV is an action because it takes time and reports progress while it
runs. A client can ask an action server to cancel a goal, but the server
decides. ARIAC's AGV move server rejects cancel requests; the course skills
accept them.


The Path of One Li-Ion Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 8 42 50
   :class: compact-table

   * - **Step**
     - **What happens**
     - **Interface (kind)**
   * - 1
     - Wait for ``READY``, then start
     - | ``/competition_status`` (topic)
       | ``/start_competition`` (service)
   * - 2
     - Start feeding Li-Ion cells
     - ``/inspection_conveyor/cell_feed/control`` (service)
   * - 3
     - Submit the cell's inspection report before the door
     - ``/inspection_conveyor/inspection/submit`` (service)
   * - 4
     - A break beam your team placed sees the cell pass
     - the beam's change topic (topic)
   * - 5
     - Inspection robot 1 places the cell in a tester
     - a course skill (action)
   * - 6
     - Read and average the voltage
     - ``/voltage_tester_1/voltage`` (topic)
   * - 7
     - Inspection robot 2 places the cell on the tray
     - a course skill (action)
   * - 8
     - Check the kit, move the AGV, submit
     - | ``/agv1/check_kit_quality`` (service)
       | ``/agv1/move`` (action)
       | ``/submit_kitting_order`` (service)

In GP1 every report says the cell passed; from GP2 on, each report gives your
lidar inspection's result.


.. _l1-refresher:

ROS 2 Refresher
---------------

Four topics, each with a short script and its measured output:

- QoS profiles: why a subscriber can receive nothing.
- Executors and callback groups: why a node can miss updates.
- Actions: goal, feedback, cancel, result.
- TF2: where a tray slot is, seen from the AGV.

The scripts use stand-in messages and static transforms, not a running ARIAC
simulation. The full scripts are on the :doc:`code page <l1_code>`.


.. _l1-qos:

QoS: What a Profile Sets
~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: QoS profile
   :class: note

   A **Quality of Service (QoS) profile** sets how messages are delivered on
   a topic: **reliability** (reliable or best effort), **durability**,
   **history** and **depth**.

- A publisher and a subscriber connect only if their profiles are compatible.
- A best-effort publisher cannot serve a subscriber that asks for reliable
  delivery.

**The ARIAC case.** ARIAC's break beam publishes its change topic with
``SensorDataQoS``, which is best effort (``ray_sensor_plugin.cpp`` in the
ARIAC source). A subscriber created with only a queue depth (``10``) gets the
default profile, which is reliable.

The demonstration builds that case in one node. ``Bool`` stands in for ARIAC's
break beam message. The node publishes every 0.1 s for 2 s, so it sends
2 / 0.1 = 20 messages. ``--match`` on the command line gives the subscriber
the sensor data profile.

.. literalinclude:: code/qos_mismatch.py
   :language: python
   :lines: 19-31
   :caption: lecture1/code/qos_mismatch.py (excerpt)

**Run 1: subscriber with the default profile.**

.. literalinclude:: outputs/qos_default.txt
   :language: text

**Run 2: subscriber with the sensor data profile.**

.. literalinclude:: outputs/qos_match.txt
   :language: text

The 20th message arrives after the loop ends (Exercise 2 shows it).

.. important::

   Run 1 has no error: the node runs and receives nothing. Read the warning,
   and match the publisher's profile.


.. _l1-executors:

Executors: Who Runs the Callbacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: executor
   :class: note

   An **executor** runs a node's callbacks.

   - A **single-threaded** executor runs one callback at a time, so a slow
     callback delays every other one.
   - A **multi-threaded** executor can run callbacks at the same time, but
     only callbacks in different callback groups, or in one reentrant group.

.. admonition:: Definition: callback group
   :class: note

   A **callback group** sets which of a node's callbacks may run at the same
   time.

   - A **mutually exclusive** group runs one of its callbacks at a time.
   - A **reentrant** group lets its callbacks run at the same time.
   - A callback created without a group joins the node's default group, which
     is mutually exclusive.

In the demonstration, a slow timer (once a second) sleeps for 1 s, standing in
for waiting on a skill's result. A fast timer at 10 Hz stands in for reading a
status topic. With ``two_groups`` true, each timer gets its own mutually
exclusive group; with it false, both join the default group.

.. literalinclude:: code/executor_blocking.py
   :language: python
   :lines: 23-36
   :caption: lecture1/code/executor_blocking.py (excerpt)

Each run lasts 5 s. At 10 Hz, the status timer should fire 5 × 10 = 50 times.

**Single-threaded executor, one group.**

.. literalinclude:: outputs/executor_single.txt
   :language: text

Why 11: the status timer reads 9 times before the slow callback first runs,
at about 1.05 s. After that, the slow timer is due again each time it ends, so
the status timer gets only 2 more turns, at about 2.05 s and 4.05 s:
9 + 2 = 11 (timed in 3 runs).

**Multi-threaded executor, two groups.**

.. literalinclude:: outputs/executor_multi.txt
   :language: text

.. important::

   While a node waits on a skill, it can miss status updates: this is how a
   system misses the start of a conveyor or tester malfunction. The course
   skills package runs on a multi-threaded executor. Your behavior tree node
   must not block its own callbacks (L4 shows how ``py_trees_ros`` ticks the
   tree from a timer).


.. _l1-actions:

Actions: Goal, Feedback, Cancel, Result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An **action** runs a long task in four parts:

1. The client sends a **goal**; the server accepts or rejects it.
2. While it works, the server sends **feedback**.
3. The client may ask to **cancel**; the server decides whether to accept.
4. The goal ends with a **result** and a status: ``SUCCEEDED``, ``CANCELED``
   or ``ABORTED``.

.. important::

   Every course skill is an action, and a behavior tree leaf that runs a skill
   is an action client. A tree stops a skill by cancelling its goal, then
   reads the result to learn what the robot still holds.

The demonstration's server uses ``control_msgs/GripperCommand``, which comes
with ARIAC; ARIAC's own gripper uses ``ariac_interfaces/GripperCommand``. The
server is a stand-in skill: it closes a gripper from ``OPEN`` = 0.085 m in
``STEP`` = 0.0085 m steps, one every ``PERIOD`` = 0.2 s, and sends feedback
after each step.

.. literalinclude:: code/action_gripper.py
   :language: python
   :lines: 40-55
   :caption: lecture1/code/action_gripper.py (excerpt)

The client sends two goals to 0.000 m. It lets the first run to the end and
asks to cancel the second after 0.5 s.

.. literalinclude:: outputs/action_gripper.txt
   :language: text

**Reading the output.**

1. Goal 1: 0.085 / 0.0085 = 10 steps, so 10 feedback messages, then
   ``SUCCEEDED``.
2. Goal 2: the cancel request arrives at 0.5 s, during the third step (steps
   end at 0.2 s, 0.4 s and 0.6 s). The server checks for a cancel between
   steps, so the third step finishes first.
3. After 3 steps the gripper is at 0.085 − 3 × 0.0085 = 0.0595 m, the
   position in the result.

The server takes the cancel request while the goal runs because it uses a
multi-threaded executor: ``execute`` holds one thread, and another thread takes
the cancel. On a single-threaded executor the cancel waits for the goal to end,
and the goal ends ``SUCCEEDED`` at 0.0000 m (measured, 5 of 5 runs).


.. _l1-tf2:

TF2: Frames and Lookups
~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: TF2
   :class: note

   **TF2** is the ROS 2 library that keeps a tree of coordinate frames, with
   a transform between each parent and child. A **lookup** returns where one
   frame is, expressed in another, by chaining the transforms between them.

ARIAC's AGV frames (``tf_publisher_plugin.cpp``):

- ``agv1_frame``: the AGV's base.
- ``agv1_tray_frame``: the tray, 0.35 m above the base and turned −1.57 rad
  about z.
- ``agv1_slot1_frame``: slot 1, at (−0.065, 0.05, 0.032) m in the tray frame.

The offsets come from ARIAC's AGV model file
(``ariac_gz/models/agv/model.sdf``). The script publishes the same two
transforms as static frames and asks TF2 where slot 1 is, seen from the AGV's
base.

.. literalinclude:: code/tf_slot_lookup.py
   :language: python
   :lines: 44-56
   :caption: lecture1/code/tf_slot_lookup.py (excerpt)

.. literalinclude:: outputs/tf_slot.txt
   :language: text

**Checking the result by hand.**

1. Height: z = 0.35 + 0.032 = 0.382 m. The turn is about z, so it does not
   change the height.
2. A turn of −1.57 rad is close to a quarter turn clockwise, seen from
   above. It maps a point (a, b) in the tray frame to about (b, −a) in the
   AGV frame.
3. Slot 1 is at (a, b) = (−0.065, 0.05), so it lands at about (0.05, 0.065).
4. The script prints x = 0.0499 instead of 0.05 because 1.57 rad is slightly
   less than a quarter turn (π / 2 = 1.5708 rad).

The skills package looks up tray slot frames this way before it places a cell.
L10 covers TF2 and motion in depth.


Next Class
----------

**L2: System Architectures for Agentic Robotics** (Wednesday,
February 3):

- Classical robot architectures and the three-layer architecture.
- Which part of a robot system runs the LLM agent, and which runs the VLM.
- Teams form, and GP1 is posted.

**Before next class:**

- Install Ubuntu 24.04, ROS 2 Jazzy and ARIAC 2025 with the
  :doc:`ARIAC Testbed </ariac/ariac>` pages, and run the example trial.
- Run the four L1 scripts and compare your outputs with the ones above.
- Find two teammates.
