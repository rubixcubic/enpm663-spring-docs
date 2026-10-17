====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   No in-class quiz covers L11: Quiz 5, the last one, covers L9 and L10.
   What this lecture teaches is graded through GP4 and the final demo, listed
   in the :doc:`syllabus </syllabus/index>`. Memorizing the answers below is
   not the goal; being able to give the reasons is.

This quiz covers Lecture 11: the final demo specification, the failure
taxonomy, behavior tree recovery in ``py_trees``, checking LLM output,
cross-checking the VLM, equipment that stops giving valid readings, the
ARIAC challenges as failure scenarios, and local or global recovery. Every
question can be answered from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 11)
===================================

.. admonition:: Question 1
   :class: hint

   A high-priority order arrives on ``/high_priority_orders`` while a Li-Ion
   kit is half built. No action has failed. Which failure type is this?

   A. Action failure

   B. Sensor failure

   C. Plan failure

   D. World drift

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   World drift means the world changed and no single action failed. The
   lecture's table uses this exact case as its ARIAC example. The signal is
   that the expected state differs from fresh observations, and recovery
   starts in the planner or agent.


.. admonition:: Question 2
   :class: hint

   A VLM reports that tray slot 3 is empty when a cell sits there. Its reply
   is valid JSON that matches the schema. How does the lecture classify this,
   and what can catch it?

   A. A plan failure; layer 2 (schema) catches it.

   B. A sensor failure; a second source, such as ``/agvN/tray_status``, can
      catch it.

   C. An action failure; the tree's Retry catches it.

   D. World drift; the L9 loop catches it without any extra source.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   In the taxonomy figure, VLM output feeds the sensor column: a wrong slot
   is wrong data from a sensor. A VLM error is well formed, so a schema
   check passes it (**A** is wrong). The Cross-Checking the VLM section
   compares the VLM with a second source, and ``/agvN/tray_status`` says
   which of the four slots are occupied, so it is a second source for this
   exact fact.


.. admonition:: Question 3
   :class: hint

   A ``py_trees`` Retry decorator has ``num_failures=3``. Its child fails
   for the first time. What does Retry return on that tick?

   A. ``FAILURE``

   B. ``SUCCESS``

   C. ``RUNNING``, and the child starts again on the next tick

   D. ``RUNNING``, and the child starts again after a built-in wait

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   From the ``py_trees`` 2.6.0 source: when the child fails and Retry has
   seen fewer than ``num_failures`` failures, Retry returns ``RUNNING``, and
   the child starts again on the next tick. There is no wait (**D** is
   wrong); a wait needs a ``Timer`` in a sequence before the action. Retry
   returns ``FAILURE`` only on the third failure.


.. admonition:: Question 4
   :class: hint

   In Run C of the demonstration, tester 1's status changes to
   ``MALFUNCTIONING`` while the place on tester 1 is running. What stops the
   place?

   A. Retry, after counting the malfunction as a failure

   B. The EternalGuard ``tester_1_ok``, which checks its condition before
      every tick

   C. The skill itself, which sees the status and cancels its own goal

   D. The planner, after the tree reports the failure

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   On tick 2 the guard checks its condition first, finds it false, and stops
   the place while it is still running. The selector starts tester 2 in the
   same tick. Retry never sees a failure (**A**), and a skill never decides
   recovery itself (**C**). In ROS, stopping a skill means cancelling its
   action goal, but the tree does it, not the skill.


.. admonition:: Question 5
   :class: hint

   Run D repeats Run B with selector memory off. What goes wrong on tick 4?

   A. The selector skips tester 2 and goes straight to ``hold_cell``.

   B. The selector goes back to tester 1, Retry's count starts again at 1,
      and the place on tester 2 is stopped halfway.

   C. Retry raises an exception because its count passed 3.

   D. Nothing: memory makes no difference in this tree.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   With memory off, the selector starts again from its first child on every
   tick. Tester 1's fourth attempt fails, Retry counts it as failure 1 of 3
   and returns ``RUNNING``, and the selector stops tester 2. With memory on,
   the selector goes on from its running child and stays with tester 2.


