====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed notes, given at the
   start of class, and they **use different questions from these**. Quiz 5
   covers L9 and L10. Working through this page is good preparation for it.
   Memorizing the answers below is not.

This quiz covers Lecture 9: what a VLM is, scene description prompts and
schemas, checking a VLM's record against a second source, the agentic closed
loop, retry, wait or replan, the two demonstrations, when PDDL is the better
tool, and GP4. Every question can be answered from the slides shown in class.

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

   Which statement about a vision-language model (VLM) matches the lecture?

   A. It takes an image and returns pixel coordinates of every object.

   B. It takes images and text in the same prompt and returns text; it gives
      positions only if you ask for coordinates in the text.

   C. It returns a confidence that tells you whether its answer is right.

   D. It needs a different validation process from a text-only LLM call.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A VLM's output is text. Compared with the L8 text call, only the input is
   new (the image); the prompt and the checked, structured output work the
   same way, so **D** is wrong. **C** is wrong because a VLM can be wrong
   with full confidence.


.. admonition:: Question 2
   :class: hint

   The tray schema in ``vlm_check.py`` allows ``UNKNOWN`` for the cell type
   and the damage. Why?

   A. ``CellTypes.msg`` defines ``UNKNOWN`` as a cell type.

   B. A model that must pick a label will guess; ``UNKNOWN`` lets it say it
      cannot see the value.

   C. JSON Schema requires every enum to have a default value.

   D. The voltage testers report ``UNKNOWN`` when they are malfunctioning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The prompt tells the model to use ``UNKNOWN`` when it cannot see a value.
   ``UNKNOWN`` (and ``NONE`` for damage) are added for this schema; the
   factory's own names are ``LI_ION`` and ``NIMH`` (``CellTypes.msg``) and
   ``DENT``, ``BULGE`` and ``SCRATCH`` (``CellDefect.msg``). A malfunctioning
   tester reports voltage -1, not ``UNKNOWN``.


.. admonition:: Question 3
   :class: hint

   Which second source checks the VLM's "occupied" field for a tray slot?

   A. The voltage your team recorded for the cell on a tester

   B. GP2's lidar point cloud

   C. ``/agvN/tray_status``

   D. A second call to the same VLM with the same image

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ``/agvN/tray_status`` is ARIAC's own signal: four booleans, one per slot,
   with no cell type (``AgvTrayStatus.msg``). The recorded voltage (**A**)
   checks the cell type. For damage there is no second source in ARIAC.


.. admonition:: Question 4
   :class: hint

   Why is the recorded tester voltage a strong check on the VLM's cell type?

   A. The nominal voltages are 3.6 V and 1.2 V, 2.4 V apart, which is 24
      times the 0.1 V spread of cell voltages.

   B. The tester and the VLM use the same camera image.

   C. The tester reads the cell type from a label on the cell.

   D. The two types differ by 0.15 V, the kit tolerance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   :math:`3.6 - 1.2 = 2.4` V, and :math:`2.4 / 0.1 = 24`. The 0.1 V spread
   comes from ``cell_feed_plugin.hpp``. With the types that far apart, one
   reading settles the type. 0.15 V (**D**) is the kit tolerance, not a
   difference between types.


.. admonition:: Question 5
   :class: hint

   In the VLM demonstration, the VLM says slot 3 holds ``LI_ION`` with
   confidence 0.6. The tray status says occupied, and the cell read 1.24 V on
   a tester. What happens?

   A. The VLM wins, because it looked at the tray most recently.

   B. The tester wins, so the agent records NiMH and submits.

   C. The verdict is ``DISAGREE: type``. The agent does not act on the field
      until a third observation settles it, and it does not submit.

   D. The confidence 0.6 is below 0.7, so the field is thrown away and the
      slot counts as agreeing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1.24 V is inside the NiMH range of :math:`1.2 \pm 0.2` V, so the record
   says NiMH and the VLM says Li-Ion. A disagreement is a flag, not a verdict:
   at least one source is wrong. The decision line in the output is "do not
   submit; slots 3 and 4 disagree". The code has no confidence threshold
   (**D**); a confidence is the model's own number, not a check.


