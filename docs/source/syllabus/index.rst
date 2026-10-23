Syllabus
========

.. role:: reading
.. role:: quiz
.. role:: assignment
.. role:: no-class

.. note::

   The authoritative, printable syllabus is the PDF distributed on
   ELMS-Canvas. This page mirrors it. If the two ever disagree, the
   Canvas PDF governs. Please report the discrepancy.

Prerequisites
-------------

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **ROS 2**
     - Create and manage packages and workspaces. Write publishers,
       subscribers, services, and action clients and servers in Python. Use
       launch files, parameters and the ``ros2`` command-line tools.
   * - **Python**
     - A significant amount of Python programming is required in every
       group project.
   * - **C++ (reading)**
     - Read C++ ROS 2 code. Writing C++ is not a prerequisite.
   * - **Git and GitHub**
     - Clone, branch, commit, push and pull, resolve a merge conflict, and
       open and review a pull request. The course does not teach them.

.. admonition:: Not sure about your ROS 2 background?
   :class: tip

   L1 includes a refresher on the ROS 2 topics this course uses most
   (QoS, executors, actions and TF2) and an **ungraded diagnostic
   quiz**. Read the ROS 2 Refresher pre-read before L1, and talk to the
   instructor in Week 1 if the diagnostic shows gaps.


Course and Instructor
---------------------

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Credits**
     - 3
   * - **Dates**
     - Jan 27 to May 5, 2027 (spring break Mar 14 to 21)
   * - **Time**
     - Wednesdays, 7:00 to 9:40 pm
   * - **Sections**
     - 0101 (in person, room TBA) and RO01 (online, details on ELMS)
   * - **Instructor**
     - Zeid Kootbally, ``zeidk@umd.edu``
   * - **Office hours**
     - By appointment

Email replies come within 24 hours on weekdays. Use email for personal,
academic or intellectual concerns, not for due dates and point values
already in this syllabus. Important announcements, including project and
due date changes, are posted on ELMS: turn on its notifications.


Grade Breakdown
---------------

These seven numbers add up to your grade. There is nothing else.

.. list-table::
   :header-rows: 1
   :widths: 60 40
   :class: compact-table

   * - Component
     - % of course grade
   * - GP1: Behavior Tree for One Kit
     - 10%
   * - GP2: Cell Inspection
     - 10%
   * - GP3: PDDL Planner and BT Executor
     - 10%
   * - GP4: LLM Agent with VLM Grounding
     - 10%
   * - Final demo
     - 20%
   * - Quizzes (5, equally weighted)
     - 25%
   * - Peer-review contribution
     - 15%
   * - **Total**
     - **100%**

- The four group projects and the final demo make up the **final project**,
  **60%** of the course.
- **The final demo counts twice as much as a group project.** It is the only
  deliverable graded on an ARIAC trial your team has never seen.
- **There is no final exam.** The final demo, with its presentation, is the
  capstone assessment.


Letter Grades
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25
   :class: compact-table

   * - Grade
     - Cutoff
     - Grade
     - Cutoff
   * - A+
     - 97.00%
     - C+
     - 77.00%
   * - A
     - 94.00%
     - C
     - 74.00%
   * - A-
     - 90.00%
     - C-
     - 70.00%
   * - B+
     - 87.00%
     - D+
     - 67.00%
   * - B
     - 84.00%
     - D
     - 64.00%
   * - B-
     - 80.00%
     - D-
     - 60.00%

F is anything below 60.00%.

.. warning::

   Cutoffs are applied consistently to every student: **89.99 is not 90.00.**


Late Work
~~~~~~~~~

- Group projects: **10% deduction per calendar day, maximum 3 days**, zero
  thereafter.
- **The projects are cumulative**, so late days on one project are days
  taken out of the next one.
- Extensions are granted only when more than one team needs more time on the
  same submission.
- No quiz or group project is dropped. The final demo is required, and
  nothing replaces its grade.


Quizzes
-------

Five quizzes, each worth **5%** of the course grade, plus an ungraded
diagnostic quiz in Week 1.

.. list-table::
   :header-rows: 1
   :widths: 25 15 20 40
   :class: compact-table

   * - Quiz
     - Week
     - Date
     - Covers
   * - Diagnostic (ungraded)
     - 1
     - 01/27
     - ROS 2 prerequisites
   * - Quiz 1
     - 4
     - 02/17
     - L1 to L3
   * - Quiz 2
     - 5
     - 02/24
     - L4
   * - Quiz 3
     - 7
     - 03/10
     - L5 and L6
   * - Quiz 4
     - 10
     - 03/31
     - L7 and L8
   * - Quiz 5
     - 12
     - 04/14
     - L9 and L10

- Quizzes are given at the start of class, on Canvas or on paper, and last
  10 to 20 minutes.
