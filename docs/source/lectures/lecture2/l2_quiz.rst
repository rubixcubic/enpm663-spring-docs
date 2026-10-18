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

This quiz covers Lecture 2: the classical robot architectures, the
three-layer architecture and what passes between its layers, the toy factory
run, the tester malfunction traced layer by layer, Nav2 and MoveIt, where AI
plugs in, ARIAC 2025 as a three-layer system, VLA models, multi-robot
coordination and GP1. Every question can be answered from the slides shown in
class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences, or the steps of a
     computation.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 12)
===================================

.. admonition:: Question 1
   :class: hint

   In the three-layer architecture, what does the **executive** do?

   A. It plans over a long horizon: which kit to build and which cells to use

   B. It runs the plan step by step: it calls skills, watches their results,
   and retries or reports failure

   C. It sends joint commands to the robot's motors

   D. It trains the policy that maps camera images to actions

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The executive sits between the other two layers. It chooses which skill
   runs next for the current situation and reacts when a skill reports
   failure. **A** is the deliberative layer and **C** is the reactive layer.
   In this course the executive is a behavior tree (GP1).


.. admonition:: Question 2
   :class: hint

   In Brooks's subsumption architecture, how does a higher layer take over a
   lower layer's role?

   A. It shuts the lower layer down until the higher layer is done

   B. It sends the lower layer a new plan

   C. It suppresses the lower layer's inputs and inhibits its outputs, while
   the lower layer keeps running

   D. It rewrites the lower layer's world model

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The layers of behaviors run in parallel, and the lower layers keep running.
   In the four-architectures figure, each circle marked S is a point where a
   higher level replaces the signal on the line below it. **A** is wrong
   because the lower layers never stop. **B** and **D** describe things
   subsumption does not have: a plan and a central world model.


.. admonition:: Question 3
   :class: hint

   Which claim does the lecture give to Brooks's **1986** paper, rather than
   to his 1991 paper "Intelligence without representation"?

   A. A robot can work with no explicit world model

   B. Not all sensors need to feed a central representation

   C. A robot needs a deliberative layer above its behaviors

   D. Behaviors should be learned from demonstrations

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The 1986 paper says: "Not all sensors need to feed into a central
   representation" (p. 17). The stronger claim, **A**, that a robot can work
   with no explicit world model, comes later, in the 1991 paper.


.. admonition:: Question 4
   :class: hint

   In the class run of the toy factory, why did **plan only** recycle cells 3
   and 5?

   A. Both cells were outside 3.4 V to 3.8 V

   B. The kit was already full when they arrived

   C. Their picks failed, so the tester was empty

   D. They were tested at tester 1 during its malfunction, and the plan read
   the −1 V as a voltage because it never checks a tester's status

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   The trace shows ``cell 3: tester 1 reads -1.00 V -> bin`` at 36.0 s and
   the same for cell 5 at 62.0 s. Their true voltages are 3.61 V and 3.49 V,
   both in range, so **A** is wrong. **C** describes the two ``no cell``
   lines, which are different steps.


.. admonition:: Question 5
   :class: hint

   Over 1000 seeds, plan only and react only accept between 600 and 613
   kits, with or without the malfunction. What does the lecture conclude?

   A. React only is clearly better than plan only

   B. The malfunction is the main reason their kits fail

   C. Neither one chooses the cells, and the counts do not differ beyond
   chance, which moves a count from 1000 runs by about 15

   D. Both would reach 919 with more seeds

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A rate from 1000 runs wanders by about
   :math:`\sqrt{0.61 \times 0.39 / 1000} \approx 0.015`, or 15 kits in
   1000. The counts are within that, so **A** is not supported. **B** is
   wrong: with the malfunction off, they still accept 613 and 612. The
   malfunction shows instead in plan only's recycled cells: 1570 with it, 28
   without.


