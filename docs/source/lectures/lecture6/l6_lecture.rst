====================================================
Lecture
====================================================

.. note::

   These notes follow the L6 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running ``lecture6/code/run_all.sh`` on 2026-10-12, with
   Python 3.12.3, ``unified-planning`` 1.3.0 and ``up-fast-downward`` 1.0.0
   (Fast Downward 26.6). The examples need no ROS 2 and no simulator. The
   scripts and how to run them are on the :doc:`code page <l6_code>`.


.. _l6-recap:

Recap
-----

From L5
~~~~~~~

- Lidar point clouds decide each cell's inspection report; the averaged
  tester voltage decides tray or recycling.
- GP2 (cell inspection) is due next week, Week 7.

From GP1
~~~~~~~~

- Your GP1 tree runs the Task 1 steps in an order your team wrote down in
  advance.

Today
~~~~~

- A planner chooses that order at run time, from a model of the factory
  written in **PDDL** (Planning Domain Definition Language).
- No quiz and no deliverable this week. Quiz 3, next week, covers L5 and L6.


.. _l6-classical:

Classical Planning
------------------

This section covers states, actions, goals and plans, and the three
assumptions behind them.

States, Actions, Goals and Plans
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definitions: the words of classical planning
   :class: note

   - A **fact** is a statement that is true or false, such as "tester1 is
     free".
   - A **state** is the set of facts that are true. A fact not listed is
     false: this rule is the **closed-world assumption**.
   - An **action** has **preconditions** (facts that must be true before it)
     and **effects** (facts it makes true and facts it makes false).
   - A **goal** is a set of facts that must be true at the end.
   - A **plan** is a sequence of actions that turns the initial state into a
     state where the goal holds.

This model comes from **STRIPS** (Fikes and Nilsson, 1971). PDDL writes it
in two files:

- a **domain**: types, predicates and actions;
- a **problem**: objects, initial state and goal.

A **predicate** is a kind of fact: ``tester-free`` becomes the fact "tester1
is free" once it names tester1.

Source: R. E. Fikes and N. J. Nilsson, STRIPS: A New Approach to the
Application of Theorem Proving to Problem Solving, *Artificial Intelligence*
2:189 to 208, 1971.

.. _l6-planning-loop:

The Planning Loop
~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l6/planning_loop.svg
   :alt: A block diagram of the planning loop. On the left, a dashed box
         labeled domain.pddl holds a gray box Actions (preconditions,
         effects), and a dashed box labeled problem.pddl holds gray boxes
         Initial state (facts true now) and Goal (facts that must hold).
         Arrows from all three lead to a white box Planner (search plus
         heuristic), whose arrow leads to a gray box Plan (steps in order).
         An arrow goes down from the plan to a white box Executor (runs one
         step at a time), then left to a white box Factory (ARIAC). An arrow
         from the factory returns along the bottom to problem.pddl.
   :width: 100%
   :align: center

- Gray boxes are files and data; white boxes are programs and the factory.
- The domain stays the same for every trial. Your team's code writes a new
  problem whenever the factory changes.

.. _l6-assumptions:

Three Assumptions, and Where ARIAC Breaks Each One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - **Assumption**
     - **Where the ARIAC factory breaks it**
   * - **Full observation:** the planner knows every fact at the start
     - A cell's defects and voltage are unknown until the lidar scan and the
       tester measure them. A malfunctioning tester gives no valid reading at
       all (it publishes −1 V with status ``MALFUNCTIONING``).
   * - **Deterministic actions:** an action always has its listed effects
     - In Task 2, a vacuum grasp by assembly_robot_2 can fail (vacuum tool
       malfunction).
   * - **A static world:** only the robots change it
     - New cells keep arriving, the conveyor can stop, and a high-priority
       order can arrive at any time.

.. important::

   So a classical plan covers a short stretch of work, and your system makes
   a new plan when the factory disagrees with the model. L7 builds that loop.

.. _l6-search:

How a Planner Searches
~~~~~~~~~~~~~~~~~~~~~~

- With :math:`n` true-or-false facts, there can be up to :math:`2^n` states.
  Planners do not list them all.
- A planner searches from the initial state, applying actions whose
  preconditions hold.
- A **heuristic** estimates how many actions a state is from the goal, so the
  search tries promising states first.

**Two kinds of search:**

- **Optimal**: A* search with an **admissible** heuristic (one that never
  overestimates) returns a shortest plan, but can be slow.
- **Satisficing**: greedy search returns a plan quickly, not always the
  shortest.

Later in the lecture, both run on our Task 1 problems, and we measure the
difference (:ref:`l6-compare`).


.. _l6-domain:

A PDDL Domain for Task 1
------------------------

This section writes types, predicates and actions for Task 1 Steps 1b to 1e.
The names are example names for this lecture, not the GP3 specification.