.. admonition:: Question 6
   :class: hint

   In ``timeout_demo.py`` the tree is ticked every 0.2 s and the Timeout
   duration is 0.5 s. ``pick_cell`` never finishes. When does the selector
   finish, and through which child?

   A. At 0.4 s, through ``timeout_0.5s``

   B. At 0.6 s, through ``report_to_planner``

   C. At 0.5 s exactly, through ``report_to_planner``

   D. Never: the selector stays ``RUNNING``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The ticks happen at 0.0, 0.2, 0.4 and 0.6 s. At 0.4 s less than 0.5 s has
   passed, so Timeout is still ``RUNNING``. At 0.6 s, more than 0.5 s after
   the pick started, Timeout stops it and fails, and the selector moves on to
   ``report_to_planner``, which succeeds. No tick falls at 0.5 s (**C**).


.. admonition:: Question 7
   :class: hint

   An LLM reply is valid JSON, matches the schema and uses only allowed
   tools, but asks to pick cell ``c9``, which is not in the world state. At
   which layer is it rejected?

   A. Layer 1, syntax

   B. Layer 2, schema

   C. Layer 3, tools

   D. Layer 4, objects

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   Only layer 4, which reads the world state, can catch an invented object.
   This is reply D in the demonstration: ``cell 'c9' is not in the world
   state``. A schema alone would have passed it.


.. admonition:: Question 8
   :class: hint

   An LLM reply fails a check. What does the lecture's policy do next?

   A. Re-prompt until a reply passes.

   B. Re-prompt once with the exact error message; if the second reply also
      fails, take a safe action.

   C. Send the reply to the executor and let the tree retry.

   D. Drop the reply and stop the trial.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Ask again once, with the exact error message (as in L8). If the second
   reply also fails, stop asking and take a safe action: hold position,
   pause the feed, or hand over to the GP3 PDDL plan for the normal flow.
   Policy run 2 shows the fall back.


.. admonition:: Question 9
   :class: hint

   What does the ARIAC code (commit 0c3e722) publish on
   ``/voltage_tester_N/voltage`` during a voltage tester malfunction?

   A. Nothing: the tester stops publishing.

   B. The last good reading, repeated.

   C. A message every 0.1 s with voltage -1 and ``operation_status``
      ``MALFUNCTIONING``.

   D. Noise around 0 V with status ``OPERATIONAL``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A timer publishes every 0.1 s, malfunction or not, and during a
   malfunction each message has voltage -1 and status ``MALFUNCTIONING``.
   **A** is what the ARIAC challenges page says, which is why the watcher
   handles both. **D** is what an empty tester publishes.


.. admonition:: Question 10
   :class: hint

   With no cell on it, tester 2 publishes -0.03 V with status
   ``OPERATIONAL``. What does this reading mean?

   A. Tester 2 is broken.

   B. Tester 2 is empty.

   C. The cell on tester 2 is defective.

   D. The reading is late, so the time limit has passed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   An empty tester publishes noise around 0 V with status ``OPERATIONAL``
   (``voltage_tester_plugin.cpp``, line 144), so about half of those
   readings are negative. A negative reading alone does not mean the tester
   is broken: check the status first.


.. admonition:: Question 11
   :class: hint

   Which ARIAC challenge does the lecture answer with **local** recovery?

   A. The voltage tester malfunction

   B. The high-priority order

   C. The vacuum tool malfunction

   D. All four challenges

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   For the vacuum tool malfunction (Example A), the shell and the tool are
   where they were, and the failure clears once the pads lose contact, so
   the tree retries a sequence that starts by moving the gripper away. The
   conveyor malfunction is local too. The voltage tester malfunction is
   global (the plan assumed two testers), and the high-priority order is
   global (the goal changed).


----


True or False (Questions 12 to 16)
==================================

.. admonition:: Question 12
   :class: hint

   True or false: when a grasp fails, the skill retries it a few times
   itself before it reports a failure to the behavior tree.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The skill never retries a task itself. It returns success or a failure
   reason, and the behavior tree decides first (retry, timeout, another
   branch). Only then does the failure move up to the planner or agent.