.. admonition:: Question 6
   :class: hint

   In the three-layer run, tester 1 starts to malfunction at 20 s. Which
   layer is **the first to see** the malfunction, and when?

   A. The deliberative layer, at 20 s

   B. The reactive layer, at 28 s

   C. The executive, at 36.0 s, when its 10 readings at tester 1 show
   ``MALFUNCTIONING``

   D. The executive, at 75.3 s

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The tester (reactive layer) reports from 20 s but decides nothing. The
   executive sees the status after averaging 10 readings at tester 1,
   36 − 20 = 16 s after the start. The gap comes from the toy, which reads a
   tester only when it uses it. 75.3 s (**D**) is the first status check after
   the tester works again.


.. admonition:: Question 7
   :class: hint

   At 41 s the executive reports to the planner. What does the report hold?

   A. The 10 readings of −1 V from tester 1

   B. Two facts: cell 3 reads 3.60 V, and tester 1 is down

   C. The two failed grasps

   D. Nothing: the executive handles everything itself

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The error is handled where it is seen, and only the status moves up. The
   −1 V readings stay in the executive (**A**): the planner never learns what
   a −1 V reading is. The grasp failures (**C**) come later, at 79.3 s and
   83.3 s, and the planner never hears of them because the third attempt
   succeeds.


.. admonition:: Question 8
   :class: hint

   Which part of Nav2 is, **in our terms**, a skill below the executive and
   not the deliberative layer?

   A. The planner server, which computes a path

   B. The BT Navigator

   C. The client application that sends a ``NavigateToPose`` goal

   D. The behavior tree XML file

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The planner server is an action server that the behavior tree calls, like
   the controller and behavior servers. Its name says "planner", but its
   role is a skill. Match layers by role, not by name. **B** is the executive
   and **C** is the deliberative layer.


.. admonition:: Question 9
   :class: hint

   According to the MoveIt documentation quoted in class, what runs the
   trajectory that ``move_group`` computes?

   A. ``move_group`` itself

   B. The behavior tree

   C. A server on the robot that serves the FollowJointTrajectoryAction
   interface, which ``move_group`` does not provide

   D. The LLM agent

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ``move_group`` "talks to the controllers on the robot using the
   FollowJointTrajectoryAction interface", and that server "is not provided by
   move_group itself." In ARIAC it is the ``follow_joint_trajectory`` action
   of each robot's joint trajectory controller. MoveIt is a motion layer: it
   does not decide what to pick next.


.. admonition:: Question 10
   :class: hint

   Compared with the course stack, what does a **two-system VLA** such as
   Helix lack?

   A. A model that reasons about the scene

   B. A fast control policy

   C. A layer between the slow model and the fast policy that checks each
   step

   D. A camera

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Helix has a slow 7B-parameter VLM at 7 to 9 Hz (**A**) and a fast
   80M-parameter policy at 200 Hz (**B**). The policy acts on the slow
   model's output directly, so nothing between them checks each step. In the
   course stack, the behavior tree is that check.


.. admonition:: Question 11
   :class: hint

   How does your team move an AGV to shipping in GP1?

   A. With the course skills package's AGV skill

   B. With ARIAC's own AGV move action, called from the behavior tree

   C. With MoveIt 2

   D. The AGV moves on its own when the tray holds four cells

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The skills cover the robot arms. Your team moves the AGVs with ARIAC's
   AGV move action (``/agvN/move``). In the course drawing, an arrow goes from
   the executive straight down to ARIAC, past the skills.


.. admonition:: Question 12
   :class: hint

   Which is a weakness of giving **each robot its own decision maker**?

   A. It is one point of failure

   B. Its plans grow with the number of robots

   C. The robots must agree, and a missed message can deadlock them

   D. It cannot see any conflict

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   One decision maker per robot scales, but the robots must negotiate for
   shared space such as the tester area. **A** and **B** are the weaknesses
   of a central decision maker.


----


True or False (Questions 13 to 17)
==================================

.. admonition:: Question 13
   :class: hint

   **True or false:** a course skill retries a failed grasp on its own before
   it reports a result.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A skill never retries a task on its own. It stops and returns a failure
   reason, and the behavior tree (the executive) decides what to do next. In
   the toy, ``pick_from_conveyor`` returns ``GRASP_FAILED`` and
   ``Executive.pick`` makes the next attempt.


