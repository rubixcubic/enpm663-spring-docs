====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the in-class quizzes listed in the
   :doc:`syllabus </syllabus/index>`. **Quiz 5**, at the start of the next
   class, covers L9 and L10. It is closed-notes and **uses different
   questions from these**. Working through this page is good preparation for
   it. Memorizing the answers below is not.

This quiz covers Lecture 10: static and moving transforms, the frames ARIAC
publishes and the three lookup failures, the pinhole camera model and the
pixel-to-table steps, the MoveIt 2 parts, the planners and how to choose one,
parameterized grasps and the moving conveyor, and the course skills package's
failure results. Every question can be answered from the slides shown in
class.

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

   Which of these transforms does ARIAC send again at every simulation step?

   A. ``world`` to ``agv1_frame``

   B. ``agv1_frame`` to ``agv1_tray_frame``

   C. ``agv1_tray_frame`` to ``agv1_slot1_frame``

   D. ``agv1_tray_frame`` to ``agv1_slot2_frame``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The AGV drives between stations, so the transform from ``world`` to
   ``agv1_frame`` changes; ARIAC sends it on the moving broadcaster. The tray
   is bolted to the AGV and the slots are fixed in the tray, so **B**, **C**
   and **D** are static: ARIAC sends them once.


.. admonition:: Question 2
   :class: hint

   In ``tf_failures.py``, a camera frame is published under ``wrld`` instead
   of ``world``. A lookup from ``world`` to that camera frame raises which
   exception?

   A. ``LookupException``

   B. ``ExtrapolationException``

   C. ``ConnectivityException``

   D. None: TF2 corrects the name

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ``world`` and ``wrld`` are different frames, so the camera sits in a second
   tree that never connects to ``world``. The fix is the name; drawing the
   tree with ``view_frames`` shows the two trees. **A** is for a frame that
   does not exist at all, and **B** for a time newer than the newest
   transform.


.. admonition:: Question 3
   :class: hint

   An ARIAC camera is 720p (1280 × 720 pixels) with FOV = 1.57 rad, and its
   SDF gives no lens values. What :math:`f_x` does Gazebo compute?

   A. 1280 pixels

   B. 640.5 pixels

   C. 360 pixels

   D. 1.57 pixels

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`f_x` = (width / 2) / tan(FOV / 2) = 640 / tan(0.785) =
   640 / 0.9992 = 640.5 pixels. The principal point is the image center,
   :math:`c_x` = 640 and :math:`c_y` = 360.


.. admonition:: Question 4
   :class: hint

   The camera of Question 3 is 1.0 m above the assembly table, looking
   straight down. A pixel is 128 pixels right of the image center. How far
   from the point under the camera does it land on the table?

   A. 0.128 m

   B. 0.064 m

   C. 0.20 m

   D. 1.28 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. The ray's slope is 128 / 640.5 = 0.1998.
   2. On a table 1.0 m below: 1.0 × 0.1998 = 0.20 m.

   This is twice the class's 64-pixel example (0.10 m), because the slope
   doubles. **A** treats one pixel as 1 mm; at this height one pixel covers
   about 1.6 mm.


.. admonition:: Question 5
   :class: hint

   A point is at (1, 2, 3) in a camera's optical frame. Where is it in the
   camera's frame as ARIAC publishes it (``{camera_name}_frame``)?

   A. (1, 2, 3)

   B. (3, -1, -2)

   C. (-2, 3, 1)

   D. (3, 1, 2)

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The rule is :math:`(x, y, z)` to :math:`(z, -x, -y)`. A Gazebo camera looks
   along its frame's +x, while the optical frame looks along +z with x right
   and y down. ``pixel_to_table.py`` printed this same check:
   ``optical (1, 2, 3) is link (3, -1, -2)``.


