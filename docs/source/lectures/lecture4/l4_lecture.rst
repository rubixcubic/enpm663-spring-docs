====================================================
Lecture
====================================================

.. note::

   These notes follow the L4 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from the scripts on the :doc:`code page <l4_code>`, run on
   2026-10-12 with Python 3.12.3, ``py_trees`` 2.6.0 and ``py_trees_ros``
   2.6.0 under ROS 2 Jazzy. The leaves in every script are stand-ins: no
   robot and no ARIAC simulation.

.. admonition:: Class logistics for this week
   :class: warning

   - **Quiz 1** takes the first 20 minutes: closed notes, no AI, on
     ELMS-Canvas or paper. It covers L1 to L3 and is worth 5% of the course
     grade. The honor pledge applies.
   - **GP1** is due next week (02/24).


.. _l4-recap:

Quiz 1 and Recap
----------------

**From L3.**

- The executive layer keeps a small world model: the cell on each tester, its
  averaged voltage, the tray slots filled, the kit total so far.
- ARIAC publishes no pose for a cell, so your system tracks each cell itself,
  from events.

**Today.**

- The structure that reads and updates that model while the robots work: a
  behavior tree (BT).
- Every example is a piece of the GP1 tree, which builds one kit and is due
  next week (02/24).


.. _l4-fsm-bt:

Trees and State Machines
------------------------

This section writes one GP1 step as a finite state machine and as a behavior
tree, then counts what each one costs when a failure case or a retry is
added.

Two Ways to Write the Executive Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: finite state machine (FSM)
   :class: note

   - The robot is in one **state** at a time: reading the voltage, picking,
     placing.
   - Each **transition** names the next state and the event that leads to
     it. You write every transition by hand.

.. admonition:: Definition: behavior tree (BT)
   :class: note

   - A tree of nodes. Many times a second, a **tick** visits the tree from
     the root down.
   - Each node visited returns a status: ``SUCCESS``, ``FAILURE`` or
     ``RUNNING``.
   - The inner nodes decide which child runs next from those statuses, so the
     order is set by where a node sits in the tree.

The step used for both: move one tested cell from the tester to a tray slot,
or to the recycling bin if its voltage is out of range.

One GP1 Step, Two Ways
~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l4/fsm_vs_bt.svg
   :alt: Tag 1, left: a state machine for moving one tested cell.
         read_voltage leads to pick_from_tester, which leads to place_in_slot
         when the cell is in range and to recycle_cell when it is out of
         range; both lead to done. Dashed red arrows run from read_voltage,
         pick_from_tester, place_in_slot and recycle_cell to a state named
         stopped: one failure transition per working state. Tag 2, right: the
         same step as a behavior tree, indented the way py_trees prints it.
         The sequence move_cell holds read_voltage, pick_from_tester and the
         selector place_or_recycle; the selector holds the sequence
         place_if_good (voltage_in_range, then place_in_slot) and
         recycle_cell.
   :width: 100%
   :align: center

- **Tag 1: the FSM.** Dashed red arrows are failure transitions: a skill or
  the tester fails, so the step stops.
- **Tag 2: the BT**, indented the way ``py_trees`` prints a tree. Orange boxes
  are sequences, the cyan octagon is a selector, gray ellipses are leaves.

Counting What Each Change Costs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Change 1: stop when a skill or the tester fails.**

1. The FSM has 6 states and 5 normal transitions. Each of the 4 working
   states needs its own arrow to ``stopped``: 5 + 4 = 9 transitions.
2. The BT needs no new node: a leaf that returns ``FAILURE`` makes its
   sequence return ``FAILURE``, and so on up to the root.

**Change 2: try the pick a second time.**

1. The FSM must remember that this is the second attempt, so it needs a new
   state, ``pick_again``, and 4 new arrows: one into it from the first pick,
   and three out of it (to place, recycle and stopped). The first pick's
   arrow to ``stopped`` goes away: 9 − 1 + 4 = 12 transitions.
2. The BT wraps ``pick_from_tester`` in one ``Retry`` decorator: 8 + 1 = 9
   nodes. Nothing else changes.

The 8 nodes of the BT are the ones in tag 2 of the figure: ``move_cell``,
``read_voltage``, ``pick_from_tester``, ``place_or_recycle``,
``place_if_good``, ``voltage_in_range``, ``place_in_slot`` and
``recycle_cell``.

