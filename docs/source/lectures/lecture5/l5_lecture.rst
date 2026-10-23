====================================================
Lecture
====================================================

.. note::

   These notes follow the L5 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from the scripts on the :doc:`code page <l5_code>`, run on
   2026-10-12 (``precision_recall.py`` and ``timing.py`` on 2026-10-18) with
   Python 3.12.3, NumPy 1.26.4 and PyYAML 6.0.1 under ROS 2 Jazzy.

.. warning::

   **Every point cloud in these notes is synthetic.** The cells, their
   defects, the lidars and the noise are made in NumPy by ``synth.py``. No
   point comes from ARIAC or Gazebo. The voltage readings are synthetic too.
   The one measurement taken from ARIAC itself is the depth of the training
   defects, read from ARIAC's mesh files by ``mesh_depths.py``.

.. admonition:: Class logistics for this week
   :class: warning

   - **Quiz 2** (on L4) opens the class.
   - **GP1 is due today.**
   - **GP2 (Cell Inspection) is posted today** and uses everything in this
     lecture.


.. _l5-recap:

Recap
-----

**From L4.**

- A behavior tree runs the executive layer: composites, decorators, and a
  blackboard of named keys.
- Your GP1 tree submits an inspection report for every cell, and every report
  says the cell passed.

**Today's question.** How does the system find out that a cell is defective,
and how sure can it be?


.. _l5-sensors:

The ARIAC Sensors and the Budget
--------------------------------

This section covers what each team may place in the factory, what it costs,
and where a lidar may go.

What Perception Gives the Rest of the System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: perception
   :class: note

   **Perception** turns sensor data into facts the system can use: "this cell
   has a dent at :math:`\theta` = 0.3 rad, :math:`z` = 14 mm" (an angle
   around the cell and a height on it, both defined in
   :ref:`l5-defects`).

- Those facts update the world model (L3). The behavior tree reads them from
  its blackboard (L4).
- **What ARIAC does not tell you.** ARIAC 2025 publishes no pose topics and no
  TF frames for cells or shells. A team learns where things are, and whether
  a cell is good, only from the sensors it places.

Each team declares its sensors in its **team configuration file**. ARIAC
checks the file at startup and does not start with a sensor it does not
allow.

Declaring a Lidar in the Team Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **lidar** measures the distance along each ray of a grid of angles. Each ray
that hits something within its range gives one 3D point. This is
the example lidar from the ARIAC documentation (``config_files.rst``):

.. code-block:: yaml

   # Lidar sensor example (must be within bounding boxes)
   - NAME: "inspection_lidar"
     TYPE: "lidar"
     POSE:
       XYZ: [0.8, 0.825, 0.52]  # Within Box A limits
       RPY: [0, 0, 0]
     UPDATE_RATE: 20
     HORIZONTAL:
       SAMPLES: 50
       MIN_ANGLE: -1.57
       MAX_ANGLE: 1.57
     VERTICAL:
       SAMPLES: 8
       MIN_ANGLE: -0.5
       MAX_ANGLE: 0.5

**Fields every sensor has.**

- ``NAME``, ``TYPE``: break_beam, distance, camera or lidar.
- ``POSE``: position ``XYZ`` (m) and orientation ``RPY`` (rad) in the world
  frame.
- ``UPDATE_RATE``: lidar 10 or 20 Hz; camera 30 Hz; break beam and distance
  10 or 30 Hz (``ariac_setup/yaml_validation.py``). ARIAC does not start
  with any other rate.

**A lidar adds** :math:`H` horizontal and :math:`V` vertical samples, each
with a minimum and a maximum angle (rad). This lidar has
:math:`H \times V` = 50 × 8 = 400 samples.

Sensor Grades and Costs
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: ARIAC 2025 sensor grades (Sensors page)
   :header-rows: 1
   :widths: 18 10 52 20
   :class: compact-table

   * - **Sensor**
     - **Grade**
     - **What the grade means**
     - **Cost**
   * - Break beam
     - A, B
     - 30 Hz; 10 Hz. Reports only whether the beam is blocked.
     - $400; $200
   * - Distance
     - A, B
     - 30 Hz; 10 Hz. Distance to the nearest object.
     - $600; $300
   * - RGB camera
     - A, B
     - 1080p; 720p; both 30 Hz, field of view 0 to :math:`\pi` rad
     - $800; $500
   * - Lidar
     - A
     - 20 Hz, :math:`H \times V \leq 400`
     - $1500
   * - Lidar
     - B
     - 10 Hz, :math:`200 < H \times V \leq 400`
     - $1250
   * - Lidar
     - C
     - 10 Hz, :math:`H \times V \leq 200`
     - $1000

.. warning::

   The code that bills a lidar (``Lidar.grade`` in
   ``ariac_setup/structures.py``) differs from the Sensors page at one edge:
   at 10 Hz it grades by samples alone and bills exactly 200 samples as
   grade B. For grade C, use at most 199 samples. At 20 Hz it bills grade A.
   More than 400 samples is refused.

.. _l5-boxes:

Where a Lidar May Go
~~~~~~~~~~~~~~~~~~~~

ARIAC allows a lidar only inside three boxes around the inspection conveyor.
The figure is a top view, drawn to scale.

