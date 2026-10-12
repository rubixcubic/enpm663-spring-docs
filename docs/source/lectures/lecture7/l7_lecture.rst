====================================================
Lecture
====================================================

.. note::

   These notes follow the L7 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running ``lecture7/code/run_all.sh`` on 2026-10-12, with
   Python 3.12.3, ``py_trees`` 2.6.0 and BehaviorTree.CPP 4.10.0. The demos use
   **mock skills**: small Python stand-ins for the course skills package and
   for ARIAC, with no ROS communication and no simulator. The scripts and how
   to run them are on the :doc:`code page <l7_code>`.


.. _l7-recap:

Recap
-----

From L6
~~~~~~~

- A **plan** is a list of **ground actions**. A ground action is an action
  name with its arguments filled in by real objects, such as
  ``(pick-from-tester inspection_robot_2 c3 tester1)``.
- A classical planner assumes three things: it sees the whole world, every
  action works, and only the robots change the world. The ARIAC factory
  breaks all three. So a plan is used for a short time, and made again when
  the factory no longer matches it.

Today's Question
~~~~~~~~~~~~~~~~

How does a behavior tree run a plan that it did not write, and what does it
do when the plan stops matching the factory?

Today
~~~~~

Quiz 3 (L5 and L6) opened the class. GP2 is due today, and GP3 is posted.


.. _l7-plan-driven-tree:

A Plan-Driven Tree
------------------

In GP1 your tree had a fixed order. In GP3 the tree is built from a plan.

Who Decides the Order of the Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 38 38
   :class: compact-table

   * -
     - **GP1**
     - **GP3**
   * - Who fixes the order
     - Your team, when it writes the tree
     - The planner, at run time
   * - When the tree is built
     - Once, in your code
     - From each new plan, then ticked
   * - A change of order needs
     - An edit to the code
     - A new plan

This is the three-layer architecture from L2:

- **Deliberative** layer (the planner): decides what to do.
- **Executive** layer (the tree): runs each step and watches for trouble.
- **Reactive** layer (the skills and controllers): moves the robots.

The Contract Between the Planner and the Executor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **executor** is the code that runs a plan: it builds the tree and ticks
it. The planner and the executor agree on three things:

1. The plan is a list of ground actions: each one is an action name and its
   arguments.
2. The executor knows how to run every action name that the domain defines.
3. Nothing else passes between them.

The same contract holds in GP4. The LLM agent of L8 writes the same action
names and arguments, and the same executor runs them. The action names are
designed once, in the L6 domain: ``pick-from-conveyor``, ``place-on-tester``,
``pick-from-tester``, ``place-in-slot``, ``recycle``, ``check-kit``,
``move-agv``, ``submit-kit``.

.. important::

   Write the GP3 executor so it does not care where a plan came from. In L8 a
   different program writes the plans, and the executor stays the same.


.. _l7-factory:

The Plan-to-BT Factory
----------------------

This section covers a registry from action names to subtree builders, and the
guard, act, verify pattern for one plan step.

.. note::

   Every output in this lecture comes from running
   ``lecture7/code/run_all.sh`` on 2026-10-12 (Python 3.12.3, ``py_trees``
   2.6.0, BehaviorTree.CPP 4.10.0). The demos use mock skills: no ROS
   communication and no simulator. The code is in the Week 7 module, and on
   the :doc:`code page <l7_code>`.

A Registry Turns Each Action into a Subtree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l7/plan_to_tree.svg
   :alt: Three panels from left to right. Tag 1: a plan of three ground
         actions: pick-from-tester inspection_robot_2 c3 tester1;
         place-in-slot inspection_robot_2 c3 agv1 s3; move-agv agv1
         inspection shipping. An arrow leads to tag 2: a registry listing the
         action names pick-from-tester, place-in-slot, move-agv and more. An
         arrow leads to tag 3: a tree whose root is a Sequence with memory and
         whose three children are step 1, step 2 and step 3. Under each step
         are four small squares: blue, red, blue and green.
   :width: 100%
   :align: center

1. A plan of three ground actions (chosen for this example).
2. The **registry**: a dictionary from each action name to a builder
   function.
3. The tree: a Sequence with memory holding one subtree per action. Each
   small square is a leaf of a subtree: blue leaves check, red leaves act,
   green leaves write the blackboard.

Two words carry this section:

- A **builder** takes the action's arguments and returns a subtree.
- The **plan-to-BT factory** looks up each action's name in the registry and
  calls its builder, in plan order.

The Registry in Code
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/executor.py
   :language: python
   :lines: 237-244
   :caption: lecture7/code/executor.py (excerpt)

