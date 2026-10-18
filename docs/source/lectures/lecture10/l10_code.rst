====================================================
Code
====================================================

L10 has five short Python scripts. Three of them use ROS 2 and TF2, and two run
in plain Python. None needs ARIAC, Gazebo or MoveIt: the ROS 2 scripts publish
the same transforms ARIAC would. The two plain scripts compute with chosen
numbers (the RRT-Connect toy) or with the course skills package's own numbers
(the conveyor catch). The outputs below come from running them
with Python 3.12.3, NumPy 1.26.4 and ROS 2 Jazzy.

.. important::

   **The ROS 2 scripts stand in for ARIAC.** ``tf_agv_moves.py``,
   ``tf_failures.py`` and ``pixel_to_table.py`` send their own transforms with
   ARIAC's frame names and offsets, then look them up. Nothing moves in a
   simulator. ``rrt_connect_toy.py`` is a teaching toy, not MoveIt or OMPL.
   ``conveyor_intercept.py`` is a model of the course skill's conveyor catch,
   not the skill itself.

.. note::

   **What you need.**

   - ROS 2 Jazzy, with the Python packages ``rclpy``, ``tf2_ros``,
     ``geometry_msgs`` and ``sensor_msgs``, for the three ROS 2 scripts.
   - NumPy for ``pixel_to_table.py`` and ``rrt_connect_toy.py`` (on Ubuntu
     24.04: ``sudo apt install python3-numpy``).
   - ``conveyor_intercept.py`` needs only Python 3.

   Go to the folder that holds the scripts, and source ROS 2 once in that
   terminal:

   .. code-block:: bash

      cd lecture10/code
      source /opt/ros/jazzy/setup.bash

.. warning::

   The ROS 2 scripts publish ARIAC's own frame names (``world``,
   ``agv1_frame``). Do not run them while an ARIAC simulation runs on the same
   ROS domain, or their transforms mix with ARIAC's. Stop the simulation
   first, or give the terminal another domain before you run them, for
   example ``export ROS_DOMAIN_ID=42``.


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **Script**
     - **What it shows**
     - **Notes section**
   * - :download:`tf_agv_moves.py <code/tf_agv_moves.py>`
     - Slot 1 of AGV 1 in the world frame at two stations, and how far off a
       cached pose is.
     - :ref:`l10-tf2`
   * - :download:`tf_failures.py <code/tf_failures.py>`
     - The three TF2 lookup failures and the exception each one raises.
     - :ref:`l10-tf-failures`
   * - :download:`pixel_to_table.py <code/pixel_to_table.py>`
     - A camera pixel to a point on the assembly table, through the optical
       frame and TF2.
     - :ref:`l10-pixel-demo`
   * - :download:`rrt_connect_toy.py <code/rrt_connect_toy.py>`
     - RRT-Connect for a point in a flat square: five seeds, five paths.
     - :ref:`l10-planners`
   * - :download:`conveyor_intercept.py <code/conveyor_intercept.py>`
     - When the course skill catches a cell on the moving conveyor, and when
       it refuses, in four separate runs.
     - :ref:`l10-conveyor`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all five and writes their outputs to ``../outputs/``.
     - See the last section


The AGV Moves, the Slot Moves With It: ``tf_agv_moves.py``
----------------------------------------------------------

The script sends the two static transforms of AGV 1 (base to tray, tray to
slot 1) with the offsets from ARIAC's AGV model. Then it sends the moving
transform from ``world`` to ``agv1_frame`` twice: once at the inspection
station, once at the assembly station. After each, it looks up slot 1 in the
world frame at the time of that transform. Its docstring lists the ARIAC file
behind each number.

.. code-block:: bash

   python3 tf_agv_moves.py

.. literalinclude:: code/tf_agv_moves.py
   :language: python
   :caption: tf_agv_moves.py

Output:

.. literalinclude:: outputs/tf_agv_moves.txt
   :language: text

Exercise 1 on the :doc:`exercises page <l10_exercises>` adds a third station.


Three Lookups That Fail: ``tf_failures.py``
-------------------------------------------