.. image:: /_static/images/l5/lidar_boxes.svg
   :alt: Top view of the inspection conveyor, drawn to scale, x to the right
         from 0.45 to 1.55 m and y up from 0.65 to 1.35 m. The gray belt runs
         from x 0.5 to 1.5 m between y 0.95 and 1.05 m. Tag 1: box A, a green
         box from x 0.5 to 1.1 m and y 0.7 to 0.95 m, below the belt. Tag 2:
         box B, the same size above the belt, y 1.05 to 1.3 m. Tag 3: box C, a
         dashed green outline over the belt itself from x 0.5 to 1.1 m. Tag 4:
         a small circle, the cell at its spawn point, x 0.55 m. Tags 5 and 6:
         dashed lines across the belt at x 1.0 m and x 1.25 m. Tag 7: an arrow
         pointing along +x. Tag 8: two green triangles at x 0.65 m, one in box
         A at y 0.9 m and one in box B at y 1.1 m, each pointing at the belt.
   :width: 90%
   :align: center

1. Box A: :math:`z` 0.42 to 0.62 m.
2. Box B: :math:`z` 0.42 to 0.62 m.
3. Box C, over the belt: :math:`z` 0.52 to 0.62 m.
4. A cell spawns at :math:`x` = 0.55 m.
5. The door opens at :math:`x` = 1.0 m.
6. The door closes after :math:`x` = 1.25 m.
7. Cells travel along :math:`+x`.
8. Today's two demo lidars, at :math:`z` = 0.457 m.

- Sources: the Sensors page (boxes); ``cell_feed_plugin.hpp`` and
  ``physical_inspection_plugin.hpp`` (spawn, door).
- The lidar's range is 0.04 to 0.2 m (``lidar/model.sdf``), and the team
  configuration file cannot change it: aim within 20 cm of the cell.

Which Sensor Each Part of the Course Needs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 60 22
   :class: compact-table

   * - **Sensor**
     - **What it is for**
     - **Where**
   * - Lidar
     - Cell inspection. ARIAC requires lidar point clouds for it (Scenario
       page, Step 1a).
     - GP2
   * - Break beam
     - Tells the skills package's conveyor pick when a cell passes, so
       ``inspection_robot_1`` can catch it.
     - GP1 on
   * - RGB camera
     - Finds the Task 2 top shell, which spawns at a random pose (Step 2c).
       The VLM and the embodied-reasoning model read camera images.
     - L9, L10, final demo

**Why cameras do not inspect the cells here.**

- ARIAC requires lidar for inspection, and an RGB image measures no depth.
- Whether a 2 mm defect shows in a Gazebo camera image has not been
  measured. The final demo tests it: Gemini Robotics ER judges defects from
  camera images and is scored against your GP2 lidar detector on the same
  cells.

The $9600 Budget and the Sensor Cost Bonus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The cost is the total, in dollars, of every sensor in your team configuration
file, each billed at its grade's cost (Sensor Grades and Costs, above). The
budget is $9600 (``SENSOR_BUDGET`` in ``ariac_db/config/scoring_weights.yaml``),
and the 1000 below is ``W6`` in the same file; ``ariac_db/scoring.py`` applies
both.

- Under the $9600 budget: a **sensor cost bonus** of
  1000 × (1 − cost / 9600) points, only if the team submitted every kit,
  module and high-priority order the trial asked for.
- Over the budget: a penalty of 1000 × (cost / 9600 − 1) points instead,
  which is 1000 / 9600 = 0.104 points per dollar over.

:doc:`Exercise 2 <l5_exercises>` works a full trade-off between a grade A
and a grade C sensor layout, the bonus points each earns, and what the
cheaper layout gives up.


.. _l5-pointclouds:

Point Clouds in ROS 2
---------------------

This section covers what a lidar publishes, how to read it into NumPy, and how
to move it into the world frame. Every point here is synthetic: made in NumPy
by ``synth.py``, not by ARIAC (Python 3.12.3, NumPy 1.26.4, ROS 2 Jazzy).

What an ARIAC Lidar Publishes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Topic and frame:**

- Message ``sensor_msgs/PointCloud2`` on ``/{lidar_name}/scan``, with
  ``frame_id`` ``{lidar_name}_frame`` (``ray_sensor_plugin.cpp``).
- ARIAC publishes that frame as a static transform from ``world``
  (``tf_publisher_plugin.cpp``), so one TF2 lookup is enough.

.. admonition:: Definition: point cloud and PointCloud2
   :class: note

   A **point cloud** is a set of 3D points, here one per lidar ray that hit
   something. ROS 2 sends it as a ``PointCloud2`` message: **packed bytes plus
   their layout**.

   - ``header``: time stamp and frame.
   - ``height``, ``width``: the cloud's shape (height 1 for an unordered
     cloud).
   - ``fields``: each field's name (x, y, z, ...), byte offset and data type.
   - ``point_step``, ``row_step``: bytes per point and per row. ``data``: the
     raw bytes.

.. _l5-roundtrip:

Demo: Build a Cloud, Then Read It Back
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pc2_roundtrip.py`` builds a ``PointCloud2`` from one synthetic scan of lidar
A, then reads it back into an :math:`N \times 3` NumPy array:

