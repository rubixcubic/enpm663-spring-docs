====================================================
Lecture
====================================================

.. note::

   These notes follow the L10 slides shown in class, in the same order and with
   the same sections, so you can read them at home. Every program output below
   is copied from the files the L10 scripts wrote when they ran with
   Python 3.12.3, NumPy 1.26.4 and ROS 2 Jazzy. The scripts and how to run them
   are on the :doc:`code page <l10_code>`.

.. important::

   **The course skills package, version 0.2.0.** The last three sections use
   the release you have, the skills of the two inspection robots, with its own
   action names and result codes. The :doc:`Course Skills Package
   </ariac/skills>` page lists every action, goal and result code. Skills for
   the Task 2 robots are planned for a later release.


.. _l10-recap:

Recap
-----

From L9
~~~~~~~

- The GP4 agent acts, observes the factory again, compares what it sees with
  what it expected, and replans when the two differ.
- A failure is a case for retrying one action or for asking for a new plan.


Today's Question
~~~~~~~~~~~~~~~~

Since GP1 you have moved the robots by calling the course skills package.
Today opens that layer: how a skill goal becomes a robot motion, and how each
step can fail.


This Week
~~~~~~~~~

No quiz and no deliverable. GP4 is due in Week 13. Quiz 5, next week, covers
L9 and L10.


.. _l10-motion-layer:

Where the Motion Layer Sits
---------------------------

This section follows one decision from the top of the stack down to a joint
trajectory on an ARIAC controller.


The Stack, Top to Bottom
~~~~~~~~~~~~~~~~~~~~~~~~

1. The GP4 agent (or the GP3 planner) decides what to do next.
2. The behavior tree executor runs the steps in order.
3. A skill goal goes to the course skills package.
4. The skills package plans the motion with MoveIt 2.
5. The plan runs on the ARIAC controllers.

Steps 1 and 2 are your team's code. Steps 3 to 5 are the **motion layer**.
Today covers steps 4 and 5, and what step 3 reports back to steps 1 and 2.

**The motion layer stays classical.**

- No learned grasping and no learned policies in the projects. AI decides at
  the task level (the GP4 agent, L8 and L9) and helps in perception (the VLM
  in GP4, the embodied-reasoning model in the final demo). Motion stays
  classical.
- Cells and shells have known shapes, so a fixed grasp per part type works,
  and when it fails, the failure is easy to read. L13 surveys the learned
  alternative.


What ARIAC 2025 Gives Each Robot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 30 46
   :class: compact-table

   * - **Robot**
     - **Motion**
     - **Grasping or tool**
   * - Inspection robots 1 and 2
     - A joint trajectory action
     - A gripper action (Robotiq 2F-85)
   * - Assembly robot 1
     - A joint trajectory action
     - A gripper action (Robotiq 2F-85)
   * - Assembly robot 2
     - A joint trajectory action
     - No gripper. Services to attach and detach a vacuum tool, and the
       tool's grasp and release services
   * - Gantry welder
     - A joint trajectory action (three slide joints)
     - No gripper. A weld service

The table is the one in L1. Source: each robot's controller file in
``ariac_description/config``, and the tool changer, vacuum tool and welder
plugins in ``ariac_plugins``.

**The two actions** (ARIAC ROS API page). The joint trajectory action, of type
``control_msgs/FollowJointTrajectory``, runs a timed list of joint positions.
The gripper action opens or closes a Robotiq 2F-85.

.. code-block:: text

   /{robot_name}/joint_trajectory_controller/follow_joint_trajectory
   /{robot_name}/gripper_controller/gripper_command

.. warning::

   ARIAC has no pick, place or move-to-pose service. The course skills package
   fills that gap.


The Five Robots
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 26 48
   :class: compact-table

   * - **Robot**
     - **Arm and tool**
     - **Job**
   * - ``inspection_robot_1``
     - UR3e, 2F-85
     - Picks cells off the moving conveyor; places them in a voltage tester
   * - ``inspection_robot_2``
     - UR5e, 2F-85
     - Takes cells off the testers; places them on an AGV tray or in recycling
   * - ``assembly_robot_1``
     - UR5e, 2F-85
     - Places four cells in the bottom shell (Task 2)
   * - ``assembly_robot_2``
     - UR5e, tool changer, VG2 and VG4
     - Places the top shell; flips the module (Task 2)
   * - Gantry welder
     - Three-axis gantry
     - Makes the six welds (Task 2)

Source: the ARIAC scenario page and the robot description files
(``ariac_description/urdf``). GP1 to GP4 use the two inspection robots. The
final demo adds the assembly robots and the welder, so this lecture is also
the first close look at Task 2 motion.


.. _l10-tf2:

TF2 in Depth
------------

**TF2** is the ROS 2 library that keeps track of coordinate frames and the
transforms between them. A **transform** says where one frame sits in
another: a translation and a rotation. This section covers static frames,
moving frames, the frames ARIAC publishes, and how a lookup fails.


Static and Moving Transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Static.**

- The L1 result: slot 1 sits at x = 0.0499 m, y = 0.0650 m, z = 0.3820 m in
  ``agv1_frame``.
- The tray is bolted to the AGV, so this transform never changes. ARIAC sends
  it once, on TF2's static broadcaster.

**Moving (dynamic).**