.. admonition:: Question 6
   :class: hint

   Which MoveIt 2 part holds the robot's current joint state and the
   collision objects around it?

   A. The planning scene

   B. The request adapters

   C. Trajectory execution

   D. MoveItPy

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The planning scene is what the planner checks paths against, so a planner
   can only avoid what is in the scene. The request adapters check or fix the
   start state, and trajectory execution sends the timed path to the ARIAC
   joint trajectory action.


.. admonition:: Question 7
   :class: hint

   Which planner fits lowering a held cell into a voltage tester?

   A. OMPL RRT-Connect

   B. OMPL PRM

   C. Pilz LIN

   D. Pilz CIRC

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   LIN moves the gripper in a straight line, and Pilz uses no random sampling,
   so the descent is the same every time. **A** and **B** are random: the same
   goal can give a different path on each run. **D** plans an arc.


.. admonition:: Question 8
   :class: hint

   In the RRT-Connect toy, the shortest route around the walls is 17.87 m,
   but the five seeds give paths from 22.51 m to 32.18 m. Why is every path
   longer?

   A. The walls are drawn too thick

   B. The trees stop at the first path they find

   C. The step of 0.5 m is longer than the walls are wide

   D. The goal tree grows backward

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   RRT-Connect stops when its two trees meet, and the path follows the random
   branches that met. Nothing in the toy shortens it afterward. RRTstar, the
   example team's OMPL setting, keeps shortening its path while time remains.


.. admonition:: Question 9
   :class: hint

   The beam is at x = 0.60 m and the catch point at x = 1.40 m, as in class,
   but the belt runs at 0.05 m/s. The cell crosses the beam at t = 0 s. When
   does ``pick_from_conveyor`` close the fingers? (``close_delay`` is
   -0.15 s.)

   A. At 7.85 s

   B. At 8.0 s

   C. At 15.85 s

   D. At 16.0 s

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. From the beam to the catch point: 1.40 - 0.60 = 0.80 m.
   2. At 0.05 m/s: 0.80 / 0.05 = 16.0 s. The cell arrives at 16.0 s.
   3. The fingers close 0.15 s earlier: 16.0 - 0.15 = 15.85 s.

   **A** is the class answer at 0.1 m/s. At the slower belt, a goal sent more
   than 8.0 s after the beam is still refused by ``max_trigger_age``; the
   comment on that limit in ``skills.yaml`` says to raise it for a slower
   belt.


.. admonition:: Question 10
   :class: hint

   ``place_in_slot`` looks up ``agv1_slot2_frame`` with TF2, and the lookup
   fails. Which code does the skill return?

   A. ``PRECONDITION_FAILED``

   B. ``PLACE_NOT_FOUND``

   C. ``PLANNING_FAILED``

   D. ``EXECUTION_FAILED``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A failed TF2 lookup becomes ``PLACE_NOT_FOUND``, not a crash. Under the L9
   rule, it means the world is not what the plan assumed, so the caller
   replans.


----


True or False (Questions 11 to 16)
==================================

.. admonition:: Question 11
   :class: hint

   A MoveItPy program needs a running ``move_group`` node.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   MoveItPy calls MoveItCpp inside the same process, with no ROS actions or
   services between them. ``move_group`` is a separate node that offers the
   same parts through ROS actions and services, and the example team runs
   none.


.. admonition:: Question 12
   :class: hint

   ARIAC publishes a TF2 frame for each cell on the inspection conveyor.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ARIAC publishes no frame and no pose topic for a cell or a shell. A cell's
   position comes from your sensors, such as a break beam on the conveyor; the
   top shell's pose comes from your camera.


.. admonition:: Question 13
   :class: hint

   The Pilz industrial motion planner gives the same motion for the same
   request.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Pilz uses no random sampling. That is one reason it fits a factory cell: a
   straight-line descent into a tester or a tray slot is predictable and
   repeatable.