.. literalinclude:: code/pc2_roundtrip.py
   :language: python
   :lines: 20-21, 30-32
   :caption: pc2_roundtrip.py (excerpt)

.. literalinclude:: outputs/pc2_roundtrip.txt
   :language: text
   :lines: 1-6

- 400 points of 3 four-byte floats: 400 × 12 = 4800 bytes. Row 0 was set to
  NaN by hand; 136 rays hit nothing and are ``inf`` in this synthetic scan.
- ``skip_nans=True`` dropped the NaN row only. ``np.isfinite`` removes the
  rest.

Demo: Move Every Point to the World Frame at Once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/pc2_roundtrip.py
   :language: python
   :lines: 47-48, 56-57
   :caption: pc2_roundtrip.py (excerpt)

.. literalinclude:: outputs/pc2_roundtrip.txt
   :language: text
   :lines: 7-9

- Target frame ``world``, source frame ``lidar_a_frame``: the result maps
  lidar points into the world. The rotation part of the 4 × 4 matrix ``m``
  comes from the quaternion (lines 49 to 55 of the script, shown in full on
  the :doc:`code page <l5_code>`). Appending a 1 to each point lets one
  matrix product apply the rotation and the translation together.
- The demo's static transform is a stand-in for ARIAC's. The first point lands
  at :math:`z` = 0.422 m: the belt.
- Measured by ``timing.py`` (see :doc:`the code page <l5_code>`) on the
  instructor's PC (Intel Core i9-14900HX), with 400 points, the best of 3
  runs of 200, repeated 5 times: a loop with one NumPy product per point,
  ``m @ [x, y, z, 1.0]``, took 0.78 to 0.91 ms per scan; the one product
  above took 0.012 to 0.013 ms. A loop in plain Python floats took
  0.096 ms: most of the cost is calling NumPy once per point.

QoS, Node Layout and Latency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**QoS** (quality of service, the delivery settings a publisher and a
subscriber must agree on):

- The lidar publishes with the default reliable QoS, depth 10. The break beam
  publishes best effort (``SensorDataQoS``).
- L1 showed a default subscriber to a best-effort publisher receiving 0 of 20
  messages: match each publisher.

**Node layout:**

- The subscriber callback only converts and stores points.
- A timer in its own callback group, under a ``MultiThreadedExecutor``,
  analyzes a cell once all its scans are in (L1: 11 of 50 status reads on one
  thread, 50 of 50 with two groups).

**Latency:** log the simulation time from a scan's header stamp to the
report. The inspection speed bonus depends on it.


.. _l5-geometry:

Lidar Geometry
--------------

This section covers how many points land on a cell, and how to aim the
samples you pay for.

Spacing Between Points: Angular Step Times Distance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l5/point_spacing.svg
   :alt: Top view, to scale. A green triangle on the left (tag 1), the lidar,
         points right at a gray circle 0.1 m away (tag 5), the cell. Seven
         rays fan out from the lidar, 0.064 rad apart; three of them end on
         the near side of the cell with a black dot, the others pass by as
         dashed lines. Tag 2 marks a small arc between two neighboring rays:
         the angular step. Tag 3 marks a short line with end ticks between two
         neighboring dots: the spacing on the cell, about 6 mm. Tag 4 marks a
         two-headed arrow from the lidar to the cell's axis: the distance.
   :width: 90%
   :align: center

Top view, to scale. 1: lidar. 2: angular step :math:`\Delta`. 3: spacing
:math:`s`. 4: distance :math:`D` to the cell's axis. 5: cell.

**Symbols.**

- :math:`N`: samples in one direction; :math:`a_{\min}`, :math:`a_{\max}`:
  the scan's angle limits (rad).
- **Angular step**: :math:`\Delta = (a_{\max} - a_{\min}) / (N - 1)`, the
  angle between neighboring rays. There are :math:`N - 1` gaps between
  :math:`N` rays.
- :math:`D`: distance from the lidar to the cell's axis.
- **Spacing** on the cell: :math:`s \approx \Delta \times D`.

**The cell.** A cylinder of radius 10.5 mm and length 70 mm
(``battery_cell/model.sdf``), standing upright on the belt.

.. _l5-spacing-example:

Worked Example: The Docs' Lidar and a Narrow Scan, 0.1 m from the Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The distance :math:`D` = 0.1 m is chosen for this example.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Docs' example: H 50 over ±1.57, V 8 over ±0.5
      :class-header: bg-primary text-white

      1. Steps: 3.14 / 49 = 0.064 rad across; 1.0 / 7 = 0.143 rad up.
      2. At :math:`D` = 0.1 m: 0.064 × 100 mm = 6.4 mm and
         0.143 × 100 mm = 14.3 mm apart.
      3. The cell spans about 2 × atan(10.5 / 100) = 0.21 rad across and
         2 × atan(35 / 100) = 0.67 rad up.
      4. 0.21 / 0.064 = 3.3 columns and 0.67 / 0.143 = 4.7 rows: about 12
         to 20 points (3 or 4 columns times 4 or 5 rows). Most of the 400
         samples miss the cell.

   .. grid-item-card:: Narrow scan: H 20 over 0.3 rad, V 20 over 0.8 rad
      :class-header: bg-warning

      1. Still 400 samples, so still grade A at 20 Hz.
      2. Steps: 0.3 / 19 = 0.016 rad and 0.8 / 19 = 0.042 rad.
      3. At 0.1 m: 1.6 mm and 4.2 mm apart.