.. admonition:: Question 6
   :class: hint

   How does an ARIAC 2025 voltage tester report a malfunction, according to
   the 2025 source (``voltage_tester_plugin.cpp``)?

   A. Its topic stops publishing.

   B. Its topic keeps publishing every 0.1 s, with voltage -1 and
      ``operation_status`` 2 (``MALFUNCTIONING``).

   C. It publishes 0 V plus noise.

   D. It publishes the last good reading again.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The challenges page says the tester stops publishing (**A**), but the
   source keeps the topic going. A check that waits for silence never fires.
   0 V plus noise (**C**) is what a working tester reads with no cell on it.


.. admonition:: Question 7
   :class: hint

   The inspection conveyor reports ``MALFUNCTIONING`` before the next
   ``load_tester``. Which exit of the decision chart does the agent take?

   A. Replan (tag 1), because the goal changed

   B. Replan (tag 2), because another conveyor is free

   C. Wait (tag 3): keep the plan and watch the status topic, because ARIAC
      has only one inspection conveyor

   D. Retry (tag 4): run ``load_tester`` again at once

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Device down? yes. Another free? no: ARIAC has one inspection conveyor. So
   the plan stays, and the agent waits. In the demonstration it waited from
   90 s to 120 s, the 30 s of the malfunction, with no model call.


.. admonition:: Question 8
   :class: hint

   At t = 190 s in the closed-loop demonstration, ``unload_to_tray(2, 3)``
   reports "grasp lost". Slot 3 is empty, and tester 2 still reads 3.63 V.
   No retry has been used yet. What does ``decide()`` return, and why?

   A. ``REPLAN``, because a skill failed

   B. ``WAIT``, because tester 2 is down

   C. ``RETRY``, because the cell is still on the tester, so the plan still
      holds, and retries are left

   D. ``RETRY``, because every failure gets two retries before anything else
      is checked

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The 3.63 V reading says the cell never left tester 2. Goal changed? no.
   Device down? no. Plan holds? yes. Retries left? yes (``RETRY_CAP`` is 2).
   The retry at 190 s succeeded at 210 s. **D** is wrong: the chart checks
   the goal and the devices before it looks at retries.


.. admonition:: Question 9
   :class: hint

   In the closed loop, which decision calls a model?

   A. Every decision, because the LLM grades each step

   B. Only replan

   C. Retry and replan

   D. Wait, because the model watches the status topic

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Exit 2 of the loop, replan, is the only exit that calls a model. Retry,
   wait and "the world matches" all go back to Act without one. The model
   never grades its own plan: the orchestrator compares each expected effect
   with fresh observations.


.. admonition:: Question 10
   :class: hint

   What is the voltage window for a kit of four Li-Ion cells?

   A. 14.20 V to 14.60 V

   B. 14.25 V to 14.55 V

   C. 13.60 V to 15.20 V

   D. 4.65 V to 4.95 V

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. Four cells: :math:`4 \times 3.6 = 14.4` V.
   2. Kit tolerance 0.15 V: :math:`14.4 - 0.15 = 14.25` V to
      :math:`14.4 + 0.15 = 14.55` V.

   **D** is the NiMH window (:math:`4 \times 1.2 = 4.8` V, plus or minus
   0.15 V). **C** uses the 0.2 V cell tolerance on each of the four cells.


.. admonition:: Question 11
   :class: hint

   In the demonstration, replanning finished at 245 s and waiting at 285 s.
   The replan made two model calls, which took 0 s in the stand-in. If each
   real call takes :math:`L` seconds, for which :math:`L` does replanning
   still finish first?

   A. :math:`L < 40` s

   B. :math:`L < 20` s

   C. :math:`L < 10` s

   D. Any :math:`L`, because replanning used the other tester

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. Replanning saved :math:`285 - 245 = 40` s.
   2. It made two calls, which add :math:`2L`.
   3. It still wins while :math:`2L < 40` s, so while :math:`L < 20` s.

   **A** forgets that there were two calls.


