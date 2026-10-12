====================================================
GP1: Behavior Tree for One Kit
====================================================

.. card:: GP1: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 2 to Week 5), posted 02/03, due 02/24
      * - **Weight**
        - 10% of the course grade
      * - **Lectures**
        - L1 to L4
      * - **Team Size**
        - 3 students
      * - **Submission**
        - Canvas + GitHub repository link


.. admonition:: Specification draft
   :class: note

   This page is the specification draft for GP1. The provided code (the
   course skills package and the GP1 starter package) is released with the
   project, on the day GP1 is posted. Details that depend on that code are
   marked on this page and are filled in when it is released.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP1 builds the behavior tree that every later project extends. A
**behavior tree** is a tree of tasks that a program ticks (runs one step at
a time) to decide what the robots do next. Your team writes the tree in
``py_trees_ros``, and the tree builds one kit in the ARIAC 2025 factory. A
**kit** is four battery cells of the same type on an AGV tray.

The tree feeds Li-Ion cells onto the inspection conveyor and submits an
inspection report for every cell. An **inspection report** says whether a
cell passed, and lists any defects. ARIAC's **inspection door** lets a cell
through only if your team submitted a passing report for it. A cell that
fails, or that has no report, is pushed into the inspection bin.

.. important::

   A cell reaches the inspection robots only if your team has submitted a
   passing inspection report for it. GP1 has no defect detection yet, so it
   runs on a trial with no defective cells, and every report says the cell
   passed. GP2 adds the real inspection.

After the door, inspection robot 1 (a UR3e) picks the cell off the moving
conveyor and places it in a voltage tester. The tree averages the tester's
noisy readings. Inspection robot 2 (a UR5e) then recycles the cell if its
voltage is out of range, or places it in a tray slot. The tree checks the
kit, moves the AGV to the shipping station and submits the kit.

The robots move only through the course skills package. You write no motion
code: your leaves call the skills and the ARIAC services and actions.
Lectures L1 to L4 cover what GP1 needs.

GP1 comes with a starter tree. Spend Weeks 2 and 3 on setup, the skills
package and the ARIAC services, and write the tree after L4 (Week 4).


The voltage limits
~~~~~~~~~~~~~~~~~~

Two limits decide which cells go in the kit. Both come from the ARIAC 2025
scenario for Li-Ion cells.

1. **Each cell:** 3.6 V nominal, ± 0.2 V. So a cell is acceptable from
   3.6 − 0.2 = 3.4 V to 3.6 + 0.2 = 3.8 V.
2. **The kit:** four cells must total 4 × 3.6 = 14.4 V, ± 0.15 V. So the kit
   total must land from 14.4 − 0.15 = 14.25 V to 14.4 + 0.15 = 14.55 V.

Four cells that each pass limit 1 can still fail limit 2: four cells at
3.7 V (chosen for this example) total 4 × 3.7 = 14.8 V, which is above
14.55 V. Cells lock to the tray once placed, so the tree must check the kit
total **before** it places each cell, not after the fourth.


Learning Objectives
-------------------

After completing GP1, you will be able to:

- Structure a behavior tree with sequences, selectors and decorators, and
  justify each composite choice.
- Write ``py_trees_ros`` leaves that call ROS 2 actions, services and
  topics.
- Share state between leaves through the blackboard.
- Submit an inspection report for every cell before it reaches the
  inspection door.
- Compute the cell and kit voltage limits and apply them when choosing
  cells.
- Run an ARIAC 2025 trial from start to end and submit an accepted kit.


Provided Resources
------------------

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - Resource
     - What it gives you
   * - Course skills package
     - Python ROS 2 actions, built on MoveIt 2, that move the inspection
       robots: pick a cell off the conveyor, place it on a voltage tester,
       take it off, place it in a tray slot, and drop it in the recycling
       bin. Its documentation page lists each action's goal, result and
       failure codes. Released with GP1.
   * - GP1 starter package
     - A ROS 2 package with a launch file for the trial, and a starter
       ``py_trees_ros`` tree: one sequence for one cell. You extend it
       after L4. Released with GP1.
   * - ARIAC 2025 example team configuration
     - A working team configuration file to start from.
   * - GP1 trial configuration
     - A trial with no defective cells (``DEFECT_RATE`` 0.0), one kit and
       no challenges. You develop on it, and the grader runs it.
   * - ARIAC 2025 documentation
     - The Scenario (Task 1), ROS API, Configuration Files and Scoring
       pages: https://pages.nist.gov/ARIAC_docs/en/latest/