- **Closed notes**: no notes, no external tools, no AI.
- Quizzes are taken in class, unless you are registered in the online
  section. Absent students cannot take a quiz.

.. note::

   The self-check quizzes on each lecture page are a different thing
   entirely. Those are **not submitted and not graded**.


Team Formation
--------------

- All project work is team-based.
- **Team size: 3 students.** Teams of 2 are allowed only with instructor
  approval, for example when the class size does not divide evenly or for
  online students. Teams of 4 or more are not permitted.
- **Teams are formed in Week 2**, in L2, the day GP1 is posted.
- Teams stay together for all four group projects and the final demo, so the
  peer-review record builds up over the semester.
- A team change needs a written reason and instructor approval. It is
  expected only when peer review documents a lasting imbalance.


The Team Charter
~~~~~~~~~~~~~~~~

When teams form in Week 2, the first deliverable is not code. Each team
writes one page and posts it to ELMS before L3:

- **Who owns what.** Name a primary and a backup for each part of the
  system. Ownership is accountability, not exclusivity.
- **When you meet.** A recurring time, agreed now.
- **How you use git.** Branch names, who reviews, what must pass before a
  merge.
- **What happens when someone goes quiet.** How long before the team raises
  it, and with whom.
- **How you will use AI tools.** One convention for the whole team.


.. _peer-evaluation:

Peer-Review Contribution
------------------------

The peer-review contribution is **15%** of the course grade. Your teammates
assess it, not the instructor, and it reflects your contribution inside the
team. It is separate from class participation, which is not graded.

The form
~~~~~~~~

After each group project and after the final demo, every student fills in a
peer-review form on ELMS-Canvas and rates each teammate (not themselves) on
five dimensions:

.. list-table::
   :header-rows: 1
   :widths: 5 30 65
   :class: compact-table

   * - #
     - Dimension
     - What it asks
   * - 1
     - Technical contribution
     - Did this teammate contribute to the technical work: code, design
       decisions, debugging, integration?
   * - 2
     - Reliability and communication
     - Did this teammate come to meetings, answer messages, and deliver
       agreed work on time?
   * - 3
     - Quality of work
     - Could you build on their work (clean, complete, tested), or did you
       have to redo it?
   * - 4
     - Knowledge and skill
     - Did this teammate bring the knowledge needed, or work to learn it?
   * - 5
     - Team-player behavior
     - Did this teammate help others, listen, accept feedback, and keep the
       team constructive?

Scale: **5** = consistently outstanding, **4** = above expectations,
**3** = meets expectations, **2** = below expectations, needs improvement,
**1** = well below expectations, raises concern.

- A short comment (one to three sentences) is required for each teammate. It
  is required in particular for any rating of 2 or below, or of 5.
- Uniform ratings (all 3s or all 5s for every teammate) with no written
  justification are returned and must be redone.
- **Confidential concern flag.** Each form has a checkbox: "I want the
  instructor to follow up about team dynamics on this project." Checking it
  starts a private check-in with the instructor. Your teammates are not told.

How the score is computed
~~~~~~~~~~~~~~~~~~~~~~~~~

- For each project, your peer score is the mean of your teammates' ratings
  over the five dimensions, put on a 0 to 100 scale: score = 80 + 10 ×
  (mean − 3), so a mean of 1 gives 60, 3 gives 80 and 5 gives 100.
- Your five project peer scores are averaged with equal weight, and the
  average is worth 15% of the course grade.
- The instructor reviews outliers before applying them. If one teammate
  rates you 1 on every dimension and another rates you 4, the instructor
  reads the comments and decides whether to keep both ratings, discard the
  outlier, or talk with the team.

Rules
~~~~~

- Ratings are visible to the instructor only, never to the student rated.
- One low rating from one teammate cannot by itself put you below 70 in this
  category. Any team-averaged peer score under 70 is reviewed by the
  instructor before it is applied.
- The instructor may override peer scores in documented cases of trading
  ratings ("you rate me high, I rate you high") or coordinated retaliation.


.. _ai-disclosure:

Academic Integrity and Generative AI
------------------------------------

Some submissions are checked with Turnitin on ELMS. The University's Code of
Academic Integrity applies to all work, and all cases of academic dishonesty
are handled under it.

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30
   :class: compact-table

   * - Assessment
     - Open notes
     - Use AI
     - Work in teams
   * - Group projects and final demo
     - Yes
     - Yes, see below
     - Yes
   * - Quizzes
     - No
     - No
     - No

- **AI tools are required** in GP4 and the final demo: the system you build
  calls an LLM and a VLM. Your team must understand, design and debug the
  code that calls them.
- You may use AI tools to clarify concepts or look up syntax on any group
  project, but the submitted code and report must be your team's own work.
