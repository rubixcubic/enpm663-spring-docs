====================================================
L4: Behavior Trees for Task Execution
====================================================

Overview
--------

**L3 gave the executive layer a small world model: the cell on each tester,
its averaged voltage, the tray slots filled and the kit total so far. This
lecture builds the structure that reads and updates that model while the
robots work.** That structure is a **behavior tree (BT)**: a tree of nodes
that a program visits from the root down many times a second. Each visit is a
**tick**, and each node it visits returns ``SUCCESS``, ``FAILURE`` or
``RUNNING``.

The lecture starts by writing one GP1 step, moving a tested cell to a tray
slot or to the recycling bin, as a **finite state machine (FSM)** and as a BT,
and counts what each one costs when a failure case or a retry is added. It
then covers the BT primitives (leaves, sequence, selector, parallel and the
decorators), each measured with a short ``py_trees`` script, and how a tick
moves through a tree, with a live demonstration of a ``Retry`` around a pick
that fails once, run with and without **memory**. Next comes the
**blackboard**, the shared key-value store that holds L3's world model inside
the tree. The second half moves to ``py_trees_ros``: the tree as a ROS 2 node,
and leaves that call actions and services and read topics, shown in three live
runs against stand-ins for ARIAC and the course skills. The lecture ends with
three patterns for the GP1 tree: retry, stop cleanly, and check before acting.

.. important::

   **ARIAC tie-in.** Every example is a piece of the tree that builds one
   ARIAC 2025 kit: read a cell's voltage at the tester, place it in a tray
   slot or recycle it, check the kit, move the AGV to shipping with
   ``/agvN/move`` and submit the kit.

.. important::

   **Group project.** GP1, a ``py_trees_ros`` tree that builds one kit, is
   **due next week (02/24)**. GP1 ships with a starter tree (one sequence for
   one cell); this lecture gives you what you need to extend it.

.. warning::

   **Two GP1 traps this lecture measured.** Both pass a quick test and break
   the kit.

   1. **A parallel skips a child that already succeeded.** With the
      ``py_trees`` default ``synchronise=True``, a ``tester_ok`` check that
      succeeded on tick 1 is not ticked again, so a tester malfunction on
      tick 2 goes unseen and four of five readings come from a broken tester.
      Use ``synchronise=False`` to keep re-checking the child. See
      :ref:`l4-parallel`.
   2. **A service leaf returns SUCCESS whatever the reply says.** The kit
      check leaf succeeds as soon as the reply arrives, even when the reply
      says the kit is bad. Follow it with a condition on the reply. See
      :ref:`l4-run3`.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why behavior trees replaced finite state machines for robot task
  execution.
- Describe the BT primitives (sequence, selector, parallel, and the retry,
  timeout and inverter decorators) and predict the status a composite returns
  from its children's statuses.
- Explain how a tick moves through a tree, and compare composites with memory
  and without memory.
- Implement a ``py_trees_ros`` tree whose leaves call ROS 2 actions and
  services and share state through the blackboard.
- Evaluate BT failure modes in an ARIAC kit-building tree: a skill that fails
  once, a skill that keeps failing, and a tick that interrupts a running
  action.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l4_lecture
   l4_code
   l4_exercises
   l4_quiz
   l4_references


Next Steps
----------

- **Next class, Wednesday, February 24:**

  - **GP1 is due.** GP2 is posted.
  - **Quiz 2** at the start of class, closed notes, covering L4: primitives,
    ticks and statuses, memory, blackboards, ``py_trees_ros`` leaves and
    failure modes.

- In the next lecture we cover **L5: Sensing and Perception for Robotic
  Systems**: lidar point clouds that find defects on battery cells (GP2), and
  how to score a detector with precision and recall.
- **Before next class:**

  - Run ``retry_demo.py`` (see :doc:`l4_code`), change the memory flag and
    ``num_failures``, and predict each output before you run it.
  - Read the `py_trees <https://py-trees.readthedocs.io/>`_ and
    `py_trees_ros <https://py-trees-ros.readthedocs.io/>`_ documentation on
    composites, decorators, the blackboard and action clients.
  - Work through the :doc:`L4 exercises <l4_exercises>` and the
    :doc:`self-check quiz <l4_quiz>`.