- The transform from ``world`` to ``agv1_frame`` changes every time the AGV
  drives between the inspection, assembly, shipping and recycling stations.
- ARIAC sends it again at every simulation step, on the moving broadcaster
  (``tf_publisher_plugin.cpp``; the AGV model sets ``<static>false</static>``).

**Chaining.** TF2 chains the moving and the static transforms, so ``world`` to
slot 1 is right wherever the AGV is.


The Frame Tree for AGV 1 and a Team Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l10/frame_tree.svg
   :alt: A tree of coordinate frames. The root, world, has two children: agv1_frame and top_camera_frame. The arrow from world to agv1_frame is dashed and marked tag 1. agv1_frame has the child agv1_tray_frame, on a solid arrow marked tag 2, and the tray has four children, agv1_slot1_frame to agv1_slot4_frame. top_camera_frame has one child, top_camera_optical_frame, drawn with a dashed outline and marked tag 3. All other arrows are solid.
   :width: 90%
   :align: center

   The frame tree for AGV 1 and a team camera.

1. A moving transform (dashed arrow), sent again as the AGV drives.
2. A static transform; every solid arrow is static.
3. A frame your team adds (dashed box); ARIAC publishes none.

``top_camera`` is a sensor name chosen for this example.


Demonstration: The AGV Moves, the Slot Moves With It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script ``tf_agv_moves.py`` stands in for ARIAC. Before the loop below, it
sends the two static transforms (tray, slot 1) from L1. Then it moves AGV 1 to
two stations and asks TF2 where slot 1 is. The AGV poses come from ARIAC's
``ariac.world`` (inspection) and ``agv_motion_plugin.hpp`` (assembly).

.. literalinclude:: code/tf_agv_moves.py
   :language: python
   :lines: 69-81
   :dedent: 4
   :caption: tf_agv_moves.py (excerpt)

Output:

.. literalinclude:: outputs/tf_agv_moves.txt
   :language: text

**The output, checked by hand:**

1. At inspection the AGV is turned 1.57 rad, about a quarter turn to the
   left. That turn maps :math:`(a, b)` to about :math:`(-b, a)`: slot 1 at
   (0.050, 0.065) becomes (-0.065, 0.050).
2. Add the AGV's position: 2.15 - 0.065 = 2.085 and 1.5 + 0.050 = 1.550.
3. At assembly the turn is 0: 5.0 + 0.050 = 5.050 and 4.5 + 0.065 = 4.565.
4. Height at both stations: 0.005 + 0.382 = 0.387 m.

.. warning::

   A skill must look up the slot frame when its goal arrives, not at startup.
   A pose cached at the inspection station sends the gripper 4.229 m from the
   slot once the AGV is at assembly.


What ARIAC Publishes, and What It Does Not
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Published** (``tf_publisher_plugin.cpp``: ``<model>_frame``, then
``<model>_<child>``):

- The voltage testers, the AGVs with their trays and slots
  (``agv1_tray_frame``, ``agv1_slot1_frame``), the tool holders, the cell feed
  point, the bottom shell insertion point, the assembly conveyor sections and
  the recycling bin.
- Each sensor your team adds: ``{sensor_name}_frame``, at the pose in your
  configuration file.

**Not published:**

- No frame and no pose topic for a cell or a shell.
- A cell's position comes from your sensors (a break beam on the conveyor).
  The top shell's pose comes from your camera.


.. _l10-tf-failures:

Demonstration: Three Lookups That Fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``tf_failures.py`` publishes ``agv1_frame`` under ``world``, and a camera frame
under ``wrld``, a typo on purpose. Then it tries three lookups:

.. literalinclude:: outputs/tf_failures.txt
   :language: text

The two times in failure 2 are clock readings, so they change on every run.


What Each Failure Means, and What to Do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 38 32
   :class: compact-table

   * - **Exception**
     - **Usual cause**
     - **What to do**
   * - ``LookupException``
     - The frame does not exist yet: a sensor or a node has not started
       publishing it
     - Wait with a timeout instead of failing at once
   * - ``ExtrapolationException``
     - The time asked for is newer than the newest transform
     - Ask for the latest transform (``Time()``), or wait briefly
   * - ``ConnectivityException``
     - Two trees: a typo in a frame name, or a frame never attached to
       ``world``
     - Fix the name; draw the tree (below)

In the skills package, a failed lookup becomes a ``PLACE_NOT_FOUND`` result,
not a crash.

**Draw the tree.** ``ros2 run tf2_tools view_frames`` listens to TF2 for
5 seconds and writes the current tree to a PDF file in the folder you run it
from. The ROS 2 Jazzy tf2 tutorial names the file ``frames.pdf``. A run on
ROS 2 Jazzy on 2026-10-12 added the date and time to the name, for example
``frames_2026-10-12_17.34.43.pdf``, and wrote a ``.gv`` file next to it.


Units and Axes: ROS REP 103
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Every frame:**

- x forward, y left, z up. Right handed.
- Distances in meters, angles in radians.

**A camera's second frame, with the** ``_optical`` **suffix:** z forward,
x right, y down. The camera section uses it next.

.. warning::

   Degrees in a pose cause wild motions. A yaw of 90 typed as degrees is read
   as 90 rad: 90 / (2 × 3.1416) = 14.3 full turns.