Why Robot Software Moved to Behavior Trees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- In an FSM, each new failure case adds transitions to many states. In a BT,
  a failure moves up the tree by itself.
- A BT subtree that does one job (move a cell from tester to tray) can be
  reused, wrapped in a retry, or put under a fallback, without touching the
  rest of the tree.
- **Industry use:** Nav2, the ROS 2 navigation stack, runs its navigation
  logic as behavior trees with the C++ library BehaviorTree.CPP. L7 shows
  BehaviorTree.CPP so you can read that code.
- This course uses ``py_trees`` and ``py_trees_ros`` (version 2.6.0 with ROS 2
  Jazzy), because Python is the course language.

**To read more:** M. Colledanchise and P. Ögren, *Behavior Trees in Robotics
and AI: An Introduction*, Chapman and Hall/CRC, 2018. Free preprint:
`arXiv 1709.00084 <https://arxiv.org/abs/1709.00084>`_.


.. _l4-primitives:

BT Primitives
-------------

This section covers leaves, sequence, selector, parallel and decorators. For
each one, it gives the status it returns from its children's statuses,
measured with ``composite_status.py`` and ``parallel_watch.py``
(``py_trees`` 2.6.0).

Nodes and Statuses
~~~~~~~~~~~~~~~~~~

**Three kinds of node.**

- A **leaf** does the work. An **action** leaf runs a skill or calls a
  service. A **condition** leaf checks a fact and returns ``SUCCESS`` or
  ``FAILURE`` at once.
- A **composite** (sequence, selector, parallel) has several children and
  decides which of them to tick.
- A **decorator** has one child and changes its result.

**Four statuses in** ``py_trees``.

- ``SUCCESS`` and ``FAILURE``: the node is done.
- ``RUNNING``: the node needs more ticks, for example while a robot moves.
- ``INVALID``: the node has not run yet, or it was stopped.

Every Node Type in One GP1 Subtree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l4/bt_node_types.svg
   :alt: A behavior tree drawn the py_trees way, root on the left. The root
         handle_cell is an orange box (a sequence, tag 1). Its three children
         are wait_for_reading, a gold parallelogram (a parallel, tag 3) with
         the leaves tester_ok and wait_for_voltage; retry_pick, a white
         ellipse (a decorator, tag 4) above the leaf pick_from_tester; and
         place_or_recycle, a cyan octagon (a selector, tag 2). The selector
         has two children: the sequence place_if_good, with the leaves
         voltage_in_range and place_in_slot, and the leaf recycle_cell.
         Leaves are gray ellipses (tag 5).
   :width: 100%
   :align: center

- **Tags:** 1 sequence (orange box), 2 selector (cyan octagon), 3 parallel
  (gold parallelogram), 4 decorator (white ellipse), 5 leaf (gray ellipse).
  These are the shapes and colors ``py_trees`` uses when it draws a tree.
- In text output, ``py_trees`` marks them ``{-}`` or ``[-]``, ``{o}`` or
  ``[o]``, ``/_/``, ``-^-`` and ``-->``. Braces mean the composite has memory
  (memory is explained in :ref:`l4-memory`).

How the Demonstration Measures a Composite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/composite_status.py
   :language: python
   :caption: composite_status.py (excerpt)
   :pyobject: Fixed

.. literalinclude:: code/composite_status.py
   :language: python
   :pyobject: show

- Each ``Fixed`` leaf is a stand-in that returns one status.
- Each case builds a fresh composite over three (or two) ``Fixed`` leaves,
  calls ``show`` once, and prints one line: each child's status, then the
  parent's after the arrow.

Sequence: Every Child Must Succeed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: sequence
   :class: note

   A **sequence** ticks its children in order. It returns ``FAILURE`` as soon
   as one child fails, ``RUNNING`` as soon as one child is running, and
   ``SUCCESS`` when all succeed.

GP1 example: ``move_cell`` = pick from the tester, place in the slot, update
the blackboard.

.. literalinclude:: outputs/composite_status.txt
   :language: text
   :lines: 1-4

Cases 2 and 3: ``update`` shows ``INVALID`` because the sequence stopped
before it. It was never ticked.