.. note::

   Every file and output in this lecture is in ``lecture6/code/`` and
   ``lecture6/outputs/``; ``run_all.sh`` writes every output. See the
   :doc:`code page <l6_code>`.

The Domain Header: Requirements, Types and Constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 3-7
   :caption: lecture6/code/domain.pddl (lines 3 to 7)

- ``:strips :typing``: plain STRIPS actions, with typed objects.
- **Types** are the kinds of objects. They play the role of L3's frame
  classes: ``cell``, ``robot``, ``tester``, ``agv``, ``slot``, ``station``.
- **Constants** are objects every problem shares. Every ARIAC tray has four
  slots (``AgvTrayStatus.msg`` has four occupied flags), so ``s1`` to ``s4``
  live in the domain.
- ARIAC has four AGV stations (``AgvStations.msg``); this domain needs only
  two of them, ``inspection`` and ``shipping``.

The Predicates: Facts That Can Be True or False
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A predicate has parameters. Given objects for its parameters, it is true
or false in each state.

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 8-24
   :caption: lecture6/code/domain.pddl (lines 8 to 24)

``?c - cell`` is a **parameter**: a variable that stands for any object of
type ``cell``.

Changing Facts and Fixed Facts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Changing facts (actions make them true or false):**

- Where a cell is: ``at-door``, ``on-tester``, ``holding``, ``in-slot``,
  ``recycled``.
- What is free: ``tester-free``, ``hand-free``, ``slot-free``.
- The AGV and the kit: ``agv-at``, ``kit-checked``, ``submitted``.

**Facts your team measures:**

- ``voltage-ok`` and ``voltage-bad``: the result of the voltage check,
  written into the problem. No action changes them.

**Fixed facts (true in every trial):**

- ``serves``, ``picks-conveyor``, ``loads-agv``: which robot can do what.
  Without them, the planner would let inspection_robot_2 pick cells off the
  conveyor.

.. _l6-objects:

The Objects and Their Predicates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - **Objects (type)**
     - **Predicates about them**
   * - c1, c2, c3, c4 (``cell``)
     - ``at-door``, ``voltage-ok``, ``voltage-bad``, ``recycled``
   * - inspection_robot_1 (``robot``)
     - ``picks-conveyor``, ``hand-free``, ``holding``
   * - inspection_robot_2 (``robot``)
     - ``loads-agv``, ``hand-free``, ``holding``
   * - tester1, tester2 (``tester``)
     - ``tester-free``, ``on-tester``, ``serves``
   * - agv1 (``agv``)
     - ``agv-at``, ``kit-checked``, ``submitted``
   * - s1, s2, s3, s4 (``slot``)
     - ``in-slot``, ``slot-free``
   * - inspection, shipping (``station``)
     - ``agv-at``

- A predicate with two or more parameters links objects.
  ``(holding ?r ?c)`` links a robot and a cell; the table lists it once,
  under the robot.
- The recycling bin is not an object: ``(recycled ?c)`` says a cell is in it.

.. _l6-objects-actions:

The Objects and the Eight Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l6/task1_objects.svg
   :alt: A diagram of the PDDL objects for Task 1 and the eight actions
         between them. Each object is a red box with its type above it. Top
         row, left to right: the cells c1 c2 c3 c4; inspection robot 1;
         tester1 above tester2; inspection robot 2. Below inspection robot 2,
         on the right, a dashed gray box, the recycling bin, which is not an
         object. Bottom row, left to right: the station shipping; agv1, whose
         tray holds four slots s1 to s4; and the station inspection, joined to
         agv1 by a short line. Arrows with numbered tags: 1 from the cells to
         inspection robot 1; 2 from it to each tester; 3 from each tester to
         inspection robot 2; 4 from it down to agv1; 5 from it down to the
         recycling bin. Tag 6 sits at agv1's top left corner, an arrow with
         tag 7 goes from agv1 left to shipping, and tag 8 sits left of
         shipping.
   :width: 100%
   :align: center

- Red: a PDDL object, its type above it. Dashed: the recycling bin, not an
  object.
- The tags are the eight actions:

  1. ``pick-from-conveyor``
  2. ``place-on-tester``
  3. ``pick-from-tester``
  4. ``place-in-slot``
  5. ``recycle``
  6. ``check-kit``
  7. ``move-agv``
  8. ``submit-kit``

.. _l6-one-action:

One Action in Full: ``pick-from-tester``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 42-48
   :caption: lecture6/code/domain.pddl (lines 42 to 48)

**Read it aloud:**

1. Robot ``?r`` can pick cell ``?c`` from tester ``?t`` if it serves that
   tester, the cell is on it, and the robot's hand is free.
2. Afterwards the robot holds the cell, the tester is free, and the hand is
   no longer free.