.. admonition:: Question 14
   :class: hint

   When a grasp fails, a skill re-picks once by itself before it reports the
   failure.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A skill never re-picks or re-places by itself. After a failure, if the arm
   moved, it lifts straight up; if it held the tester area, it then parks and
   releases the lock. It reports what it holds. Its only retries are the
   planner fallback and the re-execution after a controller timeout, which
   ``attempts`` counts; neither repeats a grasp. Retry and replan decisions
   belong to your tree and your agent.


.. admonition:: Question 15
   :class: hint

   Two MoveIt 2 plans that are each free of collisions can still make two
   robots collide.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   MoveIt 2 plans each robot as if it were alone: inspection robot 1's planning
   scene does not contain inspection robot 2. The skills package uses a zone
   lock for the known conflict, the tester area, and zone locks are coarse.


.. admonition:: Question 16
   :class: hint

   Under ROS REP 103, a yaw in a pose is given in degrees.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   REP 103 uses meters and radians. A yaw of 90 meant as degrees is read as
   90 rad: 90 / (2 × 3.1416) = 14.3 full turns.


----


Short Answer (Questions 17 to 20)
=================================

.. admonition:: Question 17
   :class: hint

   Why must a skill look up a tray slot's frame when its goal arrives, and
   not once at startup? Use the number from the class demonstration.

.. dropdown:: Answer
   :class-container: sd-border-success

   The transform from ``world`` to the AGV changes every time the AGV drives,
   so the slot's world pose changes with it. TF2 chains the moving and the
   static transforms at lookup time, so a fresh lookup is right wherever the
   AGV is. In ``tf_agv_moves.py``, a pose cached at the inspection station was
   4.229 m from the slot once the AGV was at the assembly station.


.. admonition:: Question 18
   :class: hint

   The top shell is 0.023 m tall. Your camera code finds pixel (704, 360) and
   intersects its ray with the table plane, z = 0.43 m, instead of the
   shell's top face. What goes wrong, and by how much?

.. dropdown:: Answer
   :class-container: sd-border-success

   The ray is walked to the wrong height, so the point lands in the wrong
   place. The camera is 1.43 - 0.453 = 0.977 m above the top face, so the ray
   meets it 0.977 × 0.0999 = 0.0976 m out, not 0.0999 m. The program printed
   y = 5.1024 on the top face against 5.1001 on the table: 2.3 mm apart.
   Every error in the chain lands at the gripper.


.. admonition:: Question 19
   :class: hint

   In run C, the goal is sent at 2.0 s, and the belt stops at 6.0 s while the
   arm waits for a cell the skill expects at 8.0 s. Why does the skill end
   ``PRECONDITION_FAILED`` instead of catching the cell where it stopped, and
   what should your code do next?

.. dropdown:: Answer
   :class-container: sd-border-success

   The beam saw the cell only as it crossed, at x = 0.60 m. Once the belt
   stops, the predicted arrival no longer holds, and the skill has nothing
   that says where the cell stopped. (The script knows: 0.60 + 0.1 × 6.0 =
   1.20 m, 0.20 m short of the fingers.) A stopped cell does not ride into the
   fingers, so the skill does not close, retreats, and reports that it holds
   nothing. Your code waits until the conveyor status is no longer
   ``MALFUNCTIONING``, then sends a new goal with the header of a cell that
   crosses the beam after the restart, never an old header.


.. admonition:: Question 20
   :class: hint

   Give two reasons why the course skills package reports a failure result
   instead of retrying, and say what a GP4 tool description should state
   because of it.

.. dropdown:: Answer
   :class-container: sd-border-success

   Retry and replan decisions belong to your tree and your agent (L7, L11).
   A skill that retried quietly would hide ARIAC's challenges from your code,
   and your recovery logic would never be tested. So a tool description
   should state each skill's preconditions (what the robot must hold, where
   the AGV must be) and each failure code it can return, with the message
   that explains it. An agent that reads ``PRECONDITION_FAILED`` with the
   message "AGV not at the inspection station" can move the AGV and try
   again; one that reads only "failed" cannot.
