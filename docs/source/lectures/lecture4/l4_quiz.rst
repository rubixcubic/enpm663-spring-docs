====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 2,
   next week, covers L4. Working through this page is good preparation for
   it. Memorizing the answers below is not.

This quiz covers Lecture 4: trees and state machines, the BT primitives,
ticks and memory, blackboards, ``py_trees_ros`` leaves and the three
demonstration runs, and the patterns for the GP1 tree. Every question can be
answered from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences, or the steps of a
     calculation.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 12)
===================================

.. admonition:: Question 1
   :class: hint

   The lecture's FSM for one GP1 step has 6 states and 5 normal transitions.
   After Change 1 (stop when a skill or the tester fails), how many
   transitions does it have?

   A. 5

   B. 6

   C. 9

   D. 12

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Each of the 4 working states (``read_voltage``, ``pick_from_tester``,
   ``place_in_slot``, ``recycle_cell``) needs its own arrow to ``stopped``:
   5 + 4 = 9. The BT needs no new node for the same change. 12 is the count
   after Change 2, the second pick attempt.


.. admonition:: Question 2
   :class: hint

   In ``py_trees``, which status means a node has not run yet, or was
   stopped?

   A. ``FAILURE``

   B. ``RUNNING``

   C. ``INVALID``

   D. ``SUCCESS``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ``SUCCESS`` and ``FAILURE`` mean the node is done; ``RUNNING`` means it
   needs more ticks. ``INVALID`` is what the outputs show for a child a
   composite never ticked, and for a leaf a ``Timeout`` stopped.


.. admonition:: Question 3
   :class: hint

   A sequence with memory has three children: ``check`` returns ``SUCCESS``,
   ``pick`` returns ``FAILURE``, and ``place`` would return ``SUCCESS``. After
   one tick, what are the sequence's status and ``place``'s status?

   A. Sequence ``FAILURE``; ``place`` ``INVALID``

   B. Sequence ``FAILURE``; ``place`` ``SUCCESS``

   C. Sequence ``RUNNING``; ``place`` ``INVALID``

   D. Sequence ``SUCCESS``; ``place`` ``SUCCESS``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   A sequence returns ``FAILURE`` as soon as one child fails, so it stops at
   ``pick``. ``place`` is never ticked and stays ``INVALID``, as ``update``
   does in case 2 of ``composite_status.py``.


.. admonition:: Question 4
   :class: hint

   A parallel ``wait_for_reading`` has the policy
   ``SuccessOnSelected([wait_for_voltage])`` with the default
   ``synchronise``. Its child ``tester_ok`` succeeds on tick 1. What happens
   to ``tester_ok`` on ticks 2 to 5?

   A. It is ticked on every tick, and fails as soon as the tester breaks.

   B. It is skipped; it keeps the ``SUCCESS`` from tick 1, even after the
      tester breaks.

   C. It is reset to ``INVALID`` and ticked again on tick 5 only.

   D. It is removed from the tree.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ``synchronise`` is ``True`` by default: a child that has succeeded is
   skipped on later ticks. In ``parallel_watch.py``, ``tester_ok`` was checked
   1 time, the tester broke on tick 2 unseen, and the average was −0.078 V.
   With ``synchronise=False`` the check runs on every tick and ends the wait
   on tick 2.


.. admonition:: Question 5
   :class: hint

   Which decorator returns ``FAILURE`` when its child is still ``RUNNING``
   after a set number of seconds, and stops the child?

   A. ``Retry``

   B. ``Inverter``

   C. ``EternalGuard``

   D. ``Timeout``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   ``Timeout`` takes a ``duration``. ``Retry`` gives a failed child another
   attempt; ``Inverter`` swaps ``SUCCESS`` and ``FAILURE``; ``EternalGuard``
   checks a condition before every tick of its child.


.. admonition:: Question 6
   :class: hint

   An ``Inverter``'s child returns ``RUNNING``. What does the ``Inverter``
   return?

   A. ``SUCCESS``

   B. ``FAILURE``

   C. ``RUNNING``

   D. ``INVALID``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ``Inverter`` swaps only ``SUCCESS`` and ``FAILURE``. A running child has no
   result yet, so the output shows ``child=RUNNING -> RUNNING``.


.. admonition:: Question 7
   :class: hint

   In which method does a ``py_trees_ros`` action leaf send its goal?

   A. ``setup``

   B. ``initialise``

   C. ``update``

   D. ``terminate``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ``initialise`` runs when the node starts running (its last status was not
   ``RUNNING``). ``setup`` creates the client and waits for the server, once;
   ``update`` checks the result on every tick; ``terminate`` cancels the goal
   if the leaf was stopped while running.


.. admonition:: Question 8
   :class: hint

   In ``retry_demo.py`` without memory, the place starts on tick 4. Why is it
   stopped on tick 5?

   A. The ``Retry`` has used up its 2 failures.

   B. The tick starts again at the check; the pick, no longer running, starts
      again, and the running pick ends the sequence's tick.

   C. The place leaf fails on its first attempt.

   D. A ``Timeout`` stops it after one tick.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Without memory, every tick starts at the first child. On tick 5 the
   sequence ticks the ``Retry``, which ticks the pick. The pick returned
   ``SUCCESS`` on tick 4, so it is not running, and ticking it again starts it
   again: its ``initialise`` runs and it returns ``RUNNING``. The sequence
   then stops the place (``INVALID``).
   On a robot this sends a new pick goal for a cell the gripper already
   holds.