3. ``(not (on-tester ?c ?t))`` is a **delete effect**: it makes a fact false.

Step 1b: From the Conveyor to a Tester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 26-40
   :caption: lecture6/code/domain.pddl (lines 26 to 40)

``at-door`` means the cell has passed the inspection door, so its inspection
report said "passed" (L5). A cell that fails goes into the inspection bin and
never reaches the planner.

Step 1d: To a Tray Slot or to the Recycling Bin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 50-65
   :caption: lecture6/code/domain.pddl (lines 50 to 65)

``place-in-slot`` needs ``(voltage-ok ?c)`` and the AGV at the inspection
station; ``recycle`` needs ``(voltage-bad ?c)``. So the robots recycle only
cells whose voltage is out of range.

Step 1d: Check the Kit
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 67-73
   :caption: lecture6/code/domain.pddl (lines 67 to 73)

- ``check-kit`` needs a cell in each of the four slots, while the AGV is at
  the inspection station.
- ARIAC's Step 1d says to call this service before moving the AGV. The model
  assumes the answer is "good"; your executor must check the real answer.

Step 1e: Move the AGV and Submit the Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/domain.pddl
   :language: lisp
   :lines: 75-85
   :caption: lecture6/code/domain.pddl (lines 75 to 85)

``move-agv`` works between any two stations. ``submit-kit`` needs a checked
kit and the AGV at shipping.

.. _l6-granularity:

Granularity: One Action per Skill Call or ARIAC Call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65
   :class: compact-table

   * - **PDDL action**
     - **What runs it in the factory**
   * - ``pick-from-conveyor``, ``place-on-tester``, ``pick-from-tester``,
       ``place-in-slot``, ``recycle``
     - A pick or place goal to the course skills package (an action server
       on MoveIt 2)
   * - ``check-kit``
     - ARIAC service ``/agv1/check_kit_quality``
   * - ``move-agv``
     - ARIAC action ``/agv1/move``, which your team calls; it rejects cancel
       requests
   * - ``submit-kit``
     - ARIAC service ``/submit_kitting_order`` (the AGV must be at shipping)

- L7's executor turns each plan step into one behavior tree subtree. GP4's
  agent later uses the same action names.
- The domain has no action that takes a cell off a tray: in ARIAC, cells
  lock to the tray once placed (Step 1d).

.. _l6-mistakes:

Two Modeling Mistakes, Made on Purpose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``mistakes.py`` removes one piece of ``domain.pddl`` in memory (a
precondition of ``submit-kit``, then a delete effect of
``pick-from-conveyor``), plans ``problem.pddl``, and prints the steps that
show the mistake. The full script is on the :doc:`code page <l6_code>`.

.. literalinclude:: outputs/mistakes.txt
   :language: text
   :caption: Output: lecture6/outputs/mistakes.txt

1. Without ``(kit-checked ?a)``, the plan ships and submits an empty tray in
   steps 1 and 2, then comes back. Our first draft of the domain had this
   mistake.
2. Without ``(not (hand-free ?r))``, inspection_robot_1 picks c3 and then c4
   (steps 5 and 6): one gripper holds two cells.

.. warning::

   The planner uses every shortcut the domain allows, and a validator given
   the same broken domain would
   accept both plans. Read the first plan of every new domain against the
   Task 1 steps.


.. _l6-problem:

A PDDL Problem
--------------

This section writes the objects, initial state and goal by hand, and then
generates them from the factory state.

Objects and Fixed Facts for One Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/problem.pddl
   :language: lisp
   :lines: 1-19
   :caption: lecture6/code/problem.pddl (lines 1 to 19)

The objects are the four cells, the two robots, the two testers and
``agv1``. The stations and slots are not listed here: they are the domain's
constants.

The Changing Facts and the Goal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/problem.pddl
   :language: lisp
   :lines: 20-30
   :caption: lecture6/code/problem.pddl (lines 20 to 30)

- The goal names specific cells and slots. In GP3, a selection step decides
  which ones (:ref:`l6-selection`).
- The cells have not been tested yet, so ``voltage-ok`` is an assumption. If
  a reading says otherwise, the executor stops and asks for a new plan (L7).

