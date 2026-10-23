====================================================
PDDL Primer
====================================================

.. admonition:: Read this before Lecture 6
   :class: important

   This page is **pre-read material**, not lecture content. It explains what
   a planning problem is, on a toy world with two rooms, one robot and two
   boxes: states as sets of facts, actions with preconditions and effects, a
   goal, and a plan worked out by hand. It ends with the same toy world
   written in PDDL. Reading takes about 25 minutes.

   L6 does not repeat this page. It builds a PDDL model of ARIAC Task 1,
   writes problems from the factory state, and runs the Fast Downward
   planner from Python (see :ref:`Where L6 Picks Up <preread-pddl-l6>`).


Why a Planner
-------------

Your GP1 behavior tree runs the Task 1 steps in an order your team wrote
down in advance. A **planner** works the other way round. You describe what
the world looks like, what each action needs and what it changes, and what
you want. The planner finds an order of actions that gets you there.

The description is written in **PDDL**, the Planning Domain Definition
Language. `Planning.wiki <https://planning.wiki/guide/whatis/pddl>`__ calls
it "a family of languages which allow us to define a planning problem".

The ideas are easier to see on a world small enough to solve by hand, so
this page uses one with no ARIAC in it.


The Two-Room World
------------------

- There are two rooms, ``room1`` and ``room2``, and a mobile robot that can
  drive between them.
- The robot has **one** hand: it holds at most one box at a time.
- There are two boxes, ``box1`` and ``box2``.

.. list-table:: The start and the goal
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - **room1**
     - **room2**
   * - **Start**
     - the robot (hand empty), ``box1``, ``box2``
     - nothing
   * - **Goal**
     - (does not matter)
     - ``box1``, ``box2``

The robot can do three things: **move** to the other room, **pick** up a
box in the room it is in, and **drop** the box it holds.

This is a smaller version of Gripper, a benchmark from the 1998
International Planning Competition (see :ref:`preread-pddl-reading`). In
Gripper, a robot with two grippers carries balls between two rooms.


Facts and States
----------------

A **fact** is a statement that is either true or false. The two-room world
needs four kinds:

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - **Fact**
     - **True when**
   * - ``robot-in room1``
     - the robot is in room1 (also ``robot-in room2``)
   * - ``box-in box1 room1``
     - box1 is on the floor of room1 (one fact per box and per room)
   * - ``hand-empty``
     - the robot holds nothing
   * - ``holding box1``
     - the robot holds box1 (also ``holding box2``)

A **state** is the **set of facts that are true** at one moment. The start
state is:

.. code-block:: text

   { robot-in room1, box-in box1 room1, box-in box2 room1, hand-empty }

A fact that is not in the set is **false**. ``holding box1`` is not listed,
so at the start the robot does not hold box1. ``box-in box1 room2`` is not
listed, so box1 is not in room2. L6 names this rule (the closed-world
assumption) and shows where it matters for ARIAC.

.. note::

   A state lists only what is true. Nobody writes "box1 is not in room2":
   leaving the fact out says it.


Actions: Preconditions and Effects
----------------------------------

An **action** is described by three sets of facts:

- **Preconditions**: the facts that must be true before the action can run.
- **Add effects**: the facts the action makes true.
- **Delete effects**: the facts the action makes false.

An action has **parameters**, written here with a ``?``: ``pick ?box ?room``
stands for every pick, of any box, in any room. Filling the parameters in,
as in ``pick box1 room1``, gives one concrete action.

.. list-table:: The three actions of the two-room world
   :header-rows: 1
   :widths: 19 27 24 30
   :class: compact-table

   * - **Action**
     - **Preconditions**
     - **Add effects**
     - **Delete effects**
   * - ``move ?from ?to``
     - ``robot-in ?from``
     - ``robot-in ?to``
     - ``robot-in ?from``
   * - ``pick ?box ?room``
     - ``robot-in ?room``, ``box-in ?box ?room``, ``hand-empty``
     - ``holding ?box``
     - ``box-in ?box ?room``, ``hand-empty``
   * - ``drop ?box ?room``
     - ``robot-in ?room``, ``holding ?box``
     - ``box-in ?box ?room``, ``hand-empty``
     - ``holding ?box``

