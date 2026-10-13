====================================================
Lecture
====================================================

.. note::

   These notes follow the L2 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running the toy factory, ``toy_factory.py``, with
   Python 3.12.3 on 2026-10-12. The script and how to run it are on the
   :doc:`code page <l2_code>`.


.. _l2-recap:

Recap
-----

From L1
~~~~~~~

- The course builds the **decision layer** of a factory robot system.
  Classical skills do the motion.
- ARIAC 2025 Task 1 is inspection and kit building. Every step is a ROS 2
  topic, service or action.
- QoS, executors, actions and TF2 decide whether those interfaces behave as
  you expect.

The Diagnostic Quiz
~~~~~~~~~~~~~~~~~~~

The class results are on ELMS-Canvas: the topics most of you missed, and
where to read about them.


.. _l2-classical:

Classical Robot Architectures
-----------------------------

.. admonition:: Definition: architecture
   :class: note

   A robot's **architecture** says how its software is split into parts, and
   how the parts pass decisions and data to each other.

There are four classic answers. Each one strikes a different balance between
**planning** (thinking ahead about goals) and **reacting** (answering a
sensor reading right away).


Sense-Plan-Act and Reactive
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: sense-plan-act (deliberative)
   :class: note

   In a **sense-plan-act** architecture the robot senses, builds a **world
   model** (its own record of what the world looks like), plans, then acts.

- **Strength:** it can reason about goals.
- **Weakness:** planning takes time, and the world can change before the plan
  runs.
- **ARIAC example:** planning the order in which to pick cells for a kit.

.. admonition:: Definition: reactive architecture
   :class: note

   In a **reactive** architecture, sensor readings map straight to actions,
   with no world model.

- **Strength:** fast response.
- **Weakness:** no long-range goals.
- **ARIAC example:** closing the gripper when the cell is between the
  fingers.


Behavior-Based Control and Subsumption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: subsumption architecture (Brooks, 1986)
   :class: note

   In the **subsumption** architecture, layers of simple behaviors run in
   parallel. A higher layer takes over a lower layer's role by
   **suppressing** its inputs and **inhibiting** its outputs. The lower
   layers keep running.

- The 1986 paper says that not all sensors need to feed a central
  representation.
- Brooks's stronger claim, that a robot can work with no explicit world model,
  comes later, in "Intelligence without representation" (1991).

**Where it strains.** Complex tasks are hard to express as layers of
behaviors. There is no place to write "build a kit whose total voltage is in
range".


The Three-Layer Architecture (Gat, 1998)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: three-layer architecture
   :class: note

   A **three-layer architecture** has three parts:

   - a **deliberative** layer that plans;
   - a **reactive** layer that controls;
   - an **executive** in the middle that chooses which skill runs next for
     the current situation, and reacts when a skill reports failure.

   Gat calls the three layers the **deliberator**, the **sequencer** and the
   **controller**.

.. list-table::
   :header-rows: 1
   :widths: 16 44 40
   :class: compact-table

   * - **Layer**
     - **What it decides**
     - **In this course**
   * - Deliberative
     - What to do over a long horizon: which kit to build, which cells to use
     - The PDDL planner (GP3), then the LLM agent (GP4)
   * - Executive
     - Runs the plan step by step: calls skills, watches results, retries or
       reports failure
     - A behavior tree (GP1, L4, L7)
   * - Reactive
     - Fast control close to the hardware
     - Joint trajectory controllers, grippers, MoveIt 2 inside the skills

Each layer runs at its own rate: the reactive layer fastest, the deliberative
layer slowest.

.. admonition:: Definition: skill
   :class: note

   A **skill** is one robot capability that the executive can call, such as
   picking a cell from the conveyor. In this course each skill is a ROS 2
   action from the course skills package. It reports success, or a failure
   reason, in its result.

.. important::

   The stack you build in this course follows this pattern, and it is the
   frame we use all semester.


The Four Architectures Side by Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l2/four_architectures.svg
   :alt: Four panels side by side, each standing on a gray bar labeled World. Panel 1: Sense, Model, Plan, Act in a loop: the world feeds Sense, Sense feeds Model, Model feeds Plan, Plan feeds Act, and Act changes the world. Panel 2: Sense feeds a Rule that acts on the world directly; a dashed empty box reads no model, no plan. Panel 3: three behavior boxes, Level 0, Level 1 and Level 2, all fed by the sensors; the output of Level 1 and of Level 2 each enters a circle marked S on the output line of Level 0, which drives the world. Panel 4: three stacked boxes, Deliberative, Executive and Reactive, with arrows going down on the left and up on the right, and the Reactive box connected to the world.
   :width: 100%
   :align: center

   1: sense-plan-act. 2: reactive. 3: subsumption; at each S, a higher level
   replaces the signal on the line below it (Brooks calls this suppression).
   4: three-layer. Blue: deliberation. Amber: the executive. Green: reaction.
   Gray: the world and sensing.

