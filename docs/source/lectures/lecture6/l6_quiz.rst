====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 3,
   in Week 7, covers L5 and L6. Working through this page is good
   preparation for it. Memorizing the answers below is not.

This quiz covers Lecture 6: classical planning and its assumptions, the PDDL
domain and problem for Task 1, running Fast Downward through the Unified
Planning Framework, checking a plan, and where PDDL strains. Every question
can be answered from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences, or numbered
     arithmetic steps.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 9)
==================================

.. admonition:: Question 1
   :class: hint

   A problem's initial state lists ``(tester-free tester1)`` and says
   nothing about tester2. What does the planner take as true about tester2?

   A. tester2 is free, because nothing says it is busy

   B. tester2 is not free, because a fact that is not listed is false

   C. Nothing: the planner stops with an error about a missing fact

   D. tester2 is free in half of the states it searches

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   This is the closed-world assumption: a state is the set of facts that are
   true, and a fact not listed is false. **A** is the opposite rule. **C**:
   the planner does not report missing facts; it plans with what it has.
   **D**: a classical planner works with one known state at a time.


.. admonition:: Question 2
   :class: hint

   Which part of ``pick-from-tester`` is a **delete effect**?

   A. ``(on-tester ?c ?t)`` in the precondition

   B. ``(tester-free ?t)`` in the effect

   C. ``(not (on-tester ?c ?t))`` in the effect

   D. ``(serves ?r ?t)`` in the precondition

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A delete effect makes a fact false. **A** and **D** are preconditions:
   facts that must be true before the action. **B** is an effect that makes
   a fact true.


.. admonition:: Question 3
   :class: hint

   Why does the domain have the fixed facts ``serves``, ``picks-conveyor``
   and ``loads-agv``?

   A. They tell the planner which robot can do what; without them, the
      planner would let inspection_robot_2 pick cells off the conveyor

   B. They record the voltage check, so the planner knows which cells to
      recycle

   C. ARIAC publishes them on a topic, and the generator copies them

   D. Fast Downward needs at least one fixed fact per robot to ground the
      actions

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   They are true in every trial and say which robot can reach which tester,
   which robot picks from the conveyor, and which loads the AGV. **B** is
   ``voltage-ok`` and ``voltage-bad``. **C**: the fixed facts are the same in
   every trial, not read from a topic. **D** is not a rule of Fast Downward.


.. admonition:: Question 4
   :class: hint

   ``plan_kit.py`` prints ``8 actions, 15 objects, 5 goal facts`` for
   ``problem.pddl``, which lists 4 cells, 2 robots, 2 testers and 1 AGV.
   Where do the other objects come from?

   A. Fast Downward adds one object per ground action

   B. UPF counts each robot twice, once per tester it serves

   C. The domain's constants: the 2 stations and the 4 slots

   D. The 5 goal facts are counted as objects

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   4 + 2 + 2 + 1 = 9 objects come from the problem. The domain declares
   ``inspection`` and ``shipping`` (stations) and ``s1`` to ``s4`` (slots) as
   constants, objects every problem shares: 9 + 2 + 4 = 15.


.. admonition:: Question 5
   :class: hint

   In UPF, what does ``OneshotPlanner(name="fast-downward")`` run, and what
   does ``"fast-downward-opt"`` run?

   A. Both run A* with LM-cut; the second one also validates the plan

   B. The first runs the ``lama-first`` setup (satisficing); the second runs
      A* with LM-cut (optimal)

   C. The first runs the translator only; the second runs translator and
      search

   D. The first runs VAL; the second runs Fast Downward

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ``lama-first`` is a satisficing setup that returns the first plan it
   finds; A* with the LM-cut heuristic is optimal. Both engines run the
   translator and the search. VAL is a separate validator.


