====================================================
GP2: Cell Inspection
====================================================

.. card:: GP2: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 2 weeks (Week 5 to Week 7), posted 02/24, due 03/10
      * - **Weight**
        - 10% of the course grade
      * - **Lectures**
        - L5
      * - **Team Size**
        - 3 students
      * - **Submission**
        - Canvas + GitHub repository link


.. admonition:: Specification draft
   :class: note

   This page is the specification draft for GP2. The provided code (the
   course skills package, as in GP1) and the GP2 trial configurations are
   released with the project, on the day GP2 is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP2 adds the physical inspection that GP1 skipped. ARIAC 2025 requires
teams to use lidar point cloud data to reconstruct each cell's shape as it
passes on the inspection conveyor. A **point cloud** is a set of 3D points
that the lidar measures on the surfaces it sees.

A good cell is a smooth cylinder. A defective cell has one of three
defects:

- a **dent**: a round dip,
- a **scratch**: a long, narrow dip,
- a **bulge**: a round bump.

The ARIAC Scenario page says: "All defects will be at least 2mm removed
from the normal cell surface at their furthest point". ARIAC's own training
cell meshes do not match it: their 15 defects measure 0.84 to 2.49 mm, and
10 of them are under 2 mm (L5 measures them). Set your threshold below the
shallowest defect you must find.

Your team places lidar sensors inside the three bounding boxes that ARIAC
allows around the inspection conveyor, and pays for them from the sensor
budget of $9600. For each cell, your perception node builds the inspection
report: passed or failed, and for each defect its type, its angle around the
cell (theta) and its height above the cell base (z). The report decides what
happens at the inspection door: a passing cell goes through to inspection
robot 1. For a failing cell the door stays closed, and the cell drops into
the inspection bin.

Two checks
~~~~~~~~~~

GP2 runs two checks on each cell, at two places:

1. **At the conveyor, before the door:** the lidar result decides the
   inspection report (pass or fail, and the defect list).
2. **At the voltage tester, after the door:** the averaged voltage decides
   whether inspection robot 2 places the cell on the tray or recycles it,
   as in GP1.

Your team keeps one record per cell that joins the two results. The GP1
tree uses that record when it builds the kit. You also measure how good
your detector is, with precision and recall for each defect type. Lecture L5
covers what GP2 needs.


Learning Objectives
-------------------

After completing GP2, you will be able to:

- Choose lidar grades and positions inside the ARIAC bounding boxes and
  within the sensor budget, and justify the cost.
- Write a point cloud pipeline that reconstructs each cell and finds dents,
  scratches and bulges.
- Compute each defect's type, angle (theta) and height (z) as ARIAC defines
  them.
- Submit an inspection report through the ARIAC service before each cell
  reaches the door.
- Evaluate the detector with precision and recall for each defect type
  against ground truth.


Provided Resources
------------------

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - Resource
     - What it gives you
   * - Your team's GP1 package
     - The tree that builds one kit. GP2 extends it.
   * - ARIAC 2025 sensor interfaces
     - Each lidar publishes a ``sensor_msgs/PointCloud2`` on its scan topic.
   * - ARIAC 2025 inspection interfaces
     - The ``InspectionReport`` and ``CellDefect`` messages, and the submit
       inspection report service.
   * - GP2 trial configurations
     - Trials with defective cells: ``DEFECT_RATE`` above zero and a list of
       possible defects.
   * - Ground truth for each cell
     - Launch ARIAC with ``log_cell_info:=true``: it prints each cell's
       defects to the Gazebo log. Use it offline, to measure precision and
       recall, never at run time. (ARIAC's
       ``ariac_setup/config/defects.yaml`` holds only the defect shapes.)

.. _gp2-sensor-costs:

Lidar grades and costs
~~~~~~~~~~~~~~~~~~~~~~

The ARIAC Sensors page gives three lidar grades. **H** and **V** are the
lidar's horizontal and vertical sample counts, so H × V is the number of
points in one scan.

.. list-table::
   :widths: 14 22 34 30
   :header-rows: 1
   :class: compact-table

   * - Grade
     - Update rate
     - Samples per scan (H × V)
     - Cost
   * - A
     - 20 Hz
     - at most 400
     - $1500
   * - B
     - 10 Hz
     - more than 200, at most 400
     - $1250
   * - C
     - 10 Hz
     - at most 200
     - $1000

