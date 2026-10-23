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

   A. A plan failure; the schema check catches it.

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
   the place while it is still running, which cancels its action goal. The
   cancel parks robot 1 before ``CANCELED`` comes back, so the place on
   tester 2 waits one tick and starts on tick 3. Retry never sees a failure
   (**A**), and a skill never decides recovery itself (**C**): the tree sends
   the cancel, not the skill.


.. admonition:: Question 5
   :class: hint

   Run D repeats Run B with selector memory off. What goes wrong on ticks 4
   and 5?

   A. The selector skips tester 2 and goes straight to ``hold_cell``.

   B. The selector goes back to tester 1, Retry's count starts again at 1,
      and the place on tester 2 is stopped halfway.

   C. Retry raises an exception because its count passed 3.

   D. Nothing: memory makes no difference in this tree.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   With memory off, the selector starts again from its first child on every
   tick. On tick 4 tester 1's fourth attempt waits for robot 1, and the
   selector stops the place on tester 2, which cancels it. On tick 5 the
   cancel is done, the fourth attempt fails, and Retry counts it as failure 1
   of 3. With memory on, the selector goes on from its running child and
   stays with tester 2.


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

   An LLM agent with L8's tools calls ``robot1_place_on_tester`` with the
   arguments ``{"tester": 2, "cell": "c9"}``. Which check of
   ``check_call()`` refuses it?

   A. Check 1, tool

   B. Check 2, schema

   C. Check 3, guard

   D. None: the call is accepted, and the skill ignores the extra argument.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The tool exists, so check 1 passes (**A**). Each L8 schema allows no
   other arguments, so ``cell`` breaks it: ``Additional properties are not
   allowed ('cell' was unexpected)``. This is reply D in the demonstration.
   No L8 tool takes a cell ID, so an invented cell never reaches a robot, and
   the guard is never reached (**C**).


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

   A refused call goes back to the model as that call's result, with the
   exact error (L8's ``run()``). Two refused calls in a row end the run
   (``MAX_INVALID = 2``, chosen in L8); then take a safe action: hold the
   cell, pause the feed, or hand the step to the GP3 PDDL plan. Policy run 2
   shows the fall back.


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
   conveyor malfunction is local too: keep the plan and wait. The voltage tester malfunction is
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
   result, and the behavior tree decides first (retry, wait, timeout,
   another branch). Only then does the failure move up to the planner or agent.


.. admonition:: Question 13
   :class: hint

   True or false: GP4 tests the vacuum tool malfunction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The vacuum tool malfunction happens only in Task 2. GP4 tests the
   conveyor malfunction, the voltage tester malfunction and high-priority
   orders, and not the vacuum tool malfunction.


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

   True or false: a strict enough JSON schema would have refused replies E
   (a full slot) and F (a broken tester) in the demonstration.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   Both calls name a tool that exists, with arguments that fit its schema. Slot 1
   already holds a cell, and tester 1 is ``MALFUNCTIONING``: facts about the
   factory now, which change during a run. No schema can know them. Only the
   guard, which reads the observation and the record, refuses E and F.


.. admonition:: Question 16
   :class: hint

   True or false: while your team develops GP4 and the final demo, its model
   calls run on the course key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The course key runs the graded runs only (GP4 and the final demo). While
   you develop, your team uses its own free-tier Gemini key. The rest is set
   too: the grading rubric (75 points for the run, 25 for the class session),
   the code freeze (Friday, April 30, 2027, at 11:59 pm), and the model
   (Gemini Robotics ER as the course example; another VLM is allowed if it is
   a Google model on the course key or a model that runs locally).


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

   In L9's trial, tester 1 goes down for 70 s during a kit. Which response
   does the rule give, and what did L9's two recordings show?

.. dropdown:: Answer
   :class-container: sd-border-success

   The plan assumes two testers, and one is down, but tester 2 can do its
   job. So the rule says replan, which is global: use tester 2 only, and
   replan again when tester 1 returns. In the replan recording, Gemini sent
   cells 2 and 3 to tester 2, and slot 3 was filled at 108.8 s, against
   105.1 s in the scripted dry run with no malfunction. In the wait
   recording, Gemini waited 5, 10, 20 and 30 s while robot 2 held a tested
   cell that could already go to slot 1: :math:`112.6 - 38.2 = 74.4` s. Both finished
   at about 225 s, because by chance two cells in the replan run went to
   recycling (80.0 s), so one recording of each policy is too few to tell
   which is faster. Each was recorded once, on 2026-10-17, with gemini-3.5-flash-lite.


.. admonition:: Question 19
   :class: hint

   The lecture gives two designs for where the LLM fits: the L8 and L9 agent,
   and a hybrid. How do they differ, and which of the three worked examples
   calls the LLM agent?

.. dropdown:: Answer
   :class-container: sd-border-success

   The L8 and L9 agent calls the model at every step, recovery included: in
   L9's replan recording, one kit took 26 model calls and 122,861 input
   tokens. In a hybrid, which GP4 allows, rule-based handlers cover the
   common cases (the retry, wait and replan answers in the lecture's tables),
   and the LLM is called only when no handler covers the case, so the common
   cases cost no tokens. Both fit L1's definition: the agent "picks the next
   step from what it observes, not from a fixed script". Example C, a
   high-priority order with two cells on AGV 1, calls the LLM agent: the goal
   changed, and the agent chooses which AGV takes the NiMH kit, whether to
   finish the Li-Ion kit first, and when to switch the feed back. Each of its
   tool calls still passes ``check_call()`` before any robot moves.


.. admonition:: Question 20
   :class: hint

   What does a good cell in the inspection bin cost, and what does that say
   about a defect detector?

.. dropdown:: Answer
   :class-container: sd-border-success

   A cell passes the inspection door only after a passing inspection report;
   a failing report, or no report, sends it to the inspection bin. A good
   cell in the inspection bin costs 50 points (``GOOD_CELL_IN_INSPECTION_BIN``
   in ``scoring_weights.yaml``). So a detector that flags too many cells
   costs 50 points for each good cell it rejects, and L12 uses this to
   compare detectors.