.. admonition:: Question 6
   :class: hint

   On the large problem (8 cells, 2 AGVs), the satisficing planner took
   0.56 s and the optimal planner 14.78 s, and both plans had 38 steps.
   Which conclusion fits these numbers?

   A. The optimal planner found a shorter plan, worth the wait

   B. The optimal planner took 14.78 / 0.56 = 26.4 times longer, for no
      shorter plan

   C. The satisficing planner is always optimal on Task 1 problems

   D. The times show that the large problem has no solution

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Both plans had 38 steps, so waiting bought nothing on this problem.
   **C** claims too much: a satisficing search does not promise the
   shortest plan; it happened to find one here. In a factory, a good plan
   now usually beats the best plan later, because the executor waits while
   the planner searches.


.. admonition:: Question 7
   :class: hint

   ``numeric_try.py`` gives Fast Downward the kit window as numeric PDDL.
   What happens?

   A. Fast Downward finds a kit of four cells inside 14.25 V to 14.55 V

   B. Fast Downward runs out of time while searching

   C. Fast Downward's translator stops at ``:numeric-fluents`` in the
      requirements, and no plan comes back

   D. UPF converts the numbers into true-or-false facts and solves it

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The output shows ``status: INTERNAL_ERROR``, ``plan: None`` and
   ``Reason: Invalid requirement. Got: :numeric-fluents``. Fast Downward
   supports "PDDL 2.2 level 1 plus the :action-costs requirement from PDDL
   3.1", and no part of numerical planning. UPF only warned that it could
   not tell whether Fast Downward could solve the problem.


.. admonition:: Question 8
   :class: hint

   In the small problem (4 cells), ``check-kit`` has 256 of the 311 ground
   actions. Why so many?

   A. It has four cell parameters, and each can be any of the 4 cells:
      4 × 4 × 4 × 4 = 256

   B. It is grounded once per state the search expands

   C. Each of the 4 slots has 64 possible voltages

   D. The translator keeps a copy for every station and slot

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The translator writes out the action with every combination of objects
   for its parameters. With 8 cells and 2 AGVs it is
   2 × 8 × 8 × 8 × 8 = 8192 of the 8334. A per-slot fact
   ``(filled ?a ?s)`` would let ``check-kit`` take only the AGV.