.. admonition:: Question 13
   :class: hint

   True or false: GP4 tests the vacuum tool malfunction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The vacuum tool malfunction happens only in Task 2. GP4 tests the
   conveyor malfunction, the voltage tester malfunction and high-priority
   orders; the final demo is the first place your system meets the vacuum
   tool malfunction.


.. admonition:: Question 14
   :class: hint

   True or false: a watcher that waits for the voltage tester's messages to
   stop is enough to detect a malfunction in the current ARIAC code.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The code keeps publishing during a malfunction, so a check that waits for
   the messages to stop never fires. The watcher checks the status on every
   reading and also keeps a time limit, so it catches both the code's
   behavior and the docs' behavior.


.. admonition:: Question 15
   :class: hint

   True or false: a schema check alone would have rejected replies C (a
   made-up tool) and D (a made-up cell) in the demonstration.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   Both replies are valid JSON that match the schema. Layer 3 (tools)
   rejects C, and layer 4 (objects) rejects D. A schema alone would have
   passed both.


.. admonition:: Question 16
   :class: hint

   True or false: who pays for model calls during development was announced
   with the specification in L11.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   Who pays for model calls is still to be decided. The rest is set: the
   grading rubric (75 points for the run, 25 for the class session), the
   code freeze (Friday, April 30, 2027, at 11:59 pm), and the model (Gemini
   Robotics ER as the course example, another VLM allowed on the course key
   (a Google model) or locally, one course key for
   the evaluation runs). The specification itself (what the system must do,
   and how the demo is run) was posted in L11.


----


Short Answer (Questions 17 to 20)
=================================

.. admonition:: Question 17
   :class: hint

   A window holds 3.62, 3.58 and 3.61 V from a Li-Ion cell, then -1 when the
   malfunction starts. Show what happens if the -1 is averaged in, and what
   the watcher's value rule changes.

.. dropdown:: Answer
   :class-container: sd-border-success

   The sum with the -1 kept is :math:`3.62 + 3.58 + 3.61 - 1 = 9.81` V, and
   the average is :math:`9.81 / 4 = 2.45` V. A good Li-Ion cell reads 3.4 V
   to 3.8 V, and 2.45 V is 0.95 V below the lower limit, so the code sends a
   good cell to recycling. With the -1 rejected, the average is
   :math:`10.81 / 3 = 3.60` V, inside the limits.


.. admonition:: Question 18
   :class: hint

   Tester 1 goes down for 45 s during a kit, and the feed rate is 0.1 cells
   per second. How many cells arrive during the outage, and why is the
   recovery global?

.. dropdown:: Answer
   :class-container: sd-border-success

   One cell arrives every 10 s, and :math:`45 / 10 = 4.5`, so four or five
   cells arrive during the outage. A plan that keeps sending cells to
   tester 1 stalls them for the whole outage, because its assumption of two
   working testers is false. An assumption of the plan is false, so the rule
   says replan globally: use tester 2 only, and replan again when tester 1
   returns.


.. admonition:: Question 19
   :class: hint

   The rule for choosing says to call the LLM only when the rule-based
   handlers do not cover the case. Why, and which of the three worked
   examples does call it?

.. dropdown:: Answer
   :class-container: sd-border-success

   The common cases should not cost tokens: a retry or a fixed replan
   handles them without a model call and its latency. Example C, a
   high-priority order with two cells on AGV 1, calls the LLM agent: the
   goal changed, and the agent chooses which AGV takes the NiMH kit, whether
   to finish the Li-Ion kit first, and when to switch the feed back. Its
   plan still passes the five layers of checks before any robot moves.


.. admonition:: Question 20
   :class: hint

   Why is a good cell in the inspection bin a cost you can count, and what
   does it say about a defect detector?

.. dropdown:: Answer
   :class-container: sd-border-success

   A cell passes the inspection door only after a passing inspection report;
   a failing report, or no report, sends it to the inspection bin. A good
   cell in the inspection bin costs 50 points (``GOOD_CELL_IN_INSPECTION_BIN``
   in ``scoring_weights.yaml``). So a detector that flags too many cells
   costs 50 points for each good cell it rejects, and L12 uses this to
   compare detectors.