- Each ``build_...`` function is a builder. The ``place-in-slot`` builder is
  shown below.
- ``check-voltage`` is the measurement step that L6 described as an action
  whose result is not known in advance. The name is an example for this
  lecture.
- ``RETRIES`` lists the actions that get a Retry decorator. It starts empty;
  the :ref:`Retry section <l7-retry>` fills it.

The Factory Function
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/executor.py
   :language: python
   :lines: 247-260
   :caption: lecture7/code/executor.py (excerpt)

- The root is a Sequence with memory that holds the subtrees in plan order.
- An action name with no builder raises an error when the tree is built,
  before any robot moves.

.. _l7-memory:

Why the Root Is a Sequence with Memory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``py_trees`` 2.6.0 the constructor is
``py_trees.composites.Sequence(name, memory, children)``. The ``memory``
argument has no default: you must give it.

- **With memory**, a Sequence resumes at the child that was RUNNING on the
  last tick. Finished steps are not run again.
- **Without memory**, a Sequence ticks its children from the first one on
  every tick. A finished step runs again. The
  :ref:`Debugging section <l7-debugging>` shows what this does to a plan.
- After a child fails, both kinds start again from the first child the next
  time they are ticked.

Mapping PDDL Arguments to ROS Goals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A builder turns PDDL object names into the names and numbers that ARIAC and
the course skills expect.

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **PDDL object**
     - **What the executor sends**
   * - ``agv1``
     - The ARIAC action ``/agv1/move``; the goal field ``agv`` 1 of the
       ``place_in_slot`` skill
   * - ``shipping``
     - ``station_id`` 3 (``AgvStations.msg``: ``INSPECTION`` 1,
       ``ASSEMBLY`` 2, ``SHIPPING`` 3, ``RECYCLING`` 4)
   * - ``tester1``
     - The goal field ``tester`` 1 of the ``pick_from_tester`` skill
   * - ``s3``
     - The goal field ``slot`` 3 of the ``place_in_slot`` skill

.. literalinclude:: code/executor.py
   :language: python
   :lines: 160-165
   :caption: lecture7/code/executor.py (excerpt)

``number`` strips the letters a, g, v, s, t, e and r from the start of the
name and keeps the digits, so ``agv1`` gives 1 and ``tester2`` gives 2.

.. _l7-guard-act-verify:

Guard, Act, Verify, Update: One Plan Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **blackboard** of the executor holds its own view of the factory, as a
set of PDDL facts. Each plan step is a Sequence with memory and four leaves.

.. image:: /_static/images/l7/guard_act_verify.svg
   :alt: A tree for one plan step. At the top, a Sequence with memory. Under
         it, four leaves from left to right: guard (blue), act (red), verify
         (blue) and update (green). Below the act and verify leaves is a box
         labeled skills package and ARIAC; along the bottom is a box labeled
         blackboard, the executor's facts. Tag 1: an arrow from the
         blackboard up to the guard. Tag 2: an arrow from the act down to the
         skills box, and one back up. Tag 3: an arrow from the skills box up
         to the verify. Tag 4: an arrow from the update down to the
         blackboard.
   :width: 90%
   :align: center

1. The **guard** reads the action's preconditions from the blackboard.
2. The **act** sends a goal to a skill or an ARIAC action and gets the
   result.
3. The **verify** reads an ARIAC topic to check the effect.
4. The **update** writes the action's effects to the blackboard.

The leaves run left to right. The update runs only after the verify
succeeds.

The Four Leaves for place-in-slot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Guard:** the robot holds the cell, the cell's voltage is in range, the
   slot is free, and the AGV is at the inspection station.
2. **Act:** send the ``place_in_slot`` goal. The leaf returns RUNNING until
   the result arrives. In GP3, ``py_trees_ros.action_clients.FromConstant``
   or ``FromBlackboard`` is this leaf.
3. **Verify:** ``/agv1/tray_status`` shows the slot occupied.
4. **Update:** write the effects: the cell is in the slot, the hand is free,
   the slot is not free.

Why have both a guard and a verify? The blackboard is the executor's own view
of the factory. The guard catches a step whose facts are no longer true
before the robot moves. The verify catches a step whose effect did not
happen. A failing guard or verify is the signal that the
:ref:`replanning triggers <l7-replanning>` act on.

The place-in-slot Builder
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/executor.py
   :language: python
   :lines: 153-157,179-189
   :caption: lecture7/code/executor.py (excerpt)

``needs``, ``add`` and ``delete`` are the precondition and the effects of
``place-in-slot`` in the L6 domain, except ``(loads-agv ?r)``: which robot
loads the AGV never changes, so the guard does not check it. In the mock, ``slot_occupied`` stands in
for ``/agv1/tray_status``.

