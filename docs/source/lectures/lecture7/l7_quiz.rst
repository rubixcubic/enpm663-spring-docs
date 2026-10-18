====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 4,
   in Week 10, covers L7 and L8. Working through this page is good
   preparation for it. Memorizing the answers below is not.

This quiz covers Lecture 7: the plan-to-BT factory and the guard, act,
verify pattern, the Retry and Timeout decorators and their nesting order, the
four responses to a failure, the replanning loop, reading BehaviorTree.CPP,
and debugging a running tree. Every question can be answered from the slides
shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 9)
==================================

.. admonition:: Question 1
   :class: hint

   In the plan-to-BT factory, what does a **builder** do?

   A. It sends the goal of one plan step to a skill

   B. It takes an action's arguments and returns a subtree for that step

   C. It writes the PDDL problem from the blackboard

   D. It ticks the tree until the plan succeeds or fails

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The registry maps each action name to a builder, and the factory calls the
   builder of each action in plan order. **A** is the act leaf inside the
   subtree; **C** is the L6 problem generator; **D** is the executor's tick
   loop.


.. admonition:: Question 2
   :class: hint

   A plan contains ``(move-avg agv1 inspection shipping)`` as its fifth step,
   a misspelling of ``move-agv``. What happens?

   A. Steps 1 to 4 run, then step 5 fails when it is ticked

   B. The factory skips step 5 and runs the other four

   C. The factory raises an error when it builds the tree, before any goal is
      sent

   D. The planner rejects the plan

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The registry has no builder for ``move-avg``, so ``build_tree`` stops with
   ``step 5: no builder for move-avg`` and Demo 1 reports ``goals sent: 0``.
   The error appears before any robot moves, not after four cells are on the
   tray.


.. admonition:: Question 3
   :class: hint

   Why is the root of the plan a Sequence **with memory**?

   A. So that it can hold more than one child

   B. So that a failed step is retried automatically

   C. So that on the next tick it resumes at the step that was RUNNING, and
      finished steps are not run again

   D. So that it ticks every step on every tick

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A Sequence without memory ticks its children from the first one on every
   tick, so a finished step runs again (**D** describes that bug). Neither
   kind retries a failed step (**B**): after a failure, both start from the
   first child the next time they are ticked.


.. admonition:: Question 4
   :class: hint

   In the guard, act, verify, update pattern for ``place-in-slot``, which
   leaf writes ``(in-slot c3 agv1 s3)`` to the blackboard, and when?

   A. The guard, before the act sends the goal

   B. The act, as soon as the goal is accepted

   C. The verify, when ``/agv1/tray_status`` shows the slot occupied

   D. The update, only after the verify succeeds

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   The leaves run left to right. The guard reads preconditions, the act sends
   the goal, the verify checks the effect in the factory, and the update
   writes the effects only after the verify succeeds. So the blackboard never
   records an effect that did not happen.


.. admonition:: Question 5
   :class: hint

   A pick step is wrapped in ``Retry(..., num_failures=3)``, and the mock pick
   fails every time. How many pick goals are sent, and what does Retry
   return?

   A. 3 goals, then FAILURE

   B. 4 goals, then FAILURE

   C. 3 goals, then RUNNING forever

   D. 1 goal, then FAILURE

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   ``num_failures=3`` allows three attempts in all. After the third failure,
   Retry returns FAILURE and the plan fails with it: Demo 2 with three
   failures prints ``plan FAILURE after 6 ticks; 3 goals sent``. Retries are
   always bounded.


.. admonition:: Question 6
   :class: hint

   According to the ARIAC 2025 **code** (``voltage_tester_plugin.cpp``), what
   does a malfunctioning voltage tester do?

   A. It stops publishing ``/voltage_tester_N/voltage``

   B. It keeps publishing every 0.1 s, with voltage −1 and
      ``operation_status`` ``MALFUNCTIONING``

   C. It publishes a random voltage with ``operation_status``
      ``OPERATIONAL``

   D. It publishes the last good voltage again and again

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   **A** is what the Challenges page says. The code keeps publishing, so a
   reading leaf must check ``operation_status`` and skip −1, and a Timeout
   around it fails the step in both cases.


.. admonition:: Question 7
   :class: hint

   An act has a 10 s limit and three attempts, nested as
   ``Retry(Timeout(act))``. The act never finishes. About how long can the
   step take before it fails (ignore the tick period)?

   A. 10 s

   B. 13 s

   C. 30 s

   D. It never fails

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With Retry outside, each attempt gets its own 10 s limit:
   3 × 10 = 30 s. With ``Timeout(Retry(act))``, the three attempts would share
   one 10 s limit (**A**).


.. admonition:: Question 8
   :class: hint

   In Demo 4 (``hang``), why did ``Retry(Timeout(act))`` fail at 0.64 s and
   not at 3 × 0.2 = 0.60 s?

   A. The Timeout fired late on every attempt by 0.04 s

   B. Each new attempt started about one tick (0.02 s) after the last one
      ended, so attempts started at 0.00, 0.22 and 0.44 s

   C. Retry waits 0.04 s before it returns FAILURE

   D. The act took 0.04 s to start

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The tick period was 0.02 s. Each attempt ran 0.2 s, and Retry started the
   next one on the next tick, so the third attempt started at 0.44 s and was
   cut at 0.44 + 0.20 = 0.64 s.


