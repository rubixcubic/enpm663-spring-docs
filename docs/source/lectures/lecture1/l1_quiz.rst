====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 1,
   in Week 4, covers L1 to L3. Working through this page is good preparation
   for it. Memorizing the answers below is not.

This quiz covers Lecture 1: physical AI and agents, the ARIAC 2025 factory
and how ARIAC scores a run, the kit voltage window, the path of one cell
through the ROS 2 interfaces, and the four refresher demonstrations (QoS,
executors, actions, TF2). Every question can be answered from the slides
shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 10)
===================================

.. admonition:: Question 1
   :class: hint

   In the agent loop used in this course, what is a **tool**?

   A. The LLM the agent asks what to do

   B. A robot skill the agent calls

   C. The camera image the agent reads

   D. The behavior tree that replaces the agent

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The agent observes the state of the world, asks the model what to do,
   calls a tool, checks the result and repeats. In this course the tools are
   robot skills from the course skills package. **A** is the model the loop
   runs around, not a tool.


.. admonition:: Question 2
   :class: hint

   Why does the course give every team a skills package?

   A. ARIAC has no robots in Task 1

   B. ARIAC gives its robots low-level controls only (joint motion, and a
      gripper, vacuum tools or a weld service), with no pick or place skills

   C. The course trains a motion policy for each team

   D. ARIAC's robots can only be moved from the command line

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each robot has a joint trajectory action for motion. For grasping, the
   inspection robots and assembly robot 1 have a gripper action, assembly
   robot 2 has vacuum tool services, and the gantry welder has a weld service.
   Picking a cell and placing it needs motion planning on top of these. The
   skills package provides it as Python ROS 2 actions built on
   MoveIt 2, so your team never writes motion code. **C** is out of scope:
   the course does no policy training.


.. admonition:: Question 3
   :class: hint

   A cell reaches the inspection door, and your system never submitted an
   inspection report for it. What happens?

   A. The door opens, because no report means no defect

   B. The conveyor stops until a report arrives

   C. The door stays closed, and the cell drops into the inspection bin

   D. The cell goes to the recycling bin after the voltage test

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The door lets a cell through only if your team submitted a passing report
   for it. A failing or missing report keeps the door closed, and the cell
   drops into the inspection bin. A good cell in the inspection bin is a penalty, which is why your
   system submits a report for every cell from GP1 on.


.. admonition:: Question 4
   :class: hint

   What is the kit voltage window of a Li-Ion kit?

   A. 3.4 V to 3.8 V

   B. 14.25 V to 14.55 V

   C. 13.6 V to 15.2 V

   D. 4.65 V to 4.95 V

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Four cells at 3.6 V nominal give 4 × 3.6 = 14.4 V, and the kit tolerance
   is plus or minus 0.15 V: 14.4 − 0.15 = 14.25 V to 14.4 + 0.15 = 14.55 V.
   **A** is the range for one Li-Ion cell, and **D** is the Ni-MH kit window.


.. admonition:: Question 5
   :class: hint

   A Li-Ion cell's averaged voltage is 3.85 V. Where does inspection robot 2
   put it?

   A. On the AGV tray, because it passed lidar inspection

   B. In the inspection bin

   C. Back on the inspection conveyor

   D. In the recycling bin

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   A cell outside its nominal voltage plus or minus 0.2 V goes to the
   recycling bin. For Li-Ion that range is 3.4 V to 3.8 V, and 3.85 V is
   0.05 V above it. The inspection bin (**B**) is where a cell drops when the
   inspection door stays closed.


.. admonition:: Question 6
   :class: hint

   Where may your team place a lidar in ARIAC 2025?

   A. Anywhere in the factory, if the total sensor cost is under budget

   B. Only in three bounding boxes around the inspection conveyor

   C. Only on the robots

   D. Only above the AGV trays

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Lidar may only sit in three bounding boxes around the inspection conveyor,
   where your team uses its point clouds to find cell defects (GP2). The
   budget (**A**) limits what you buy, not where a lidar goes.


.. admonition:: Question 7
   :class: hint

   A run finishes every kit but one, very fast, with sensors well under the
   budget. What does it earn in bonuses?

   A. The speed bonus only

   B. The sensor cost bonus only

   C. Both bonuses, reduced by the missing kit

   D. No bonus at all

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   Bonuses are paid only if every desired kit and module was submitted. One
   missing kit lowers the base score and removes every bonus, so finishing
   every order comes first.


.. admonition:: Question 8
   :class: hint

   Why is moving an AGV an action rather than a service?

   A. Services cannot carry a station name

   B. It takes time and reports progress while it runs

   C. Actions are faster than services

   D. Only actions can be called from Python

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A service is one short request and one reply. An action is a long goal
   with feedback and a result, which fits a move that takes time and reports
   progress.