.. _l10-camera:

From a Camera Pixel to a Robot Target
-------------------------------------

This section covers the pinhole camera model, and the Task 2 top shell on the
assembly table.


Task 2: The Top Shell Lands Somewhere New Each Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The task** (scenario page, Step 2c):

- After your ``/insert_top_shell`` call, the top shell appears on the assembly
  table at a random position and orientation.
- In the code: up to 0.05 m off in x, up to 0.1 m off in y, any yaw
  (``shell_insertion_plugin.hpp``).
- Assembly robot 2 can pick it only after your sensors find it.

**The chain, in numbered steps:**

1. Your camera publishes an image and its intrinsics.
2. Your camera code finds the shell in the image (OpenCV: ``threshold``,
   ``findContours``, ``minAreaRect``).
3. The pinhole camera model turns the pixel and the known table height into a
   3D point in the camera's optical frame.
4. TF2 moves that point into the ``world`` frame, using the camera pose in
   your configuration file.
5. The result is a stamped pose. The pick skill for the top shell (planned
   for the package's Task 2 release) takes it from your camera, never the true
   pose from the simulator.


What an ARIAC Camera Publishes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``/{camera_name}/image``: ``sensor_msgs/Image``.
- ``/{camera_name}/info``: ``sensor_msgs/CameraInfo``, with the intrinsic
  matrix :math:`K`.
- Both stamped in the frame ``{camera_name}_frame`` (``image_plugin.cpp``).

.. admonition:: Definition: the intrinsic matrix K
   :class: note

   The **intrinsics** are the numbers that describe the camera itself, not
   where it is mounted. ROS stores them in a 3 by 3 matrix:

   .. math::

      K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}

   - :math:`f_x`, :math:`f_y`: the **focal length**, in pixels, along the
     image's width and height.
   - :math:`c_x`, :math:`c_y`: the **principal point**, the pixel where the
     camera's optical axis meets the image.
   - ``CameraInfo.k`` holds the nine numbers row by row.


The Pinhole Model: The Picture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **pinhole camera model** treats the camera as a single point: every ray
of light passes through it and lands on a flat image plane in front of it.

.. figure:: /_static/images/l10/pinhole_model.svg
   :alt: A pinhole camera seen from above. Tag 1 marks the camera center, where the optical frame starts: z points right along the optical axis, x points down the page, and y points into the page. Tag 2 is the image plane, a distance f in front of the center. A dashed ray runs from the center to a point, tag 3, at depth Z and sideways offset X. The ray crosses the image plane at tag 4, a distance u minus c x from the axis.
   :width: 90%
   :align: center

   Seen from above; not to scale.

1. The camera center, origin of the optical frame (z forward, x right,
   y down).
2. The image plane, :math:`f` pixels in front of the center.
3. A point at depth :math:`Z`, sideways offset :math:`X`.
4. Its image, at pixel column :math:`u`.


The Pinhole Model: The Formula
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The point and the pixel.**

- A point at :math:`(X, Y, Z)` in the optical frame: :math:`Z` ahead of the
  camera, :math:`X` to the right, :math:`Y` down, in meters.
- Its image is at pixel column :math:`u` (counted from the left) and pixel row
  :math:`v` (counted down from the top).

**Similar triangles.**

- In the picture, the small triangle (sides :math:`f_x` and :math:`u - c_x`)
  and the large one (sides :math:`Z` and :math:`X`) have the same shape:
  :math:`(u - c_x) / f_x = X / Z`.
- The same holds for rows, with :math:`Y`, :math:`f_y` and :math:`c_y`.

**The model:**

.. math::

   u = f_x \frac{X}{Z} + c_x, \qquad v = f_y \frac{Y}{Z} + c_y


The Intrinsics of an ARIAC Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What sets them.**

- Resolution: ``720p`` is 1280 × 720 pixels, ``1080p`` is 1920 × 1080
  (``ariac_setup/structures.py``).
- ``FOV`` in your configuration file is the horizontal field of view, in
  radians: ARIAC writes it into the camera's ``horizontal_fov``.

**What Gazebo computes.** ARIAC's camera model gives no lens values, so
Gazebo computes them (gz-rendering ``Utils.cc``, gz-sensors
``CameraSensor.cc``):

.. math::

   f_x = f_y = \frac{\text{width} / 2}{\tan(\text{FOV} / 2)}, \qquad
   c_x = \frac{\text{width}}{2}, \qquad c_y = \frac{\text{height}}{2}

.. tip::

   Read :math:`K` from ``/{camera_name}/info`` in your code. The formula is for
   checking it, and for planning a camera before you buy it.


.. _l10-pixel-example:

Worked Example: One Pixel on the Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The camera** (pose chosen for this example):

- 720p (1280 × 720), FOV = 1.57 rad: the FOV in the ARIAC docs' example
  configuration.
- 1.0 m above the assembly table, looking straight down.

**In numbered steps:**

1. :math:`f_x` = (1280 / 2) / tan(1.57 / 2) = 640 / tan(0.785) =
   640 / 0.9992 = 640.5 pixels.
2. A pixel 64 pixels right of the image center is a ray with slope
   64 / 640.5 = 0.0999.
3. On the table 1.0 m below, that ray lands 1.0 × 0.0999 = 0.10 m from the
   point straight under the camera.
