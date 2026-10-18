====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 1,
   next week, covers L1 to L3. Working through this page is good preparation
   for it. Memorizing the answers below is not.

This quiz covers Lecture 3: why representation matters, frames, ontologies,
the two ideas from 4D/RCS, the three views of one kit with the JSON record and
the schema check, the fourth-cell example and its margin for chance, and the
observed, inferred and unknown facts of Task 1. Every question can be answered from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 14)
===================================

.. admonition:: Question 1
   :class: hint

   Which of the three readers of the world model needs typed action
   arguments: which robot, which tester, which AGV, which slot?

   A. The PDDL planner

   B. The LLM agent

   C. The executor

   D. The VLM

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The executor (from GP1 on) calls skills and ARIAC services, and each call
   names exactly which robot, tester, AGV or slot. The planner needs typed
   objects and true or false facts; the agent reads text and answers in a
   form a JSON schema can check.


.. admonition:: Question 2
   :class: hint

   In Minsky's 1974 memo, what are a frame's named slots called?

   A. Fillers

   B. Terminals

   C. Predicates

   D. Instances

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Minsky calls them terminals. A **filler** (**A**) is what a slot holds:
   a value, or a link to another frame.


.. admonition:: Question 3
   :class: hint

   A ``NiMHCell`` frame is created for a new cell before it reaches a tester.
   What is in its ``nominal_voltage`` slot?

   A. Nothing, until the tester readings are averaged

   B. 3.6 V, the default of the general ``Cell`` frame

   C. 1.2 V, the default ``NiMHCell`` gives the slot

   D. The voltage the break beam measured

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ``NiMHCell`` takes every slot of ``Cell`` and fills ``nominal_voltage``
   with its own default, 1.2 V. **A** describes ``measured_voltage``, which is
   filled only after the tester readings are averaged. **D** is wrong: a
   break beam reports only whether its beam is broken.


.. admonition:: Question 4
   :class: hint

   Where are the tolerances (plus or minus 0.2 V per cell, 0.15 V per kit)
   stored in the lecture's frames?

   A. In every cell frame, as its own slot

   B. Once for the class, not per cell

   C. In the kit frame's status slot

   D. Nowhere: they are read from the tester

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   They are the same for every cell of a type, so they are stored once for
   the class. Copying them into every cell frame would give many places for
   one fact to drift apart.


.. admonition:: Question 5
   :class: hint

   Using the lecture's relations, which statement does the ontology reject?

   A. atStation(agv3, recycling)

   B. partOf(c4, kit2)

   C. inSlot(voltage_tester_2, agv1, s1)

   D. testedBy(c4, voltage_tester_2)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   inSlot takes a Cell, an AGV and a slot. A tester is not a cell, so the
   statement makes no sense, and software that knows the ontology can reject
   it. The other three use each relation with the classes it accepts.


.. admonition:: Question 6
   :class: hint

   By Idea 1 from 4D/RCS, which layer's world model holds the tray slot
   frames from TF2?

   A. Deliberative

   B. Executive

   C. Reactive

   D. All three, at the same detail

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Each layer keeps only the detail it decides with. The reactive layer
   holds joint positions, gripper width and tray slot frames. The
   deliberative layer holds orders, kits, which cells are good and AGV
   stations, with no poses. **D** is what Idea 1 argues against.


.. admonition:: Question 7
   :class: hint

   A place skill loses its grasp on a cell. By Idea 2, which part decides
   first what to do about it?

   A. The LLM agent, which makes a new plan

   B. The behavior tree, which reads the skill's failure reason and retries
      the skill or tries another branch

   C. The PDDL planner

   D. ARIAC, which puts the cell back

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Errors are handled as low as possible, and status moves up. The skill
   sees the lost grasp, stops and returns a failure reason; it never retries
   the task itself. The behavior tree is the next layer up, so it decides
   first: it retries the skill or tries another branch. Only when the tree
   cannot finish the kit does the planner or agent make a new plan.


.. admonition:: Question 8
   :class: hint

   For the five-slot record, the schema check prints
   ``slots.4.slot: maximum 4``. Which item does ``slots.4`` name?

   A. The fourth item

   B. The fifth item, because the path counts items from 0

   C. Every item with a slot number of 4

   D. The slot rule's maximum

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The path counts list items from 0, so ``slots.4`` is the fifth item, the
   one added. Its ``slot`` number is 5, above the maximum of 4.