The script publishes ``agv1_frame`` under ``world`` and ``top_camera_frame``
under ``wrld``, a typo on purpose. It waits until both are in the buffer, then
tries three lookups that fail, and prints each exception's class and message.

.. code-block:: bash

   python3 tf_failures.py

.. literalinclude:: code/tf_failures.py
   :language: python
   :caption: tf_failures.py

Output:

.. literalinclude:: outputs/tf_failures.txt
   :language: text

The two times in failure 2 are clock readings: your run prints other numbers,
5 s apart.


From a Pixel to the Table: ``pixel_to_table.py``
------------------------------------------------

The script builds the ``CameraInfo`` matrix :math:`K` of a 720p camera with a
1.57 rad field of view, with Gazebo's formula. It sends two static
transforms: the camera at (3.85, 5.2, 1.43) m looking straight down (chosen
for this example), and the optical frame under it. Then it checks the
optical-to-camera rule, turns two pixels into table points, repeats one pixel
at the height of the top shell's top face, and projects a table point back to
a pixel.

.. code-block:: bash

   python3 pixel_to_table.py

.. literalinclude:: code/pixel_to_table.py
   :language: python
   :caption: pixel_to_table.py

Output:

.. literalinclude:: outputs/pixel_to_table.txt
   :language: text

Exercise 2 on the :doc:`exercises page <l10_exercises>` changes the pixels and
the camera.


RRT-Connect in a Flat Square: ``rrt_connect_toy.py``
----------------------------------------------------

The script plans with seeds 1 to 5 and prints, for each, the number of samples
drawn, the size of each tree and the path length. It also prints the length
of the shortest route around the walls. It writes the trees and the path of
seed 1 to a JSON file, the data behind the figure in the notes. Give the file
name as the argument; without one it writes ``rrt_seed1.json`` in the current
folder.

.. code-block:: bash

   python3 rrt_connect_toy.py ../outputs/rrt_seed1.json

.. literalinclude:: code/rrt_connect_toy.py
   :language: python
   :caption: rrt_connect_toy.py

Output:

.. literalinclude:: outputs/rrt_connect.txt
   :language: text

The JSON file it writes: :download:`rrt_seed1.json <outputs/rrt_seed1.json>`.
Exercise 4 on the :doc:`exercises page <l10_exercises>` changes the seeds, the
step and the sample limit.


The Moving Conveyor: ``conveyor_intercept.py``
----------------------------------------------

The script models ``pick_from_conveyor`` from the course skills package,
v0.2.0. ``plan_catch()`` follows the skill's ``conveyor.py``: it predicts when
the cell reaches the fixed catch point, or refuses before any motion.
``wait()`` follows the skill's ``_belt_change``: a belt that stops or changes
speed while the arm waits ends the goal. The numbers (beam at x = 0.60 m,
catch point at x = 1.40 m, ``side_lead_time``, ``close_delay``,
``max_trigger_age``) come from the package's ``team_config.yaml`` and
``skills.yaml``; the docstring gives the file and line of each. Each run
gives the belt's speed history as a list of (start time, speed) pairs and the
time the goal is sent, both chosen for this example. The script plays four
separate runs, each with one cell.

.. code-block:: bash

   python3 conveyor_intercept.py

.. literalinclude:: code/conveyor_intercept.py
   :language: python
   :caption: conveyor_intercept.py

Output:

.. literalinclude:: outputs/conveyor_intercept.txt
   :language: text

Exercise 5 on the :doc:`exercises page <l10_exercises>` adds runs.


Running All Five: ``run_all.sh``
--------------------------------

``run_all.sh`` is the script that produced the outputs above. It runs each
example in a clean environment (``env -i``) and on its own ROS domain, so a
simulation running on the same machine does not see its transforms. It
writes the Python, NumPy and ROS 2 versions to ``../outputs/versions.txt``.
You do not need it: the commands in the sections above give the same results,
apart from the clock readings in ``tf_failures.py``.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

Versions used for the outputs on this page:

.. literalinclude:: outputs/versions.txt
   :language: text