- **Submitting AI-generated code that your team cannot explain is a
  violation.** Any team member may be asked to explain any part of the
  submission.
- Course assistance websites (such as CourseHero) are not permitted as
  sources unless the instructor explicitly allows them.
- Every team member signs the honor pledge on each group project
  submission: *"I pledge on my honor that I have not given or received any
  unauthorized assistance on this group project."* The same pledge applies
  to each quiz.


.. _course-schedule:

Course Schedule
---------------

Lectures meet on **Wednesdays**. The first lecture is **January 27, 2027**
and the last class is **May 5, 2027**. Spring break (**Mar 14 to 21**)
includes Wednesday Mar 17, so there is no class that week. Dates below are
given as MM/DD.

**Color key:** :reading:`pre-read material`; :quiz:`quizzes`;
:assignment:`group projects and final demo posted or due`;
:no-class:`no class`.

.. list-table::
   :header-rows: 1
   :widths: 10 8 34 20 28
   :class: compact-table schedule-table

   * - Date
     - Week
     - Topic
     - Lecture
     - Deliverable
   * - 01/27
     - 1
     - Course Overview and ROS 2 Refresher
     - L1
     - | :reading:`Read before class: ROS 2 Refresher`
       | :quiz:`Diagnostic quiz (ungraded)`
   * - 02/03
     - 2
     - System Architectures for Agentic Robotics
     - L2
     - | Teams formed
       | :assignment:`GP1 posted`
   * - 02/10
     - 3
     - Knowledge Representation for Agentic Robotics
     - L3
     - Team charter due
   * - 02/17
     - 4
     - Behavior Trees for Task Execution
     - L4
     - :quiz:`Quiz 1`
   * - 02/24
     - 5
     - Sensing and Perception for Robotic Systems
     - L5
     - | :quiz:`Quiz 2`
       | :assignment:`GP1 due, GP2 posted`
   * - 03/03
     - 6
     - Task-Level Planning with PDDL
     - L6
     - :reading:`Read before class: PDDL Primer`
   * - 03/10
     - 7
     - Plan Execution Patterns with Behavior Trees
     - L7
     - | :quiz:`Quiz 3`
       | :assignment:`GP2 due, GP3 posted`
   * - 03/17
     -
     - :no-class:`Spring break: no class`
     -
     -
   * - 03/24
     - 9
     - LLM Agents I: Agent Loops, Tool Use, and Structured Output
     - L8
     - :reading:`Read before class: LLM Prompting, MCP`
   * - 03/31
     - 10
     - LLM Agents II: VLM Grounding and Agentic Replanning
     - L9
     - | :quiz:`Quiz 4`
       | :assignment:`GP3 due, GP4 posted`
   * - 04/07
     - 11
     - Frames, Transforms, and Motion Planning
     - L10
     -
   * - 04/14
     - 12
     - Recovery, Robustness, and Failure Handling for Agentic Systems
     - L11
     - | :quiz:`Quiz 5`
       | :assignment:`Final demo specification posted`
   * - 04/21
     - 13
     - Evaluation and Measurement Science for Agentic Systems
     - L12
     - :assignment:`GP4 due`
   * - 04/28
     - 14
     - The Physical AI Frontier: VLAs, Robot Foundation Models, and World
       Models
     - L13
     -
   * - 05/05
     - 15
     - Final demo and presentations
     -
     - :assignment:`Final demo`

.. note::

   This is a tentative schedule, subject to change as necessary. Monitor
   ELMS-Canvas for current deadlines. If the university closes for a long
   period, the schedule, deadlines and assignments are adjusted to the dates
   missed.


Final Project: Building an Agentic Factory Cell
-----------------------------------------------

The course grade is built around a single **final project** made of four
cumulative group projects (GP1 to GP4) and a final demo. Each GP extends
your team's system from the previous one, so that by the final demo your
team has an LLM agent that runs a full ARIAC 2025 trial.

The robot arms move through the **course skills package**: Python ROS 2
actions for picking and placing parts, built on MoveIt 2 and provided with
GP1. Your team decides what the robots do; the skills package carries it
out. L10 shows how the skills are built. Your team moves the AGVs with
ARIAC's own AGV move action.

In ARIAC 2025, a cell on the inspection conveyor reaches the inspection
robot only if your team has submitted a passing inspection report for it.
A failing or missing report keeps the inspection door closed, and the cell
drops into the inspection bin. So every project submits an inspection report
for every cell.