.. warning::

   The ARIAC code bills a lidar with exactly 200 samples as grade B
   ($1250), although the Sensors page lists 200 under grade C. To be billed
   as grade C, use at most 199 samples. ARIAC accepts a lidar only at 10 or
   20 Hz (``ariac_setup/yaml_validation.py``) and bills every 20 Hz lidar as
   grade A.

The GP1 break beam counts toward the same $9600 budget. Spending less than
the budget earns a sensor cost bonus.


Tasks
-----

.. dropdown:: Task 1: Choose and place the lidars
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** enough points on each cell to find a defect under 1 mm deep
   (the shallowest training defect is 0.84 mm), at a cost you can justify.

   **Requirements:**

   - Choose the number, grade and pose of your lidars. Every lidar must
     sit inside bounding box A, B or C (ARIAC Sensors page).
   - Compute the total sensor cost, including the GP1 break beam, from the
     table in :ref:`gp2-sensor-costs`. Show the sum.
   - Justify each grade in the write-up: what a cheaper grade would give up
     (rate, points per scan) and what that costs in detection.

.. dropdown:: Task 2: Build the point cloud pipeline
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** each cell's points, in a frame centered on the cell.

   **Requirements:**

   - Write a ROS 2 node that subscribes to the lidar scans and keeps the
     points that fall on the cell.
   - Transform those points into a frame centered on the cell's axis.
   - Combine several scans as the cell moves. One scan has at most 400
     points (grade A or B), so one scan is not enough to cover a cell.
   - Log, for each cell, the number of points kept and the fitted radius.

.. dropdown:: Task 3: Detect and classify the defects
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** find each defect and name its type.

   **Requirements:**

   - Fit the cylinder, and measure each point's distance from its surface.
   - ARIAC's training defects reach 0.84 to 2.49 mm from the surface at
     their furthest point (L5). Points well inside the surface belong to a dent or a scratch;
     points well outside belong to a bulge.
   - Group those points into regions, and tell a dent (round) from a
     scratch (long and narrow).
   - Keep every threshold a ROS 2 parameter, not a value in the code.

   .. note::

      The ARIAC documentation says the defect shapes in this release are
      for training, and that the competition version will change them
      (Configuration Files page). The final demo runs an unseen trial. A
      detector that measures distance from a fitted cylinder carries over
      to new shapes better than one tuned to the training shapes.

.. dropdown:: Task 4: Locate each defect
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** each defect's theta and z, as ARIAC defines them.

   **Requirements:**

   - **theta:** the angle around the cell's axis. It is zero when the
     defect faces along the conveyor's direction of travel, and it is
     positive by the right-hand rule about the vertical axis.
   - **z:** the defect's height above the cell base.

   Classifying defects is optional in ARIAC, but reports whose type, theta
   and z are all correct earn the inspection classification bonus.

.. dropdown:: Task 5: Submit the report in time
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a report for every cell before it reaches the door.

   **Requirements:**

   - Submit the report through the ARIAC service before the cell reaches
     the inspection door.
   - ARIAC rewards a short average inspection time (target 4 s) with the
     inspection speed bonus.

.. dropdown:: Task 6: Measure precision and recall
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a measured answer to "how good is the detector?".

   For one defect type, count over the test cells:

   - **TP** (true positives): cells with that defect that your detector
     reported with that defect.
   - **FP** (false positives): cells your detector reported with that
     defect that do not have it.
   - **FN** (false negatives): cells with that defect that your detector
     missed.

   Then **precision** = TP / (TP + FP) is the share of your detector's
   calls that were right, and **recall** = TP / (TP + FN) is the share of
   the real defects your detector found.

   **Requirements:**

   - Measure precision and recall for each defect type (dent, scratch,
     bulge) on cells from several trial seeds, against the ground truth
     from ``log_cell_info:=true``.
   - Report how many cells you used, and keep the raw counts (TP, FP, FN)
     so the grader can recompute any row.

.. dropdown:: Task 7: Wire the results into the GP1 tree
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** one kit built on a trial with defects.

   **Requirements:**

   - Keep one record per cell that joins the inspection result and the
     averaged voltage.
   - The tree does not wait for cells that dropped into the inspection bin.
   - The tree still builds and submits the kit on a trial with defects.