Where Each Fact Comes From in ARIAC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65
   :class: compact-table

   * - **Fact**
     - **Source**
   * - ``agv-at``
     - ``/agv1/info`` (``AgvStatus``: the AGV's station)
   * - ``slot-free``
     - ``/agv1/tray_status`` (four occupied flags)
   * - ``on-tester``, ``tester-free``
     - Your team's records of where it placed each cell
   * - ``voltage-ok``, ``voltage-bad``
     - Averaged readings from ``/voltage_tester_1/voltage`` and
       ``/voltage_tester_2/voltage``
   * - ``at-door``
     - Your team's inspection results (L5): cells with a passing report
   * - ``serves``, ``picks-conveyor``, ``loads-agv``
     - Fixed: the same in every trial

.. important::

   The domain file never changes. A Python **problem generator** writes a new
   problem file from these sources, so the same domain serves every trial,
   including the unseen trial of the final demo.

.. _l6-generator:

A Problem Generator: the Factory State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/gen_problem.py
   :language: python
   :lines: 9-18
   :caption: lecture6/code/gen_problem.py (lines 9 to 18)

- ``STATE`` is a stand-in for what a team's node reads from ARIAC and from
  its own records. The values are chosen for this example.
- A fifth cell, c5, sits on tester2. Its averaged reading, 3.86 V, is above
  3.8 V.

A Problem Generator: Voltages and Goals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/gen_problem.py
   :language: python
   :lines: 39-50
   :caption: lecture6/code/gen_problem.py (lines 39 to 50)

1. A cell with no reading yet, or a reading from 3.4 V to 3.8 V, gets
   ``voltage-ok``.
2. A cell outside that range gets ``voltage-bad``, and the goal says it must
   end up recycled.
3. The cells chosen for each kit become ``in-slot`` goals, plus
   ``submitted``.

The Generated Problem Gives a Plan with a Recycle Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/gen_problem.txt
   :language: text
   :lines: 1-8
   :caption: Output: lecture6/outputs/gen_problem.txt (first 7 of 21 steps)

- inspection_robot_2 clears c5 from tester2 to the recycling bin (steps 3
  and 5) while inspection_robot_1 starts on c1 and c2.
- The rest of the plan matches the four-cell plan: 21 steps, the 19 of the
  four-cell plan plus 2 for c5 (one pick, one recycle).
- The generated file is ``outputs/problem_generated.pddl``. Both files are on
  the :doc:`code page <l6_code>`.


.. _l6-planner:

Running a Planner
-----------------

This section runs Fast Downward, from the command line and from Python
through the Unified Planning Framework.

.. _l6-install:

Installing the Planner in a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **virtual environment** (venv) is a folder with its own Python and
packages, kept apart from the system Python. The **Unified Planning
Framework (UPF)** is a Python library that reads PDDL, runs planners and
checks plans; up-fast-downward adds Fast Downward to it.

.. code-block:: console

   python3 -m venv ~/venvs/planning
   ~/venvs/planning/bin/pip install unified-planning up-fast-downward

The versions used for every output in this lecture:

.. literalinclude:: outputs/versions.txt
   :language: text
   :caption: lecture6/outputs/versions.txt

- The up-fast-downward package ships a built Fast Downward, so there is
  nothing to compile.
- The UPF installation page lists Python 3.8 to 3.11; every demo here ran on
  Python 3.12.3 (Ubuntu 24.04).
- ``pip install unified-planning[fast-downward]``, the form on the
  up-fast-downward page, installed up-fast-downward 0.5.2 instead. Use the
  two-package command above.

Fast Downward: Translate, Then Search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Fast Downward** is a classical planner. It runs in two stages:

1. The **translator** grounds the PDDL: it writes out actions with concrete
   objects in place of their parameters. Each result is a **ground action**,
   such as ``check-kit agv1 c1 c2 c3 c4``.
2. It drops only the ground actions that a quick **relaxed** test rules out.
   The test ignores every delete effect, so a fact, once true, stays true.
   The help text of the translator's ``--relaxed`` option says the same:
   "output relaxed task (no delete effects)".
3. The **search** looks for a plan over the ground actions that are left and
   writes it to a file, ``sas_plan`` by default.

Fast Downward's documentation (`Problem transformations performed by the
planner <https://www.fast-downward.org/latest/for-developers/problem-transformations/>`_)
states the rule: "The translator can prune facts and actions that are not
relaxed reachable from the initial state or that are not relevant to the
goal in the sense that they never contribute to an irreducible plan."

So the ground actions that are left are not all usable. With delete effects
ignored, c1 stays held after it is placed, so it can fill every slot:
``check-kit agv1 c1 c1 c1 c1`` passes the test and stays, though it can
never apply. In the small problem, 232 of the 256 ``check-kit`` ground
actions repeat a cell like this (:ref:`l6-many-objects`). The test does drop
what it can rule out: ``place-in-slot`` keeps 16 of its 2 × 4 × 1 × 4 = 32
combinations, because only inspection_robot_2 has ``loads-agv``, and
``recycle`` keeps none of its 2 × 4 = 8, because no cell has
``voltage-bad``.

Running Fast Downward from the Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Optimal (A* with the LM-cut heuristic) and satisficing (LAMA, first
plan):**

.. code-block:: console

   fast-downward.py domain.pddl problem.pddl --search "astar(lmcut())"
   fast-downward.py --alias lama-first domain.pddl problem.pddl

- **LM-cut** (landmark cut, Helmert and Domshlak, 2009) is a heuristic that
  Fast Downward's documentation lists as admissible, so A* with it returns a
  shortest plan.
- **LAMA** is a satisficing planner built on **landmarks**: facts every plan
  must make true. The ``lama-first`` alias runs greedy search with two
  heuristics (FF, the length of a plan found with delete effects ignored,
  and a count of landmarks not yet reached) and stops at the first plan.

``fast-downward.py`` is in the up-fast-downward package folder, under
``downward/``. ``run_all.sh`` finds it and runs the first command on two
problems (:ref:`l6-many-objects`).

Planning from Python with the Unified Planning Framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UPF reads PDDL files (or builds problems in Python code) and calls planners
such as Fast Downward through one interface.

.. literalinclude:: code/plan_kit.py
   :language: python
   :lines: 11-23
   :caption: lecture6/code/plan_kit.py (lines 11 to 23)

- ``OneshotPlanner(name="fast-downward")`` runs the ``lama-first`` setup;
  ``"fast-downward-opt"`` runs A* with LM-cut.
- UPF can also build a problem from Python objects instead of text, which
  removes string-formatting bugs from a generator.

The Plan: Status and the First 10 Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/plan_kit.txt
   :language: text
   :lines: 1-12
   :caption: Output: lecture6/outputs/plan_kit.txt (lines 1 to 12)

15 objects: 4 cells, 2 robots, 2 testers, 1 AGV, and the domain's 2
stations and 4 slots (4 + 2 + 2 + 1 + 2 + 4 = 15). The 5 goal facts are the
four ``in-slot`` facts and ``(submitted agv1)``.

.. dropdown:: The full output (19 steps)
   :class-container: sd-border-secondary

   .. literalinclude:: outputs/plan_kit.txt
      :language: text
      :caption: lecture6/outputs/plan_kit.txt

.. _l6-timeline:

The 19 Steps, One Row per Robot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Steps 1 to 10:**

.. image:: /_static/images/l6/plan_timeline_1.svg
   :alt: A chart of steps 1 to 10 of the 19-step plan for the four-cell
         problem. Three rows, tagged 1 for inspection robot 1, 2 for
         inspection robot 2 and 3 for agv1. The x axis is the plan step, an
         order and not a time, and the y axis, labeled who acts, holds the
         rows; each step is one box in the row of the robot that acts. Row 1:
         pick c1 (step 1), place c1 on t1 (2), pick c2 (3), place c2 on t2
         (4), pick c3 (5), place c3 on t1 (8), pick c4 (9). Row 2: pick c1
         from t1 (6), place c1 in s1 (7), pick c3 from t1 (10). Row 3 is
         empty. Only one box appears in each column.
   :width: 100%
   :align: center

**Steps 11 to 19:**

.. image:: /_static/images/l6/plan_timeline_2.svg
   :alt: A chart of steps 11 to 19 of the 19-step plan for the four-cell
         problem, with the same three rows and axis as the chart of steps 1 to
         10. Row 1, inspection robot 1: place c4 on t1 (step 12). Row 2,
         inspection robot 2: place c3 in s3 (11), pick c4 from t1 (13), place
         c4 in s4 (14), pick c2 from t2 (15), place c2 in s2 (16). Row 3,
         agv1: check (17), move to shipping (18, its box reads move ship),
         submit (19). Only one box appears in each column.
   :width: 100%
   :align: center

- Drawn from ``outputs/plan.txt``. Rows: 1 inspection_robot_1, 2
  inspection_robot_2, 3 agv1. t1, t2: tester1, tester2.
- Each line of the plan is a **ground action**, an action name with its
  arguments. In L7, each one becomes a behavior tree subtree.
- One step per column: a classical plan is a single sequence, even when the
  two robots could work at the same time (steps 5 and 6).
- inspection_robot_2 fills slots s3, s4 and then s2; agv1 acts only in the
  last three steps.
- c2 waits on tester2 from step 4 to step 15. The model has no time, so it
  sees no cost in that.

.. _l6-compare:

Satisficing Against Optimal, on a Small and a Large Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/compare_planners.txt
   :language: text
   :caption: Output: lecture6/outputs/compare_planners.txt

1. The large problem has 8 cells and 2 AGVs
   (``outputs/problem_large.pddl``, written by ``make_problem()`` from a
   stand-in state).
2. On both problems, the satisficing plan is as short as the optimal one: 19
   and 38 steps.
3. On the large problem, the optimal planner took 14.78 s and the satisficing
   one 0.56 s: 14.78 / 0.56 = 26.4 times longer, for no shorter plan.
4. Times are wall-clock seconds for one run on the course machine. They
   vary: in six more runs (2026-10-18, on a PC under other load), the
   optimal planner took 22.5 to 25.2 times as long as the satisficing one.

.. important::

   In a factory, a good plan now usually beats the best plan later: the
   executor waits while the planner searches.


.. _l6-checking:

Checking a Plan
---------------

This section covers what a valid plan is, a validator rejecting a broken
plan, and why valid is not the same as working.

What a Validator Checks
~~~~~~~~~~~~~~~~~~~~~~~

- A plan is **valid** if each action's preconditions hold in the state
  reached so far, and the goal holds after the last action.
- A **validator** checks this by replaying the plan on the model, one action
  at a time.
- UPF has one (``PlanValidator``). VAL is the standard stand-alone validator
  for PDDL (`github.com/KCL-Planning/VAL
  <https://github.com/KCL-Planning/VAL>`_).

**Plans from other sources need checking.** A plan file can be edited by hand, or
come from another program. In GP4, plans come from an LLM agent, and code
must check them before any robot moves (L8).

Validating the Plan and an Edited Copy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/validate_plan.py
   :language: python
   :lines: 14-29
   :caption: lecture6/code/validate_plan.py (lines 14 to 29)

Lines 11 and 12 (not shown) make ``reader``, a PDDL reader, and read
``domain.pddl`` and ``problem.pddl`` into ``problem``. The edit swaps steps 6
and 7 of ``outputs/plan.txt`` (list items 5 and 6, counting from 0), so
inspection_robot_2 places c1 before it picks it.

The Validator Rejects the Edited Plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/validate_plan.txt
   :language: text
   :caption: Output: lecture6/outputs/validate_plan.txt

1. The planner's plan is ``VALID``.
2. The edited plan is ``INVALID``: step 6 is ``place-in-slot`` for c1, and
   its precondition ``holding(inspection_robot_2, c1)`` is false, because the
   pick now comes after it.
3. The validator names the first step that fails and the precondition that
   does not hold, so you know where to look.

.. _l6-valid-not-working:

Valid in the Model Is Not the Same as Working in the Factory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **The model has no time.** It does not know that the conveyor keeps
  moving, or that a tester needs about a second to give ten readings (L5).
- **The model has no geometry.** It does not know that inspection_robot_1 and
  inspection_robot_2 can collide near the testers. The course skills package
  keeps the two robots out of the tester area at the same time.
- **The model is only as true as its facts.** If tester2 malfunctions,
  ``(tester-free tester2)`` can be true in the problem and useless in the
  factory.

**Plan quality measures:**

- Validity, plan length, plan cost and planning time. In L6 every action
  costs 1, so a plan's cost is its length.
- GP4 compares its LLM agent with this planner on the same trials by
  validity, plan length, cost and latency. In GP4, "cost" means the tokens
  or dollars the model uses, not plan cost.


.. _l6-strains:

Where PDDL Strains
------------------

This section covers numbers (the kit voltage window) and many objects.

.. _l6-kit-rule:

The Kit Rule, and a Kit That Cannot Be Finished
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The rule (ARIAC Scenario page; CellTypes.msg):**

1. A Li-Ion kit must total 4 × 3.6 = 14.4 V, plus or minus 0.15 V: from
   14.25 V to 14.55 V.
2. Each cell must be 3.6 V plus or minus 0.2 V: from 3.4 V to 3.8 V.

**Worked example: three cells at 3.75 V are on the tray.**

1. The tray holds 3 × 3.75 = 11.25 V.
2. The fourth cell must be at least 14.25 − 11.25 = 3.00 V and at most
   14.55 − 11.25 = 3.30 V.
3. Every acceptable cell is at least 3.4 V, so no fourth cell can complete
   the kit.
4. Cells lock to the tray, so the kit is lost: the AGV goes to the recycling
   station (Step 1e), where the tray is cleared.
5. This tray needs a team with no check. GP1's check, before every place,
   refuses the third cell: three cells must total 14.25 − 3.8 = 10.45 V to
   14.55 − 3.4 = 11.15 V, and 11.25 V is above 11.15 V.

Every Cell Placed Narrows the Window for the Rest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Worked example: two cells at 3.75 V are on the tray.**

1. The tray holds 2 × 3.75 = 7.5 V.
2. The last two cells must add up to between 14.25 − 7.5 = 6.75 V and
   14.55 − 7.5 = 7.05 V.
3. Each of them is at least 3.4 V, so neither can be above
   7.05 − 3.4 = 3.65 V.
4. A cell at 3.70 V is in range on its own, yet it would make the kit
   impossible to finish. GP1's check refuses it: 7.5 + 3.70 = 11.20 V, above
   11.15 V.

.. important::

   The choice of a cell must look ahead to the cells still to come, before
   the cell is placed: GP1's check before every place. That is arithmetic on
   sums of voltages.

Classical PDDL Has No Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Our domain has only true-or-false facts. ``voltage-ok`` says a cell is in
  range; it cannot say 3.75 V, or add four voltages.
- PDDL 2.1 adds **numeric fluents**: values such as a kit's total voltage
  that actions can increase.
- Fast Downward does not plan with them. Its PDDL support page says it
  "aims to support PDDL 2.2 level 1 plus the :action-costs requirement from
  PDDL 3.1", and lists "All aspects of numerical planning" as unsupported,
  with one exception: "some numerical features are part of the
  :action-costs requirement of PDDL 3.1, and these are supported by the
  planner."

.. literalinclude:: code/kit_numeric.pddl
   :language: lisp
   :lines: 8-13
   :caption: lecture6/code/kit_numeric.pddl (lines 8 to 13)

``total`` and ``placed`` are numeric fluents of the AGV; ``volts`` is a
number per cell. The problem file, ``kit_numeric_problem.pddl``, asks for 4
cells with a total from 14.25 V to 14.55 V.

Fast Downward Refuses the Numeric Kit Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/numeric_try.txt
   :language: text
   :caption: Output: lecture6/outputs/numeric_try.txt (from numeric_try.py)

1. UPF sees numeric features in the problem and warns that it cannot tell
   whether Fast Downward can solve it.
2. Fast Downward's translator stops at the ``:requirements`` line:
   ``:numeric-fluents`` is not on its list. No plan comes back.
3. A numeric planner (ENHSP is one UPF engine) could take this problem, but
   numeric search is harder, and the course does not use one.

.. _l6-selection:

The Selection Step in Plain Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **selection step** decides which measured cell goes to which slot,
before the problem is written. It uses the window arithmetic above.

.. literalinclude:: code/select_cells.py
   :language: python
   :lines: 15-25
   :caption: lecture6/code/select_cells.py (lines 15 to 25)

- Lines 8 to 12 compute the limits from the ``CellTypes.msg`` values:
  ``LOW`` = 3.6 − 0.2 = 3.4 V, ``HIGH`` = 3.6 + 0.2 = 3.8 V,
  ``KIT_LOW`` = 4 × 3.6 − 0.15 = 14.25 V, ``KIT_HIGH`` = 4 × 3.6 + 0.15 =
  14.55 V.
- ``window`` gives the range for the sum of the cells still to place.
- ``can_finish`` asks: with the cells left to place, each from 3.4 V to
  3.8 V, can the total still land in that range?

Placing Cells as They Arrive, Without Look-Ahead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/select_cells.txt
   :language: text
   :lines: 1-7
   :caption: Output: lecture6/outputs/select_cells.txt (lines 1 to 7)

1. The first two lines repeat the two worked examples: after three cells at
   3.75 V the kit cannot be finished; after two it can.
2. Cells c1 to c6 arrive measured, one at a time (voltages chosen for this
   example).
3. Without look-ahead, every in-range cell goes on agv1. After c3, the tray
   holds 3.75 + 3.78 + 3.72 = 11.25 V, and the kit is lost. GP1's check
   would have refused c3 (11.25 V is above 11.15 V); this run has no check.

Placing Cells as They Arrive, With Look-Ahead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/select_cells.txt
   :language: text
   :lines: 8-19
   :caption: Output: lecture6/outputs/select_cells.txt (lines 8 to 19)

1. The look-ahead is GP1's check. c3 would bring three cells to 11.25 V,
   above 11.15 V, leaving 3.00 V to 3.30 V for the last cell, so it goes to
   agv2 for the next kit. c4 (3.86 V) is out of range: recycling.
2. c5 and c6 fill agv1: 3.75 + 3.78 + 3.45 + 3.52 = 14.50 V, inside
   14.25 V to 14.55 V by the averages. The goal lines go to the problem
   generator.
3. ARIAC checks the true voltages; your team knows only averages of noisy
   readings. The next section asks how safe 14.50 V is.

.. _l6-against-chance:

The Look-Ahead Kit Against Chance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``kit_margin.py`` measures how far the look-ahead kit sits from ARIAC's
limits, in standard deviations (sd) of the team's averages, and how often
ARIAC's check would reject it.

.. literalinclude:: outputs/kit_margin.txt
   :language: text
   :caption: Output: lecture6/outputs/kit_margin.txt (from kit_margin.py)

1. ARIAC's voltage tester adds normal noise with an sd of 0.05 V to each
   reading (``noise_std_dev`` in ``ariac_gz/models/voltage_tester/model.sdf``).
   An average of 10 readings has an sd of 0.05 / :math:`\sqrt{10}` =
   0.016 V (L5). The kit total is a sum of four such averages; for
   independent errors the variances add, so its sd is
   :math:`\sqrt{4}` × 0.016 = 2 × 0.016 = 0.032 V.
2. c2 sits only 0.02 V, or 1.3 sd, below 3.8 V, and the total only 0.05 V, or
   1.6 sd, below 14.55 V. c1 and c5 are 3.2 sd from their limits.
3. ARIAC's kit check uses the true voltages: each cell within 0.2 V of 3.6 V
   and the total within 0.15 V of 14.4 V
   (``agv_tray_interface_plugin.cpp``, ``check_kit_quality``).
4. **Model 1:** each true voltage is its average plus a normal error with an
   sd of 0.016 V, independent from cell to cell. The script draws one
   million such kits and applies ARIAC's check: 13.9 % fail, about 1 in 7.
5. **Model 2** also uses how ARIAC makes the cells: its cell feed draws each
   true voltage around 3.6 V with an sd of 0.1 V
   (``voltage_std_dev`` in
   ``ariac_plugins/include/ariac_plugins/cell_feed_plugin.hpp``). That
   pulls a high reading's likely true voltage back toward 3.6 V, so fewer
   kits fail: 9.3 %.

.. important::

   So 14.50 V is in range by the averages, not a safe kit: ARIAC would
   reject it about 1 time in 7 to 1 time in 11. Keep each cell and the
   total a few sd inside the limits.

.. _l6-many-objects:

Many Objects: Ground Actions Multiply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/ground_actions.txt
   :language: text
   :caption: Output: lecture6/outputs/ground_actions.txt

1. Small is ``problem.pddl``. ``check-kit`` has four cell parameters. With 4
   cells there are 4 × 4 × 4 × 4 = 256 ways to fill them: 256 of the 311
   ground actions.
2. A cell fills at most one slot: no action takes a cell off a tray or picks
   it up again. So only 4 × 3 × 2 × 1 = 24 of the 256 can ever apply. The
   translator's relaxed test keeps the other 232, which repeat a cell, such
   as ``check-kit agv1 c1 c1 c1 c1``.
3. Large has 8 cells and 2 AGVs: 2 × 8 × 8 × 8 × 8 = 8192 of the 8334.
4. Doubling the cells and the AGVs took A* with LM-cut from 124 to 2346
   expanded states (``outputs/fd_summary.txt``). The full
   ``fd_summary.txt`` is on the :doc:`code page <l6_code>`, under "Run
   everything".

.. important::

   Keep only the cells that matter for the current kit, and few parameters
   per action: a per-slot fact ``(filled ?a ?s)`` would let ``check-kit``
   take only the AGV.


.. _l6-gp3:

PDDL in GP3
-----------

This section covers the GP3 pipeline: numbers in Python, order in PDDL.

The GP3 Pipeline: Numbers in Python, Order in PDDL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l6/gp3_pipeline.svg
   :alt: A block diagram of the GP3 pipeline in two rows. Top row, left to
         right: a gray box Factory state; a white box Selection with tag 1; a
         white box Generator with tag 2; a white box Planner with tag 3, which
         also takes an arrow from a gray box Domain on its right. An arrow
         goes down from the planner to a gray box Plan. Bottom row, right to
         left: Plan, a white box Plan-to-BT with tag 4, a white box Behavior
         tree, and a white box Factory. An arrow goes up from the factory to
         Factory state, closing the loop.
   :width: 100%
   :align: center

1. Selection: which cell goes in which slot (Python, the voltage window).
2. Generator: writes ``problem.pddl`` from the factory state.
3. Planner: Fast Downward, with the fixed domain file.
4. Plan-to-BT: one subtree a step (L7); the behavior tree calls the skills.

Gray: files and data; white: programs and the factory. Numbers stay in
ordinary code; PDDL orders the actions.

**Class discussion:** which facts about the ARIAC factory can PDDL state, and
which can it not? Name examples from Task 1 and the four challenges (conveyor
malfunction, voltage tester malfunction, vacuum tool malfunction,
high-priority orders).


.. _l6-next:

Next Class
----------

**Quiz 3 (Wednesday, March 10, start of class)**

- Closed notes, on ELMS-Canvas or paper, covering L5 and L6.
- From this lecture: PDDL domains and problems, planners, plan validity, and
  where PDDL strains.

**L7: Plan Execution Patterns with Behavior Trees**

- A plan-to-BT factory turns this lecture's plans into trees, adds retry and
  timeout, and defines the triggers that stop a plan and ask for a new one.
- GP2 is due, and GP3 (PDDL planner and BT executor) is posted.

**Before next class**

- Install the planner in a virtual environment, run the L6 scripts from
  ``lecture6/code/`` with ``VENV=~/venvs/planning bash run_all.sh``, and
  compare your outputs with the notes
  (:doc:`code page <l6_code>`).