4. At this height one pixel covers 1.0 / 640.5 m, about 1.6 mm, of the table.


Three Frames at the Camera, Seen From the Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l10/camera_table_ray.svg
   :alt: A side view of a camera 1.0 m above the assembly table, looking straight down. A dashed line drops from the camera to the table; a solid ray goes from the camera to a red point on the table, tag 4, 0.10 m to the right of the dashed line. Three sets of axes are drawn on the left. Tag 1, the world: z up, y left, x into the page. Tag 2, the camera link frame: x down, y left, z into the page. Tag 3, the optical frame: z down, x right, y out of the page.
   :width: 90%
   :align: center

   Side view, looking along world +x; not to scale. The camera's lens is
   1.0 m above the table, with RPY (roll, pitch, yaw) = (0, :math:`\pi`/2, 0).

1. ``world``.
2. ``top_camera_frame``, the frame ARIAC publishes.
3. The optical frame.
4. Where pixel (704, 360) meets the table.


The Camera's Frame Is Not the Optical Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ARIAC publishes only ``{camera_name}_frame``, the camera model's frame, and
  no optical frame.
- A Gazebo camera looks along its frame's +x axis, with z up (sdformat
  issue 425).
- The pinhole formulas use the optical frame: z forward, x right, y down. Add
  it yourself, as a static child of the camera's frame.

**The rule between the two.**

- A point at :math:`(x, y, z)` in the optical frame is at
  :math:`(z, -x, -y)` in the camera's frame.
- In the picture above, optical z (tag 3) and the camera frame's x (tag 2)
  both point down, and optical x points right, opposite to the camera frame's
  y.
- With RPY (0, :math:`\pi`/2, 0) in the configuration file, the camera's +x
  points straight down.


From a Pixel to a Point on a Known Plane
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The method, in numbered steps:**

1. Turn pixel :math:`(u, v)` into a ray in the optical frame:
   :math:`r = \big((u - c_x) / f_x,\ (v - c_y) / f_y,\ 1\big)`.
2. Rotate the ray into the ``world`` frame with TF2. The camera's origin,
   :math:`o`, comes from the same lookup.
3. Walk along the ray until it reaches the plane
   :math:`z = z_\text{table}`. The distance factor is
   :math:`t = (z_\text{table} - o_z) / r_z`, where :math:`r_z` is the ray's
   world z part, and the point is :math:`o + t\,r`.
4. For the yaw, find the shell's outline with OpenCV (``threshold``,
   ``findContours``, ``minAreaRect``). The shell's black and white bands must
   be aligned (Step 2c), which helps fix the yaw.

The assembly table top is at z = 0.43 m (``assembly_table/model.sdf``: a
0.43 m tall box on the floor).


.. _l10-pixel-demo:

Demonstration: The Code
~~~~~~~~~~~~~~~~~~~~~~~

The three steps above, in ``pixel_to_table.py``:

.. literalinclude:: code/pixel_to_table.py
   :language: python
   :lines: 70-75
   :caption: pixel_to_table.py (excerpt: the method)

The camera pose and the optical frame, sent as two static transforms:

.. literalinclude:: code/pixel_to_table.py
   :language: python
   :lines: 87-94
   :dedent: 4
   :caption: pixel_to_table.py (excerpt: the frames)

Chosen for this example: the sensor ``top_camera`` at (3.85, 5.2, 1.43) m,
1.0 m above the table top, over the spot where ARIAC drops the top shell
before its random offset.


Demonstration: The Output
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/pixel_to_table.txt
   :language: text

1. :math:`f_x` = 640.5, as in the worked example.
2. TF2 turns optical (1, 2, 3) into (3, -1, -2): the rule :math:`(x, y, z)` to
   :math:`(z, -x, -y)`.
3. Pixel (704, 360), 64 pixels right of the center, lands
   5.2 - 5.1001 = 0.0999 m from the point under the camera, as in the worked
   example. For this camera pose, image right is world -y.
4. Pixel (576, 296) is 64 pixels left and 64 up: 0.0999 m toward world +x
   and +y.
5. Projecting the table point back gives pixel 704.1: the chain agrees with
   itself.


Every Error in the Chain Lands at the Gripper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The shell's top face is not the table.**

1. The top shell is 0.023 m tall (its collision mesh), so its top face is at
   0.43 + 0.023 = 0.453 m.
2. The camera is then 1.43 - 0.453 = 0.977 m above it, and the 64-pixel ray
   lands 0.977 × 0.0999 = 0.0976 m out.
3. The program agrees: y = 5.1024 on the shell's top face against 5.1001 on
   the table, 2.3 mm apart.

**Other errors.**

- A camera yaw typed wrong in the configuration file moves every target. L12
  measures this as position error.
- The camera frame's direction is checked from the source code only. Check it
  once in simulation, with an object at a known position, before you trust
  the chain.


.. _l10-moveit:

MoveIt 2 Architecture
---------------------

**MoveIt 2** is the ROS 2 motion planning framework. This section covers the
parts between a skill goal and the ARIAC controller (MoveIt 2.12 on ROS 2
Jazzy).