.. admonition:: Question 9
   :class: hint

   Which ``py_trees`` node matches BehaviorTree.CPP's ``ReactiveFallback``?

   A. ``Sequence`` with memory

   B. ``Sequence`` without memory

   C. ``Selector`` with memory

   D. ``Selector`` without memory

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   ``Fallback`` matches a ``Selector`` with memory, and ``ReactiveFallback``
   a ``Selector`` without memory. In the same way, ``Sequence`` matches a
   ``Sequence`` with memory and ``ReactiveSequence`` one without.


True or False (Questions 10 to 14)
==================================

.. admonition:: Question 10
   :class: hint

   After a child fails, a Sequence with memory resumes at that child the next
   time it is ticked.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   After a child fails, both kinds of Sequence start again from the first
   child the next time they are ticked. Memory only matters for a child that
   was RUNNING.


.. admonition:: Question 11
   :class: hint

   A ``py_trees`` Timeout with ``duration=2.0`` fails its child at exactly
   2.0 s.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Timeout checks the clock only when it is ticked, so it fires up to one
   tick period late. In Demo 3 the tree was ticked every 0.05 s.


.. admonition:: Question 12
   :class: hint

   When a replanning trigger fires while AGV 1 is moving, the executor
   cancels ``/agv1/move`` and replans at once.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ARIAC's ``/agvN/move`` action rejects cancel requests
   (``agv_motion_plugin.cpp``). A moving AGV finishes its move, and the
   executor waits for the result before it replans. A course skill, in
   contrast, accepts a cancel.


.. admonition:: Question 13
   :class: hint

   In Demo 5, plan 2 has steps that place ``c1`` and ``c2`` again.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The new problem is written from the current blackboard, which records
   ``(in-slot c1 agv1 s1)`` and ``(in-slot c2 agv1 s2)``. Plan 2 recycles
   ``c3`` and places ``c4`` and ``c5``; it has no step for ``c1`` or ``c2``.


.. admonition:: Question 14
   :class: hint

   BehaviorTree.CPP's ``RetryUntilSuccessful num_attempts="3"`` and
   ``py_trees``' ``Retry(num_failures=3)`` allow the same number of attempts.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Both allow three attempts in all: the mapping table pairs
   ``RetryUntilSuccessful`` (port ``num_attempts``) with ``Retry``
   (``num_failures``). With three failures, the ``PlaceCell`` tree in each
   library prints three ``FAILURE`` lines and fails; with one failure, both
   succeed on the second attempt.


Short Answer (Questions 15 to 18)
=================================

.. admonition:: Question 15
   :class: hint

   Why does a leaf that watches only for silence never fire during an ARIAC
   2025 voltage tester malfunction? What does the lecture put in its place?

.. dropdown:: Answer
   :class-container: sd-border-success

   In the ARIAC 2025 code a malfunctioning tester keeps publishing every
   0.1 s, with voltage −1 and ``MALFUNCTIONING``, so messages never stop. The
   reading leaf checks ``operation_status`` on every message and skips −1,
   and a Timeout around it fails the step when no valid readings arrive. In
   Demo 3 that gave ``FAILURE after 2.00 s`` with 20 messages, all skipped.


.. admonition:: Question 16
   :class: hint

   In "Demo 1 again", the root was built with ``memory=False``. What happened
   on tick 3, and why did the plan fail although nothing went wrong in the
   factory?

.. dropdown:: Answer
   :class-container: sd-border-success

   On tick 3 the root started step 1 again, though step 1 had finished on
   tick 2. Step 1's guard checked ``(on-tester c3 tester1)``, which was false
   because the robot had already taken ``c3``, so the step failed and the
   plan failed with it. Without the guard (``noguard``), the pick goal was
   sent a second time while the robot still held ``c3``.


.. admonition:: Question 17
   :class: hint

   Three Li-Ion cells at 3.70 V each are on the tray (values chosen for this
   question). Has the kit window closed? Show the arithmetic.

.. dropdown:: Answer
   :class-container: sd-border-success

   No.

   1. The three cells total 3 × 3.70 = 11.10 V.
   2. The kit window is 14.25 V to 14.55 V, so the fourth cell must be from
      14.25 − 11.10 = 3.15 V to 14.55 − 11.10 = 3.45 V.
   3. An acceptable cell is 3.4 V to 3.8 V. The two ranges overlap from
      3.40 V to 3.45 V, so a fourth cell can still complete the kit. In the
      lecture's example (three cells at 3.75 V) the range was 3.00 V to
      3.30 V, with no overlap.


.. admonition:: Question 18
   :class: hint

   Why should the GP3 executor not care where a plan came from?

.. dropdown:: Answer
   :class-container: sd-border-success

   The contract is only a list of ground actions (names and arguments) that
   the executor knows how to run. In L8 and GP4 an LLM agent writes the same
   action names and arguments instead of the PDDL planner, and the same
   executor runs them. An executor tied to the planner would have to be
   rewritten; one that follows the contract carries over unchanged.
