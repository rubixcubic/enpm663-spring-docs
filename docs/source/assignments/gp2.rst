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

GP2 adds perception. Your team places RGB cameras over the inspection
conveyor within the ARIAC sensor budget, detects dents, scratches and bulges
with OpenCV, and combines the defects with the voltage readings into an
inspection report for each cell. The GP1 tree then recycles the cells that
fail.


Learning Objectives
-------------------

- Choose and place sensors within a budget.
- Detect surface defects on cells from RGB images with OpenCV.
- Submit inspection reports through the ARIAC service.
- Measure a detector with precision and recall.


Provided Resources
------------------

- Your team's GP1 package.
- The ARIAC 2025 sensor and inspection interfaces.


Tasks
-----

- Place cameras and justify their placement and cost.
- Detect each defect type and report it in the inspection report.
- Measure precision and recall of your detector on a set of cells.
- Wire the results into the GP1 tree so defective cells are recycled.


Deliverables
------------

- The perception package and the updated tree.
- A results table: precision and recall per defect type, and the sensor cost.