.. admonition:: Question 9
   :class: hint

   The three cells total 10.87 V, so the window allows a fourth cell from
   3.38 V to 3.68 V. Why does the answer start at 3.40 V?

   A. Rounding

   B. A single Li-Ion cell may only be 3.4 V to 3.8 V, so 3.38 V is not
      allowed for one cell

   C. The tester cannot read below 3.40 V

   D. The kit tolerance is plus or minus 0.2 V

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The fourth cell must satisfy two ranges: the one from the kit window
   (14.25 − 10.87 = 3.38 V to 14.55 − 10.87 = 3.68 V) and the single-cell
   range (3.4 V to 3.8 V). Both hold from 3.40 V to 3.68 V.


.. admonition:: Question 10
   :class: hint

   Why does GP3 pick the four cells in a separate step instead of in the
   PDDL planner?

   A. PDDL handles numbers poorly, and choosing cells depends on voltages

   B. PDDL cannot describe AGVs

   C. The planner runs only after the kit is shipped

   D. ARIAC chooses the cells

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The planner reads true or false facts. Which cells fit together depends on
   their measured voltages, which are numbers, so a separate step picks the
   cells and gives the planner only facts (L6).


.. admonition:: Question 11
   :class: hint

   In ARIAC 2025 Task 1, where does a cell's inspection result (passed or
   not, and its defects) come from?

   A. ARIAC publishes it on a ``CellDefect.msg`` topic

   B. Your team decides it from lidar (GP2) and submits it as an
      ``InspectionReport.msg``

   C. The voltage tester reports it

   D. The inspection door measures it

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ARIAC never sends your team an inspection result. Your team decides it
   from lidar and submits it with ``SubmitInspectionReport.srv``; the report
   holds ``passed`` and a list of ``CellDefect`` entries. ``CellDefect.msg``
   is only the format of one defect, which is why **A** is wrong.


.. admonition:: Question 12
   :class: hint

   The PDDL view lists ``(in-slot c1 agv1 s1)``, ``(in-slot c2 agv1 s2)``,
   ``(in-slot c3 agv1 s3)`` and ``(slot-empty agv1 s4)``, among others. What
   does the planner take ``(in-slot c2 agv1 s4)`` to be?

   A. True, because c2 is on the tray

   B. False, because a fact that is not listed is false

   C. Unknown, until the planner asks ARIAC

   D. An error, because s4 is empty

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A PDDL state is a list of facts, and a fact that is not listed is false.
   ``(in-slot c2 agv1 s4)`` is not in the list, so the planner treats it as
   false. c2 is in slot s2, not s4.


.. admonition:: Question 13
   :class: hint

   ``kit_record.json`` shows slot 3's voltage as ``3.7``, while the kit was
   written with 3.70 V. Why?

   A. The tester rounded the reading

   B. JSON writes a number without its trailing zero

   C. The schema changed the value

   D. The cell was measured again

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   3.70 and 3.7 are the same number, and JSON writes it as 3.7. The record
   still passes the schema, which checks only that the voltage is a number.


.. admonition:: Question 14
   :class: hint

   Each tester reading has noise with a standard deviation of 0.05 V, and
   your team averages five readings per cell. About how far does chance move
   the measured total of a full kit of four cells?

   A. 0.010 V

   B. 0.0224 V

   C. 0.045 V

   D. 0.20 V

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. One average wanders by about 0.05 / √5 = 0.0224 V (**B** is one
      cell, not the kit).
   2. A sum of four averages wanders by √4 × 0.0224 = 0.045 V.

   So the 3.75 V cell's 0.07 V overshoot is about 1.6 times what chance
   moves a full kit (0.07 / 0.0447 = 1.57). A true 14.55 V kit would read
   that high about 6 times in 100, so a failed kit is likely, not certain.

----


True or False (Questions 15 to 22)
==================================

.. admonition:: Question 15
   :class: hint

   The course requires your team to write its world model in OWL, following
   IEEE 1872-2015.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The course requires neither. IEEE 1872-2015 (with its core ontology,
   CORA) and OWL show that standards bodies define such ontologies. IEEE made
   1872-2015 inactive (reserved) on 2026-03-26 and is drafting a revision,
   P1872.


.. admonition:: Question 16
   :class: hint

   If your system loses track of a cell, it can ask ARIAC for the cell's
   pose.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ARIAC publishes no frames or pose topics for individual cells or shells.
   Your system must track each cell itself, from events: the beam time, the
   tester reading, the skill result.