Read ``pick`` out loud: *the robot can pick up a box in a room if it is in
that room, the box is there, and its hand is empty. Afterwards it holds the
box, the box is no longer on the floor, and the hand is no longer empty.*


.. _preread-pddl-apply:

Applying One Action
-------------------

Applying an action to a state takes three steps:

1. **Check.** Every precondition must be in the state. If one is missing,
   the action cannot run here.
2. **Delete.** Remove the delete effects from the state.
3. **Add.** Add the add effects to the state.

**Worked example:** apply ``pick box1 room1`` to the start state.

1. **Check.** The preconditions are ``robot-in room1``,
   ``box-in box1 room1`` and ``hand-empty``. All three are in the start
   state, so the action can run.
2. **Delete** ``box-in box1 room1`` and ``hand-empty``:

   .. code-block:: text

      { robot-in room1, box-in box2 room1 }

3. **Add** ``holding box1``:

   .. code-block:: text

      { robot-in room1, box-in box2 room1, holding box1 }

Every fact the action does not mention stays as it was. Here,
``robot-in room1`` and ``box-in box2 room1`` carry over unchanged.


The Goal
--------

A **goal** is a set of facts that must all be true at the end. Here:

.. code-block:: text

   { box-in box1 room2, box-in box2 room2 }

The goal says nothing about the robot, so a final state with the robot in
either room reaches it. A goal lists only the facts you care about.


A Plan by Hand
--------------

A **plan** is a sequence of actions that turns the start state into a state
that contains the goal. Each action must be possible in the state the one
before it left.

The robot holds one box at a time, so it must carry box1, come back, then
carry box2:

.. list-table:: A 7-step plan, and the state after each step
   :header-rows: 1
   :widths: 7 23 70
   :class: compact-table

   * - **Step**
     - **Action**
     - **State after the step**
   * - 0
     - (start)
     - robot-in room1, box-in box1 room1, box-in box2 room1, hand-empty
   * - 1
     - ``pick box1 room1``
     - robot-in room1, box-in box2 room1, **holding box1**
   * - 2
     - ``move room1 room2``
     - **robot-in room2**, box-in box2 room1, holding box1
   * - 3
     - ``drop box1 room2``
     - robot-in room2, **box-in box1 room2**, box-in box2 room1,
       **hand-empty**
   * - 4
     - ``move room2 room1``
     - **robot-in room1**, box-in box1 room2, box-in box2 room1, hand-empty
   * - 5
     - ``pick box2 room1``
     - robot-in room1, box-in box1 room2, **holding box2**
   * - 6
     - ``move room1 room2``
     - **robot-in room2**, box-in box1 room2, holding box2
   * - 7
     - ``drop box2 room2``
     - robot-in room2, box-in box1 room2, **box-in box2 room2**,
       **hand-empty**

Bold marks the facts each step added. After step 7, both goal facts are in
the state, so the plan reaches the goal.

**Why 7 steps is the fewest.**

1. Each box must be picked once and dropped once: 2 × 2 = 4 steps.
2. The robot carries one box at a time, so it drives from room1 to room2
   twice, and must come back to room1 once in between: 3 moves.
3. 4 + 3 = 7.

Plans are not unique. Moving box2 first gives another 7-step plan. A
planner returns one plan, not all of them.


Checking a Plan in Python
-------------------------

The rules above fit in a short program. Each state is a Python ``set`` of
strings; each action returns its three sets; ``replay`` applies a plan one
step at a time, with the check, delete and add steps of
:ref:`Applying One Action <preread-pddl-apply>`.