.. important::

   Under a fixed sample limit, the angle range is the main design choice. Aim
   the samples at the cell, not at the room.

.. _l5-point-count:

Demo: Counting the Rays That Hit a Synthetic Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``point_count.py`` casts every ray of one scan at a perfect synthetic
cylinder, with the cell's axis 0.1 m in front of the lidar:

.. literalinclude:: outputs/point_count.txt
   :language: text
   :lines: 1-4

1. The docs' lidar: 20 points, the top of the 12 to 20 estimate. The near side
   of the cell is 100 − 10.5 = 89.5 mm away, not 100 mm, so the cell spans a
   little more than the estimate assumed.
2. The narrow scan puts 240 of its 400 samples on the cell instead of 20.
3. A third layout, :math:`H` 10 by :math:`V` 40 (chosen for this example),
   puts 212 on the cell with a vertical step of 0.021 rad: 2.1 mm at 0.1 m,
   half the narrow scan's 4.2 mm.

.. note::

   Each count comes from casting rays at a perfect synthetic cylinder. None is
   a measurement in Gazebo.

The Moving Belt Fills In the Horizontal Direction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Between two scans the cell moves** :math:`v / f`, where :math:`v` is the
belt speed (set in the team configuration, at most 0.1 m/s) and :math:`f` is
the scan rate.

- 0.1 / 20 = 0.005 m = 5 mm at 20 Hz; 0.1 / 10 = 0.01 m = 10 mm at 10 Hz.
- Each scan sees the cell from a slightly different angle, so stacking the
  scans fills in the surface across. Nothing fills in the vertical direction:
  spend samples there.

A whole pass at 0.1 m/s and 20 Hz, from the two demo lidars (tag 8 in the box
figure), counted by ``point_count.py``:

.. literalinclude:: outputs/point_count.txt
   :language: text
   :lines: 5-7

- Each cell spawns turned by a random angle from :math:`-\pi` to :math:`\pi`
  (``cell_feed_plugin.cpp``), so a defect can face any way.
- One lidar at :math:`D` = 0.1 m sees at most
  2 × acos(10.5 / 100) = 2.93 rad of the 6.28 rad around the cell: less than
  half.


.. _l5-defects:

From Points to Defects
----------------------

This section builds a cylinder-fit detector in eight steps and runs it on
synthetic cells with defects of known size.

Dents, Scratches and Bulges, and Where a Defect Is
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l5/cell_theta_z.svg
   :alt: Two views of one cell with three defects. Left, a top view with x to
         the right, y up and z out of the page: the cell's outline is a gray
         circle with a blue notch at tag 1 (a dent, about -1.0 rad, below and
         right of center), a narrower blue notch at tag 2 (a scratch, about
         1.3 rad, upper side) and a red bump at tag 3 (a bulge, about -2.3
         rad, lower left). Tag 4 marks an arc from the +x axis clockwise to
         the dent's direction: theta, negative here. Tag 6 marks the +x axis,
         the direction of travel. Right, a side view from -y with x to the
         right and z up: a gray rectangle on a gray belt. The dent (tag 1) is
         a blue oval low on the right, the bulge (tag 3) a red oval high on
         the left, and the scratch (tag 2), on the far side, a dashed blue
         outline in the middle. Tag 5 marks an arrow from the cell's base up
         to the dent's center: z.
   :width: 90%
   :align: center

Left: top view (:math:`z` out of the page). Right: side view from
:math:`-y` (dashed: on the far side). 1: dent. 2: scratch. 3: bulge.
4: :math:`\theta` of the dent. 5: :math:`z` of the dent. 6: :math:`+x`, the
direction of travel.

.. admonition:: Definition: the three defect types (Scenario page)
   :class: note

   - **Dent**: a roughly round area set in from the cylinder.
   - **Scratch**: a long, narrow area set in, usually along the cell.
   - **Bulge**: a roughly round area sticking out.

**Location:**

- :math:`\theta`: angle of the defect's center around the cell
  (``CellDefect.msg``). ARIAC checks it against the ``defects.yaml`` angle
  plus the cell's spawn yaw (``physical_inspection_plugin.cpp``), so 0 is
  along :math:`+x`, the direction of travel, and positive is
  counterclockwise seen from above.
- :math:`z`: height of the defect's center above the cell's base.

The Detector in Eight Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l5/detect_pipeline.svg
   :alt: A block diagram in two rows. Row 1: a green box for the scans in the
         world frame, then boxes tagged 1 Crop, 2 Separate cells, 3 Undo
         motion and 4 Fit the axis, joined by arrows. An arrow runs from box 4
         down and back to the start of row 2. Row 2: boxes tagged 5 Residual
         d, 6 Threshold, 7 Cluster and 8 Classify, then a gray box for the
         report.
   :width: 100%
   :align: center