Panel 1 puts a model and a plan between every reading and every action.
Panel 2 puts nothing there. Panels 3 and 4 are two ways to have both.


.. _l2-three-layer:

The Three-Layer Architecture
----------------------------

This section is the frame of the course: what passes between the layers, and
one example of goals going down and status coming up.


What Passes Between the Layers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Down and up.**

- **Goals and plans go down.** The deliberative layer sends a decision; the
  executive sends skill goals.
- **Status, results and failures come up.** A skill reports success or a
  failure reason; the executive reports when a step cannot finish.

**Every boundary is an interface.**

- Executive to reactive: a ROS 2 action (a skill goal and its result).
- Inside the executive: blackboard keys (L4).
- Deliberative to executive: a plan, or an agent's decision checked against a
  JSON schema (L8).

.. note::

   L3 covers how to design what crosses each boundary: the world model each
   layer needs.


Goals Down, Status Up: One Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l2/goals_status.svg
   :alt: Three stacked boxes: Deliberative (slowest) on top, Executive in the middle, Reactive (fastest) below, and World at the bottom. Arrows on the left go down and carry goals: test the next cell at tester 1; pick and place in tester 1 (skills); joint commands (controllers). Arrows on the right go up and carry status: joint states and sensor data; GRASP_FAILED and tester 1 at -1 V, MALFUNCTIONING, in red; and cell 3 at 3.60 V with tester 1 down, in red.
   :width: 75%
   :align: center

   The labels are messages from the toy factory run later in this lecture
   (``lecture2/outputs/three_layers.txt``). Red: a failure report on its way
   up.

Read the figure from the bottom up on the right side. The reactive layer
passes up what it measures: joint states and sensor data. The executive hears
two failures from below: a skill result ``GRASP_FAILED`` and a tester that
reads −1 V with the status ``MALFUNCTIONING``. What the executive sends to
the planner is shorter: cell 3 reads 3.60 V, and tester 1 is down. The
−1 V readings stay in the executive.


.. _l2-toy-factory:

A Toy Factory, Three Ways
-------------------------

In class this section is a **live demonstration**: one short Task 1 run under
three architectures, with a voltage tester malfunction switched on. The
program is plain Python with no ROS: ``lecture2/code/toy_factory.py``. Try it
at home (not graded); the :doc:`code page <l2_code>` says how.


What the Toy Keeps from ARIAC, and What It Makes Up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   This is a toy, not ARIAC: no simulator, no ROS, one robot action at a
   time. Only the rules below come from ARIAC 2025 (source, branch
   ``ariac2025``).

**Kept from ARIAC.**

- Li-Ion cells: 3.6 V nominal, plus or minus 0.2 V per cell, plus or minus
  0.15 V per kit of four (``CellTypes.msg``).
- Cell voltages spread with a standard deviation of 0.1 V
  (``cell_feed_plugin.hpp``).
- Two testers. Each reading has noise with a standard deviation of 0.05 V
  (``voltage_tester/model.sdf``). A new reading comes every 0.1 s. An empty
  tester reads about 0 V.
- A malfunctioning tester keeps publishing: −1 V with the status
  ``MALFUNCTIONING`` (``voltage_tester_plugin.cpp``). ARIAC's challenge page
  says a malfunctioning tester stops publishing; the toy follows the code.
  **Check the status field, not only the voltage.**