.. code-block:: python
   :caption: two_rooms.py
   :linenos:

   """Replay a plan in the two-room world: states are sets of facts."""

   # The start: the robot and both boxes in room1, the hand empty.
   start = {'robot-in room1', 'box-in box1 room1', 'box-in box2 room1',
            'hand-empty'}
   goal = {'box-in box1 room2', 'box-in box2 room2'}


   def move(frm, to):
       return {'pre': {f'robot-in {frm}'},
               'add': {f'robot-in {to}'},
               'delete': {f'robot-in {frm}'}}


   def pick(box, room):
       return {'pre': {f'robot-in {room}', f'box-in {box} {room}',
                       'hand-empty'},
               'add': {f'holding {box}'},
               'delete': {f'box-in {box} {room}', 'hand-empty'}}


   def drop(box, room):
       return {'pre': {f'robot-in {room}', f'holding {box}'},
               'add': {f'box-in {box} {room}', 'hand-empty'},
               'delete': {f'holding {box}'}}


   ACTIONS = {'move': move, 'pick': pick, 'drop': drop}


   def replay(plan):
       state = set(start)
       print('start:', sorted(state))
       for i, step in enumerate(plan, start=1):
           name, *args = step.split()
           action = ACTIONS[name](*args)
           missing = action['pre'] - state
           if missing:
               print(f'step {i} ({step}) cannot run: missing {sorted(missing)}')
               return
           state = (state - action['delete']) | action['add']
           print(f'step {i} ({step}):', sorted(state))
       print('goal reached:', goal <= state)


   print('Plan 1')
   replay(['pick box1 room1', 'move room1 room2', 'drop box1 room2',
           'move room2 room1', 'pick box2 room1', 'move room1 room2',
           'drop box2 room2'])
   print()
   print('Plan 2')
   replay(['pick box1 room1', 'drop box1 room2'])

- Line 37, ``action['pre'] - state``, is the check: the preconditions that
  are not in the state.
- Line 41, ``(state - action['delete']) | action['add']``, is the delete
  step, then the add step.
- Line 43, ``goal <= state``, asks whether every goal fact is in the
  state.

It needs only Python, no packages. Run it with ``python3 two_rooms.py``.
Our run used Python 3.12.3 (Ubuntu 24.04); ``sorted`` prints each state in
alphabetical order:

.. code-block:: text

   Plan 1
   start: ['box-in box1 room1', 'box-in box2 room1', 'hand-empty', 'robot-in room1']
   step 1 (pick box1 room1): ['box-in box2 room1', 'holding box1', 'robot-in room1']
   step 2 (move room1 room2): ['box-in box2 room1', 'holding box1', 'robot-in room2']
   step 3 (drop box1 room2): ['box-in box1 room2', 'box-in box2 room1', 'hand-empty', 'robot-in room2']
   step 4 (move room2 room1): ['box-in box1 room2', 'box-in box2 room1', 'hand-empty', 'robot-in room1']
   step 5 (pick box2 room1): ['box-in box1 room2', 'holding box2', 'robot-in room1']
   step 6 (move room1 room2): ['box-in box1 room2', 'holding box2', 'robot-in room2']
   step 7 (drop box2 room2): ['box-in box1 room2', 'box-in box2 room2', 'hand-empty', 'robot-in room2']
   goal reached: True

   Plan 2
   start: ['box-in box1 room1', 'box-in box2 room1', 'hand-empty', 'robot-in room1']
   step 1 (pick box1 room1): ['box-in box2 room1', 'holding box1', 'robot-in room1']
   step 2 (drop box1 room2) cannot run: missing ['robot-in room2']

1. Plan 1 is the table above, and it reaches the goal.
2. Plan 2 forgets to move. ``drop box1 room2`` needs ``robot-in room2``,
   which is false after step 1, so the plan stops at step 2.

The program only checks a plan you give it. A planner has to **find** the
plan: it tries actions from the start state until it reaches a state that
contains the goal. L6 explains how planners search, and how they check a
plan someone else wrote.


The Same World in PDDL
----------------------

PDDL writes the same model in two files:

- the **domain**: the kinds of objects, the kinds of facts, and the
  actions. It describes every two-room world.
- the **problem**: the objects of one situation, the start state and the
  goal.

.. code-block:: lisp
   :caption: domain.pddl

   (define (domain two-rooms)
     (:requirements :strips :typing)
     (:types room box)

     (:predicates
       (robot-in ?r - room)
       (box-in ?b - box ?r - room)
       (hand-empty)
       (holding ?b - box))

     (:action move
       :parameters (?from - room ?to - room)
       :precondition (robot-in ?from)
       :effect (and (robot-in ?to) (not (robot-in ?from))))

     (:action pick
       :parameters (?b - box ?r - room)
       :precondition (and (robot-in ?r) (box-in ?b ?r) (hand-empty))
       :effect (and (holding ?b) (not (box-in ?b ?r)) (not (hand-empty))))

     (:action drop
       :parameters (?b - box ?r - room)
       :precondition (and (robot-in ?r) (holding ?b))
       :effect (and (box-in ?b ?r) (hand-empty) (not (holding ?b)))))

.. code-block:: lisp
   :caption: problem.pddl

   (define (problem move-two-boxes)
     (:domain two-rooms)
     (:objects room1 room2 - room
               box1 box2 - box)
     (:init (robot-in room1)
            (box-in box1 room1)
            (box-in box2 room1)
            (hand-empty))
     (:goal (and (box-in box1 room2)
                 (box-in box2 room2))))

.. list-table:: From this page to PDDL
   :header-rows: 1
   :widths: 38 62
   :class: compact-table

   * - **On this page**
     - **In PDDL**
   * - The fact ``box-in box1 room1``
     - ``(box-in box1 room1)``: the name first, then the objects, all in
       parentheses
   * - A kind of fact, with parameters
     - A **predicate** in ``:predicates``, such as
       ``(box-in ?b - box ?r - room)``
   * - Preconditions
     - ``:precondition``, with ``and`` around several facts
   * - Add effects
     - The facts listed in ``:effect``
   * - Delete effects
     - The facts in ``:effect`` wrapped in ``(not ...)``
   * - The start state
     - ``:init`` in the problem; every fact not listed is false
   * - The goal
     - ``:goal`` in the problem

- ``?b - box`` says the parameter ``?b`` stands for an object of **type**
  ``box``. Types stop the planner from trying ``pick room1 box1``.
- ``:requirements`` names the PDDL features a file uses. Planning.wiki's
  `requirements page <https://planning.wiki/ref/pddl/requirements>`__ says
  ``:strips`` "Allows the usage of basic add and delete effects as
  specified in STRIPS" and ``:typing`` "Allows the usage of typing for
  objects".

We gave these two files to Fast Downward, the planner L6 uses
(``unified-planning`` 1.3.0 with ``up-fast-downward`` 1.0.0, Fast Downward
26.6, on 2026-10-12). With its optimal setting, it returned the 7-step plan
of the table above. L6 shows how to run it.


.. _preread-pddl-l6:

Where L6 Picks Up
-----------------

L6 assumes everything above and builds on it:

- :ref:`The assumptions behind this kind of planning <l6-assumptions>`, and
  where each one does not hold in the ARIAC factory.
- :ref:`How a planner searches <l6-search>`, and the difference between a
  shortest plan and a quick one.
- :ref:`A PDDL domain for ARIAC Task 1 <l6-domain>`: eight actions, from
  picking a cell off the conveyor to submitting the kit, and two modeling
  mistakes made on purpose.
- :ref:`A problem generator <l6-generator>` that writes the problem file
  from the factory state.
- :ref:`Running Fast Downward from Python <l6-planner>` and
  :ref:`checking a plan with a validator <l6-checking>`.
- :ref:`The limits of PDDL <l6-strains>`: the kit voltage arithmetic, and
  problems with many objects.


Check Yourself
--------------

Answer each question before you open its answer.