.. _l7-demo1:

Demo 1: A Five-Step Plan Becomes a Tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``demo_factory.py build`` prints the plan and the tree the factory builds
from it.

.. literalinclude:: outputs/factory_build.txt
   :language: text
   :caption: Output of demo_factory.py build

**The starting state (chosen for this example).**

- Slots ``s1`` and ``s2`` of ``agv1`` were filled earlier. Cell ``c3`` waits
  on ``tester1`` and ``c4`` on ``tester2``; both were measured in range
  (3.62 V and 3.55 V).
- Each mock skill returns its result on its second tick; the mock AGV move,
  on its third.

Demo 1: The Tree After Two Ticks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/factory_tick.txt
   :language: text
   :caption: Output of demo_factory.py tick

- ``py_trees.display.ascii_tree(root, show_status=True)`` prints the tree.
  ``[o]`` means SUCCESS, ``[*]`` means RUNNING, and ``[-]`` means not ticked
  yet. The text after a leaf is its feedback message.
- The program cuts the print after step 2; steps 3 to 5 show ``[-]`` on every
  node.

Demo 1: The Tick Trace
~~~~~~~~~~~~~~~~~~~~~~

A **tick trace** is a log line for every status change of a step, with the
tick number.

.. literalinclude:: outputs/factory_trace.txt
   :language: text
   :caption: Output of demo_factory.py trace

1. On each tick, the root ticks only the running step. An act leaf returns
   RUNNING while its robot moves, so each tick returns at once and the
   executor stays responsive (the L1 executor lesson).
2. A step that finishes hands over to the next step in the same tick, so
   steps 1 to 4 end on ticks 2 to 5. The move takes three ticks (5, 6, 7).
3. One goal per step: 5 steps, 5 goals.

Demo 1: An Unknown Action Name Fails at Build Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``demo_factory.py unknown`` builds the same plan with ``move-agv`` misspelled
as ``move-avg`` in step 5.

.. literalinclude:: outputs/factory_unknown.txt
   :language: text
   :caption: Output of demo_factory.py unknown

- The registry has no builder for ``move-avg``, so the factory stops before
  it returns a tree.
- No goal was sent: the error appears before any robot moves, not after four
  cells are on the tray.
- An LLM agent in GP4 can also return a name the domain does not define. The
  same check catches it.


.. _l7-retry-timeout:

Retry and Timeout
-----------------

A **decorator** is a node with one child that changes the child's result.
This section covers two decorators that tolerate a failure, the ARIAC case for
each, and the order in which to nest them.

.. _l7-retry:

Retry: Run the Child Again After a Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The constructor is ``py_trees.decorators.Retry(name, child, num_failures)``.

- When the child fails, Retry returns RUNNING and starts the child again on
  the next tick.
- After ``num_failures`` failures, Retry returns FAILURE. With
  ``num_failures=3``, the child gets three attempts in all.
- Use it when a second attempt can succeed with the world unchanged.

.. literalinclude:: code/executor.py
   :language: python
   :lines: 255-257
   :caption: lecture7/code/executor.py (excerpt of build_tree)

Retry wraps the whole subtree, so the guard checks the preconditions again
before each new attempt.

Demo 2: Retry Absorbs Two Failed Picks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``demo_retry.py``, the mock pick answers ``GRASP_FAILED`` a set number of
times, then succeeds. ``demo_retry.py 2`` makes it fail twice.

.. literalinclude:: outputs/retry_2.txt
   :language: text
   :caption: Output of demo_retry.py 2 (the mock pick fails twice, then succeeds)

1. ``RETRIES["pick-from-tester"] = 3``. The plan is two steps: pick ``c3``
   from ``tester1``, place it in ``s3``.
2. The subtree fails on ticks 2 and 4; Retry stays RUNNING, so the plan does
   not see these failures.
3. 4 goals: 3 pick attempts and 1 place.

Demo 2: Retry Runs Out After Three Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/retry_3.txt
   :language: text
   :caption: Output of demo_retry.py 3 (the mock pick fails three times)

The third failure is the last one Retry allows, so Retry fails, and the plan
fails with it. The place step never starts.

.. important::

   Retries are always bounded. After the last failure, the failure goes up the
   tree, where it becomes a replanning trigger or a stop.

ARIAC Case for Retry: The Vacuum Tool Malfunction (Task 2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What ARIAC 2025 does.**

- One chosen grasp attempt of ``assembly_robot_2``'s vacuum tools (VG_2 or
  VG_4) fails. The trial file sets which attempt with ``GRASP_OCCURRENCE``.