The Parts Between a Skill Goal and the Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l10/moveit_architecture.svg
   :alt: A block diagram. A skill goal goes to MoveItPy, which calls MoveItCpp; both sit inside a dashed box marked tag 1. MoveItCpp sends the request into the planning pipeline, tag 2: request adapters, then a planner (OMPL or Pilz), then response adapters. A planning scene block, tag 3, feeds the planner. The result goes to trajectory execution, which sends it to the ARIAC joint trajectory controller outside the dashed box. A separate dashed block on the left, move_group node, is marked tag 4 and has no arrows.
   :width: 85%
   :align: center

   The parts between a skill goal and the ARIAC controller.

**The parts, one sentence each:**

1. **The skills server process:** **MoveItPy**, MoveIt 2's Python interface,
   calls **MoveItCpp** inside the same process, with no ROS actions or
   services between them.
2. **The planning pipeline:** request adapters check or fix the start state, a
   planner plugin finds a path, and response adapters check the path or add
   its timing. OMPL's path gets its timing from a response adapter; Pilz times
   its own path (skills package NOTICE).
3. **The planning scene:** the robot's current joint state and the collision
   objects around it. A planner can only avoid what is in the scene.
4. ``move_group``: a node that offers the same parts through ROS actions and
   services. A MoveItPy program does not need it, and the example team runs
   none.

**Trajectory execution** sends the timed path to the ARIAC joint trajectory
action.


Instructor Demonstration: The Example Team's Move Robots Demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What the example team ships** (``usnistgov/ariac_example_team``):

- ARIAC ships no MoveIt configuration. The example team ships one for each of
  the five robots, and the course skills package starts from it.
- Its planner settings: Pilz PTP by default, Pilz LIN for a straight line, and
  OMPL's RRTstar on request (``moveit_cpp.yaml``, ``robot_interface.py``). The
  next section explains each planner.

.. code-block:: bash

   ros2 run example_team move_robots

**What it does** (``move_robots.py``, ARIAC demos page):

- Creates one MoveItPy instance per robot and moves all five at once.
- Each UR arm goes 0.1 m down, then up; the gantry goes 0.05 m back and forth
  along x. Every robot makes 20 such moves, each a straight line planned with
  Pilz LIN.
- It runs each plan right after planning. The example team ships no RViz setup
  for viewing the planning scene or a path before it runs.

It needs the ``moveit_py`` package (``example_team/package.xml``). If it does
not run on the classroom machine, a recorded run replaces it.


.. _l10-planners:

Planners and When Each Fits
---------------------------

This section covers sampling-based planners (OMPL), the Pilz industrial
motion planner, and how to choose between them.