The skills package moves the robots, but it does not move the AGVs. Your
tree moves an AGV with ARIAC's own AGV move action (``/agvN/move``, for
example ``/agv1/move``).

.. note::

   **The skills package never retries a task on its own.** Each skill
   reports success or a failure reason, so recovery is your tree's job
   (L4, and L7 later).


Tasks
-----

.. dropdown:: Task 1: Set up the team configuration and the trial
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** start an ARIAC 2025 trial with your team's configuration, and
   feed Li-Ion cells.

   **Requirements:**

   - Write the team configuration file: the conveyor speed and the cell
     feed rate inside the limits on the ARIAC Configuration Files page,
     and a break beam on the inspection conveyor.
   - The conveyor pickup skill uses the time this break beam fires to catch
     the moving cell, so the beam is not optional.
   - Start the competition, and set the cell feed to Li-Ion with the cell
     feed control service.

   .. note::

      **Added when the skills package is released:** where to place the
      break beam, and which grade the pickup skill needs. The ARIAC Sensors
      page gives the two grades: grade A (30 Hz, $400) and grade B (10 Hz,
      $200).

   **Done when:** the competition reaches the STARTED state, and cells move
   on the inspection conveyor.

.. dropdown:: Task 2: Submit an inspection report for every cell
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** every cell reaches the robots.

   **Requirements:**

   - Submit a passing inspection report for every cell before it reaches
     the inspection door.
   - ARIAC applies each report to the cell nearest the door that has no
     report yet. So submit one report per cell, in order, and do not skip a
     cell.

   **Done when:** the number of reports in your run log equals the number
   of cells fed, and no good cell lands in the inspection bin.

.. dropdown:: Task 3: Read each cell's voltage
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a voltage you can trust for each cell.

   **Requirements:**

   - Have inspection robot 1 pick each cell off the moving conveyor and
     place it in a free voltage tester.
   - Average the tester's readings over a short window. The tester adds
     noise to each reading, so one reading is not enough.
   - Store the averaged voltage on the blackboard.

   **Done when:** the log shows, for each cell, the readings used and their
   average.

.. dropdown:: Task 4: Place or recycle each cell
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** four cells on the tray whose total lands inside the kit limit.

   **Requirements:**

   - Have inspection robot 2 recycle a cell outside 3.4 V to 3.8 V.
   - Before placing a cell inside that range, check that the four-cell
     total can still land in 14.25 V to 14.55 V (see
     `The voltage limits`_). If it cannot, recycle the cell.
   - Keep the running kit total and the slots used on the blackboard.

   **Done when:** the log shows a decision (place or recycle) with its
   reason for every tested cell.

.. dropdown:: Task 5: Check, ship and submit the kit
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** one kit submitted and accepted.

   **Requirements:**

   - Call the check kit quality service.
   - Move the AGV to the shipping station with ARIAC's AGV move action,
     and submit the kit.
   - If the kit is not accepted, send the AGV to the recycling station and
     recycle the tray.

   **Done when:** the ARIAC run results show 1 of 1 kit submitted and
   accepted.

.. dropdown:: Task 6: Handle failures
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a tree that recovers from one failure and stops cleanly on a
   repeated one.

   **Requirements:**

   - A skill that fails once: retry it.
   - A skill that keeps failing: stop the tree cleanly and log why.
   - Show both cases with a forced-failure test (for example, a test leaf
     that fails on purpose), and describe the test in the README.

   **Done when:** the log of the forced-failure test shows the retry and the
   clean stop.

.. dropdown:: Task 7: Keep shared state on the blackboard
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** leaves that share values only through the blackboard.

   **Requirements:**

   - Keep the averaged voltage, the slots used and the running kit total on
     the blackboard, not in global variables.
   - List every blackboard key, with its type and the leaves that write and
     read it, in the README.
   - Each leaf does one job.


Suggested Schedule
------------------

GP1 is posted before L4, the behavior tree lecture. This plan uses the first
two weeks for setup, so your team arrives at L4 ready to write the tree.

.. list-table::
   :widths: 16 44 40
   :header-rows: 1
   :class: compact-table

   * - Week
     - Work
     - Done when
   * - Week 2 (from 02/03)
     - Install the skills package and the starter package, launch the
       example trial, run the starter tree. List the ARIAC services and
       skills each step of the kit needs.
     - The team can start the competition and feed cells (Task 1).
   * - Week 3 (from 02/10)
     - List the facts the tree must track (L3), and agree on the blackboard
       key names and types.
     - The key list is in the README draft.
   * - Week 4 (from 02/17)
     - After L4: write the tree (Tasks 2 to 7), run it on the GP1 trial,
       test the two failure cases.
     - One full run submits an accepted kit.
   * - Week 5 (02/24)
     - Write-up, run log, final check.
     - Submitted by 02/24.