Tag :math:`n` is step :math:`n`. Input: the scans of every lidar, already in
the world frame (TF2). Output: the inspection report.

- Steps 1 to 4 find the cell and its axis. Steps 5 to 8 find what differs
  from a perfect cylinder.
- The code: ``detector.py`` (see :doc:`the code page <l5_code>`), one
  function each for steps 1, 3, 4, 5, 7 and 8. Step 6 is one line in
  ``detect()``. Step 2 is not coded: each demo run has one cell.

Steps 1 to 3: Crop, Separate, Undo the Motion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Crop.** Keep the points over the belt and above its surface. The belt
   surface is at :math:`z` = 0.422 m (the cell spawn height in
   ``cell_feed_plugin.hpp``); check it once in RViz. The demo keeps 2 mm to
   66 mm above the belt: the top of ARIAC's cell mesh narrows above about
   68 mm (read from ``base.glb``), and those points would look like a dent.
2. **Separate cells.** With the docs' example settings (0.1 cells/s,
   0.1 m/s) a cell arrives every 1 / 0.1 = 10 s, so cells are
   0.1 × 10 = 1.0 m apart.
3. **Undo the motion.** Read the belt speed :math:`v` from
   ``/inspection_conveyor/status``. Shift each scan's points by
   :math:`-v (t - t_0)` along :math:`x`, so every scan lines up with the
   cell's position at the first scan's time :math:`t_0`. During a conveyor
   malfunction the status shows speed 0.

.. literalinclude:: code/detector.py
   :language: python
   :lines: 21-26
   :caption: detector.py (excerpt)

Steps 4 and 5: Fit the Axis, Then Measure Each Point Against It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. **Fit the axis.** The cell stands upright, so fit a circle to the
   :math:`x` and :math:`y` of its points (least squares). Its center
   (:math:`x_0`, :math:`y_0`) is the axis. Compare the fitted radius with
   10.5 mm as a check.
5. **Residual.** For each point, :math:`d` = (distance from the axis) −
   :math:`R`, with :math:`R` = 10.5 mm. Negative :math:`d`: the surface is set
   in (dent or scratch). Positive :math:`d`: it sticks out (bulge).

.. admonition:: Definition: residual
   :class: note

   A point's **residual** :math:`d` is how far it lies from the perfect
   cylinder: its distance from the fitted axis minus the cell's radius
   :math:`R`. On a perfect cell with no noise, every :math:`d` is 0.

.. literalinclude:: code/detector.py
   :language: python
   :lines: 29-39
   :caption: detector.py (excerpt)

- A circle is :math:`x^2 + y^2 = a x + b y + c`, which is linear in
  :math:`a`, :math:`b`, :math:`c`: one least-squares solve. The center is
  (:math:`a/2`, :math:`b/2`), and the radius is
  :math:`\sqrt{c + x_0^2 + y_0^2}`.
- The demo fits twice, the second time without the points that look
  defective, so a defect does not pull the axis toward itself.

Steps 6 to 8: Threshold, Cluster, Classify
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6. **Threshold.** Flag points with :math:`|d|` above a threshold. Set it from
   the spread of :math:`d` measured on good cells, not by guessing.
7. **Cluster.** Group flagged points that lie close together (the demo:
   within 3 mm, at least 3 points). Set-in and sticking-out points never share
   a cluster. A lone noisy point is not a defect.
8. **Classify.** Sticking out: bulge. Set in and roughly round: dent. Set in
   and long and narrow: scratch. The demo calls a cluster long when its spread
   in one direction is more than 2.5 times its spread in the other.

**Location of each cluster.**

- :math:`\theta`: each point's angle is atan2(:math:`y - y_0`,
  :math:`x - x_0`), 0 along :math:`+x`, counterclockwise positive. The demo
  averages these angles as directions (the mean of unit vectors), so −3.1
  and +3.1 rad average to :math:`\pi`, not 0.
- :math:`z` = the cluster's mean height above the belt surface, which is the
  cell's base.
- ARIAC's training set also has horizontal and diagonal scratches
  (``defects.yaml``): measure length and width in any direction.

.. _l5-mesh-depths:

Measured: How Deep ARIAC's Training Defects Are
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``mesh_depths.py`` reads ARIAC's li-ion cell meshes and ``defects.yaml`` from
the ARIAC 2025 source (branch ``ariac2025``). For each defect it finds the
deepest mesh point near the listed :math:`\theta` and :math:`z`, measured from
the 10.5 mm cylinder (negative: set in). This is the one measurement in the
lecture taken from ARIAC's own files.

.. literalinclude:: outputs/mesh_depths.txt
   :language: text

- "ty": the defect type number in ``defects.yaml``. Types 4 and 7 to 10 have
  two defects on one cell.
- "yaml": :math:`\theta` in ``defects.yaml``. "mesh": where the defect sits
  in the mesh (rad). "depth": mm.

What the Mesh Measurement Means for Your Detector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Depth.**

1. The ARIAC Scenario page says: "All defects will be at least 2mm removed
   from the normal cell surface at their furthest point, ensuring they are
   detectable using LIDAR point cloud analysis."
2. In these meshes, the deepest points run from 0.84 mm to 2.49 mm, and 10 of
   15 are under 2 mm.