Sampling-Based Planners (OMPL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: sampling-based planner
   :class: note

   A **sampling-based planner** picks random joint configurations, keeps the
   ones that are free of collisions, and links them into a path. OMPL, the
   Open Motion Planning Library, holds MoveIt's sampling-based planners.

- **RRT-Connect** grows two random trees, one from the start and one from the
  goal, until they meet. It is fast for one query at a time, which suits a
  robot that plans each move fresh.
- **PRM** (probabilistic roadmap) builds a roadmap of free configurations once
  and reuses it for many queries. It pays off when the scene does not change.
- **RRTstar**, the example team's OMPL setting, grows one tree and keeps
  shortening its path while time remains. OMPL's documentation calls it
  "asymptotically-optimal" and says it "is guaranteed to converge to an
  optimal solution", where "the notion of optimality is with respect to a
  specified OptimizationObjective".

.. warning::

   All three are random. The same goal can give a different path on each run,
   and a planner can run out of time even when a path exists. L12 counts this
   as run-to-run variation.

**The class demonstration** (``rrt_connect_toy.py``):

- A teaching toy, not MoveIt or OMPL: RRT-Connect for a point in a 10 m
  square, in 0.5 m steps. OMPL samples the same way in a UR arm's six joint
  angles.
- The walls, the start, the goal and the step are chosen for this example
  (Kuffner and LaValle, ICRA 2000).
- The full script is on the :doc:`code page <l10_code>`.


The Two Trees for Seed 1
~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l10/rrt_tree.svg
   :alt: A square plot, x and y from 0 to 10 meters. Two gray rectangles are walls: one from x 3 to 4 m rising from the bottom to y 7 m, one from x 6 to 7 m hanging from the top down to y 3 m. Tag 1, the start, is at (1.5, 1.5) m; tag 2, the goal, at (8.5, 8.5) m. A tree of thin solid black lines grows from the start, and a tree of dashed orange lines grows from the goal. A thick red path joins start and goal, going over the first wall and under the second.
   :width: 70%
   :align: center

   A plot of the toy's flat square, not of the robot cell.

- 1: the start. 2: the goal.
- Gray boxes: walls.
- Thin solid lines: the tree from the start.
- Dashed orange lines: the tree from the goal.
- Thick red line: the path, where the trees met.


Five Runs, Five Different Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/rrt_connect.txt
   :language: text

1. The same start, goal and walls give paths from 22.51 m to 32.18 m. Only the
   random seed changed.
2. The shortest route, a taut string around the wall corners, is 17.87 m.
   Every path is longer: the trees stop at the first path they find.
3. The number of samples drawn ranges from 141 to 400. With a time limit, a
   slow run becomes a failed run.

.. tip::

   MoveIt's OMPL interface has a setting that shortens a sampled path, but the
   variation from run to run stays. Plan the same move twice and expect two
   different motions.


The Pilz Industrial Motion Planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Three standard industrial motions** (MoveIt documentation):

- **PTP**: point to point in joint space; all joints start and stop together.
- **LIN**: a straight line of the gripper in Cartesian space.
- **CIRC**: a circular arc in Cartesian space.

**Why it fits a factory cell.**

- No random sampling: the same request gives the same motion. The MoveIt
  planners page calls Pilz "a deterministic generator for circular and linear
  motions".
- A straight-line descent is what you want when you lower a cell into a
  voltage tester or a tray slot: predictable and repeatable.
- Each motion has a fixed shape, so it cannot go around an obstacle.

**A course measurement: Pilz planned into a box.**

- With the example team's Pilz settings, which have no response adapters, a
  goal 0.02 m inside a collision box still planned "successfully" (skills
  package NOTICE, checked 2026-10-12 with ``is_state_colliding()`` on the
  plan's last state).
- So the skills package adds the response adapter ``ValidateSolution`` to its
  Pilz settings. It checks the path against the planning scene, and a Pilz
  plan into an obstacle then fails.


Choosing a Planner for an ARIAC Motion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 42 20 38
   :class: compact-table

   * - **Motion**
     - **Planner**
     - **Why**
   * - Lower a cell into a tester or a tray slot; lift it out
     - Pilz LIN
     - A straight line, the same every time
   * - Carry a cell between the conveyor, the testers and an AGV, in open
       space
     - Pilz PTP
     - A joint move with no sampling; the example team's default
   * - A move where the PTP motion would hit equipment
     - OMPL (RRTstar)
     - Searches around obstacles; random

**In the course skills package:**

- It plans with Pilz first. If Pilz finds no path, it tries once with OMPL.
- One more retry: when MoveIt stops a motion with "controller is taking too
  long" (ARIAC issue 386), it re-plans the rest with Pilz and runs it once
  more. The result's ``attempts`` counts both retries.
- **Trajectory optimization** (CHOMP, STOMP) starts from a path and pushes it
  away from obstacles while keeping it smooth. It is installed with MoveIt 2
  but not used here.


.. _l10-grasps:

Parameterized Grasps
--------------------

This section defines a grasp as a fixed offset from a part frame, and finds a
cell on the moving conveyor.


A Grasp Is a Part Frame Plus a Fixed Offset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: parameterized grasp
   :class: note

   A **parameterized grasp** places the gripper at a part's frame combined
   with a fixed offset.

In the skills package, each place in ``skills.yaml`` has a TF frame, an offset
and an approach height. Tester 1: the frame ``voltage_tester_1_frame``, offset
(0, 0, 0), approach 0.05 m above it. The 2F-85 opens from 0 to 0.085 m
(ARIAC's gripper controller rejects other widths).

**A tester pick is a short sequence of poses** (``pick_from_tester``):

1. Approach: move 0.05 m above the tester frame.
2. Descend in a straight line (Pilz LIN) to the frame.
3. Close the gripper.
4. Lift back to the approach point, then retreat to the park pose.

The skill reports each stage as action feedback: ``open``, ``enter_zone``,
``approach``, ``descend``, ``grasp``, ``lift``, ``retreat``.

The conveyor pick is different: the arm waits at one fixed pose, and the cell
comes to it.


.. _l10-conveyor:

Worked Example: When Does the Cell Reach the Catch Point?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is known.**

- ARIAC publishes no pose for a cell. Your **break beam** (a sensor that
  fires when something crosses its light beam) fires when a cell crosses it.
  The goal of ``pick_from_conveyor`` carries that message's header: the
  beam's frame (where) and its stamp (when).
- The arm waits at one fixed pose: gripper level, pointing upstream, fingers
  open across the belt at the **catch point**, x = 1.40 m. The cell rides
  into the fingers. A cell held from the side can be laid flat in a tester;
  one held from the top cannot (package README).
- The package's own setup: beam at x = 0.60 m, belt at 0.1 m/s, the largest
  speed ARIAC allows.

**In numbered steps** (``conveyor.py``):

1. From the beam to the catch point: 1.40 - 0.60 = 0.80 m.
2. At 0.1 m/s that takes 0.80 / 0.1 = 8.0 s: the cell arrives 8.0 s after the
   beam fired.
3. The fingers close 0.15 s earlier, at 8.0 - 0.15 = 7.85 s (``close_delay``,
   measured).


The Catch Seen From Above
~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l10/conveyor_intercept.svg
   :alt: The inspection conveyor seen from above, moving to the right (arrow), along world x. A break beam, tag 1, crosses the belt at x = 0.6 m. A gripper, tag 2, waits at x = 1.4 m with two open fingers pointing upstream, one on each side of the belt's center. Red circles show one cell: faded at 0.6 m (t = 0 s) and 0.8 m (t = 2.0 s), solid between the fingers at 1.4 m (t = 8.0 s), tag 3. A hollow red circle at 1.2 m (t = 6.0 s) is tag 4. Below, a world x axis from 0.6 to 1.4 m.
   :width: 95%
   :align: center

   The belt moves along world +x (arrow). Distances along the belt are to
   scale; the belt's width and the sizes of the cell and the gripper are not.
   :math:`t`: seconds after the beam fired.

1. The break beam.
2. The gripper, waiting at the catch point.
3. The cell reaches the fingers (run A).
4. Where the cell stops in run C, when the belt stops at :math:`t` = 6.0 s.

.. note::

   **A contrast, not the course skill.** A **moving intercept** aims the arm
   at a predicted point anywhere in its reach. The course skill never does
   this: it waits at one pose.


When the Catch Skill Refuses or Gives Up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Refused before any motion** (``PRECONDITION_FAILED``):

1. The beam's stamp is older than 8.0 s (``max_trigger_age``), or in the
   future.
2. The cell would reach the catch point sooner than 3.925 s from now
   (``side_lead_time``). That is the longest measured move to the catch pose,
   3.015 s, plus 0.410 s to open the gripper, plus a 0.5 s margin.
3. The belt is stopped, and the beam is not at the catch point (within
   0.005 m).

**Ends while waiting** (``PRECONDITION_FAILED``): the belt stops or changes
speed. The skill does not close the gripper, retreats, and reports that it
holds nothing. The beam saw the cell only as it crossed, so the skill no
longer knows where the cell is.

Sources, in the skills package v0.2.0: ``conveyor.py`` (``plan_catch``),
``inspection_robot_1.py`` (``_belt_change``), ``skills.yaml`` and the README.
The :doc:`Course Skills Package </ariac/skills>` page says the same.


Demonstration: Four Separate Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``conveyor_intercept.py`` is a model of the skill's timing and refusals, with
the package's numbers. It plays four separate runs, A to D, each with one
cell:

.. literalinclude:: outputs/conveyor_intercept.txt
   :language: text

"Refused" is ``PRECONDITION_FAILED``. Run C stands in for the conveyor
malfunction challenge.

Passing the timing checks only lets the skill go on to the grasp. The real
``pick_from_conveyor`` can still end ``GRASP_FAILED`` if the fingers close on
nothing (``inspection_robot_1.py``, lines 130 to 140, v0.2.0); the script does
not simulate the grasp.


Reading the Four Runs
~~~~~~~~~~~~~~~~~~~~~

1. Run A: 8.0 - 2.0 = 6.0 s remain, more than 3.925 s. The skill waits and
   catches the cell.
2. Run B: 8.0 - 5.0 = 3.0 s remain, less than 3.925 s, so the skill refuses
   before moving. The latest goal is 8.0 - 3.925 = 4.075 s after the beam.
3. Run C: the belt stops at 6.0 s, with the cell at 0.60 + 0.1 × 6.0 =
   1.20 m, 0.20 m short of the fingers. Only the script knows that. The skill
   ends ``PRECONDITION_FAILED`` without closing.
4. Run D: a goal sent while the belt is stopped is refused. The beam
   (0.60 m) is not at the catch point.

**The conveyor malfunction challenge (L9: wait).** Wait until the status is no
longer ``MALFUNCTIONING``. Then send a new goal with the header of a cell that
crosses the beam after the restart. Never reuse an old header (README).

**The time budget per cell.** A feed of 0.1 cells per second gives one cell
every 1 / 0.1 = 10 s, so cells are 0.1 × 10 = 1.0 m apart.


.. _l10-skills:

Inside the Course Skills Package
--------------------------------

This section traces one goal from call to result, and covers robots sharing
space. It describes version 0.2.0, the release you use: the skills of the two
inspection robots. The :doc:`Course Skills Package </ariac/skills>` page lists
every action, goal and result code.


How the Package Is Built
~~~~~~~~~~~~~~~~~~~~~~~~

- One server process. Inside it, one ROS 2 node per robot, each serving that
  robot's skills as ROS 2 actions at ``/<robot>/skills/<skill>``.
- Each robot node owns its robot's MoveItPy instance.
- A ``MultiThreadedExecutor`` lets the robots move at the same time: the L1
  executor demonstration, where a single-threaded executor let one slow
  callback starve a timer.
- Each skill goes from a goal to a MoveIt 2 plan, to a joint trajectory on the
  ARIAC controller, to a gripper command.
- Skills for the assembly robots and the welder (Task 2) are planned for a
  later release.

.. tip::

   Your code sends a goal, reads the feedback (the current stage) and reads one
   result. It never imports MoveIt.


Trace: ``place_in_slot``, Goal ``agv`` (1 to 3) and ``slot`` (1 to 4)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check what the robot holds. Placing with an empty gripper is refused:
   ``PRECONDITION_FAILED``.
2. Check that the AGV is at the inspection station, with ``/agvN/info``. The
   skill checks again before the descent and before the release.
3. Look up the slot frame with TF2 now, because the AGV moves. A failed lookup
   returns ``PLACE_NOT_FOUND``.
4. Plan with MoveIt 2: Pilz first, then OMPL once if Pilz finds no path.
5. Run the plan on the joint trajectory action, with a time limit per stage,
   so a hung controller becomes a failure result instead of a hang.
6. Check that the cell is still held, open the gripper, lift, and return a
   result: a code, a message, what the robot holds and how many attempts were
   made.


.. _l10-failure-results:

The Failure Codes, by Meaning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every skill returns a ``SkillResult``. Its ``code`` is one of these, or
``SUCCESS``:

.. list-table::
   :header-rows: 1
   :widths: 32 68
   :class: compact-table

   * - **Code**
     - **When**
   * - ``PLANNING_FAILED``
     - Pilz, then OMPL, found no path
   * - ``EXECUTION_FAILED``
     - The controller rejected or stopped the trajectory, or a stage ran past
       its time limit
   * - ``GRASP_FAILED``
     - The gripper closed on nothing, or the cell slipped out before release
   * - ``PRECONDITION_FAILED``
     - Wrong object held or AGV away; for the conveyor catch, a stale
       trigger, a cell the arm cannot meet in time, or a stopped or changed
       belt
   * - ``PLACE_NOT_FOUND``
     - A TF2 lookup failed
   * - ``ZONE_BUSY_TIMEOUT``
     - The other robot held the tester area too long (below)
   * - ``CANCELED``
     - The caller canceled the goal

``holding`` says what the robot holds at the end: ``NOTHING``, ``CELL``,
``SHELL`` or ``MODULE``.


No Hidden Retries
~~~~~~~~~~~~~~~~~

**After a failure.**

- A skill never re-picks, re-places or re-checks a precondition by itself.
  The only retries are the two that ``attempts`` counts: the planner fallback
  and the re-execution after a controller timeout (above).
- If the arm moved, it lifts straight up. If the skill held the tester area,
  it then parks and releases the lock. The result says what the robot holds.

**After a cancel.** It stops the trajectory, retreats, releases its zone lock
and returns ``CANCELED`` with what it holds.

**Why.**

- Retry and replan decisions belong to your tree and your agent (L7, L11).
- A skill that retried quietly would hide ARIAC's challenges from your code,
  and your recovery logic would never be tested.


Robots Sharing Space: Two Safe Plans Can Collide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- MoveIt 2 plans each robot as if it were alone: inspection robot 1's planning
  scene does not contain inspection robot 2.
- Two plans that are each free of collisions can still hit each other.

**What a collision costs** (scoring page, ``scoring_weights.yaml``):

- 100 points for every 5 s a robot is in contact.
- A collision between two robots counts twice: each robot is charged.
- L12 works through the scoring formula.

**Zone locks: one zone in v0.2.0.** A **zone lock** lets one robot at a time
into a shared area.

- ``tester_area``, shared by the two inspection robots. ``pick_from_tester``
  and ``place_on_tester`` take its lock before the arm enters and release it
  once the arm is parked outside. A lock not free within 120 s of wall-clock
  time (``zone_wait``) returns ``ZONE_BUSY_TIMEOUT``.
- ``place_in_slot`` and ``drop_in_recycling`` take no zone: in 20 runs beside
  inspection robot 1 at a tester, the two robots never touched (README).

**Zone locks: what your code must know.**

- If a retreat after a failure or a cancel does not finish, the robot keeps
  the lock, because the arm may still be inside.
- Every later result from that robot then says so in its message. Only a
  ``move_home`` that succeeds releases the lock.
- Zones for the Task 2 robots are not settled yet: they come with the later
  release.

.. warning::

   Zone locks are coarse. They prevent the known conflicts, not every possible
   one. Watch for collisions in your test runs.


.. _l10-gp4:

What the GP4 Agent and the Final Demo Need
------------------------------------------

This section covers preconditions and failure results in the agent's tool
descriptions, and Task 2 motion.


Tool Descriptions That Name Preconditions and Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What a tool description should state:**

- Each skill's **preconditions** (what must be true before it runs): what the
  robot must hold, where the AGV must be.
- Each failure code it can return, with the message that explains it.
- An agent that reads ``PRECONDITION_FAILED`` with the message "AGV not at the
  inspection station" can move the AGV and try again. One that reads only
  "failed" cannot.

**Retry or replan (the L9 rule):**

- ``GRASP_FAILED``: a candidate for one local retry.
- ``PLACE_NOT_FOUND``, or the AGV at the wrong station: the world is not what
  the plan assumed. Replan.


Task 2 Motion in the Final Demo (Scenario Page)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Assembly robot 1 places four cells in the bottom shell, in the polarity the
   shell marks. The AGV tray's center hole can be used to regrasp a cell.
2. Assembly robot 2 changes to VG2 and places the top shell. The shell's pose
   comes from your camera: today's pixel-to-table chain.
3. The gantry welder makes four top welds.
4. Assembly robot 2 changes to VG4 and flips the module.
5. The welder makes two bottom welds: six welds in all.

.. warning::

   The vacuum tool malfunction challenge makes one chosen grasp of VG2 or VG4
   fail. The Task 2 skill (planned) reports it; your code moves the tool away
   and retries.


Next Class
----------

**Quiz 5** (Wednesday, April 14, start of class) covers L9 and L10. Review:
VLM grounding and replanning; static and moving frames; the pinhole model and
the pixel-to-table steps; the MoveIt 2 parts; RRT-Connect, PRM and Pilz; the
conveyor catch and its refusals; the skill failure codes.

**L11: Recovery, Robustness, and Failure Handling for Agentic Systems.** What
your tree and agent do with today's failure results. The final demo
specification is posted.

**Before next class:**

- GP4 (due Week 13): write tool descriptions that list each skill's
  preconditions and failure results.
- Read the course skills package documentation page.
- Run the L10 scripts (see :doc:`l10_code`) and compare your outputs with the
  ones above. Optional: the Move Robots demo.