.. admonition:: Question 9
   :class: hint

   In the action demonstration, the client asks to cancel the second goal
   after 0.5 s. Why does the result say 0.0595 m and not 0.068 m?

   A. The server ignores the first cancel request

   B. The cancel arrives during the third step, and the server checks for a
      cancel only between steps, so the third step finishes first

   C. The gripper moves back after a cancel

   D. Feedback messages are lost after a cancel

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Steps end at 0.2 s, 0.4 s and 0.6 s, so 0.5 s falls in the third step.
   After 3 steps the gripper is at 0.085 − 3 × 0.0085 = 0.0595 m. The value
   0.068 m is the position after 2 steps.


.. admonition:: Question 10
   :class: hint

   The TF2 lookup prints z = 0.3820 m for slot 1 in ``agv1_frame``. Where does
   that number come from?

   A. 0.35 + 0.032, because the turn about z does not change the height

   B. 0.35 × 1.57

   C. 0.35 − 0.032, because the turn flips the slot downward

   D. It is measured by a sensor on the AGV

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The tray is 0.35 m above the AGV base, and the slot is 0.032 m above the
   tray. The tray's turn of −1.57 rad is about z, which moves x and y but
   leaves the height alone: 0.35 + 0.032 = 0.382 m. **D** is wrong: the
   script publishes static transforms; nothing is measured.


----


True or False (Questions 11 to 16)
==================================

.. admonition:: Question 11
   :class: hint

   ARIAC's AGV move server accepts cancel requests, so a behavior tree can
   stop an AGV halfway.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A client can ask an action server to cancel, but the server decides.
   ARIAC's AGV move server rejects cancel requests. The course skills accept
   them.


.. admonition:: Question 12
   :class: hint

   In the ARIAC 2025 code, a voltage tester that malfunctions stops
   publishing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   In the ARIAC 2025 code it keeps publishing, with a voltage of −1 and the
   status ``MALFUNCTIONING``. A system that only checks whether messages
   still arrive would miss it, and would average −1 into a cell's voltage.


.. admonition:: Question 13
   :class: hint

   A callback created without a callback group can run at the same time as
   the node's other default-group callbacks on a multi-threaded executor.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   It joins the node's default group, which is mutually exclusive, so only
   one of its callbacks runs at a time, whatever the executor.


.. admonition:: Question 14
   :class: hint

   A finished ARIAC module has six welds: four on top and two on the bottom.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The gantry welder makes four top welds, assembly robot 2 flips the
   module, and the welder makes two bottom welds.


.. admonition:: Question 15
   :class: hint

   The competition state becomes ``ORDERS_COMPLETE`` as soon as every
   announced order is done, even if a high-priority order is still to come.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The state becomes ``ORDERS_COMPLETE`` when every order is done, but not
   while a high-priority order is still to be announced.


.. admonition:: Question 16
   :class: hint

   Your team builds Task 2, module construction, in GP1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Task 2 appears only in the final demo. GP1 builds one kit (Task 1).


----


Short Answer (Questions 17 to 19)
=================================

.. admonition:: Question 17
   :class: hint

   Give the two reasons from the lecture for keeping AI at the decision
   layer rather than in motion control.

.. dropdown:: Answer
   :class-container: sd-border-success

   An agent's decisions leave a trace a person can read and grade: each tool
   call and its arguments. A learned motion policy leaves no such trace of
   tool calls, and this course grades your system on trials it has never
   seen. So the agent decides what happens next, and classical skills
   (MoveIt 2) do the motion.


.. admonition:: Question 18
   :class: hint

   Four Li-Ion cells each pass the per-cell check. Explain why the kit can
   still fail, and what that means for when your system chooses the cells.

.. dropdown:: Answer
   :class-container: sd-border-success

   Each cell may be anywhere from 3.4 V to 3.8 V, but the kit total must be
   within 14.25 V to 14.55 V. Four cells all at 3.8 V total 15.2 V, 0.8 V
   above 14.4 V. Cells lock to the tray once placed, so your system must
   choose which cells go together before it places them.


.. admonition:: Question 19
   :class: hint

   In the executor demonstration, the single-threaded run counted 11 status
   reads where 50 were expected. What does that mean for a behavior tree node
   in ARIAC, and what fixed it in the demonstration?

.. dropdown:: Answer
   :class-container: sd-border-success

   While one callback waits on a skill (here, a 1 s sleep), a single-threaded
   executor runs nothing else, so the node misses status updates. In ARIAC
   that is how a system misses the start of a conveyor or tester
   malfunction. The fix in the demonstration was a multi-threaded executor
   with the slow and fast timers in two different callback groups, which gave
   50 of 50. Your behavior tree node must not block its own callbacks.