.. dropdown:: 1. Write the state after step 3 of the plan. Which facts are false in it?
   :class-container: sd-border-secondary

   ``{ robot-in room2, box-in box1 room2, box-in box2 room1, hand-empty }``.

   Every fact not in the set is false: ``robot-in room1``,
   ``box-in box1 room1``, ``box-in box2 room2``, ``holding box1`` and
   ``holding box2``.

.. dropdown:: 2. Right after step 1 (pick box1 room1), can the robot run drop box1 room1? What state does it reach?
   :class-container: sd-border-secondary

   Yes. The preconditions are ``robot-in room1`` and ``holding box1``, and
   both are true after step 1. The action deletes ``holding box1`` and adds
   ``box-in box1 room1`` and ``hand-empty``: the result is the start state
   again. Nothing in the model forbids an action that undoes another one; a
   plan with it is valid, only longer.

.. dropdown:: 3. Add a third box, box3, in room1, and add box-in box3 room2 to the goal. How many steps does the shortest plan take?
   :class-container: sd-border-secondary

   11 steps.

   1. Picks and drops: 3 boxes × 2 = 6 steps.
   2. Moves: the robot drives from room1 to room2 once per box, 3 times,
      and comes back between trips, 2 times: 5 moves.
   3. 6 + 5 = 11.

   Fast Downward's optimal setting returned an 11-step plan for this
   problem in our run.

.. dropdown:: 4. Someone forgets hand-empty in the add effects of drop. What happens to the plan?
   :class-container: sd-border-secondary

   After the first ``drop``, ``hand-empty`` stays false for good: ``pick``
   deleted it, and no action adds it back. So the second ``pick`` can never
   run, and no plan reaches the goal. Fast Downward, given this broken
   domain, reported the problem unsolvable in our run.

   A wrong effect does not cause an error message: it changes which plans
   exist.

.. dropdown:: 5. How many different states contain the goal, in this world?
   :class-container: sd-border-secondary

   2. When both boxes are in room2, the robot holds neither, so
   ``hand-empty`` is true. Only the robot's room is left open: room1 or
   room2. The 7-step plan ends in the one with the robot in room2.

.. dropdown:: 6. The start state of problem.pddl does not list (robot-in room2). Is that a mistake?
   :class-container: sd-border-secondary

   No. A fact not listed in ``:init`` is false, so the robot is not in
   room2 at the start. Writing every false fact would make the file long
   and add nothing.


.. _preread-pddl-reading:

Further Reading
---------------

- `What is PDDL? <https://planning.wiki/guide/whatis/pddl>`__,
  `PDDL domain <https://planning.wiki/ref/pddl/domain>`__,
  `PDDL problem <https://planning.wiki/ref/pddl/problem>`__ and
  `PDDL requirements <https://planning.wiki/ref/pddl/requirements>`__, on
  Planning.wiki: a reference for every part of the files above.
- `Gripper, IPC 1998
  <https://github.com/potassco/pddl-instances/tree/master/ipc-1998/domains/gripper-round-1-strips>`__:
  the benchmark the two-room world is based on, with its domain file and
  problem files (a robot with a left and a right gripper, two rooms, and
  balls).
- M. Ghallab, D. Nau and P. Traverso, `Acting, Planning, and Learning
  <https://projects.laas.fr/planning/>`__, Cambridge University Press,
  2025. The site links a free preprint of the book.
- P. Haslum, N. Lipovetzky, D. Magazzeni and C. Muise, `An Introduction to
  the Planning Domain Definition Language
  <https://doi.org/10.2200/S00900ED2V01Y201902AIM042>`__, Synthesis
  Lectures on Artificial Intelligence and Machine Learning, 2019.
- R. E. Fikes and N. J. Nilsson, `STRIPS: A New Approach to the
  Application of Theorem Proving to Problem Solving
  <https://doi.org/10.1016/0004-3702(71)90010-5>`__, *Artificial
  Intelligence* 2:189 to 208, 1971: where states as sets of facts and
  actions with add and delete effects come from.
