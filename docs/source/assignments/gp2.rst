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


.. admonition:: Specification in progress
   :class: note

   This page is the plan for GP2. The full specification (provided code,
   folder structure, submission checklist and grading rubric) is added
   before it is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP2 adds perception. Your team places lidar sensors around the inspection
conveyor within the ARIAC sensor budget, as ARIAC 2025 requires, and detects
dents, scratches and bulges from the point clouds. Each cell gets an
inspection report before it reaches the inspection door: a failing report
sends the cell into the inspection bin. The GP1 tree then reads the voltage
of each cell that passes and places or recycles it. Your team keeps one
record per cell that joins the two checks.


Learning Objectives
-------------------

- Choose and place sensors within a budget.
- Detect surface defects on cells from lidar point clouds.
- Submit inspection reports through the ARIAC service.
- Measure a detector with precision and recall.


Provided Resources
------------------

- Your team's GP1 package.
- The ARIAC 2025 sensor and inspection interfaces.


Tasks
-----

- Place lidar sensors inside ARIAC's bounding boxes and justify their placement and cost.
- Detect each defect type and report it in the inspection report.
- Measure precision and recall of your detector on a set of cells.
- Wire the results into the GP1 tree: a failing report keeps a defective cell out of the kit.


Deliverables
------------

- The perception package and the updated tree.
- A results table: precision and recall per defect type, and the sensor cost.