**Chosen for this example.** 10 cells; step times of 3 s to 10 s; each pick
fails with probability 0.2; tester 1 malfunctions from 20 s for 45 s (45 s is
the duration in ARIAC's example configuration); seed 1.

.. admonition:: Definition: seed
   :class: note

   A **seed** is the number that starts a random number generator. The same
   seed gives the same "random" cell voltages, reading noise and grasp
   failures, so every run with seed 1 repeats exactly.


Architecture 1: Plan Only
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/toy_factory.py
   :language: python
   :lines: 161-171
   :caption: lecture2/code/toy_factory.py (excerpt)

- The plan is made once, at :math:`t = 0`: testers 1, 2, 1, 2, and so on.
- It foresees one branch: ``sort_cell`` sends a reading inside 3.4 V to 3.8 V
  to AGV 1, and any other reading to the recycling bin.
- It never looks at a skill result or a tester status.


Architecture 2: React Only
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/toy_factory.py
   :language: python
   :lines: 175-191
   :caption: lecture2/code/toy_factory.py (excerpt)

Each pass of the loop looks at what the sensors show now and fires the first
rule that matches:

1. Rule 1: four cells on AGV 1's tray, so ship.
2. Rule 2: a tester holds a cell and reads −1 V with ``MALFUNCTIONING``, and
   the other tester is free, so move the cell there.
3. Rule 3: a tester holds a cell and works, so sort the cell on that one
   reading.
4. Rule 4 (below the excerpt): a cell is waiting and a tester is free and
   working, so pick the cell into it. A failed pick just fires the rule again.

There is no memory: one reading, no average, and no record of the tray.


Architecture 3: The Executive Retries and Moves the Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Executive.pick: retry a failed grasp.**

.. literalinclude:: code/toy_factory.py
   :language: python
   :lines: 238-245
   :caption: lecture2/code/toy_factory.py (excerpt)

The pick skill, ``pick_from_conveyor``, tries once and returns ``SUCCESS`` or
a failure reason. It never retries. The executive decides to try again, up to
``1 + retries`` attempts (3 by default).

**Executive.test_cell (excerpt): after 10 readings at tester n.**

.. literalinclude:: code/toy_factory.py
   :language: python
   :lines: 256-262
   :caption: lecture2/code/toy_factory.py (excerpt)

The comments mark the idea: the executive **sees** the malfunction and
**handles** it in the same place, by moving the cell to the other tester and
averaging again.


Architecture 3: The Planner Chooses the Cells for the Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Planner.destination.**

.. literalinclude:: code/toy_factory.py
   :language: python
   :lines: 219-229
   :caption: lecture2/code/toy_factory.py (excerpt)

- ``k`` is the kit slot this cell would fill (1 to 4).
- ``off`` is how far the kit so far, plus this cell, sits from
  :math:`k \times 3.6` V.
- ``room`` is :math:`0.15 - 0.05` V, plus 0.05 V for each slot still empty.
  ``MARGIN`` (0.05 V) and ``SLACK`` (0.05 V) are chosen for this example. So
  the room is 0.25 V for slot 1, 0.20 V for slot 2, 0.15 V for slot 3 and
  0.10 V for slot 4.
- A cell that is in range but does not fit goes to a spare tray (AGV 2, then
  AGV 3) for a later kit. **Robots recycle only out-of-range cells.**


.. _l2-toy-result:

The Result: Only the Three Layers Finish the Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running the script with no options runs all three architectures on seed 1:

.. literalinclude:: outputs/summary.txt
   :language: text
   :caption: lecture2/outputs/summary.txt

The first line lists the true voltage of each of the 10 cells, in the order
they arrive. The kits:

1. **Plan only** ships cells 1, 2, 4 and 6:
   3.73 + 3.74 + 3.52 + 3.60 = 14.59 V, which is 0.04 V above 14.55 V. It
   recycled cells 3 and 5, which were in range.
2. **React only** ships cells 1 to 4: 3.73 + 3.74 + 3.61 + 3.52 = 14.60 V,
   which is 0.05 V above 14.55 V.
3. **Three layers** ships cells 1, 3, 4 and 6:
   3.73 + 3.61 + 3.52 + 3.60 = 14.46 V, inside the window. It takes 107 s,
   against 74 s for react only, because it sets aside cells that do not fit.


Plan Only and React Only, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each trace line gives the toy's clock, then what happened. A line such as
``cell 1: tester 1 reads 3.72 V -> AGV 1`` means: the average of the readings
of cell 1 at tester 1 was 3.72 V, and the cell went to AGV 1.

.. literalinclude:: outputs/plan_only.txt
   :language: text
   :caption: lecture2/outputs/plan_only.txt

- Cells 3 and 5 reach tester 1 while it malfunctions. The plan reads −1.00 V
  as a voltage, finds it out of range, and recycles two good cells.
- ``no cell``: a pick failed. The plan goes on and reads an empty tester
  (about 0 V).

.. literalinclude:: outputs/react_only.txt
   :language: text
   :caption: lecture2/outputs/react_only.txt

- At 20.5 s rule 2 moves cell 2 away from the malfunctioning tester 1:
  reaction handles the malfunction well.
- Then it puts the first four in-range cells on the tray, because it keeps no
  record of the tray.
- Each of its readings is one reading, not an average of 10, so it carries
  the full 0.05 V noise. Cell 2, whose true voltage is 3.74 V, reads 3.78 V
  here.


Three Layers, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/three_layers.txt
   :language: text
   :caption: lecture2/outputs/three_layers.txt

The planner's choices for the first three cells. The room for slot
:math:`k` is :math:`0.15 - 0.05 + 0.05 \times (4 - k)` V.

1. **Cell 1, 3.72 V.** 3.72 − 3.60 = 0.12 V. The room for slot 1 is 0.25 V,
   so AGV 1.
2. **Cell 2, 3.72 V.** 3.72 + 3.72 − 7.20 = 0.24 V. The room for slot 2 is
   0.20 V, so AGV 2 (a spare for a later kit).
3. **Cell 3, 3.60 V.** 3.72 + 3.60 − 7.20 = 0.12 V, within 0.20 V, so AGV 1.

Exercise 1 on the :doc:`exercises page <l2_exercises>` finishes the kit with
cells 4 to 6.


One Run Is One Sample: 1000 Seeds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One run could be luck. ``--sweep 1000`` runs each architecture on seeds 1 to
1000 and counts how each run ended.

.. literalinclude:: outputs/sweep.txt
   :language: text
   :caption: lecture2/outputs/sweep.txt

The same sweep with the malfunction switched off:

.. literalinclude:: outputs/sweep_off.txt
   :language: text
   :caption: lecture2/outputs/sweep_off.txt

- **Columns:** kits accepted; kits rejected for the kit total, for a cell out
  of range, or for fewer than four cells; clean stops; in-range cells
  recycled, all runs together.
- **Plan only and react only** accept 600 to 613 kits, with or without the
  malfunction: nobody chooses the cells. A rate from 1000 runs wanders by
  about :math:`\sqrt{0.61 \times 0.39 / 1000} \approx 0.015` by chance alone
  (15 kits in 1000), so these counts do not differ beyond chance.
- **The malfunction shows in plan only's recycled cells:** 1570 with it, 28
  without.
- **Three layers** accepts 919 kits. It has 70 clean stops: a grasp failed
  three times in 36 runs, and the 10 cells ran out in 34. Its other 11
  failures (7 + 4) come from reading noise: an average of 10 readings still
  wanders by about :math:`0.05 / \sqrt{10} \approx 0.016` V.

.. admonition:: Definition: clean stop
   :class: note

   A system **stops cleanly** when it cannot finish a task and stops on
   purpose, with a reason, instead of going on with bad data. In the toy the
   three-layer run ends with ``stopped cleanly:`` and the failure that moved
   up.


.. _l2-malfunction-story:

One Tester Malfunction, Layer by Layer
--------------------------------------

This is the three-layer run from the demonstration, one step at a time.
Tester 1 malfunctions from 20 s to 65 s (20 + 45). At each step, ask three
questions: which layer sees the failure, which layer handles it, and what
moves up.

Steps 1 to 3: The Tester Reports, the Executive Sees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **20 s, reactive layer.** Tester 1 starts to malfunction. It publishes
   −1 V with the status ``MALFUNCTIONING`` every 0.1 s. It reports; it
   decides nothing.
2. **28 s, deliberative layer.** The planner has heard nothing, so its rule
   (alternate the testers) assigns cell 3 to tester 1. Cell 2 used tester 2.
3. **36.0 s, executive.** The executive averages 10 readings at tester 1 and
   sees ``MALFUNCTIONING``. This is the first layer to see the failure,
   36 − 20 = 16 s after it started.

.. important::

   The 16 s gap comes from the toy: it reads a tester only when it uses it.
   ARIAC's challenge page asks teams to watch the tester topics. In GP1, a
   leaf of your behavior tree does this reading: it reads
   ``/voltage_tester_1/voltage`` and checks the ``operation_status`` field of
   each message.

The 28 s is not in the trace. Cell 2 is logged at 22.0 s, and its move to the
tray takes 6 s, so the planner's next choice comes at 22 + 6 = 28 s.


Steps 4 to 6: Handled Where Seen, Then Status Moves Up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. **36 s to 41 s, executive.** It handles the failure without asking anyone:
   it calls a skill to move cell 3 to tester 2 (4 s) and reads again (1 s).
   At 41.0 s, tester 2 reads 3.60 V.
5. **41 s, executive to planner.** The report holds two facts: cell 3 reads
   3.60 V, and tester 1 is down. The −1 V readings stay in the executive.
6. **After 41 s, deliberative layer.** The planner marks tester 1 down in its
   world model and stops choosing it: cells 4 and 5 go to tester 2 (logged at
   55.1 s and 69.2 s).

.. important::

   This is the rule from 4D/RCS that L3 covers: **an error is handled where
   it is seen, and only the status moves up.** The planner never learns what
   a −1 V reading is.


Steps 7 and 8: Recovery, and the Whole Story in One Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

7. **65 s to 75.3 s.** Tester 1 works again at 65 s. Before each new cell,
   the planner asks for the status of the testers it marked down. The first
   check after 65 s comes at 75.3 s.
8. **79.3 s to 91.3 s.** Two grasps fail and the executive retries; the
   planner never hears of them. Cell 6 is tested at tester 1 (logged at
   91.3 s).

.. list-table::
   :header-rows: 1
   :widths: 18 24 28 30
   :class: compact-table

   * - **Event**
     - **Who sees it**
     - **Who handles it**
     - **What moves up**
   * - Malfunction
     - Executive, reading the tester
     - Executive: moves the cell
     - "tester 1 down"
   * - Grasp failure
     - Skill: ``GRASP_FAILED``
     - Executive: up to 3 attempts
     - Nothing, unless all 3 fail
   * - Recovery
     - Executive: status check
     - Planner: uses tester 1 again
     - "tester 1 OPERATIONAL"

.. note::

   In the grasp failure row, the skill sees the failure and reports it. It
   does not retry: it stops and returns a failure reason, and the executive
   (your behavior tree) decides what to do next.


.. _l2-real-software:

Three Layers in Real Robot Software
-----------------------------------

This section looks at Nav2 (ROS 2 navigation) and MoveIt (motion planning),
quoted from their documentation, read on 2026-10-12. The layer names are
ours: the documentation uses its own words.

Nav2: A Behavior Tree Calls the Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Nav2 documentation says:

   "For this project, we use BehaviorTree CPP V4 as the behavior tree
   library. We create node plugins which can be constructed into a tree,
   inside the BT Navigator."

   "When the behavior tree ticks the corresponding BT node, it will call the
   action server to process its task."

.. list-table::
   :header-rows: 1
   :widths: 18 82
   :class: compact-table

   * - **Our layer**
     - **Nav2**
   * - Deliberative
     - The client application that sends a navigation goal (Nav2 offers the
       ``NavigateToPose`` action for it)
   * - Executive
     - The BT Navigator: a BehaviorTree.CPP tree
   * - Reactive
     - The planner, controller and behavior servers, each an action server

.. important::

   Nav2's **planner server** computes a path. In our terms it is a skill
   below the executive, not the deliberative layer. **Match layers by role,
   not by name.**

Sources (Nav2 documentation, Jazzy):
`Behavior Trees <https://docs.nav2.org/jazzy/getting_started/navigation_concepts/behavior_trees/>`__,
`Navigation Servers <https://docs.nav2.org/jazzy/getting_started/navigation_concepts/navigation_servers/>`__,
`Behavior-Tree Navigator <https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/configuring_bt_navigator/>`__.


MoveIt: A Motion Layer, Not an Executive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MoveIt documentation says that the ``move_group`` node "serves as an
integrator: pulling all the individual components together to provide a set
of ROS actions and services for users to use." It "talks to the controllers
on the robot using the FollowJointTrajectoryAction interface"; that server "is
not provided by move_group itself." And "the result coming out of move_group
is a trajectory and not just a path."

- In the course stack, MoveIt 2 sits inside the skills package. A skill asks
  it for a trajectory, and the ``follow_joint_trajectory`` action of the
  robot's joint trajectory controller in ARIAC runs it (ARIAC API page).
- MoveIt does not decide which cell to pick next or what to do when a grasp
  fails. Your executive and your planner do.

Sources (MoveIt documentation, Rolling version):
`The move_group node <https://moveit.picknik.ai/main/doc/concepts/move_group.html>`__,
`Motion Planning <https://moveit.picknik.ai/main/doc/concepts/motion_planning.html>`__.


.. _l2-where-ai:

Where AI Plugs In
-----------------

An LLM agent goes in the deliberative layer, a VLM goes in perception, and
everything else stays classical.

Two AI Components and Their Places
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**LLM agent: deliberative layer (GP4).**

- It decides the next step from the world state and calls skills as tools.
- It handles situations a fixed planning model does not describe, such as the
  ARIAC challenges.

**VLM: perception (GP4, final demo).**

.. admonition:: Definition: VLM
   :class: note

   A **vision-language model (VLM)** takes an image and text and answers in
   text. In this course it describes what a camera sees, as text or a checked
   record the agent can use.

In the final demo, a hosted **embodied-reasoning model** (a model built to
reason about physical scenes) judges cell defects from camera images, and
your team compares it with its GP2 lidar detector.

**Stays classical.** Motion planning and grasping (MoveIt 2 in the skills
package), the controllers, the behavior-tree executive, and the ARIAC factory
services.


Why the Executive Stays Classical
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The behavior tree checks each skill result and stops cleanly on failure,
  whatever planner sits above it.
- In GP3 the tree runs a PDDL plan; in GP4 the same tree runs the agent's
  decisions.
- Because the executive is the same, GP4 can compare the agent with the
  planner on identical trials: validity, plan length, cost and latency.

.. important::

   Swap the deliberative layer, keep the executive: that is how this course
   measures what an LLM adds.


Discussion: Which Layer Decides Each Task 1 Step?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In class we fill in this table together on the board.

.. list-table::
   :header-rows: 1
   :widths: 34 33 33
   :class: compact-table

   * - **Task 1 step**
     - **Which layer decides?**
     - **Would an LLM add anything?**
   * - Feed a cell type
     -
     -
   * - Inspect a cell
     -
     -
   * - Pick from the conveyor
     -
     -
   * - Test the voltage
     -
     -
   * - Place on the tray or recycle
     -
     -
   * - Ship the kit
     -
     -

**Hint:** think about which steps change when a high-priority order arrives.


.. _l2-ariac:

ARIAC 2025 as a Three-Layer System
----------------------------------

This section says who provides each layer (ARIAC, the course, or your team)
and gives the drawing we keep for the rest of the semester.

Who Provides Each Layer
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 16 68
   :class: compact-table

   * - **Layer**
     - **Provided by**
     - **What it is**
   * - Deliberative
     - Your team
     - The GP3 PDDL planner, replaced in GP4 by an LLM agent that calls the
       same skills as tools
   * - Executive
     - Your team
     - The GP1 behavior tree: it calls the skills and the ARIAC services in
       order
   * - Skills
     - The course
     - The skills package: Python ROS 2 actions on MoveIt 2, such as picking a
       cell or placing it in a tray slot
   * - Reactive
     - ARIAC
     - Each robot's joint trajectory and gripper actions, the AGV move
       actions, the conveyor and feed services, the sensors, the submission
       services
   * - Perception
     - Your team
     - Lidar point clouds for cell defects (GP2); cameras later, for the VLM
       (GP4) and the top shell (final demo)

The vacuum tools on assembly robot 2 use grasp and release services instead of
a gripper action.


The Drawing We Keep All Semester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l2/ariac_three_layers.svg
   :alt: The course stack drawn as boxes. Top, in blue: Deliberative (your team), GP3 PDDL planner, and in GP4 an LLM agent. Below it, in amber: Executive (your team), the GP1 behavior tree in py_trees_ros. Below that, in green: Skills (the course), pick and place as ROS 2 actions on MoveIt 2. At the bottom, in green: Reactive (ARIAC), the controllers, grippers, conveyor, testers, AGVs and sensors. Arrows go down on the left and up on the right between the layers. A separate arrow goes from the executive straight down to ARIAC, past the skills, labeled /agvN/move and ARIAC services. On the left, a purple Perception box (your team: GP2 lidar defects, GP4 VLM on camera images) receives sensor data from ARIAC and sends its results to the executive and to the deliberative layer.
   :width: 90%
   :align: center

   Left arrows: goals down. Right arrows: status up. The executive calls the
   skills for the arms, and calls ARIAC directly to move the AGVs and to use
   the factory services. Each later lecture points to the box it fills.


What the Course Skills Package Promises
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Your team calls skills and never writes motion code.
- Each skill is a ROS 2 action: it reports success, or a failure reason in its
  result.
- **A skill never retries a task on its own.** It stops and returns a failure
  reason, and your behavior tree decides what to do next. Recovery stays your
  team's job (L7, L11), so failures and the ARIAC challenges reach your code.
- A skill can be cancelled while it runs, the way the L1 action demonstration
  was.
- Your team moves the AGVs with ARIAC's own AGV move action
  (``/agvN/move``, for example ``/agv1/move``). The skills cover the robot
  arms.

.. important::

   The skills package is the boundary between the reactive layer you are
   given and the executive you build. L10 opens it up.


.. _l2-vla:

The End-to-End Alternative
--------------------------

This section is a survey only: no policy training and no hands-on VLA work.
L13 goes deeper.

What a VLA Model Is
~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: vision-language-action (VLA) model
   :class: note

   A **VLA model** maps camera images and a language instruction straight to
   robot actions, with no separate planner or skills. It is one learned model
   from camera to action.

Examples: `OpenVLA <https://openvla.github.io/>`__ (an open 7B-parameter
model), Physical Intelligence's `pi-0 <https://arxiv.org/abs/2410.24164>`__,
Google DeepMind's `Gemini Robotics
<https://deepmind.google/models/gemini-robotics/>`__, Figure's `Helix
<https://www.figure.ai/news/helix>`__. ("7B" means 7 billion parameters, the
numbers a model learns in training; "80M" below means 80 million.)