Deliverables
------------

1. A ROS 2 package with a behavior tree that starts with one launch command,
   pushed to your team's GitHub repository. Submit the repository link on
   Canvas.
2. A ``README.md`` with the build and launch commands, the ARIAC version
   used, the blackboard keys and the forced-failure test.
3. A short write-up (1 to 2 pages) with the tree diagram and the reason for
   each composite choice (why a selector here, why memory there).
4. A log of one full run on the provided trial. For each cell it shows the
   report, the averaged voltage and the decision, and at the end the kit
   submission result.
5. The honor pledge, signed by every team member: *"I pledge on my honor
   that I have not given or received any unauthorized assistance on this
   group project."*


Submission Checklist
--------------------

.. admonition:: Before submitting, check every item
   :class: tip

   - [ ] A fresh clone builds, and the README's launch command starts the
         tree.
   - [ ] The run log has one inspection report per cell fed.
   - [ ] Every recycled cell was outside 3.4 V to 3.8 V, or would have
         pushed the kit total outside 14.25 V to 14.55 V.
   - [ ] The log shows the check kit quality call before the AGV moved.
   - [ ] The forced-failure test shows a retry and a clean stop.
   - [ ] The README lists every blackboard key.
   - [ ] Every composite in the code appears in the write-up's diagram,
         with a reason for its type.
   - [ ] Every team member signed the honor pledge.
   - [ ] Each member fills in the peer-review form after the deadline (see
         :ref:`peer-evaluation`).


Grading Rubric (Draft)
----------------------

.. admonition:: Draft rubric
   :class: note

   This rubric is a draft. It may change before GP1 is posted. The total is
   100 points, scaled to 10% of the course grade.

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Criterion
     - Points
     - How the grader checks it
   * - Builds and launches
     - 10
     - The grader clones the repository, builds it and runs the launch
       command from the README on the provided defect-free trial. The tree
       starts and the competition reaches the STARTED state.
   * - Inspection report for every cell
     - 15
     - The grader compares the number of cells fed with the number of
       reports in the run log, and reads the ARIAC run results: no good
       cell in the inspection bin.
   * - Voltage reading and cell decisions
     - 15
     - The grader reads the leaf that averages the tester readings, and
       checks in the log that every cell outside 3.4 V to 3.8 V went to the
       recycling bin and every placed cell was inside it.
   * - Kit accepted
     - 25
     - ARIAC run results on the grader's run: 1 of 1 kit submitted and
       accepted. The log shows the check kit quality call before the AGV
       moved, and a kit total inside 14.25 V to 14.55 V.
   * - Failure handling
     - 15
     - The grader reads the tree for a retry around each skill leaf and a
       branch that stops cleanly. The README describes a forced-failure
       test, and its log shows the retry and the clean stop.
   * - Blackboard use and tree structure
     - 10
     - The grader reads the code: shared values are blackboard keys listed
       in the README, leaves do one job each, and no global variables pass
       values between leaves.
   * - Write-up
     - 10
     - The grader reads the 1 to 2 page write-up: every composite in the
       code appears in the diagram with a reason for its type.

The points add up to 10 + 15 + 15 + 25 + 15 + 10 + 10 = 100.


Common Mistakes
---------------

.. danger::

   - **Skipping a report.** A cell with no report is pushed into the
     inspection bin, and ARIAC counts a good cell in the inspection bin as a
     penalty.
   - **Checking the kit total after the fourth cell.** Cells lock to the
     tray once placed. Check before each placement.
   - **Deciding on one voltage reading.** The tester adds noise to each
     reading. Average over a window.
   - **Expecting the skills package to retry.** It does not. Put the retry
     in the tree.
   - **Planning to cancel an AGV move.** ARIAC's AGV move action rejects
     cancel requests, so check the kit before the AGV leaves.
   - **Global variables between leaves.** Share values through blackboard
     keys only. The "Blackboard use and tree structure" row checks this.


Tips for Success
----------------

.. tip::

   **Run the starter tree in Week 2.** If the trial does not start, or no
   cell reaches the door, nothing else in GP1 can be tested.

.. tip::

   **Log from the first day.** Print each cell's report, readings, average
   and decision. The run log is a deliverable, and it is the grader's
   evidence for three rubric rows.

.. tip::

   **Agree on the blackboard keys before you split the work.** The keys are
   the interface between teammates' leaves.