Selector: The First Child That Succeeds Wins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: selector (fallback)
   :class: note

   A **selector**, also called a **fallback**, ticks its children in order.
   It returns ``SUCCESS`` as soon as one child succeeds, and ``FAILURE`` only
   if all fail.

GP1 example: ``place_or_recycle``. If the averaged voltage is in range, place
the cell in a slot; otherwise drop it in the recycling bin.

.. literalinclude:: outputs/composite_status.txt
   :language: text
   :lines: 5-8

Case 4: the cell was placed, so ``recycle`` never runs. Case 6: both branches
failed, so the selector fails and its parent must handle it.

.. _l4-parallel:

Parallel: Tick Every Child on Every Tick
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: parallel
   :class: note

   - A **parallel** ticks all its children on every tick. It returns
     ``FAILURE`` if any child fails.
   - A **policy** sets when it succeeds: ``SuccessOnAll``, ``SuccessOnOne``,
     or ``SuccessOnSelected`` (a list of children you choose).
   - ``SuccessOnAll`` and ``SuccessOnSelected`` take a ``synchronise`` flag,
     ``True`` by default: a child that has succeeded is **skipped** on later
     ticks.

**GP1 example:** ``wait_for_reading``.

- Child ``tester_ok``: ``SUCCESS`` while the tester reports ``OPERATIONAL``.
- Child ``wait_for_voltage``: collects one reading per tick and succeeds
  after five.
- Policy: ``SuccessOnSelected([wait_for_voltage])``. A tester malfunction
  should end the wait.
- Stand-in tester, values chosen for this example: 3.61 V on tick 1; then
  −1.0 V and ``MALFUNCTIONING``, as ARIAC's tester publishes during that
  challenge.

**The same tree with** ``synchronise`` **True and False**
(``parallel_watch.py``):

.. literalinclude:: outputs/parallel_watch.txt
   :language: text

1. With ``synchronise=True``, ``tester_ok`` succeeded on tick 1, so it was
   skipped on ticks 2 to 5. Its ``SUCCESS`` is left over from tick 1.
2. The average is (3.61 + 4 × (−1.0)) / 5 = −0.39 / 5 = −0.078 V: four of the
   five readings came from a broken tester.
3. With ``synchronise=False``, the check runs on every tick and ends the wait
   on tick 2.

.. warning::

   **GP1 trap 1: a parallel needs** ``synchronise=False`` **to keep checking
   a child.** With the default, ``synchronise=True``, a condition that
   succeeded once is never ticked again, and the status you see is left over
   from that tick. A tester malfunction goes unseen, and the tree averages
   −1.0 V readings into the cell's voltage. When a parallel watches a
   condition that must stay true, build its policy with
   ``synchronise=False``.

Decorators: One Child, a Changed Result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 46 32
   :class: compact-table

   * - **Decorator**
     - **What it does**
     - **GP1 use**
   * - ``Retry``
     - Turns a child's ``FAILURE`` into another attempt, up to
       ``num_failures`` failures
     - A pick that can work on the second try
   * - ``Timeout``
     - Returns ``FAILURE`` if the child is still ``RUNNING`` after
       ``duration`` seconds, and stops the child
     - A place skill that never finishes
   * - ``Inverter``
     - Swaps ``SUCCESS`` and ``FAILURE``
     - "tester is NOT malfunctioning"
   * - ``FailureIsSuccess``
     - Reports a child's ``FAILURE`` as ``SUCCESS``
     - An optional step, such as a log entry
   * - ``EternalGuard``
     - Checks a condition before every tick of its child; stops the child
       when the condition fails
     - Keep placing only while the AGV is at the inspection station

All five are in ``py_trees.decorators`` (``py_trees`` 2.6.0).

Decorators: Measured
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/composite_status.txt
   :language: text
   :lines: 9-15

- ``Inverter`` leaves ``RUNNING`` alone: a running child is not yet a yes or a
  no.
- ``Timeout`` with ``duration=0.2`` s: on tick 2, 0.3 s had passed and the
  child was still running, so the decorator stopped the child (now
  ``INVALID``) and returned ``FAILURE``.
- In ``py_trees_ros``, stopping an action leaf cancels its goal. The live
  demonstration later shows the cancel reach the server (:ref:`l4-run2`).


.. _l4-memory:

Ticks and Memory
----------------