.. admonition:: Question 17
   :class: hint

   The record that names AGV 5 breaks two schema rules.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   It breaks one: ``agv: maximum 3``, because ARIAC 2025 has three AGVs. The
   five-slot record is the one that breaks two (``maxItems`` and the fifth
   item's slot number).


.. admonition:: Question 18
   :class: hint

   The deliberative layer's world model holds the joint positions of the
   robots.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Joint positions belong to the reactive layer. The deliberative layer
   holds orders, kits, which cells are good and AGV stations, with no poses.
   The design rule: put each fact in the lowest layer that needs it, and pass
   up only what the layer above decides with.


.. admonition:: Question 19
   :class: hint

   A Li-Ion cell at 3.75 V can be the fourth cell of the lecture's kit,
   because it passes the single-cell check.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   It passes on its own (3.4 V to 3.8 V), but 10.87 + 3.75 = 14.62 V, which
   is above 14.55 V, the top of the window.


.. admonition:: Question 20
   :class: hint

   The course uses the eight levels of 4D/RCS, from servo to battalion, for
   the ARIAC stack.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The eight levels are sized for a military vehicle hierarchy, with plans
   from 50 ms at the servo level to 24 h at the battalion level. ARIAC's stack
   is shallow, so the three layers are enough. The course takes only two
   ideas from 4D/RCS.


.. admonition:: Question 21
   :class: hint

   In L3, the "executor" that reads the world model is a ROS 2 executor,
   the object that runs a node's callbacks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   In L3, the executor is the part that runs actions: from GP1 on, your
   behavior tree and the skills it calls. A ROS 2 executor (L1) runs a
   node's callbacks; it is a different thing with the same name.


.. admonition:: Question 22
   :class: hint

   In the lecture's kit frame, the ``window`` slot is measured for each kit
   and stored with it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``window`` is computed from the class: 4 × 3.6 = 14.40 V, plus or minus
   0.15 V, gives 14.25 V to 14.55 V. Only the cells' measured voltages are
   stored; the total and the window are computed, so they cannot drift from
   the cells.

----


Short Answer (Questions 23 to 26)
=================================

.. admonition:: Question 23
   :class: hint

   Why must the world model keep each cell's measured voltage, and not only
   whether the cell passed?

.. dropdown:: Answer
   :class-container: sd-border-success

   Choosing the fourth cell needs the sum of the other three: 10.87 V in the
   lecture's example, which leaves a range of 3.40 V to 3.68 V. A record that
   says only "passed" cannot give that sum, so the system could place a cell
   such as 3.75 V that passes on its own but breaks the kit window. Cells
   lock to the tray, so the mistake cannot be undone.


.. admonition:: Question 24
   :class: hint

   Give one observed, one inferred and one unknown fact in Task 1, and say
   where each comes from.

.. dropdown:: Answer
   :class-container: sd-border-success

   Observed: a tester's voltage, read from its topic (also the competition
   state, AGV station, slot occupancy, high-priority order IDs). Inferred: this
   cell is the one the break beam saw at that time, from your team's own
   reasoning (also "its averaged voltage is in range", "the kit total is in
   the window"). Unknown: where each cell is, because ARIAC publishes no frames
   or pose topics for individual cells.


.. admonition:: Question 25
   :class: hint

   An LLM agent answers with a kit record that names AGV 5. What stops a
   robot from acting on it, and where in the course does that idea come back?

.. dropdown:: Answer
   :class-container: sd-border-success

   The JSON schema. Your code checks the agent's record against it, and the
   check rejects it (``agv: maximum 3``) before any robot moves. L8 uses this
   for structured output from an LLM agent.


.. admonition:: Question 26
   :class: hint

   With margins, the lecture's fourth-cell range shrinks from 3.40 V to
   3.68 V to 3.47 V to 3.59 V. Why, and what must the world model store to
   compute it?

.. dropdown:: Answer
   :class-container: sd-border-success

   ARIAC checks the true voltages, but your team knows only averages of
   noisy readings. With five readings per cell, a full kit's measured total
   wanders by about 0.045 V, so the lecture keeps a margin of
   2 × 0.045 = 0.09 V inside the kit window and 2 × 0.0224 = 0.04 V inside
   the cell range. That gives 14.25 + 0.09 − 10.87 = 3.47 V to
   14.55 − 0.09 − 10.87 = 3.59 V. To compute the margin, the world model must
   store how many readings are behind each average, as well as the average.
   The price: ``c4``, which averages 3.599 V, no longer fits, and GP1's safe
   call is to recycle it.