.. list-table::
   :header-rows: 1
   :widths: 30 10 10 10 40
   :class: compact-table

   * - Component
     - Posted
     - Due
     - Weight
     - Cumulative Output
   * - GP1: Behavior Tree for One Kit
     - Week 2
     - Week 5
     - 10%
     - A ``py_trees_ros`` tree that builds and ships one kit.
   * - GP2: Cell Inspection
     - Week 5
     - Week 7
     - 10%
     - Lidar within the sensor budget, defect detection from point clouds,
       an inspection report for every cell.
   * - GP3: PDDL Planner and BT Executor
     - Week 7
     - Week 10
     - 10%
     - A PDDL plan for Task 1, run by a plan-to-BT executor, with
       replanning.
   * - GP4: LLM Agent with VLM Grounding
     - Week 10
     - Week 13
     - 10%
     - An LLM agent in place of the PDDL planner, grounded by a VLM, that
       handles the ARIAC challenges.
   * - **Final demo**
     - Week 12
     - Week 15
     - 20%
     - GP1 to GP4 integrated for Task 1 and Task 2, run by the instructor
       from your Docker image on an unseen trial, with a presentation.

**GP1: Behavior Tree for One Kit.** Build a ``py_trees_ros`` behavior tree
that builds one kit: feed cells onto the inspection conveyor, submit a
passing inspection report for each cell, read their voltages, recycle the
cells outside the voltage range, place four cells on an AGV tray, move the
AGV to shipping and submit the kit. The leaves call the course skills
package and the ARIAC services. No defect detection yet. GP1 comes with a
starter tree: Weeks 2 and 3 go to setup, the skills package and the ARIAC
services, and the tree work follows L4 (Week 4).

**GP2: Cell Inspection.** Place lidar sensors around the inspection
conveyor within the ARIAC sensor budget, as ARIAC 2025 requires, and detect
dents, scratches and bulges from the point clouds. Submit an inspection
report for each cell before it reaches the inspection door: a failing
report sends the cell into the inspection bin. The GP1 tree then reads the
voltage of each cell that passes and places or recycles it. Keep one record
per cell that joins the two checks, and report the precision and recall of
your detector.

**GP3: PDDL Planner and BT Executor.** Write a PDDL domain for Task 1 with
the two inspection robots and the AGVs, and execute its plans through a
behavior tree built from the plan. Replan when a cell fails inspection.
Choosing four cells that meet the kit voltage tolerance is a numeric
problem, so it is a separate selection step.

**GP4: LLM Agent with VLM Grounding.** Replace the PDDL planner with an LLM
agent that calls the robot skills as tools (through MCP if you choose) and
returns structured output checked against a JSON schema. A VLM describes
the cells for the agent. Test the agent on the situations GP3's domain does
not model: a conveyor malfunction, a voltage tester malfunction and
high-priority orders. (The vacuum tool malfunction affects only Task 2, so
the final demo tests it.) Compare it with GP3 on the same trials.

**Final demo.** Integrate GP1 to GP4 into one system that runs a full trial,
Task 1 and Task 2 (the assembly robots and the gantry welder). A hosted
embodied-reasoning model judges cell defects from camera images over the
inspection conveyor, and is scored with precision and recall on the same
cells as your GP2 lidar detector. The code freeze is Friday, April 30, 2027, at 11:59 pm. The trial used
for grading is unseen: before the Week 15 class, the instructor runs every team's Docker image on
it, on one machine, and each team presents with its recorded run.
Each team presents for 5 to 6 minutes: architecture, design decisions,
failure modes met and how they were handled, followed by 3 minutes of
questions, one for each team member. Your solution runs from a
Dockerfile, as ARIAC requires.

.. note::

   See the :doc:`Final Project </assignments/index>` page for the
   specifications, rubrics and submission instructions as each project is
   posted.


Required Software and Tools
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Component
     - Details
   * - Operating System
     - Ubuntu 24.04 LTS (Noble Numbat)
   * - ROS 2
     - Jazzy Jalisco
   * - Simulator
     - Gazebo Harmonic
   * - Testbed
     - ARIAC 2025 (Docker or native)
   * - Robotics tools
     - MoveIt 2, ``py_trees_ros``, OpenCV, Unified Planning Framework or
       Fast Downward
   * - AI access
     - From GP4 on: Google Gemini by default. While it develops, your team uses its own
       free-tier Gemini API key. The course Gemini key runs only the graded
       GP4 and final demo evaluations. A team may run a local open-weight
       model instead, as the GP4 and final demo pages allow.
   * - IDE
     - Visual Studio Code (recommended)
   * - Version Control
     - Git + GitHub

See the :doc:`ARIAC Testbed </ariac/ariac>` pages for installation.


University Policies
-------------------

Graduate courses follow the University of Maryland's course-related
policies: academic integrity, student and instructor conduct, accessibility
and accommodations, attendance and excused absences, grades and appeals,
and copyright. See https://gradschool.umd.edu/course-related-policies for
the full set. The Canvas PDF lists the campus resources (Accessibility &
Disability Service, counseling, basic needs, veteran resources) and the
mandatory reporting notice.