This section covers how a tick moves through a tree, what a node does on each
tick, and composites with and without memory, with a live demonstration
(``retry_demo.py``, ``py_trees`` 2.6.0, ROS 2 Jazzy, run 2026-10-12).

What a Tick Is
~~~~~~~~~~~~~~

.. admonition:: Definition: tick
   :class: note

   A **tick** is one pass from the root down. The root ticks its children;
   each composite decides which of its own children to tick; each node
   visited returns a status to its parent.

- A node that is not visited keeps the status it returned last.
- A long action returns ``RUNNING`` on each tick until it finishes. The tick
  returns at once, so the program that ticks the tree never waits while a
  robot moves.
- In ``py_trees_ros``, a ROS 2 timer ticks the tree at a period you choose
  (100 ms in today's demonstrations).

.. warning::

   **A leaf must never wait inside a tick.** A leaf that sleeps until a skill
   is done blocks the whole tree, and with it the node's other callbacks (the
   L1 executor demonstration: 11 status reads instead of 50).

The Four Methods of a Node
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 40 44
   :class: compact-table

   * - **Method**
     - **When** ``py_trees`` **calls it**
     - **An action leaf uses it to**
   * - ``setup``
     - Once, before the first tick
     - Create the action client and wait for the server
   * - ``initialise``
     - When the node starts running (its last status was not ``RUNNING``)
     - Send the goal
   * - ``update``
     - On every tick that visits the node
     - Check the result; return ``RUNNING``, ``SUCCESS`` or ``FAILURE``
   * - ``terminate``
     - When the node finishes, or is stopped by its parent
     - Cancel the goal if it was stopped while running

This is how ``py_trees_ros.action_clients.FromConstant`` works
(``action_clients.py`` in ``py_trees_ros`` 2.6.0). It sends the cancel only
when its status goes from ``RUNNING`` to ``INVALID``.

Memory in a Sequence or Selector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: memory
   :class: note

   - **With memory** (``memory=True``): while a child is ``RUNNING``, the
     next tick resumes at that child. Children that already finished are not
     ticked again.
   - **Without memory** (``memory=False``): every tick starts again at the
     first child, so earlier children are checked again. Good for a condition
     that must stay true while later children run. Bad for an action that
     already finished: it runs again.

**The demonstration tree.**

- Sequence ``move_cell``: ``check_tester_ok``, then a ``Retry`` (up to 2
  failures) around ``pick_from_tester``, then ``place_in_slot``.
- Stand-in leaves, no robot. The pick fails on its first attempt and succeeds
  on its second. Each action leaf returns ``RUNNING`` for one tick before its
  result.

The Demonstration Code
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/retry_demo.py
   :language: python
   :caption: retry_demo.py (excerpt)
   :pyobject: build

- ``Step(name, results, run_ticks)`` is a stand-in leaf: it returns
  ``RUNNING`` for ``run_ticks`` ticks, then the next of ``results``.
- The script builds the tree twice, with ``memory=True`` and
  ``memory=False``, ticks each up to 14 times, and prints every leaf's status
  after each tick.

Step 1: The Run with Memory
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/retry_demo.txt
   :language: text
   :lines: 1-7

1. Tick 1: the check succeeds; the pick starts (``RUNNING``).
2. Tick 2: the pick fails. ``Retry`` counts 1 failure of the 2 allowed and
   returns ``RUNNING``, so the sequence is still running.
3. Tick 3: the sequence resumes at the ``Retry``, which starts the pick
   again.
4. Tick 4: the pick succeeds; the place starts. Tick 5: the place succeeds,
   so the root succeeds.
5. The check ran once. The pick was updated 4 times: two attempts of two
   ticks each.

Step 2: The Run without Memory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/retry_demo.txt
   :language: text
   :lines: 8-23

The script stops after 14 ticks. The tree is still ``RUNNING``, and it
repeats the same two ticks.

Step 3: Tick 5, Drawn
~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l4/bt_tick_path.svg
   :alt: Two copies of the tree move_cell from the retry demonstration, on
         tick 5. Top, memory=True: tag 1 marks move_cell and tag 2 marks
         place_in_slot, the only two nodes the tick visits; place_in_slot
         returns SUCCESS, so move_cell returns SUCCESS. check_tester_ok,
         retry_pick and pick_from_tester are faded: not visited, they keep the
         SUCCESS from ticks 1 and 4. Bottom, memory=False: tags 1 to 4 mark
         move_cell, check_tester_ok (SUCCESS), retry_pick and
         pick_from_tester, which starts again and returns RUNNING. move_cell
         returns RUNNING, and the faded place_in_slot is stopped and shows
         INVALID.
   :width: 100%
   :align: center