.. admonition:: Question 9
   :class: hint

   A ``py_trees_ros.service_clients.FromConstant`` leaf calls the kit check
   service, and the reply says the kit is rejected. What does the leaf
   return?

   A. ``FAILURE``, because the reply is negative

   B. ``RUNNING``, until a positive reply arrives

   C. ``INVALID``

   D. ``SUCCESS``, because the reply arrived

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   A service leaf returns ``RUNNING`` until the reply arrives, then
   ``SUCCESS``, whatever the reply says (``FAILURE`` only if the request could
   not be sent). Run 3 shows
   ``check_kit SUCCESS`` with ``success=False``. Only the condition
   ``kit_is_good`` after it made the tree fail.


.. admonition:: Question 10
   :class: hint

   Why does a ``py_trees_ros`` tree whose leaves never wait inside a tick not
   block its node's other callbacks?

   A. Each leaf runs in its own thread.

   B. The ticks come from a ROS 2 timer callback, so subscription and action
      callbacks run between ticks.

   C. The tree ticks only when a message arrives.

   D. ``py_trees_ros`` turns off the executor while the tree runs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ``tick_tock(period_ms=100.0)`` creates a timer that ticks the tree every
   100 ms. In run 1, the node heard 21 voltage messages in 21 ticks: none was
   missed while the skills ran. A leaf that waits inside a tick would still
   block the tree and the node's other callbacks.


.. admonition:: Question 11
   :class: hint

   Which ARIAC interface rejects cancel requests, so the tree must not
   interrupt it once it is sent?

   A. The course pick skill

   B. The ``/agvN/move`` action

   C. The voltage tester topic

   D. The check kit quality service

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Once the AGV leaves, it finishes its move. Any interrupt must come before
   the tree sends the AGV. The course skills accept a cancel.


.. admonition:: Question 12
   :class: hint

   In ``blackboard_demo.py``, the leaf ``voltage_in_range`` tries to write
   ``/tester1/voltage``. What happens?

   A. The write succeeds and the next reader sees 0.0 V.

   B. The write is ignored with no message.

   C. An ``AttributeError``: the client does not have write access to that
      key.

   D. The tree returns ``FAILURE``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Each behavior registers its keys with ``Access.READ`` or ``Access.WRITE``.
   Any other access raises an error. ``voltage_in_range`` registered
   the key for reading only.


----


True or False (Questions 13 to 15)
==================================

.. admonition:: Question 13
   :class: hint

   True or false: a selector **with** memory stops a running lower-priority
   child when a higher-priority child succeeds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   A selector with memory skips the higher-priority children while a child is
   running, so this interrupt does not happen there. It happens in a selector
   without memory, which starts every tick at the first child.


.. admonition:: Question 14
   :class: hint

   True or false: the course skills package retries a failed task by itself,
   so the tree does not need a ``Retry``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The skills package never retries a task by itself. Any retry must be in
   your tree, for example a ``Retry`` around the skill leaf.


.. admonition:: Question 15
   :class: hint

   True or false: in run 2, when ``timeout_place`` fired, the stand-in server
   reported the place goal canceled.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   ``timeout_place`` stopped its child: ``place_in_slot`` became ``INVALID``,
   its ``terminate`` sent the cancel, and the log shows
   ``[server] place_in_slot: goal canceled`` at 3.4 s, the same time as the
   timeout.


----


Short Answer (Questions 16 to 18)
=================================

.. admonition:: Question 16
   :class: hint

   A Li-Ion kit already holds three cells of 3.50 V, 3.60 V and 3.65 V. The
   kit window is 14.25 V to 14.55 V, and one cell is good from 3.40 V to
   3.80 V. GP1 checks the kit before every place. Did the check allow the
   third place? Which voltages can the fourth cell have? Show the steps.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. The three cells total 3.50 + 3.60 + 3.65 = 10.75 V.
   2. With one cell missing, three cells must total from
      14.25 − 3.80 = 10.45 V to 14.55 − 3.40 = 11.15 V. 10.75 V is inside, so
      the check allowed the third place.
   3. The fourth cell must be from 14.25 − 10.75 = 3.50 V to
      14.55 − 10.75 = 3.80 V.
   4. It must also be inside 3.40 V to 3.80 V on its own, so the range is
      3.50 V to 3.80 V.

   A cell at 3.45 V passes ``voltage_in_range`` but would make the kit
   10.75 + 3.45 = 14.20 V, below the window. A condition on ``/kit/total``
   must catch it before the place, because cells lock to the tray once
   placed.


.. admonition:: Question 17
   :class: hint

   You write a GP1 subtree with two parts: a sequence of skills (pick, then
   place) and a condition that must stay true while they run. Which goes
   under a composite with memory, which under one without memory (or a
   guard), and why?

.. dropdown:: Answer
   :class-container: sd-border-success

   The sequence of skills goes under a composite with memory: a finished
   skill is not run again, and the tick resumes at the running one. Without
   memory, each tick starts again at the first child and restarts a skill
   that already succeeded, as the ``retry_demo.py`` run without memory shows.
   The condition goes under a composite without memory, or under a guard such
   as ``EternalGuard``, so it is checked again on every tick.


.. admonition:: Question 18
   :class: hint

   In run 2, ``timeout_place`` allows 2.0 s and the place starts at 1.3 s on
   tick 13. Over 10 more runs, the timeout fired on tick 33 in 3 runs and on
   tick 34 in 7. Why does it move between two ticks?

.. dropdown:: Answer
   :class-container: sd-border-success

   The timeout can fail after 1.3 + 2.0 = 3.3 s. ``Timeout`` fails only once
   *more* than 2.0 s have passed, and the 2.0 s mark falls on a tick (the
   tree ticks every 0.1 s). With timer jitter, the tick near the mark sees a
   little more than 2.0 s or a little less, so the failure lands
   on that tick or the next.