.. admonition:: Question 14
   :class: hint

   **True or false:** in the ARIAC 2025 code, a malfunctioning voltage tester
   stops publishing, so a missing message is the way to detect it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The challenge page says the tester stops publishing, but the code keeps
   publishing −1 V with the status ``MALFUNCTIONING``. Check the
   ``operation_status`` field of each message, not only the voltage.


.. admonition:: Question 15
   :class: hint

   **True or false:** in the class run, the three layers took longer than
   react only (107 s against 74 s) mostly because the planner sets aside
   cells that do not fit the kit.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Cells 2 and 5 were in range but did not fit, so the planner sent them to
   AGV 2 and tested six cells, not four. One cell takes about 14 s (cell 1 is
   logged at 8.0 s and cell 2 at 22.0 s), so the two extra cells are about
   2 × 14 = 28 s of the 107 − 74 = 33 s. React only shipped the first four
   in-range cells, faster, and its kit was rejected at 14.60 V.


.. admonition:: Question 16
   :class: hint

   **True or false:** in the toy, the two grasp failures at 79.3 s and
   83.3 s reach the planner.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The executive retries and the third attempt succeeds, so nothing moves
   up. The lecture's table says it: for a grasp failure, nothing moves up
   unless all 3 attempts fail.


.. admonition:: Question 17
   :class: hint

   **True or false:** in GP1, a cell with no inspection report still reaches
   the robots, because every GP1 cell is free of defects.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Without a report, the inspection door stays closed, the cell drops into
   the inspection bin, and nothing reaches the robots. GP1 has no defect detection and runs on
   a trial with no defective cells, so your tree submits a report for every
   cell, and every report says passed.


----


Short Answer (Questions 18 to 20)
=================================

.. admonition:: Question 18
   :class: hint

   The course swaps the deliberative layer between GP3 and GP4 but keeps the
   same executive. Why?

.. dropdown:: Answer
   :class-container: sd-border-success

   **Sample answer.** The behavior tree checks each skill result and stops
   cleanly on failure, whatever planner sits above it. In GP3 it runs a PDDL
   plan and in GP4 the agent's decisions. Because the executive is the same,
   GP4 can compare the agent with the planner on identical trials (validity,
   plan length, cost and latency), which measures what the LLM adds.


.. admonition:: Question 19
   :class: hint

   The toy's planner has one cell on AGV 1, read at 3.55 V. The next cell
   reads 3.78 V (readings chosen for this question). The room for slot
   :math:`k` is :math:`0.15 - 0.05 + 0.05 \times (4 - k)` V. Where does the
   cell go? Show the steps. Where would it go if it read 3.38 V instead?

.. dropdown:: Answer
   :class-container: sd-border-success

   **3.78 V.**

   1. 3.78 V is inside 3.4 V to 3.8 V, so the planner checks the kit.
   2. The cell would fill slot 2: 3.55 + 3.78 = 7.33 V.
   3. Target for two cells: 2 × 3.6 = 7.20 V, so ``off`` is 0.13 V above.
   4. Room for slot 2: 0.10 + 0.05 × 2 = 0.20 V.
   5. 0.13 V is within 0.20 V, so the cell goes to **AGV 1**.

   **3.38 V.** It is outside 3.4 V to 3.8 V, so it goes to the **bin**. The
   planner does not check the kit for an out-of-range cell.


.. admonition:: Question 20
   :class: hint

   A factory asks why your team built a modular stack instead of training an
   end-to-end VLA. Give two tradeoffs from the lecture, and the one point on
   which the VLA is better.

.. dropdown:: Answer
   :class-container: sd-border-success

   **Sample answer.** Any two of these: a VLA needs robot demonstration data
   and GPUs to train or fine-tune, while the modular stack runs without
   training; a failure inside a learned policy is hard to trace, while a plan
   or an agent's tool calls can be read line by line; a VLA decision is hard
   to check against a rule, while the stack's decisions can be checked
   against one, such as the kit voltage window. The VLA is better on new
   tasks: it can handle tasks no one wrote skills for, and the stack is
   limited to the skills it has.