Tags 1 to 4: the order in which tick 5 visits the nodes. Faded nodes are not
visited on this tick. Statuses come from the output, tick 5.

Step 4: Why the Run without Memory Never Ends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Tick 4: the pick succeeded and the place started.
2. Tick 5: the sequence starts again at the check, which succeeds.
3. The ``Retry`` is not running any more (it returned ``SUCCESS`` on tick 4),
   so it starts its child again. The pick restarts and returns ``RUNNING``.
4. A running child ends the sequence's tick, so the sequence stops the place
   (``INVALID``).
5. Tick 6 is tick 4 again: the pick succeeds, the place starts. The pattern
   repeats on every pair of ticks.

.. warning::

   On a robot, step 3 sends a new pick goal for a cell the gripper already
   holds. **Put a sequence of actions under a composite with memory. Put a
   condition that must stay true under a composite without memory, or under
   a guard.**

A Tick That Interrupts a Running Action
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What** ``py_trees`` **does.**

- In a selector without memory, every tick starts at the first child. If a
  higher-priority child succeeds or runs while a lower one is ``RUNNING``,
  the selector stops the lower one, and its ``terminate`` method is called.
- A selector with memory skips the higher-priority children while a child is
  running, so this interrupt does not happen there.

**What your leaf must do.**

- If ``terminate`` does not cancel the goal, the robot keeps moving under a
  tree that has moved on.
- ``py_trees_ros`` action leaves cancel the goal. The course skills accept a
  cancel.
- ARIAC's ``/agvN/move`` action rejects cancel requests: once the AGV leaves,
  it finishes its move. Interrupt the tree before you send the AGV, not while
  it drives.


.. _l4-blackboards:

Blackboards
-----------

This section covers the shared state that leaves read and write: L3's world
model, inside the tree. It is measured with ``blackboard_demo.py``
(``py_trees`` 2.6.0).

Keys, Access and the GP1 World Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: blackboard
   :class: note

   The **blackboard** is a key-value store that every leaf can reach. In
   ``py_trees``, each behavior registers the keys it uses with
   ``Access.READ`` or ``Access.WRITE``, and the blackboard refuses any other
   use.

**GP1 keys, from the L3 world model.**

.. list-table::
   :header-rows: 1
   :widths: 28 38 34
   :class: compact-table

   * - **Key (example name)**
     - **Holds**
     - **Written by**
   * - ``/tester1/cell``
     - The cell on tester 1
     - The leaf that puts the cell on the tester
   * - ``/tester1/voltage``
     - That cell's averaged voltage
     - The averaging leaf
   * - ``/kit/slots_filled``
     - Tray slots used, 0 to 4
     - The place leaf
   * - ``/kit/total``
     - Sum of the placed cells' voltages
     - The place leaf
   * - ``/step``
     - The high-level step under way
     - The first leaf of each step

A Reader: ``voltage_in_range``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/blackboard_demo.py
   :language: python
   :caption: blackboard_demo.py (excerpt)
   :pyobject: VoltageInRange

- The leaf registers ``/tester1/voltage`` for reading in its constructor,
  then reads it on every tick.
- ``LOW`` and ``HIGH`` are 3.4 V and 3.8 V: Li-Ion's 3.6 V plus or minus
  0.2 V.
- The writer of that key is a leaf named ``average_voltage``. It stands in
  for averaging the tester's readings.

A Writer: ``place_in_slot``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/blackboard_demo.py
   :language: python
   :caption: blackboard_demo.py (excerpt)
   :pyobject: PlaceInSlot

The leaf reads the voltage and writes the two kit keys. It writes them only
after the pick-and-place skill would have succeeded.

Three Cells through ``handle_cell``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tree: sequence ``handle_cell`` = ``average_voltage``, then the selector
``place_or_recycle`` from the selector section. Tester readings are chosen for
this example: five per cell, averaging 3.55 V, 3.85 V and 3.62 V.