- The Challenges page asks teams to detect the failure, move the gripper away
  from the part, and try the grasp again.
- The plugin clears the failure only after every suction cup has lost contact
  (``vacuum_tool_plugin.cpp``). So the retried subtree must move the gripper
  away before it grasps again.

**What the course skills package does.**

- A skill never retries a task step itself, so failures and challenges reach
  your code. After a failure it keeps what it holds and lifts to a safe
  height, so a retry starts from a known state (skills package design, still
  in progress).
- The final demo tests this challenge; GP4 does not.

Timeout: Fail a Child That Runs Too Long
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The constructor is ``py_trees.decorators.Timeout(name, child, duration)``.

- ``duration`` is in seconds (default 5.0). When Timeout starts, it notes the
  time at which the limit ends.
- On a tick after that time, if the child is still RUNNING, Timeout stops the
  child and returns FAILURE.
- Timeout checks the clock only when it is ticked, so it fires up to one tick
  period late.

.. important::

   A leaf that waits for a message never fails on its own: it stays RUNNING.
   Timeout turns this silence into a FAILURE that the tree can act on.

ARIAC Case for Timeout: The Voltage Tester Malfunction (Task 1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation and the code of ARIAC 2025 describe this challenge
differently.

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **Source**
     - **What a malfunctioning tester does**
   * - Challenges page
     - "One or both voltage testers will stop publishing data."
   * - ARIAC 2025 code
     - ``voltage_tester_plugin.cpp`` keeps publishing
       ``/voltage_tester_N/voltage`` every 0.1 s, with ``voltage`` −1 and
       ``operation_status`` ``MALFUNCTIONING``

**What the reading leaf must do.**

- Check ``operation_status`` on every message and skip a voltage of −1.
- A leaf that watches only for silence never fires: in the code, messages
  keep arriving.
- Put a Timeout around the leaf that waits for valid readings. It fails the
  step in both cases: a silent tester, and one that reports
  ``MALFUNCTIONING``.

Demo 3: A Reading Leaf Inside a Timeout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/demo_timeout.py
   :language: python
   :lines: 46-57
   :caption: lecture7/code/demo_timeout.py (excerpt)

- A mock tester publishes every 0.1 s, as the plugin does. The leaf needs 10
  valid readings, which is 1 s of data at 10 Hz.
- The tree is ``Timeout("timeout", read, duration=2.0)``, ticked every
  0.05 s. The limit and the tick period are chosen for this demo.

Demo 3: A Working, a Silent and a Malfunctioning Tester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/timeout_normal.txt
   :language: text
   :caption: Output of demo_timeout.py normal

.. literalinclude:: outputs/timeout_silent.txt
   :language: text
   :caption: Output of demo_timeout.py silent

.. literalinclude:: outputs/timeout_malfunction.txt
   :language: text
   :caption: Output of demo_timeout.py malfunction

1. Normal: 10 readings × 0.1 s = 1.0 s, then the leaf succeeds.
2. Silent: no message at all. Timeout fails the step at its 2.0 s limit.
3. Malfunction: 2.0 s / 0.1 s = 20 messages, all with −1 and
   ``MALFUNCTIONING``, all skipped. Timeout fails the step at 2.0 s. A
   message arrived every 0.1 s, so a silence watch would never have fired.

.. _l7-nesting:

Demo 4: The Nesting Order Changes the Meaning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can put Retry outside Timeout, or Timeout outside Retry.
``demo_nesting.py`` tries both, on an act that never finishes.

.. image:: /_static/images/l7/retry_timeout_nesting.svg
   :alt: Two rows, each with a small tree on the left and a time line on the
         right; the time axis runs from 0 to 0.7 seconds. Tag 1: Retry above
         Timeout above act. Three red bars, attempts starting at 0.00, 0.22,
         0.44 seconds, each about 0.2 seconds long; the step fails at 0.64
         seconds. Tag 2: Timeout above Retry above act. One red bar from 0 to
         0.20 seconds, where the step fails.
   :width: 90%
   :align: center

1. ``Retry(Timeout(act))``.
2. ``Timeout(Retry(act))``.

This is a graph of time, not a picture of the factory. The x axis is the time
since the step started. Each red bar is one attempt of the act running, and
the black line is when the step failed. The act never finishes. The limit of
0.2 s, ``num_failures=3`` and the tick period of 0.02 s are all chosen for
this demo. The bar positions come from run 1 of ``outputs/nesting_hang.txt``.

Demo 4: The Measured Times, Five Runs of Each
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/nesting_hang.txt
   :language: text
   :caption: Output of demo_nesting.py hang (the act never finishes)

.. literalinclude:: outputs/nesting_fail.txt
   :language: text
   :caption: Output of demo_nesting.py fail (each attempt fails after 0.15 s)

1. ``Retry(Timeout(act))``: each attempt gets its own 0.2 s, so
   3 × 0.2 = 0.6 s of attempts. Each new attempt starts about one tick
   (0.02 s) after the last one ends: 0.00, 0.22, 0.44 s. So the step fails at
   about 0.64 s.
2. ``Timeout(Retry(act))``: one 0.2 s limit covers all attempts. An act that
   never ends gets 1 attempt; one that fails after 0.15 s gets a second
   attempt, which the limit cuts off.

Choosing the Order and Setting the Limit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The order.** The 10 s limit and three attempts below are chosen for this
example.

- ``Retry(Timeout(act))``: each attempt has its own limit. With a 10 s limit
  and three attempts, the step can take up to 3 × 10 = 30 s.
- ``Timeout(Retry(act))``: the three attempts share one 10 s limit.

**The limit.**

1. Run each action about 20 times and record how long it takes.
2. Set the limit above the longest time you saw.

.. warning::

   A guessed limit either fires on normal runs or waits too long on real
   failures. In ARIAC, time limits are simulation time, while your tree's
   clock is wall time: measure in the same setup you will run.

   The clock part is checked: ``py_trees`` 2.6.0's Timeout reads
   ``time.monotonic()``, the computer's clock, not ROS simulation time. What
   the gap between the two clocks does to a GP3 run is reasoned, not
   measured: none of the L7 demos runs in the simulator. If the simulation
   runs slower than real time, a limit in wall time gives a skill less
   simulated time than its number says, so time your actions in the
   simulator on the machine you will use.


.. _l7-classifying:

Classifying Failures
--------------------

Retry, wait, replan or stop: which response fits which failure?

Four Responses to a Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 14 86
   :class: compact-table

   * - **Response**
     - **When it fits**
   * - Retry
     - The failure is short-lived and the plan is still right: a grasp that
       failed once.
   * - Wait
     - The world stops for a while and comes back. The plan is still right
       once it does.
   * - Replan
     - The plan's facts are no longer true, so the remaining steps are wrong.
   * - Stop
     - No plan can reach the goal, or the system is unsafe. Stop the robots
       and report why.

.. important::

   A Retry decorator handles the first row inside the tree. The other three
   need the executor around the tree: it waits, asks for a new plan, or
   stops.

Class Discussion: The Four ARIAC 2025 Challenges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * - **Challenge**
     - **What the tree can watch**
     - **What the Challenges page asks**
   * - Conveyor malfunction
     - ``/inspection_conveyor/status``
     - Pause, watch the status until it reports operational, resume
   * - Voltage tester malfunction
     - ``/voltage_tester_N/voltage``: −1 with ``MALFUNCTIONING`` (code), or
       silence (docs)
     - Use only the working tester; watch for recovery
   * - Vacuum tool malfunction (Task 2)
     - The grasp result
     - Move the gripper away, grasp again
   * - High-priority order
     - ``/high_priority_orders`` (an ID)
     - Feed Ni-MH cells, build and ship that kit, submit it with
       ``/submit_high_priority_order``

For each challenge, ask two questions: is it retry, wait, replan or stop?
Which leaf or branch of your tree detects it?

Task 1 Events That Call for a New Plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. A cell fails inspection, and the inspection door pushes it into the
   inspection bin. The plan expected it at the conveyor pick. **GP3 must show
   this case.**
2. A cell's averaged voltage is outside 3.4 V to 3.8 V (Li-Ion). It must be
   recycled, and the kit needs another cell.
3. The kit window closes. L6's example: three cells at 3.75 V put
   3 × 3.75 = 11.25 V on the tray. The Li-Ion kit window is 14.25 V to
   14.55 V, so the fourth cell must be from 14.25 − 11.25 = 3.00 V to
   14.55 − 11.25 = 3.30 V. That is below the 3.4 V that any acceptable cell
   has. The AGV must go to recycling, and the kit starts over.
4. A voltage tester malfunctions. The new plan uses only the other tester.
5. A high-priority order arrives on ``/high_priority_orders``. The current
   plan stops at a safe point, and a Ni-MH kit is planned (GP4 and L11 cover
   this in depth).


.. _l7-replanning:

The Replanning Loop
-------------------

This section gives five steps from a failed step to a new tree, and a traced
run of one replan.

Five Steps Around the Running Tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l7/replanning_loop.svg
   :alt: A loop of six boxes. Top row, left to right: run the tree (red), tag
         1 detect a trigger, tag 2 stop at a safe point. An arrow goes down to
         the bottom row, which runs right to left: tag 3 write a new problem
         from the blackboard, tag 4 plan, build the tree, swap it in, tag 5
         count replans. An arrow goes from count replans back up to run the
         tree. A second arrow from count replans leads down to a dashed box:
         no plan, or past the limit: stop and report.
   :width: 100%
   :align: center

The red box is where the tree runs and the robots move. A **replanning
trigger** is an event that tells the executor the plan no longer fits the
factory. Tags 1 to 5 are the five steps:

1. A monitor detects a trigger: a guard or verify that fails, or a branch
   that watches the blackboard next to the plan.
2. The executor stops the plan at a **safe point**: between subtrees, or by
   cancelling the running action.
3. The problem generator from L6 writes a new problem from the current
   blackboard.
4. The planner returns a new plan, the factory builds a new tree, and the
   executor swaps it in.
5. The executor counts replans. If the planner finds no plan, or the count
   passes a limit, it stops and reports.

Step 2 in ARIAC: Where It Is Safe to Stop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Between subtrees.** This is the safest point: the last step finished and the
next has not started. A failed guard or verify stops the plan at such a
point.

**By cancelling the running action.**

- A course skill accepts a cancel: the robot stops, retreats up and out of any
  shared zone with what it holds, and the skill returns ``CANCELED`` (skills
  package design).
- ARIAC's ``/agvN/move`` action rejects cancel requests
  (``agv_motion_plugin.cpp``). An AGV that is moving finishes its move; the
  executor waits for the result before it replans.

.. important::

   After a stop, the blackboard must say what the robot holds and where each
   cell is. The next plan starts from those facts.

.. _l7-demo5:

Demo 5: The Setup
~~~~~~~~~~~~~~~~~

``demo_replan.py`` runs the whole loop with mock skills.

**Values chosen for this example.**

- ``tester1`` holds ``c1``, then ``c3``, then ``c5``. ``tester2`` holds
  ``c2``, then ``c4``.
- True voltages: ``c1`` 3.58 V, ``c2`` 3.62 V, ``c3`` 3.86 V, ``c4`` 3.60 V,
  ``c5`` 3.59 V. Only ``c1`` and ``c2`` were measured before plan 1.
- At most 3 replans before the executor stops.

**What the demo simplifies.**

- The planner is a stand-in for the L6 planner: it does no search. It
  recycles bad cells, fills the free slots in order, then ships the AGV. Like
  a classical planner, it assumes that a cell not yet measured will pass its
  check.
- ``inspection_robot_1`` is not in the plan: the mock factory puts the next
  cell on a tester as soon as it is free. In GP3 these steps are in the plan
  too.

The output of ``demo_replan.py`` is one file, ``outputs/replan.txt``. The
slides show it in five parts, and so do these notes.

Demo 5: Plan 1
~~~~~~~~~~~~~~

.. literalinclude:: outputs/replan.txt
   :language: text
   :lines: 1-12
   :caption: Output of demo_replan.py (part 1 of 5)

Plan 1 puts ``c1`` to ``c4`` in slots ``s1`` to ``s4``. It checks ``c3`` and
``c4`` first, because they were not measured yet.

Demo 5: Plan 1 Fails at Step 5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/replan.txt
   :language: text
   :lines: 13-20
   :caption: Output of demo_replan.py (part 2 of 5)

1. Steps 1 to 4 place ``c1`` and ``c2``. Step 1 freed ``tester1``, so ``c3``
   landed on it.
2. Step 5 averages ``c3``'s readings: 3.86 V. A Li-Ion cell must be within
   3.6 V plus or minus 0.2 V (``CellTypes.msg``), so at most
   3.6 + 0.2 = 3.8 V. 3.86 V is 3.86 − 3.8 = 0.06 V above, so the verify
   fails.
3. The fact the plan expected, ``(voltage-ok c3)``, is false, and step 7
   needs it. The robot holds nothing at step 5, so stopping here is safe.

Demo 5: The New Problem
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/replan.txt
   :language: text
   :lines: 21-32
   :caption: Output of demo_replan.py (part 3 of 5)

``+`` marks a fact added since plan 1's problem; ``-`` a fact removed. The
two ``in-slot`` facts record the finished steps, and ``(voltage-bad c3)``
comes from the measured 3.86 V.

Demo 5: Plan 2
~~~~~~~~~~~~~~

.. literalinclude:: outputs/replan.txt
   :language: text
   :lines: 33-42
   :caption: Output of demo_replan.py (part 4 of 5)

- Plan 2 recycles ``c3``, then places ``c4`` in ``s3`` and ``c5`` in ``s4``.
- It has no step for ``c1`` or ``c2``: the blackboard records that they are
  in their slots.

Demo 5: Plan 2 Finishes the Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/replan.txt
   :language: text
   :lines: 43-53
   :caption: Output of demo_replan.py (part 5 of 5)

**Checking the kit.**

1. The kit holds 3.58 + 3.62 + 3.60 + 3.59 = 14.39 V.
2. The Li-Ion kit window is 4 × 3.6 = 14.4 V plus or minus 0.15 V:
   14.4 − 0.15 = 14.25 V to 14.4 + 0.15 = 14.55 V. 14.39 V is inside it.


.. _l7-btcpp:

BehaviorTree.CPP
----------------

This section shows how to read an industry behavior tree: an XML file and C++
nodes, next to the same tree in ``py_trees``.

What It Is
~~~~~~~~~~

- **BehaviorTree.CPP** is a C++ behavior tree library used in industry. Nav2
  builds its navigation trees with it: the Jazzy package
  ``ros-jazzy-nav2-behavior-tree`` depends on ``ros-jazzy-behaviortree-cpp``.
- A tree is written in XML and loaded at run time.
- A node is a C++ class, registered with a factory under a name. The XML uses
  that name.
- A node's **ports** are its typed inputs and outputs. ``{key}`` in the XML
  connects a port to a blackboard entry.

.. note::

   In this course you read BehaviorTree.CPP; assignments do not require you
   to write C++. The examples run with BehaviorTree.CPP 4.10.0, the ROS 2
   Jazzy package. ``PickFromTester`` and ``PlaceInSlot`` are example node
   names for this lecture.

The XML Tree and the Same Tree in py_trees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/btcpp/place_cell.xml
   :language: xml
   :caption: lecture7/code/btcpp/place_cell.xml

.. literalinclude:: code/demo_place_cell.py
   :language: python
   :lines: 41-46
   :caption: lecture7/code/demo_place_cell.py (excerpt)

Both trees pick a cell from a tester, with up to three attempts, then place it
in a slot.

A C++ Action Node
~~~~~~~~~~~~~~~~~

.. literalinclude:: code/btcpp/place_cell.cpp
   :language: cpp
   :lines: 14-29
   :caption: lecture7/code/btcpp/place_cell.cpp (excerpt)

- ``providedPorts()`` declares the input port ``tester``; ``getInput`` reads
  it, here from the blackboard entry ``{tester}``.
- ``tick()`` returns SUCCESS, FAILURE or RUNNING, as ``update()`` does in
  ``py_trees``. This mock fails a set number of times.

Registering the Nodes and Running the Tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/btcpp/place_cell.cpp
   :language: cpp
   :lines: 45-58
   :caption: lecture7/code/btcpp/place_cell.cpp (excerpt)

- ``registerNodeType`` ties each XML name to its C++ class. A name in the XML
  with no registered class fails when the tree is created, as an action with
  no builder does in the Python factory.
- ``tickWhileRunning()`` ticks the tree until it returns SUCCESS or FAILURE.

Both Libraries Give the Same Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The number after the XML file (C++) or after the script (Python) is how many
times the mock pick fails before it succeeds.

.. list-table::
   :header-rows: 1
   :widths: 50 50
   :class: compact-table

   * - **BehaviorTree.CPP**
     - **py_trees**
   * - .. literalinclude:: outputs/btcpp_1.txt
          :language: text
          :caption: One failure

     - .. literalinclude:: outputs/pytrees_1.txt
          :language: text
          :caption: One failure

   * - .. literalinclude:: outputs/btcpp_3.txt
          :language: text
          :caption: Three failures

     - .. literalinclude:: outputs/pytrees_3.txt
          :language: text
          :caption: Three failures

``RetryUntilSuccessful num_attempts="3"`` and ``Retry(num_failures=3)`` both
allow three attempts in all.

Mapping BehaviorTree.CPP to py_trees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 55
   :class: compact-table

   * - **BehaviorTree.CPP 4**
     - **py_trees and py_trees_ros**
   * - ``Sequence``
     - ``Sequence`` with memory
   * - ``ReactiveSequence``
     - ``Sequence`` without memory
   * - ``Fallback``
     - ``Selector`` with memory
   * - ``ReactiveFallback``
     - ``Selector`` without memory
   * - ``RetryUntilSuccessful`` (port ``num_attempts``)
     - ``Retry`` (``num_failures``)
   * - ``Timeout`` (port ``msec``, in milliseconds)
     - ``Timeout`` (``duration``, in seconds)
   * - Ports with ``{key}``
     - Blackboard keys read and written by the leaves
   * - A C++ node's ``tick()``
     - A behaviour's ``update()``

.. important::

   The XML file is itself a plan format: a plan-to-BT factory could write XML
   instead of building Python objects. In both libraries the tree's shape is
   data, built at run time.


.. _l7-debugging:

Debugging a Running Tree
------------------------

This section covers tools that show a running tree, and four common bugs with
their symptoms.

Print the Tree, Watch Snapshots, Log Every Change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Print.** Use ``py_trees.display.unicode_tree(root, show_status=True)``, or
``ascii_tree`` as in Demo 1. A plan-driven tree changes at run time, so print
it after every rebuild too.

**Snapshots while the system runs.** A **snapshot** is the tree's structure
and each node's status at one moment, sent as a ROS message.

- ``py_trees_ros`` publishes snapshots of the tree on ``~/snapshots`` when the
  tree's ``default_snapshot_stream`` parameter is on (it is off by default), or
  on a stream opened with the ``~/snapshot_streams/open`` service.
- ``py-trees-tree-watcher`` shows them in a terminal; ``py_trees_ros_viewer``
  (apt package ``ros-jazzy-py-trees-ros-viewer``) shows them in a window.
- For BehaviorTree.CPP the matching tool is **Groot2**, which works with
  versions 3 and 4. Its free version monitors a running tree of up to 20
  nodes.

**Log.** Log every status change with the plan step number and the action
name, as the traces in this lecture do. The log shows why a step failed after
the run ends.

Demo 1 Again: The Root Without Memory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``demo_factory.py nomemory`` builds the Demo 1 tree, then sets the root's
``memory`` to ``False``.

.. literalinclude:: outputs/factory_nomemory.txt
   :language: text
   :caption: Output of demo_factory.py nomemory (root built with memory=False)

- On tick 3 the root starts step 1 again, though step 1 finished on tick 2.
- Step 1's guard fails: ``(on-tester c3 tester1)`` is false, because the
  robot already took ``c3``. The plan fails although nothing went wrong in the
  factory.

Demo 1 Again: No Memory and No Guards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``demo_factory.py noguard`` keeps the root without memory and makes every
guard pass.

.. literalinclude:: outputs/factory_noguard.txt
   :language: text
   :caption: Output of demo_factory.py noguard (guards always pass)

- Without guards, tick 3 sends the pick goal a second time while the robot
  still holds ``c3``. Only the mock skill's own check refuses it.
- A Sequence without memory repeats robot moves; a guard turns that into a
  failure you can see in the trace.

Common Bugs and Their Symptoms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 66
   :class: compact-table

   * - **Bug**
     - **Symptom**
   * - A Sequence without memory
     - Finished steps run again on every tick, and a robot repeats a move
       (Demo 1 again)
   * - A misspelled blackboard key
     - A guard always fails, or reads an old value
   * - A leaf that blocks inside ``update()``
     - The whole tree freezes until the call returns
   * - A time limit set too short
     - Normal runs fail at random

.. important::

   Each symptom shows in a tick trace. Write the logger before the first test
   in the simulator.


.. _l7-gp3:

GP3
---

**GP3: PDDL Planner and BT Executor** is posted today and is due in Week 10,
on March 31.

- It is worth 10% of the course grade. It combines L6 and L7: a PDDL domain
  for Task 1, a problem generator, a selection step for the kit voltages, and
  a plan-to-BT executor with Retry and replanning triggers.
- Your team gives a demo on two or three trials, one of which triggers a
  replan when a cell fails inspection, and writes a short reflection on what
  PDDL captured well and where it strained.
- GP3 uses the two inspection robots through the course skills package. It
  does not model the four challenges in PDDL. GP4 tests an LLM agent on three
  of them (conveyor, voltage tester, high-priority order); the final demo
  tests the vacuum tool malfunction.

.. warning::

   GP3 spans spring break. A team that does not start before the break has
   about one working week after it.


Next Class
----------

**Spring break (March 14 to 21): no class on March 17.**

**L8: LLM Agents I: Agent Loops, Tool Use, and Structured Output** (Wednesday,
March 24): an LLM agent replaces the planner and calls the same executor. The
executor you write for GP3 carries over unchanged.

**Before next class:**

- Rate each teammate in the GP2 peer review on ELMS-Canvas.
- Read the LLM Prompting and Structured Output pre-read and the Model Context
  Protocol (MCP) pre-read.
- Try at home: run ``lecture7/code/run_all.sh`` and compare your outputs with
  the ones above. The timing numbers will differ a little from run to run.
