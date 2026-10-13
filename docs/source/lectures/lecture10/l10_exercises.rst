====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work: Quiz 5, which covers L9 and L10, and GP4, listed in the
   :doc:`syllabus </syllabus/index>`.

Six take-home exercises built on the L10 slides and their running examples:
slot 1 of AGV 1, the camera 1.0 m above the assembly table, the RRT-Connect
toy, the cell on the moving conveyor, and the skill failure results.
Exercises 1, 2, 4 and 5 mix paper arithmetic with a change to one of the
:doc:`L10 scripts <l10_code>`. Exercise 3 changes ``tf_failures.py``.
Exercise 6 is paper only, and is the one closest to GP4.

.. note::

   Copy a script before you change it, and work on the copy. The ROS 2
   scripts need ``source /opt/ros/jazzy/setup.bash`` in the terminal first.
   Do not run them while an ARIAC simulation runs on the same ROS domain (see
   the :doc:`code page <l10_code>`). Every number in the solutions below was
   computed by hand and checked by running the changed script.


.. dropdown:: Exercise 1. Slot 1 at a Third Station
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Chain a moving and a static transform by hand, check it with TF2, and see
   how far a cached pose goes wrong.

   .. raw:: html

      <hr>

   **Part A. By hand**

   Slot 1 sits at (0.050, 0.065, 0.382) m in ``agv1_frame`` (the L1 result,
   rounded as in ``tf_agv_moves.py``'s output). Chosen for this exercise: AGV 1
   drives to (10.0, 2.0, 0.005) m with a yaw of 3.14 rad, about a half turn.

   1. A half turn maps :math:`(a, b)` to about :math:`(-a, -b)`. Where is
      slot 1 in the world frame?
   2. A skill cached slot 1's world pose at the inspection station,
      (2.085, 1.550, 0.387) m. How far is that pose from the slot now?
   3. Of the three transforms in the chain (world to AGV, AGV to tray, tray to
      slot), which one changed? Which one would ARIAC send again?

   .. raw:: html

      <hr>

   **Part B. With TF2**

   4. In a copy of ``tf_agv_moves.py``, add a third station to the
      ``stations`` list:

      .. code-block:: python

         ("exercise", (10.0, 2.0, 0.005), 3.14),

      and change ``a, b = found`` to ``a, b = found[0], found[2]`` so the last
      line compares inspection with the new station. Run it and compare with
      Part A.

   .. raw:: html

      <hr>

   **Part C. Degrees by mistake**

   5. A teammate meant a quarter turn and typed a yaw of 90, in degrees. ROS
      reads it in radians. How many full turns is that, and what angle is
      left over after the full turns? How far is that from the intended
      :math:`\pi / 2`?

   .. dropdown:: Solution
      :color: success

      **1.** The half turn: (0.050, 0.065) becomes (-0.050, -0.065). Add the
      AGV's position: 10.0 - 0.050 = 9.950 and 2.0 - 0.065 = 1.935. The
      height is 0.005 + 0.382 = 0.387. Slot 1 is at
      **(9.950, 1.935, 0.387) m**.

      **2.** The heights are the same, so only x and y differ.

      1. Along x: 9.950 - 2.085 = 7.865 m.
      2. Along y: 1.935 - 1.550 = 0.385 m.
      3. Distance: :math:`\sqrt{7.865^2 + 0.385^2} = \sqrt{61.858 + 0.148}
         = \sqrt{62.006} = 7.874` m.

      **3.** Only world to AGV changed: it is the moving transform, and ARIAC
      sends it again at every simulation step. The tray and slot transforms
      are static; ARIAC sent them once.

      **4.** The changed script prints:

      .. code-block:: text

         slot 1 of AGV 1, in meters
         in world, AGV at inspection: x = 2.085, y = 1.550, z = 0.387
         in world, AGV at assembly  : x = 5.050, y = 4.565, z = 0.387
         in world, AGV at exercise  : x = 9.950, y = 1.935, z = 0.387
         in agv1_frame, any station : x = 0.050, y = 0.065, z = 0.382
         a pose cached at inspection is 7.874 m off

      It agrees with Part A to the last digit. 3.14 rad is not exactly
      :math:`\pi`: it is 3.1416 - 3.14 = 0.0016 rad short. Slot 1 is
      :math:`\sqrt{0.050^2 + 0.065^2}` = 0.082 m from the AGV's origin in
      x and y, so the shortfall moves it by about 0.082 × 0.0016 = 0.0001 m,
      too little to show at three decimals.

      **5.** One full turn is :math:`2\pi` = 6.2832 rad.

      1. Full turns: 90 / 6.2832 = 14.3, so 14 full turns.
      2. Fourteen turns: 14 × 6.2832 = 87.9646 rad.
      3. Left over: 90 - 87.9646 = 2.0354 rad, about 116.6 degrees
         (2.0354 × 180 / 3.1416).
      4. The intended angle is :math:`\pi / 2` = 1.5708 rad, so the pose is
         turned 2.0354 - 1.5708 = 0.4646 rad (about 26.6 degrees) too far.


.. dropdown:: Exercise 2. More Pixels on the Table
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work the pixel-to-table chain by hand for new pixels and a new camera, then
   check it with ``pixel_to_table.py``.

   .. raw:: html

      <hr>

   **Part A. Optical frame to camera frame**

   1. A point is at (0.2, -0.1, 0.9) m in the optical frame. Where is it in
      the camera's frame (``top_camera_frame``)? Say in words which way
      "0.9 m ahead" points in each frame.

   .. raw:: html

      <hr>

   **Part B. A new pixel, by hand**

   Use the class camera: 720p, :math:`f_x = f_y` = 640.5, :math:`c_x` = 640,
   :math:`c_y` = 360, at (3.85, 5.2, 1.43) m, looking straight down, 1.0 m
   above the table top (z = 0.43 m). From the class output: image right is
   world -y, and image up is world +x.

   2. Where on the table does pixel (800, 400) land?
   3. Where does pixel (0, 0), the top left corner, land? About how much of
      the table does the camera see? Is that enough for the top shell's
      random offset (up to 0.05 m in x, up to 0.1 m in y)?
   4. The shell's top face is 0.977 m below the camera. Where does pixel
      (800, 400) land on it, and how far is that from the table point? Compare
      with the 2.3 mm for pixel (704, 360) in class.

   .. raw:: html

      <hr>

   **Part C. With the script**

   5. In a copy of ``pixel_to_table.py``, change the pixel list to
      ``[(704, 360), (800, 400), (0, 0)]``, and the top-face line to use
      pixel (800, 400) (both the ``pixel_to_plane`` call and its ``print``).
      Run it and compare with Part B.
   6. Now a 1080p camera with the same FOV at the same pose. Compute
      :math:`f_x` by hand, the size of one pixel on the table, and how many
      pixels right of center land 0.10 m out. Check: set
      ``W, H, FOV = 1920, 1080, 1.57`` and the pixel list to
      ``[(1056, 540)]``, and run.

   .. dropdown:: Solution
      :color: success

      **1.** The rule is :math:`(x, y, z)` to :math:`(z, -x, -y)`, so
      (0.2, -0.1, 0.9) becomes **(0.9, -0.2, 0.1)** in the camera's frame.
      "0.9 m ahead" is along optical +z, and along the camera frame's +x: a
      Gazebo camera looks along its frame's +x.

      **2.** In numbered steps:

      1. Offsets from the center: 800 - 640 = 160 pixels right, and
         400 - 360 = 40 pixels down.
      2. Slopes: 160 / 640.5 = 0.2498 and 40 / 640.5 = 0.0625.
      3. On the table 1.0 m below: 1.0 × 0.2498 = 0.2498 m and
         1.0 × 0.0625 = 0.0625 m from the point under the camera.
      4. Directions: right is world -y; down is the opposite of up, so world
         -x.
      5. The point: x = 3.85 - 0.0625 = 3.7875, y = 5.2 - 0.2498 = 4.9502,
         z = 0.430. So **(3.7875, 4.9502, 0.430) m**.

      **3.** Pixel (0, 0) is 640 pixels left and 360 pixels up.

      1. Left: 640 / 640.5 = 0.9992 m toward world +y, so y = 5.2 + 0.9992 =
         6.1992.
      2. Up: 360 / 640.5 = 0.5621 m toward world +x, so x = 3.85 + 0.5621 =
         4.4121.
      3. The corner lands at (4.4121, 6.1992, 0.430) m.

      The view is about 2 × 0.9992 = 2.0 m wide (along world y) and
      2 × 0.5621 = 1.12 m tall (along world x). The shell moves at most
      0.1 m in y and 0.05 m in x from the point under the camera, well inside
      that.

      **4.** The slopes do not change; the height does.

      1. Sideways: 0.977 × 0.2498 = 0.2441 m, so y = 5.2 - 0.2441 = 4.9559.
      2. Forward: 0.977 × 0.0625 = 0.0610 m, so x = 3.85 - 0.0610 = 3.7890.
      3. Against the table point: 4.9559 - 4.9502 = 0.0057 m in y and
         3.7890 - 3.7875 = 0.0015 m in x. About 6 mm, against 2.3 mm for
         pixel (704, 360).

      The error is the 0.023 m height mistake times the slope, so it grows
      with the distance from the image center. Use the height of the face you
      grasp, not the table's.

      **5.** The changed script prints:

      .. code-block:: text

         K: fx = fy = 640.5, cx = 640, cy = 360
         optical (1, 2, 3) is link (3, -1, -2)
         pixel (704, 360) on the table: (3.8500, 5.1001, 0.430)
         pixel (800, 400) on the table: (3.7875, 4.9502, 0.430)
         pixel (0, 0) on the table: (4.4121, 6.1992, 0.430)
         pixel (800, 400) at z = 0.453: (3.7890, 4.9559, 0.453)
         check: world (3.85, 5.10, 0.43) -> pixel (704.1, 360.0)

      It matches Part B to the fourth decimal.

      **6.** In numbered steps:

      1. :math:`f_x` = (1920 / 2) / tan(1.57 / 2) = 960 / 0.9992 = 960.8
         pixels.
      2. One pixel on the table 1.0 m below: 1.0 / 960.8 m = 1.04 mm, against
         1.6 mm for 720p.
      3. 0.10 m out needs a slope of 0.10, so 0.10 × 960.8 = 96 pixels right
         of center: pixel (960 + 96, 540) = (1056, 540).

      The script's first and third lines then read:

      .. code-block:: text

         K: fx = fy = 960.8, cx = 960, cy = 540
         pixel (1056, 540) on the table: (3.8500, 5.1001, 0.430)

      The same table point as pixel (704, 360) of the 720p camera. The
      top-face line still uses pixel (704, 360) and can be ignored.


.. dropdown:: Exercise 3. Make the Lookups Succeed
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Tie each TF2 exception to its cause, and fix two of the three in
   ``tf_failures.py``.

   .. raw:: html

      <hr>

   **Part A. Which exception?**

   For each case, name the exception TF2 raises and what to do.

   1. Your node starts before the simulation and at once looks up
      ``agv1_slot1_frame`` in ``world``.
   2. Your camera node stamps each detection with the image time, and looks
      up ``world`` to ``top_camera_frame`` at that time. A moving frame on
      the path has not been sent for that time yet.
   3. Your configuration file attaches the camera to ``wrold`` (a typo).
      Every lookup from ``world`` to the camera fails, however long you
      wait.

   .. raw:: html

      <hr>

   **Part B. Change the script**

   4. In a copy of ``tf_failures.py``, fix the typo: publish
      ``top_camera_frame`` under ``"world"`` instead of ``"wrld"`` (two
      places: the ``sendTransform`` call and the ``can_transform`` wait). Run
      it. What does failure 3 print now?
   5. In another copy, ask failure 2 for the latest transform instead of
      ``later``: add ``from rclpy.time import Time`` and pass ``Time()`` as the
      last argument of that ``attempt`` call. What does it print?
   6. Failure 1 asks for ``agv9_frame``. How many AGVs does ARIAC 2025 have,
      and why can no wait fix this lookup?

   .. dropdown:: Solution
      :color: success

      **1.** ``LookupException``: the frame does not exist yet. Wait with a
      timeout instead of failing at once.

      **2.** ``ExtrapolationException``: the time asked for is newer than the
      newest transform. Ask for the latest transform (``Time()``) or wait
      briefly.

      **3.** ``ConnectivityException``: ``world`` and ``wrold`` are two
      different names, so the camera hangs in a second tree. Fix the name;
      draw the tree with ``ros2 run tf2_tools view_frames`` to see the two
      trees.

      **4.** Failure 3 prints ``found``. Failures 1 and 2 are unchanged:

      .. code-block:: text

         3. two trees that never connect
           found

      **5.** Failure 2 prints ``found``:

      .. code-block:: text

         2. a time newer than the newest transform
           found

      ``Time()`` means "the latest transform in the buffer", so TF2 never has
      to extrapolate. The cost: you get the transform at the time it was
      sent, not at your image's time.

      **6.** ARIAC 2025 has three AGVs, so no ``agv9_frame`` will ever exist.
      A wait with a timeout ends in the same ``LookupException``; the fix is
      the name.


.. dropdown:: Exercise 4. The RRT-Connect Toy, Run by Run
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Check the toy's shortest route by hand, then measure how much a sampling
   planner varies, and what a sample limit does to it.

   The lecture notes describe the toy but do not show its code. Parts B to D
   change ``rrt_connect_toy.py``: read the full script on the
   :doc:`code page <l10_code>` first.

   .. raw:: html

      <hr>

   **Part A. By hand**

   1. The shortest route is a taut string from the start (1.5, 1.5) around
      the wall corners (3, 7), (4, 7), (6, 3), (7, 3) to the goal (8.5, 8.5).
      Compute its length, segment by segment.

   .. raw:: html

      <hr>

   **Part B. More seeds**

   2. In a copy of ``rrt_connect_toy.py``, change ``range(1, 6)`` to
      ``range(1, 21)`` and run it. What are the shortest and longest paths,
      and how many runs needed more than 200 samples?

   .. raw:: html

      <hr>

   **Part C. A sample limit**

   3. Back to seeds 1 to 5. Set ``MAX_ITER`` to 200, so a run gives up after
      200 samples, the toy's version of a time limit. The script then crashes
      on a run with no path, because ``length(None)`` fails. Make the loop
      print ``no path`` and ``continue`` when ``path is None``. Before you
      run it, predict from the class table which seeds fail. Then run it.

   .. raw:: html

      <hr>

   **Part D. A longer step**

   4. Back to ``MAX_ITER = 5000``. Set ``STEP`` to 1.0 m and run seeds 1 to 5.
      Do the samples go down? Do the paths get shorter?

   .. dropdown:: Solution
      :color: success

      **1.** Five segments:

      1. (1.5, 1.5) to (3, 7): :math:`\sqrt{1.5^2 + 5.5^2} = \sqrt{2.25 +
         30.25} = \sqrt{32.5}` = 5.701 m.
      2. (3, 7) to (4, 7): 1.000 m.
      3. (4, 7) to (6, 3): :math:`\sqrt{2^2 + 4^2} = \sqrt{20}` = 4.472 m.
      4. (6, 3) to (7, 3): 1.000 m.
      5. (7, 3) to (8.5, 8.5): the same as segment 1, 5.701 m.

      Total: 5.701 + 1.000 + 4.472 + 1.000 + 5.701 = **17.874 m**, the
      17.87 m the script prints.

      **2.** The 20 runs:

      .. code-block:: text

         shortest route around the walls: 17.87 m
         seed  samples  start tree  goal tree  path length
            1      173          56         50      23.92 m
            2      385          91         95      24.64 m
            3      400         108         89      27.61 m
            4      141          30         54      22.51 m
            5      364         100         82      32.18 m
            6      210          59         62      27.62 m
            7      130          45         34      21.69 m
            8      263          62         89      25.62 m
            9      265          81         68      26.35 m
           10      240          70         54      24.73 m
           11      209          62         62      26.53 m
           12      371          96         98      26.80 m
           13      207          44         73      24.83 m
           14      152          52         51      22.81 m
           15      345          68         91      26.25 m
           16      259          73         82      26.65 m
           17      315          85         80      26.41 m
           18      368          79         96      25.41 m
           19      267          67         81      28.20 m
           20      352          87         85      24.70 m

      The shortest path is 21.69 m (seed 7) and the longest 32.18 m (seed 5),
      all above 17.87 m. Only 4 runs (seeds 1, 4, 7, 14, with 173, 141, 130
      and 152 samples) stayed at or under 200 samples; the other 16 needed
      more. Seeds 1 to 5 are the same as in class: a seed fixes the random
      numbers.

      **3.** Seeds 2, 3 and 5 needed 385, 400 and 364 samples in class, more
      than 200, so they fail. Seeds 1 and 4 needed 173 and 141, so they find
      the same paths as before. The changed loop:

      .. code-block:: python

         if path is None:
             print(f"{seed:4d}  {k:7d}  {len(ts):10d}  {len(tg):9d}  "
                   "  no path")
             continue

      prints:

      .. code-block:: text

         shortest route around the walls: 17.87 m
         seed  samples  start tree  goal tree  path length
            1      173          56         50      23.92 m
            2      200          50         51    no path
            3      200          48         37    no path
            4      141          30         54      22.51 m
            5      200          59         40    no path

      A path exists in every run, yet 3 of 5 fail. This is what the slide
      means by "a slow run becomes a failed run".

      **4.** With ``STEP = 1.0``:

      .. code-block:: text

         shortest route around the walls: 17.87 m
         seed  samples  start tree  goal tree  path length
            1      104          34         25      23.50 m
            2      239          57         60      29.25 m
            3      112          26         28      24.81 m
            4      113          18         37      24.18 m
            5      196          52         47      23.91 m

      The samples go down in every run (for example seed 3: 400 to 112).
      The paths do not all get shorter: seed 2 goes from 24.64 m to 29.25 m.
      The average over seeds 1 to 5 is (23.92 + 24.64 + 27.61 + 22.51 +
      32.18) / 5 = 26.17 m with a 0.5 m step, and (23.50 + 29.25 + 24.81 +
      24.18 + 23.91) / 5 = 25.13 m with a 1.0 m step. Five runs are too few to
      say that one step size gives shorter paths: the spread between seeds
      (22.51 m to 32.18 m) is larger than the change.


.. dropdown:: Exercise 5. The Conveyor, With More Runs
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict a cell's position from a speed history, find the latest moment
   the arm can start, and check both with ``conveyor_intercept.py``.

   .. raw:: html

      <hr>

   **Part A. By hand**

   Use the class numbers: the arm takes 1.5 s to reach the grasp, and it can
   reach from 0.00 m to 0.45 m past the beam (both chosen for the example).

   1. Run D: the belt runs at 0.1 m/s, stops 1.0 s after the beam fires, and
      starts again at 0.1 m/s at 3.0 s. The arm starts at 2.0 s. Where is the
      cell when the arm starts, and when it arrives? Can the arm take it?
   2. In run D, what would "current speed × elapsed time" give at the
      meeting time, and how far off is it?
   3. With the belt at 0.1 m/s the whole time, what is the latest time the
      arm can start and still meet the cell inside the reach?
   4. The feed is one cell every 10 s. Below what belt speed would two cells
      sit inside the 0.45 m reach at once?

   .. raw:: html

      <hr>

   **Part B. With the script**

   5. In a copy of ``conveyor_intercept.py``, add three runs before the
      ``feed_rate`` line:

      .. code-block:: python

         plan("D. belt stops at 1.0 s, restarts at 3.0 s",
              [(0.0, 0.1), (1.0, 0.0), (3.0, 0.1)], 2.0)
         plan("E. belt at 0.1 m/s, arm starts after 2.9 s",
              [(0.0, 0.1)], 2.9)
         plan("F. belt at 0.1 m/s, arm starts after 3.0 s",
              [(0.0, 0.1)], 3.0)

      Run it and compare with Part A.

   .. dropdown:: Solution
      :color: success

      **1.** Add the distance piece by piece.

      1. From 0 to 1.0 s: 0.1 × 1.0 = 0.10 m.
      2. From 1.0 to 2.0 s, stopped: 0 m. When the arm starts the cell is at
         0.10 m.
      3. From 2.0 to 3.0 s, still stopped: 0 m.
      4. From 3.0 to 3.5 s (the arm arrives at 2.0 + 1.5 = 3.5 s):
         0.1 × 0.5 = 0.05 m.
      5. At 3.5 s: 0.10 + 0.05 = **0.15 m**, inside the reach. The arm can
         take it.

      **2.** At 3.5 s the belt runs at 0.1 m/s again, so
      0.1 × 3.5 = 0.35 m. That is 0.35 - 0.15 = 0.20 m too far along the
      belt: the 2.0 s the belt stood still, at 0.1 m/s.

      **3.** The arm meets the cell 1.5 s after it starts. The cell must be at
      most 0.45 m out then, so the meeting time is at most 0.45 / 0.1 = 4.5 s
      after the beam, and the start at most 4.5 - 1.5 = **3.0 s**.

      **4.** The cells are (speed × 10 s) apart. Two fit inside 0.45 m when
      that gap is less than 0.45 m: speed × 10 < 0.45, so a speed below
      0.45 / 10 = **0.045 m/s**. At the class speed of 0.1 m/s they are
      1.0 m apart.

      **5.** The three new runs print:

      .. code-block:: text

         D. belt stops at 1.0 s, restarts at 3.0 s
           arm starts at t = 2.0 s, cell at 0.10 m
           arm meets it at t = 3.5 s, cell at 0.15 m
           in reach: move
         E. belt at 0.1 m/s, arm starts after 2.9 s
           arm starts at t = 2.9 s, cell at 0.29 m
           arm meets it at t = 4.4 s, cell at 0.44 m
           in reach: move
         F. belt at 0.1 m/s, arm starts after 3.0 s
           arm starts at t = 3.0 s, cell at 0.30 m
           arm meets it at t = 4.5 s, cell at 0.45 m
           in reach: move

      Run F starts at the latest time from Part A and lands exactly on the
      0.45 m edge. Run B in class started at 3.5 s, 0.5 s later, and was out
      of reach.


.. dropdown:: Exercise 6. Failure Results and a Tool Description
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Map what goes wrong in a cell to the skill failure results, decide what
   the caller does next, and write the tool description a GP4 agent needs.

   .. raw:: html

      <hr>

   **Part A. Which result?**

   For each case, name the failure result the skills package is planned to
   return. Where the L9 rule from the slides applies, say whether your code
   retries or replans.

   1. Your agent calls place on inspection robot 2, but its gripper is empty.
   2. AGV 1 is still at the assembly station when place is called.
   3. The TF2 lookup of ``agv1_slot3_frame`` fails.
   4. The gripper closes on a cell, and after the lift nothing is held.
   5. The trajectory controller stops the trajectory halfway.
   6. Inspection robot 2 waits for the voltage tester zone, and the lock is
      not free in time.
   7. Your tree cancels the goal because a high-priority order arrived.

   .. raw:: html

      <hr>

   **Part B. A tool description**

   8. Write the tool description your GP4 agent would get for the place skill:
      what it does, its preconditions, and each failure result it can return.
      Who moves the AGV if the precondition on its station fails?

   .. raw:: html

      <hr>

   **Part C. Why no hidden retries**

   9. Suppose (numbers chosen for this exercise) a skill retried a failed
      grasp 2 times by itself before reporting, and your tree also retries a
      failed pick 2 times. How many grasp attempts can one pick in your tree
      cause? Give two reasons, from the slides, why the skills package
      reports instead of retrying.

   .. dropdown:: Solution
      :color: success

      **1. Precondition failed** (nothing held). The slides' rule does not
      list this case. The plan assumed a held cell, so the world is not what
      the plan assumed, the reason the rule gives for replanning.

      **2. Precondition failed** (AGV at the wrong station). The L9 rule:
      replan. An agent that reads the reason can move the AGV and try again.

      **3. Place not found.** The L9 rule: replan.

      **4. Grasp failed.** The L9 rule: a candidate for one local retry.

      **5. Execution failed.** The slides give no rule for it; your tree or
      agent decides (L11 covers recovery).

      **6. Zone busy.** The skill is planned to leave every shared zone and
      report what it holds.

      **7. Canceled.** The skill is planned to stop the trajectory, retreat,
      release its zone locks, and return "canceled" with what it holds.

      **8.** One possible description:

      .. code-block:: text

         place_in_tray_slot(robot, agv, slot)
         Places the cell the robot holds into a tray slot of an AGV.
         Preconditions:
           - the robot holds a cell;
           - the AGV is at the inspection station (check /agvN/info).
         Failure results:
           - precondition failed: no cell held, or AGV at the wrong station;
           - place not found: the slot frame lookup failed;
           - no path found: both planners failed;
           - grasp failed: the cell was lost on the way;
           - execution failed: the controller stopped, or a stage timed out;
           - zone busy: a shared zone stayed locked too long;
           - canceled: the caller canceled the goal.
         Every result says what the robot holds.

      The name and arguments are made up for this exercise; the package's
      real action names will be on its documentation page. If the AGV is at
      the wrong station, your code moves it with ARIAC's own ``/agvN/move``
      action. Moving an AGV is not a skill.

      **9.** Each skill call makes 1 + 2 = 3 grasp attempts, and the tree
      calls the skill 1 + 2 = 3 times, so one pick can cause 3 × 3 = **9**
      grasp attempts, and the tree sees only 3 of them. The two reasons:

      - Retry and replan decisions belong to your tree and your agent (L7,
        L11).
      - A skill that retried quietly would hide ARIAC's challenges from your
        code, and your recovery logic would never be tested.