.. literalinclude:: outputs/blackboard_demo.txt
   :language: text

1. Cell 2: 3.85 V is above 3.6 + 0.2 = 3.8 V, so ``voltage_in_range`` fails
   and the selector recycles the cell. The kit keys do not change.
2. Cell 3: the kit total becomes 3.55 + 3.62 = 7.17 V.
3. The last lines: ``voltage_in_range`` registered the key for reading only,
   so its write raises an error.

Conventions and Pitfalls
~~~~~~~~~~~~~~~~~~~~~~~~

**Conventions.**

- One writer per key where you can. Give each key a clear name and type.
- Write a key only after the action it describes succeeded:
  ``place_in_slot`` updates the kit keys after the skill reports success.
- Clear a key when it no longer holds.

**Pitfalls.**

- **A stale value.** In the demonstration, ``/tester1/voltage`` still says
  3.85 V after cell 2 was recycled, until the next cell's average replaces
  it.
- **Two leaves that write the same key.**
- **Keys used as a hidden second control flow** ("if this flag is set, skip
  that step") instead of tree structure that a reader can see.

Watching a Running Tree
~~~~~~~~~~~~~~~~~~~~~~~

``py_trees_ros`` installs two command-line watchers for a running tree node.

The tree, with visited blackboard keys:

.. code-block:: bash

   py-trees-tree-watcher -b

The blackboard, visited keys and who accessed them:

.. code-block:: bash

   py-trees-blackboard-watcher --visited --activity

Both options are from the tools' own ``--help`` (``py_trees_ros`` 2.6.0). Use
them in GP1 when a leaf reads a value you did not expect.


.. _l4-py-trees-ros:

py_trees_ros
------------

This section covers the tree as a ROS 2 node, and leaves that call actions and
services and read topics. A live demonstration, ``ros_tree_demo.py``, has
three runs (ROS 2 Jazzy, ``py_trees_ros`` 2.6.0, run 2026-10-12).

The Tree as a ROS 2 Node
~~~~~~~~~~~~~~~~~~~~~~~~

1. ``py_trees_ros.trees.BehaviourTree(root)`` wraps a ``py_trees`` tree.
2. ``setup(node_name=..., timeout=...)`` creates the ROS 2 node and calls
   each behavior's ``setup``: clients connect to their servers here.
3. ``tick_tock(period_ms=100.0)`` creates a ROS 2 timer that ticks the tree
   every 100 ms.
4. You spin the node with an executor, as for any node.

.. tip::

   The ticks come from a timer callback, so subscription and action callbacks
   run between ticks. The tree never blocks the node: the problem from the L1
   executor demonstration does not happen.

Leaves That Talk to ROS 2
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 44 26
   :class: compact-table

   * - **Leaf (module.class)**
     - **Returns**
     - **GP1 use**
   * - ``action_clients.FromConstant``, ``FromBlackboard``
     - Sends a fixed goal, or a goal read from a key. ``RUNNING`` while the
       action runs; ``SUCCESS`` only if the result status is ``SUCCEEDED``;
       otherwise ``FAILURE``
     - Course skills; ``/agvN/move``
   * - ``service_clients.FromConstant``, ``FromBlackboard``
     - ``RUNNING`` until the reply arrives, then ``SUCCESS``, **whatever the
       reply says**
     - Submit report, check kit quality, submit kit
   * - ``subscribers.ToBlackboard``
     - ``RUNNING`` until a message has arrived, then ``SUCCESS``; copies the
       message, or a field of it, to a key
     - Tester voltage, conveyor status

Each row's behavior is from the ``py_trees_ros`` 2.6.0 source. A subscriber
leaf's QoS must match the publisher's, as in the L1 QoS demonstration.

The Demonstration: Stand-ins for ARIAC and the Skills
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 36 30
   :class: compact-table

   * - **Stand-in in the script**
     - **What it does**
     - **Stands in for**
   * - Topic ``tester1/voltage`` (``std_msgs/Float64``)
     - Publishes 3.62 V every 0.1 s
     - ``/voltage_tester_1/voltage``
   * - Actions ``pick_from_tester``, ``place_in_slot``
       (``control_msgs/GripperCommand``)
     - Pick: the first goal aborts after 0.4 s; the second succeeds after
       0.4 s. Place: succeeds after 0.6 s
     - Course skills
   * - Service ``check_kit`` (``std_srvs/Trigger``)
     - Replies ``success`` and a message
     - ``/agv1/check_kit_quality``, which answers ``is_good``

- Run 2 changes one thing: the place goal runs 5.0 s. Run 3 changes another:
  the kit check replies ``success=False``. All times are chosen for this
  example.
- The stand-ins share the tree's process, so the script spins both nodes on a
  multi-threaded executor. In GP1 the skills run in their own process.

The Leaves and the Tree in Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/ros_tree_demo.py
   :language: python
   :caption: ros_tree_demo.py (excerpt)
   :pyobject: build

- ``blackboard_variables`` copies the message's ``data`` field to
  ``/tester1/voltage``. ``key_response`` stores the service reply in
  ``/kit/check``.
- The root is a sequence with memory (``{-}`` in the print below): the skills
  run in order, and a finished skill is not run again.
- ``KitIsGood`` is a condition leaf written for the demonstration. It returns
  ``SUCCESS`` only if the reply in ``/kit/check`` says ``success``.

**Printed by** ``py_trees``:

.. literalinclude:: outputs/ros_tree_ok.txt
   :language: text
   :lines: 4-11

.. _l4-run1:

Run 1: The Pick That Fails Once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ticks 1 to 13:

.. literalinclude:: outputs/ros_tree_ok.txt
   :language: text
   :lines: 13-23

1. Tick 1: no voltage message yet, so ``read_voltage`` returns ``RUNNING``.
   Tick 2 has one.
2. Tick 2 (0.2 s) sends the pick goal; the server aborts it 0.4 s later, at
   0.6 s. The leaf sees ``FAILURE`` on the next tick, 7.
3. ``Retry`` counts 1 failure of 2 and stays ``RUNNING``. Tick 8 sends a new
   goal, which succeeds at 0.8 + 0.4 = 1.2 s.

Run 1: Place, Check, Done
~~~~~~~~~~~~~~~~~~~~~~~~~

Ticks 13 to 21:

.. literalinclude:: outputs/ros_tree_ok.txt
   :language: text
   :lines: 24-34

1. The place goal starts at 1.3 s and runs 0.6 s, so it ends at 1.9 s, and
   tick 20 sees ``SUCCESS``.
2. The service leaf takes one tick to get its reply. The condition
   ``kit_is_good`` reads the reply from ``/kit/check``.
3. The node heard 21 voltage messages in 21 ticks. 21 ticks at 0.1 s are
   2.1 s, and 2.1 s at one message every 0.1 s is 21 messages: none was
   missed while the skills ran.

.. _l4-run2:

Run 2: A Place That Never Finishes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output, from tick 13:

.. literalinclude:: outputs/ros_tree_timeout.txt
   :language: text
   :lines: 24-30

1. The place starts at 1.3 s. ``timeout_place`` allows 2.0 s, so it fails
   after 1.3 + 2.0 = 3.3 s.
2. It stops its child: ``place_in_slot`` becomes ``INVALID``, its
   ``terminate`` sends the cancel, and the server reports the goal canceled
   in the same 0.1 s.
3. Over 10 more runs (``outputs/ros_tree_repeats.txt`` on the
   :doc:`code page <l4_code>`), the timeout fired on tick 33 in 3 runs and on
   tick 34 in 7. ``Timeout`` fails only once *more* than 2.0 s have passed,
   and the 2.0 s mark falls on a tick, so timer jitter decides which tick sees
   it.

.. _l4-run3:

Run 3: A Service Leaf Succeeds on a Bad Reply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output, from tick 20:

.. literalinclude:: outputs/ros_tree_bad_kit.txt
   :language: text
   :lines: 29-34

1. ``check_kit`` returns ``SUCCESS``: a service leaf succeeds when the reply
   arrives, whatever the reply says.
2. The condition ``kit_is_good`` reads the reply and fails, so ``move_cell``
   fails.

.. warning::

   **GP1 trap 2: a service leaf returns SUCCESS even when the reply says the
   kit is bad.** ARIAC's check kit quality service answers ``is_good``. A
   tree with only the service leaf would ship a rejected kit. **Follow every
   service leaf whose reply matters with a condition on that reply**, as
   ``kit_is_good`` does here.


.. _l4-patterns:

Patterns for the GP1 Tree
-------------------------

This section goes from the starter tree to a tree that builds one kit, with
three patterns: retry, stop cleanly, check before acting.

The Starter Tree: One Sequence for One Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l4/gp1_starter_tree.svg
   :alt: A sequence named one_cell, drawn as an orange box on the left, with
         seven gray leaves in order from top to bottom: submit_report (tag 1,
         a service leaf), wait_for_beam (tag 2, a subscriber leaf),
         pick_from_conveyor (tag 3, an action leaf), place_on_tester (tag 3),
         read_voltage (tag 2), pick_from_tester (tag 3) and place_in_slot
         (tag 3).
   :width: 55%
   :align: center

- **Tags:** 1 service leaf, 2 subscriber leaf (a topic), 3 action leaf (a
  course skill).
- Inspection robot 1 runs the two tag 3 leaves at the top
  (``pick_from_conveyor``, ``place_on_tester``); inspection robot 2 runs the
  two at the bottom (``pick_from_tester``, ``place_in_slot``).
- The names follow the Task 1 steps in L1. The handout's code may name them
  differently.
- After four cells, the tree checks the kit, moves the AGV to shipping with
  ``/agvN/move`` and submits the kit.

Pattern 1: Retry
~~~~~~~~~~~~~~~~

- Wrap a skill leaf in ``Retry`` for a failure that can pass on a second try
  (:ref:`run 1 <l4-run1>`).
- The skills package never retries a task by itself. Any retry must be in
  your tree.

Pattern 2: Stop Cleanly
~~~~~~~~~~~~~~~~~~~~~~~

- When a skill keeps failing, ``Retry`` returns ``FAILURE`` after
  ``num_failures`` attempts. Let that failure reach the root.
- Leave the robot where the skill left it: the skill's result says what the
  gripper still holds.
- Log the reason, and do not loop forever. A ``Timeout`` turns a skill that
  never answers into a failure (:ref:`run 2 <l4-run2>`).

Pattern 3: Check Before Acting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Put a condition before each step that cannot be undone. Cells lock to the tray
once placed, so the voltage decision comes before the place.

Before the fourth cell, check the kit total too. L3's worked example, in
steps:

1. Three placed cells total 3.55 + 3.62 + 3.70 = 10.87 V.
2. The Li-Ion kit window is 14.25 V to 14.55 V (L1).
3. The fourth cell must be from 14.25 − 10.87 = 3.38 V to 14.55 − 10.87 =
   3.68 V, and inside 3.40 V to 3.80 V on its own: so from 3.40 V to 3.68 V.
4. A cell at 3.75 V passes ``voltage_in_range`` but would make the kit
   10.87 + 3.75 = 14.62 V. A second condition, on ``/kit/total``, must catch
   it.

The check kit quality service comes after the fourth place, when the cells are
already locked, and its reply needs its own condition
(:ref:`run 3 <l4-run3>`).

Class Discussion and the GP1 Write-up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Class discussion.**

- Which GP1 steps need a retry, which need a timeout, and which must stop the
  tree?
- For each composite in your tree: if one child fails, what does the
  composite return?

**GP1 write-up.**

- The tree diagram, and the reason for each composite choice: why a selector
  here, why memory there.
- Test the two failure cases: a skill that fails once, and a skill that keeps
  failing.

**Later in the course.** L7 builds a tree from a PDDL plan and adds
replanning. L11 adds recovery for the ARIAC challenges.


.. _l4-next:

Next Class
----------

**Wednesday, February 24.**

- GP1 is due. GP2 is posted.
- Quiz 2 at the start of class, closed notes, covering L4: primitives, ticks
  and statuses, memory, blackboards, ``py_trees_ros`` leaves and failure
  modes.

**L5: Sensing and Perception for Robotic Systems.** Lidar point clouds that
find defects on battery cells (GP2), and how to score a detector with
precision and recall.

**Before next class.**

- Run ``retry_demo.py``, change the memory flag and ``num_failures``, and
  predict each output before you run it. The :doc:`exercises <l4_exercises>`
  walk you through it.
- Read the `py_trees <https://py-trees.readthedocs.io/>`_ and
  `py_trees_ros <https://py-trees-ros.readthedocs.io/>`_ documentation on
  composites, decorators, the blackboard and action clients.