True or False (Questions 12 to 15)
==================================

.. admonition:: Question 12
   :class: hint

   True or false: if the VLM reports a field with confidence 0.9, the
   orchestrator can treat that field as checked.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   A confidence is the model's own number, not a check. In the demonstration
   the two wrong slots had confidences of 0.6 and 0.7, and a VLM can be wrong
   with full confidence. A field is checked when a second source agrees.


.. admonition:: Question 13
   :class: hint

   True or false: the ARIAC challenges page and the ARIAC 2025 source agree
   that the cell feed pauses during a conveyor malfunction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The challenges page says the feed pauses. In the 2025 source,
   ``linear_conveyor_plugin.cpp`` stops only the belt, and
   ``cell_feed_plugin.cpp`` has no malfunction check. The lecture's advice:
   watch the feed in simulation before you rely on either.


.. admonition:: Question 14
   :class: hint

   True or false: GP4 tests the agent on the vacuum tool malfunction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   GP4 tests a conveyor malfunction, a voltage tester malfunction and
   high-priority orders. The vacuum tool malfunction affects only Task 2, so
   the final demo tests it.


.. admonition:: Question 15
   :class: hint

   True or false: in the closed-loop demonstration, model call 2 sent a cell
   to the broken tester 1, and the orchestrator rejected that plan before any
   robot moved.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   The output shows "model call 2 rejected: step 1 uses tester 1,
   MALFUNCTIONING". Every plan goes through the schema and a check against
   the observed state before it runs. The re-prompt, model call 3, gave a
   valid 4-step plan.


Short Answer (Questions 16 to 19)
=================================

.. admonition:: Question 16
   :class: hint

   Why does the orchestrator keep the expected state outside the LLM, and how
   does it use it after each action?

.. dropdown:: Answer
   :class-container: sd-border-success

   The orchestrator keeps the world-state record (cells, testers, tray slots,
   AGV stations, orders), and each action has an expected effect, like a PDDL
   effect: after ``load_tester``, the tester reads 3.4 V to 3.8 V. After the
   action it checks that effect against fresh observations. Keeping this
   outside the LLM means the model never grades its own plan.


.. admonition:: Question 17
   :class: hint

   The agent switched the cell feed to NiMH for a high-priority order. Why
   does it still ask the VLM whether all four cells on the tray are NiMH
   before it submits?

.. dropdown:: Answer
   :class-container: sd-border-success

   Li-Ion cells already on the conveyor when the feed switched can still
   arrive, so a Li-Ion cell can end up in the NiMH kit. The VLM shows the tray
   as it looks now. Its answer is then cross-checked against the tray status
   and the recorded voltages before the agent submits with
   ``/submit_high_priority_order``.


.. admonition:: Question 18
   :class: hint

   The lecture names three kinds of situation where an LLM agent earns its
   place over the PDDL planner. Name them, with an example of each.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. **Ambiguity:** the VLM says a cell "may be dented".
   2. **Novelty:** a case the domain has no action for.
   3. **Recovery the domain did not plan for:** the ARIAC challenges, which
      GP3's domain does not model.

   For a fully specified task, such as the normal Task 1 flow, PDDL is the
   better tool: no fee per call, the same plan for the same problem, and a
   domain file anyone can read.


.. admonition:: Question 19
   :class: hint

   GP4 compares the agent with GP3 "on identical trials". What has to be the
   same, and why is one run per system not enough?

.. dropdown:: Answer
   :class-container: sd-border-success

   The same trial file (``SEED``, ``DEFECT_RATE``, ``CHALLENGES``) and the
   same team file (``SENSORS``, ``CONVEYOR_SPEED``, ``CELL_FEED_RATE``); only
   the planner changes. One run is not enough because the same prompt can
   give different plans on different runs, so one run per system is not a
   comparison. L12 shows how many runs a claim needs.