.. admonition:: Question 9
   :class: hint

   Where does the problem generator get the ``slot-free`` facts in ARIAC?

   A. ``/agv1/info``

   B. ``/agv1/tray_status``, which has four occupied flags

   C. ``/voltage_tester_1/voltage``

   D. The domain file

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ``/agv1/info`` gives ``agv-at`` (the AGV's station). The tester topics
   give the averaged voltages behind ``voltage-ok`` and ``voltage-bad``. The
   domain file never changes and holds no facts about one trial.


----


True or False (Questions 10 to 14)
==================================

.. admonition:: Question 10
   :class: hint

   **True or false:** a validator would have rejected the plan that ships
   and submits an empty tray, made with the domain whose ``submit-kit`` had
   lost ``(kit-checked ?a)``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The validator replays the plan on the model it is given. With the
   changed domain, every precondition of that plan holds, so the plan is
   valid. The lecture's warning: a validator would accept both mistaken
   plans, so read the first plan of every new domain against the Task 1
   steps.


.. admonition:: Question 11
   :class: hint

   **True or false:** a satisficing search always returns the shortest plan.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   A satisficing (greedy) search returns a plan quickly, not always the
   shortest. Only A* with an admissible heuristic, one that never
   overestimates, promises a shortest plan.


.. admonition:: Question 12
   :class: hint

   **True or false:** a cell that fails inspection reaches the planner with
   the fact ``voltage-bad``, and inspection_robot_2 recycles it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   A cell that fails inspection goes into the inspection bin and never
   reaches the planner. ``voltage-bad`` is for a cell whose averaged
   voltage is outside 3.4 V to 3.8 V; those are the only cells the robots
   recycle.


.. admonition:: Question 13
   :class: hint

   **True or false:** the domain has no action that takes a cell off a tray.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   In ARIAC, cells lock to the tray once placed (Task 1, Step 1d), so the
   domain does not offer an action the factory does not allow. A kit that
   can no longer be finished is lost: the AGV goes to the recycling
   station.


.. admonition:: Question 14
   :class: hint

   **True or false:** the PDDL action ``move-agv`` is carried out by a goal
   to the course skills package.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   ``move-agv`` maps to ARIAC's action ``/agv1/move``, which your team
   calls itself; it rejects cancel requests. The five pick and place
   actions are the ones that go to the course skills package.


----


Short Answer (Questions 15 to 19)
=================================

.. admonition:: Question 15
   :class: hint

   Name the three assumptions of classical planning, and for each one give
   a way the ARIAC factory breaks it.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. **Full observation**: a cell's defects and voltage are unknown until
      the lidar scan and the tester measure them.
   2. **Deterministic actions**: a malfunctioning tester gives no valid
      reading (−1 V with status ``MALFUNCTIONING``); in Task 2, a vacuum
      grasp can fail.
   3. **A static world**: new cells keep arriving, the conveyor can stop,
      and a high-priority order can arrive at any time.

   So a plan covers a short stretch of work, and the system plans again
   when the factory disagrees with the model.


.. admonition:: Question 16
   :class: hint

   Three Li-Ion cells at 3.70 V each are on agv1's tray (chosen for this
   question). The kit must total 14.25 V to 14.55 V, and each cell must be
   3.4 V to 3.8 V. Which fourth cells complete the kit? Show the steps.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. The tray holds 3 × 3.70 = 11.10 V.
   2. The fourth cell must be at least 14.25 − 11.10 = 3.15 V and at most
      14.55 − 11.10 = 3.45 V.
   3. It must also be at least 3.4 V, so the cells that fit are from
      **3.40 V to 3.45 V**.

   The kit can still be finished, but only by a narrow band of cells.
   Compare three cells at 3.75 V in the lecture: there the fourth had to be
   3.00 V to 3.30 V, and no cell in range could finish the kit.


.. admonition:: Question 17
   :class: hint

   The validator says a plan is ``VALID``. Give two reasons from the
   lecture why it can still fail in the factory.

.. dropdown:: Answer
   :class-container: sd-border-success

   Any two of:

   - **The model has no time**: it does not know that the conveyor keeps
     moving, or that a tester needs about a second to give ten readings.
   - **The model has no geometry**: it does not know that the two
     inspection robots can collide near the testers.
   - **The model is only as true as its facts**: if tester2 malfunctions,
     ``(tester-free tester2)`` can be true in the problem and useless in
     the factory.

   A validator checks the plan against the model, not the model against the
   factory.


.. admonition:: Question 18
   :class: hint

   Why does GP3 choose the cells for a kit in a separate selection step in
   Python, instead of in the PDDL domain?

.. dropdown:: Answer
   :class-container: sd-border-success

   The kit rule is arithmetic on a sum: four voltages must add up to
   14.25 V to 14.55 V, and every cell placed narrows the window for the
   rest. Classical PDDL has only true-or-false facts, and Fast Downward does
   not plan with numeric fluents. So the selection step does the arithmetic
   (with look-ahead) and hands the planner its result as ``in-slot`` goals.
   Numbers stay in ordinary code; PDDL orders the actions.


.. admonition:: Question 19
   :class: hint

   In the 19-step plan, c2 waits on tester2 from step 4 to step 15, while
   the other three cells go through tester1. Why does the planner not avoid
   that wait, and what does it mean for the executor?

.. dropdown:: Answer
   :class-container: sd-border-success

   The model has no time: a plan is an order of steps, and every action
   costs 1, so a cell that waits costs nothing. A classical plan is also a
   single sequence, one step per column, even when the two robots could
   work at the same time. The executor can run steps for different robots
   together when they touch different objects, but the plan itself does not
   say so.