.. warning::

   Your threshold must sit below the shallowest defect you want to catch, so
   a threshold just under 2 mm would miss most of these. Check one cell of
   each type in simulation.

**Angle.**

- The mesh :math:`\theta` matches ``defects.yaml`` within 0.18 rad (the
  largest gap in the table: type 8's scratch, +0.064 against −0.112), so
  ``defects.yaml`` measures :math:`\theta` from the mesh's :math:`x` axis.
  ARIAC adds the spawn rotation to get the true :math:`\theta`.
- The docs say these shapes are for training and will change for the
  competition. A detector that measures distance from a fitted cylinder
  carries over to new shapes better than one tuned to these ten meshes.

.. _l5-demo-setup:

Demo Setup: What Is Synthetic, and Setting the Threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Made up in NumPy** (``synth.py``):

- **Cell:** radius 10.5 mm, length 70 mm (ARIAC's ``model.sdf``); a perfect
  cylinder plus the defects.
- **Lidars:** the two of tag 8 on the box figure, 0.1 m from the axis,
  :math:`H` 10 by :math:`V` 40, 20 Hz; belt at 0.1 m/s.
- **Noise:** 0.2 mm along each ray, chosen for this example. ARIAC's
  ``lidar/model.sdf`` sets no noise, so in simulation the spread comes from
  the meshes and from your motion correction.
- **Defects:** dent and bulge of radius 4 mm, scratch 4 mm wide and 28 mm
  long, all chosen for this example; depths chosen per run.

**Step 6 on 20 good cells** (``calibrate.py``):

.. literalinclude:: outputs/calibrate.txt
   :language: text

The rule: threshold = the largest :math:`|d|` on any good cell, rounded up to
the next 0.1 mm. For two lidars, 0.79 mm rounds up to 0.8 mm; for four, 0.81
mm rounds up to 0.9 mm. The four-lidar layout comes later in the lecture.

.. _l5-detect-one:

Demo: One Synthetic Cell with a Dent, a Scratch and a Bulge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``detect_one.py`` runs steps 1 to 8 on one synthetic cell and prints what it
finds next to the truth:

.. literalinclude:: outputs/detect_one.txt
   :language: text

- Each defect is 2 mm deep at its deepest point. The cell has three defects
  so one run shows all three types; ARIAC's training cells have one or two.
- "match" uses ARIAC's rule: same type, :math:`z` within 5 mm,
  :math:`\theta` within 0.26 rad. All three match.
- 13508 points in: belt and cell over 61 scan times from each lidar (0 to 3 s
  after spawn at 20 Hz: 3 × 20 + 1 = 61).

The Same Cell, Unrolled: :math:`d` at Every Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l5/residual_map.svg
   :alt: A scatter plot of the points of one synthetic cell, with theta in
         radians from -3.14 to 3.14 across and z in millimeters from 0 to 70
         up. Most points are small and gray. They fill two bands, theta from
         about -3 to -0.1 and from about 0.1 to 3; near theta 0 (tag 4) and
         near plus or minus 3.14 there are almost no points. Tag 1 marks a
         small cluster of blue points at theta -1.0, z 18 mm (the dent). Tag
         2 marks a tall, narrow blue cluster at theta 1.3, z 24 to 52 mm (the
         scratch). Tag 3 marks a small cluster of red points at theta -2.3, z
         50 mm (the bulge).
   :width: 100%
   :align: center

Data: ``outputs/residuals.csv``. Gray: :math:`|d| \leq` 0.9 mm. Blue:
:math:`d < -0.9` mm. Red: :math:`d >` 0.9 mm. 1: dent. 2: scratch. 3: bulge.
4: :math:`\theta` = 0.

- **This is not a picture of space.** It is the cell's side cut open and laid
  flat: across is the angle :math:`\theta`, up is the height :math:`z`.
- Lidar A fills the left band, lidar B the right band.
- Near :math:`\theta` = 0 and :math:`\pm\pi`, the front and back of the cell,
  each lidar sees the surface edge-on, and almost no points land.


.. _l5-report:

The Inspection Report and the Door
----------------------------------

This section covers what a report holds, which cell it lands on, and the two
bonuses it earns.

The Report and How ARIAC Matches It to a Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**InspectionReport.msg and CellDefect.msg.**

- ``passed``: true for a good cell, false for a defective one.
- ``defects``: a list of ``CellDefect``, each with ``defect_type``
  (DENT = 1, BULGE = 2, SCRATCH = 3), ``theta`` and ``z``.
- Service ``/inspection_conveyor/inspection/submit``
  (``SubmitInspectionReport``): the request holds a timestamp and the report.
  Classifying is optional: ``passed = false`` alone rejects the cell.

**Matching and the door** (``physical_inspection_plugin.cpp``).

- A report goes to the cell nearest the door, upstream of :math:`x` = 1.0 m
  (plus a 5 mm margin), that has no report yet. Submit after the cell leaves
  your lidars and before :math:`x` = 1.0 m: a late report lands on the next
  cell.
- After a passing report, the door opens at :math:`x` = 1.0 m and closes
  after :math:`x` = 1.25 m. A failing or missing report keeps the door
  closed, and the cell drops into the inspection bin. A good cell there
  costs 50 points.

.. _l5-bonuses:

The Two Bonuses a Report Earns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every ARIAC bonus counts only if the team submitted every kit, module and
high-priority order the trial asked for. Otherwise ARIAC sets each bonus to
0 (``ariac_db/scoring.py``; ``competition_manager_plugin.cpp`` marks such a
run as aborted).

**Inspection speed: 500 × (1 − g / 4 s).**

- :math:`g`: the average time from a cell's spawn to its report. :math:`g` of
  4 s or more gives 0.
- The demo's two lidars last see the cell at :math:`t` = 1.25 s
  (``detect_one.py``). A report right then would give
  500 × (1 − 1.25 / 4) = 343.75 points, before your processing time.

**Inspection classification: 500 × (correct / defective cells).**

- A cell counts only if the report has the right number of defects, and each
  matches in type, in :math:`z` within 5 mm, and in :math:`\theta` within
  0.26 rad, about 15 degrees.
- The true :math:`\theta` is the defect's :math:`\theta` in ``defects.yaml``
  plus the cell's spawn rotation.

.. warning::

   As written, the :math:`\theta` check in ``physical_inspection_plugin.cpp``
   applies ``abs()`` to the comparison, not to the angle difference, so it
   also accepts some reports far off in one direction. Aim for 0.26 rad
   either way.


.. _l5-voltage:

Voltage Readings
----------------

This section covers the second check on each cell, made later at a voltage
tester (Scenario page, Step 1c).

What a Tester Publishes, and Why One Reading Is Not Enough
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The facts.**

- Each tester publishes ``VoltageReading`` (``voltage``,
  ``operation_status``) on ``/voltage_tester_1/voltage`` and
  ``/voltage_tester_2/voltage``.
- A Li-Ion cell is in range from 3.6 − 0.2 = 3.4 V to 3.6 + 0.2 = 3.8 V
  (``CellTypes.msg``). For Ni-MH the nominal voltage is 1.2 V.
- Each reading has normal noise with standard deviation :math:`\sigma` =
  0.05 V (``voltage_tester/model.sdf``). The average of :math:`n` readings
  wanders by about :math:`\sigma / \sqrt{n}`: 0.05 / √10 = 0.016 V for
  :math:`n` = 10.

**Worked example: a good cell at 3.78 V** (chosen for this example).

1. 3.8 V is 0.02 V above it: 0.02 / 0.05 = 0.4 standard deviations for one
   reading. One reading lands above 3.8 V with probability 0.34.
2. For the average of 10: 0.02 / 0.0158 = 1.26 standard deviations
   (0.0158 is 0.05 / √10 before rounding), probability 0.10.
3. A cell read above 3.8 V is recycled for nothing.

The probabilities in steps 1 and 2 are the share of a normal distribution that
lies more than 0.4 and 1.26 standard deviations above its mean, read from a
normal table.

Demo: Checking the Probabilities with Synthetic Readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/voltage_average.py
   :language: python
   :lines: 14-17
   :caption: voltage_average.py (excerpt)

.. literalinclude:: outputs/voltage_average.txt
   :language: text
   :lines: 1-4

- 0.345 and 0.104 agree with the 0.34 and 0.10 computed by hand. With 100000
  trials, chance moves each fraction by about 0.002.
- The spread of the average, 0.0158 V, is the 0.016 V that
  :math:`\sigma / \sqrt{10}` predicts.

Demo: Skipping Readings That Are Not Valid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What the plugin publishes** (``voltage_tester_plugin.cpp``):

- No cell in the tester: 0 V plus noise.
- During a tester malfunction it keeps publishing: voltage −1,
  ``operation_status`` MALFUNCTIONING (2). The Challenges page says it stops;
  the code does not.
- It publishes on a 0.1 s wall-clock timer, so 10 readings take about 1 s of
  real time.

.. literalinclude:: code/voltage_average.py
   :language: python
   :lines: 31-32
   :caption: voltage_average.py (excerpt)

.. literalinclude:: outputs/voltage_average.txt
   :language: text
   :lines: 5-8

The reading of 3.85 V, alone, would have recycled this good cell. GP2 joins
both checks in one record per cell: the lidar decides the report, the averaged
voltage decides tray or recycling.


.. _l5-measuring:

Measuring a Detector
--------------------

This section covers precision, recall, and what each kind of error costs in
ARIAC.

Four Outcomes, Two Ratios
~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l5/confusion_matrix.svg
   :alt: A two by two table. Columns: the detector rejects the cell, or passes
         it. Rows: the cell is defective, or good. Defective and rejected: TP,
         7. Defective and passed: FN, 1. Good and rejected: FP, 2. Good and
         passed: TN, 30. The two error squares, FN and FP, are orange; the two
         correct squares are gray.
   :width: 70%
   :align: center

Counts from the worked example below. Orange: an error.

.. admonition:: Definition: the four outcomes (a defective cell is a positive)
   :class: note

   - **TP** (true positive): a defective cell the detector rejects.
   - **FP** (false positive, a false alarm): a good cell it rejects.
   - **FN** (false negative, a missed defect): a defective cell it passes.
   - **TN** (true negative): a good cell it passes.

   This two by two table of counts is a **confusion matrix**.

.. admonition:: Definition: precision and recall
   :class: note

   - **Precision** = TP / (TP + FP): of the cells rejected, the share that
     were defective.
   - **Recall** = TP / (TP + FN): of the defective cells, the share that were
     caught.

Worked Example, and What Each Error Costs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Numbers chosen for this example:** 40 cells, 8 of them defective. The
detector rejects 9, and 7 of those are defective.

1. TP = 7, FP = 9 − 7 = 2, FN = 8 − 7 = 1, TN = 40 − 7 − 2 − 1 = 30.
2. Precision = 7 / 9 = 0.78. Recall = 7 / 8 = 0.875.
3. With only 9 rejections, one more false alarm moves precision from
   7 / 9 = 0.78 to 7 / 10 = 0.70: report the counts with the ratios.

**The cost in ARIAC.**

- **FP:** a good cell in the inspection bin, 50 points. The two here cost 100
  points.
- **FN:** a defective cell goes through the door. In a kit, it fails the kit
  at submission (Step 1e), and the AGV must go to recycling. With a trial of 3
  kits (chosen for this example), a kit is worth 5000 / 3 = 1667 base points.

.. admonition:: Class discussion: which error would you rather make?
   :class: tip

   A missed defect can cost a 1667-point kit; a false alarm costs 50 points.
   So favor recall when you set the threshold.

.. _l5-pr-demo:

Demo: 200 Synthetic Cells, Two Lidars, Three Thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``precision_recall.py`` passes 200 synthetic cells by the lidars. Each cell is
defective with probability 0.25 and then has one defect of a random type,
place and depth. A cell is rejected when the detector finds any defect.
"classified (ARIAC rule)" counts the defective cells whose report would earn
the classification bonus.

.. literalinclude:: outputs/precision_recall.txt
   :language: text
   :lines: 1-12

Each "missed" line gives the defect's :math:`\theta` (rad) and depth (mm),
the number of points that landed on it, how many of those have :math:`|d|`
above 0.9 mm, and the deepest :math:`d` on it (mm). The script takes about
4 minutes, so in class this output was recorded beforehand.

1. 0.5 mm is below the noise on good cells (0.53 to 0.79 mm): 5 false alarms.
   Precision = 55 / (55 + 5) = 0.92; recall = 55 / 56 = 0.98.
2. 0.9 mm, from the good cells: no false alarms, 3 misses. Each sits within
   0.26 rad of :math:`\theta` = 0 or :math:`\pm\pi`, where each lidar sees
   the surface at a grazing angle (the edges of the gap on the residual
   map). Points land on each (33, 6 and 22), but at most one passes 0.9 mm,
   and a cluster needs 3.
3. 1.5 mm misses one more. A higher threshold flags fewer points, so it
   cannot catch these.

Demo: Four Lidars, and Shallower Defects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/precision_recall.txt
   :language: text
   :lines: 13-22

1. On set 1, four lidars (two in each side box, at :math:`x` = 0.7 m, turned
   0.6 rad upstream and downstream) see the front and back of the cell: all
   56 caught.
2. Set 2 uses depths from 0.8 to 2.5 mm, the range measured in ARIAC's
   meshes. Both misses are dents. The 0.82 mm dent is below the 0.9 mm
   threshold: none of its 52 points passes. The 0.91 mm dent is just above
   it, but only 2 of its 84 points pass, and a cluster needs 3.
3. Chance: with about 55 defective cells, one miss moves recall by
   1 / 55 = 0.018. Compare layouts on the same cells, as here.

What the four-lidar layout costs in sensor cost and inspection speed, in
ARIAC points, is :doc:`Exercise 6 <l5_exercises>` on the exercises page.

.. _l5-gp2:

GP2: Cell Inspection
--------------------

**Posted today, due Week 7 (03/10), 10% of the grade.**

- Place lidars inside the boxes and within the budget; justify the layout and
  its cost with numbers.
- Detect defects from the point clouds and submit an inspection report for
  every cell before :math:`x` = 1.0 m.
- Average the voltage readings, skipping invalid ones; keep one record per
  cell that joins both checks.
- Measure precision and recall for each defect type against
  ``log_cell_info:=true`` ground truth, used offline only, never in the
  running system.

**Deliverables:** the perception package, the updated GP1 tree, and a results
table: precision and recall per defect type, the number of cells tested, and
the sensor cost. Also the team configuration file and a 1 to 2 page
write-up. The full list is on the :doc:`GP2 page </assignments/gp2>`.


.. _l5-next:

Next Class
----------

**L6: Task-Level Planning with PDDL (Wednesday, March 3):** domains and
problems, typed predicates, and running a planner from Python.

**Before next class:**

- Read the PDDL Primer pre-read on the course site.
- Install the Unified Planning Framework with Fast Downward in a virtual
  environment: ``python3 -m venv ~/venvs/planning``, then
  ``~/venvs/planning/bin/pip install unified-planning up-fast-downward``.
- Run the L5 scripts (``run_all.sh``, see :doc:`l5_code`) and compare your
  outputs with these notes.
- Quiz 3, at the start of Week 7, covers L5 and L6.