**Two kinds.**

- **Single models:** OpenVLA and pi-0.
- **Two-system designs:** a slower model reasons about the scene and the task
  above a fast control policy.

  - Helix runs a 7B-parameter VLM at 7 to 9 Hz above an 80M-parameter policy
    at 200 Hz (Figure's Helix page).
  - Gemini Robotics pairs an embodied-reasoning model that plans with a VLA
    model that acts.


A Two-System VLA Next to the Three Layers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l2/vla_vs_stack.svg
   :alt: Two columns. Column 1, a two-system VLA: a blue box, slow model, a VLM with 7B parameters at 7 to 9 Hz; below it a dashed empty amber box reading no executive; below that a green box, fast policy with 80M parameters at 200 Hz; then the robot. The arrow from the slow model goes straight to the fast policy, past the empty box. Column 2, the course stack: a blue box with the PDDL planner (GP3) and the LLM agent (GP4); an amber box, the behavior tree (GP1), which checks every result; a green box with the skills, MoveIt 2 and the controllers; then the robot.
   :width: 90%
   :align: center

   1: a two-system VLA; numbers from Figure's Helix page. 2: this course.
   Same colors as the earlier drawings: blue deliberates, amber executes,
   green reacts.

.. important::

   A two-system VLA has the deliberative and reactive roles, but nothing
   between them checks each step: the policy acts on the slow model's output
   directly. Your behavior tree is that check.


The Tradeoffs This Course Weighs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 38 42
   :class: compact-table

   * - **Question**
     - **End-to-end VLA**
     - **Modular stack (this course)**
   * - Data and compute
     - Needs robot demonstration data and GPUs to train or fine-tune
     - Runs without training; no GPU required
   * - Inspecting a failure
     - Hard to trace inside a learned policy
     - A plan or an agent's tool calls can be read line by line
   * - Auditing a decision
     - Hard to check against a rule
     - A decision can be checked against a rule, such as the kit voltage
       window
   * - New tasks
     - Can handle tasks no one wrote skills for
     - Limited to the skills it has

.. important::

   The course keeps the modular stack because it grades your engineering on
   trials your system has never seen, and the last row is the price of that
   choice.


.. _l2-multi-robot:

Multi-Robot Coordination
------------------------

ARIAC 2025 has two inspection robots, two assembly robots, a gantry welder and
three AGVs. They share one workspace and one set of orders.

Shared Space and What a Collision Costs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The tester area.** Inspection robot 1 places cells in the voltage testers;
inspection robot 2 takes them out. Both arms reach into the same area.

**The cost.**

- A robot collision costs 100 points for every 5 s in contact.
- A collision between two robots counts twice.
- Source: the ARIAC scoring page, and ``scoring_weights.yaml`` (branch
  ``ariac2025``) for the 100, which the docs say may change.

**Who prevents it.**

- The skills package keeps two robots out of a shared area at the same time.
- Deciding which robot goes first is your team's job.


The Shared Tester Area, to Scale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l2/tester_area.svg
   :alt: A top view of the ARIAC Task 1 inspection area, drawn to scale, x to the right and y up, with a 0.5 m scale bar. Tag 1: the inspection conveyor on the left, with an arrow showing cells moving to the right. Tag 2: the inspection door across the conveyor. Tag 3: inspection robot 1, a UR3e, below the end of the conveyor. Tags 4 and 5: voltage testers 1 and 2, one above the other (tester 1 higher), to the right of robot 1. Tag 6: inspection robot 2, a UR5e, to the right of the testers. Tag 7: the recycling bin below robot 2. Tag 8: AGVs 1 to 3 in a row above robot 2. A dashed circle around each robot shows its reach, 0.5 m and 0.85 m. The two circles overlap in a shaded yellow area that holds both testers.
   :width: 85%
   :align: center

   Top view, to scale, with :math:`x` to the right and :math:`y` up. The
   tags are listed below.

1. Inspection conveyor; the arrow shows where cells move.
2. Inspection door.
3. Inspection robot 1 (UR3e).
4. Voltage tester 1.
5. Voltage tester 2.
6. Inspection robot 2 (UR5e).
7. Recycling bin.
8. AGVs 1 to 3.

- **Dashed circles:** each arm's reach, 0.50 m and 0.85 m, drawn flat around
  its base. These are Universal Robots' published reach values for the
  original UR3e (500 mm) and the UR5e (850 mm). ARIAC builds both arms from
  those models' kinematics in the ``ur_description`` package.
- **Shaded:** the area both arms reach. It holds both testers.
- Positions come from ``ariac.world`` and the robot URDFs. The tester and bin
  outlines are schematic.


One Decision Maker, or One per Robot?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Central
      :class-card: sd-border-secondary

      One decision maker plans for every robot.

      It sees every conflict, but it is one point of failure, and its plans
      grow with the number of robots.

   .. grid-item-card:: One per robot
      :class-card: sd-border-secondary

      Each robot decides for itself and negotiates for shared space.

      It scales, but the robots must agree, and a missed message can
      **deadlock** them (each one waits for the other, forever).

.. important::

   An LLM agent that controls several robots in GP4 and the final demo meets
   these conflicts. L11 returns to them.


.. _l2-gp1:

GP1 and Teams
-------------

GP1: Behavior Tree for One Kit is posted today (02/03), is due on 02/24, and
is worth 10% of the course grade. Teams form today. The full specification is
on the :doc:`GP1 page </assignments/gp1>`.

What GP1 Asks For
~~~~~~~~~~~~~~~~~

A ``py_trees_ros`` behavior tree that builds one kit:

1. Feed cells onto the inspection conveyor.
2. Submit an inspection report for every cell.
3. Read each cell's voltage at a tester; recycle cells outside the voltage
   range.
4. Place four acceptable cells on an AGV tray with the skills package.
5. Move the AGV to shipping and submit the kit.
6. Handle a skill that fails once (retry) and one that keeps failing (stop
   cleanly).

.. warning::

   GP1 has no defect detection and runs on a trial with no defective cells,
   so every report says passed. Without a report, the inspection door pushes
   the cell into the inspection bin and nothing reaches the robots.


What You Get, What You Submit, and When
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Provided.**

- The course skills package.
- A starter ROS 2 package with a launch file for the trial.
- A starter ``py_trees_ros`` tree: one sequence for one cell.
- The ARIAC 2025 example team configuration.

**Deliverables.**

- A ROS 2 package with a launchable behavior tree.
- A 1 to 2 page write-up: the tree diagram and the reason for each composite
  choice.

**Timeline.**

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - **Week**
     - **GP1 work**
   * - 2 (02/03)
     - Setup, repository, run the trial
   * - 3 (02/10)
     - Skills package, ARIAC services
   * - 4 (02/17)
     - L4: write the tree
   * - 5 (02/24)
     - GP1 due


Forming Your Team
~~~~~~~~~~~~~~~~~

**Rules.**

- Three students per team; two only with the instructor's approval; four or
  more not allowed.
- Submit your roster on Canvas, and set up one shared Git repository.
- Teams stay together for all four projects and the final demo. A change
  needs a written reason and the instructor's approval.

.. admonition:: Definition: team charter
   :class: note

   The **team charter** is a one-page agreement your team posts on ELMS
   before L3. It says:

   - who owns which part of the system, with a primary and a backup;
   - when the team meets, and how it uses Git;
   - what happens when someone goes quiet;
   - how the team uses AI tools.


.. _l2-next-class:

Next Class
----------

**L3: Knowledge Representation for Agentic Robotics** (Wednesday,
February 10):

- Frames and ontologies for cells, kits and AGVs.
- A world model at each layer, and errors that move up (two ideas from
  4D/RCS).
- One kit written three ways: PDDL predicates, a JSON schema, a text
  description.

**Before next class:**

- Form your team, submit the roster, and post the team charter on ELMS.
- Get the starter package and the skills package running in the ARIAC trial.

**Try the toy factory at home** (optional, not graded):

.. code-block:: bash

   python3 toy_factory.py --arch "three layers" --retries 0
   python3 toy_factory.py --pick-fail 0.5 --duration 200
   python3 toy_factory.py --sweep 1000 --cells 6

The :doc:`code page <l2_code>` explains every option, and the
:doc:`exercises <l2_exercises>` change the simulator and ask you to predict
the result before you run it.