Deliverables
------------

1. The perception package and the updated tree in your team's repository.
   Submit the repository link on Canvas.
2. The team configuration file, with the lidar poses and grades.
3. A results table: precision and recall per defect type (dent, scratch,
   bulge), the number of cells measured, the raw counts, and the total
   sensor cost.
4. A short write-up (1 to 2 pages): the sensor choice, the detection method
   and the cases the detector gets wrong.
5. The honor pledge, signed by every team member.


Submission Checklist
--------------------

.. admonition:: Before submitting, check every item
   :class: tip

   - [ ] Every lidar pose is inside box A, B or C.
   - [ ] The total sensor cost is shown as a sum and is under $9600.
   - [ ] The perception node logs, for each cell, the points kept, the
         fitted radius and the defects found.
   - [ ] On a trial with defects, the number of reports matches the number
         of cells fed (apart from cells still on the conveyor at the end).
   - [ ] The results table states the ground truth source, the number of
         cells and the raw counts.
   - [ ] Thresholds and sensor names are parameters.
   - [ ] The README launch commands work as written.
   - [ ] Every team member signed the honor pledge.
   - [ ] Each member fills in the peer-review form after the deadline (see
         :ref:`peer-evaluation`).


Grading Rubric (Draft)
----------------------

.. admonition:: Draft rubric
   :class: note

   This rubric is a draft. It may change before GP2 is posted. The total is
   100 points, scaled to 10% of the course grade.

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Criterion
     - Points
     - How the grader checks it
   * - Sensor placement and cost
     - 15
     - The grader reads the team configuration: each lidar position is
       inside box A, B or C, and the grader recomputes the total cost from
       the ARIAC grade table. The total is under $9600, and the write-up
       justifies the grades.
   * - Point cloud pipeline
     - 15
     - The grader runs the perception node on a grader trial and reads its
       per-cell log: points kept on the cell, fitted radius, defects found.
   * - Pass and fail decisions on a grader trial
     - 20
     - The grader runs a trial with defects (seed unknown to the team) and
       compares the reports with the ground truth: good cells in the
       inspection bin (ARIAC penalty count) and defective cells that went
       through the door. The run database's Run table also counts the
       reports with a correct pass or fail (``num_correct_reports`` against
       ``num_reports_submitted``).
   * - Defect type and location
     - 10
     - ARIAC run results on the same trial: the inspection classification
       bonus, which counts reports whose type, theta and z are all correct.
   * - Report timing
     - 10
     - The run database's Run table gives ``total_cells`` (cells fed) and
       ``num_reports_submitted``. They match, apart from cells still on the
       conveyor when the run ended, so no cell reached the door without a
       report. The ARIAC App's Run Results page lists the average report
       time, which the grader compares with the 4 s target.
   * - Precision and recall table
     - 15
     - The grader reads the table and the method: counts add up, the ground
       truth source and the number of cells are stated, and the grader
       recomputes one row from the team's raw counts.
   * - Integration with the GP1 tree
     - 10
     - On the grader trial with defects, the kit is submitted and accepted
       (ARIAC run results), and the log shows the tree skipping binned
       cells.
   * - README and code quality
     - 5
     - The README launch commands work as written, and thresholds and
       sensor names are parameters, not values inside the code.

The points add up to 15 + 15 + 20 + 10 + 10 + 15 + 10 + 5 = 100.


Common Mistakes
---------------

.. danger::

   - **A lidar at exactly 200 samples.** It is billed as grade B ($1250),
     not grade C. See :ref:`gp2-sensor-costs`.
   - **Deciding from one scan.** One scan has at most 400 points. Combine
     scans as the cell moves.
   - **Tuning to the training shapes.** The competition shapes change, and
     the grader's trial uses a seed you have not seen.
   - **Reading the ground truth at run time.** ``log_cell_info`` is for
     measuring the detector offline. The report must come from your lidar
     data.
   - **Precision and recall with no counts.** A percentage alone cannot be
     checked. Keep TP, FP and FN for each defect type.


Tips for Success
----------------

.. tip::

   **Look at one cell first.** Show one cell's point cloud in RViz before
   you write any detection code, so you know how many points land on it.

.. tip::

   **Measure on several seeds.** Precision and recall from one trial
   describe that trial. Several seeds tell you how the detector does on
   cells it has not seen.
