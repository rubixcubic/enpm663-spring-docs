====================================================
Final Demo: Full ARIAC Trial, Unseen
====================================================

.. card:: Final Demo: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 12 to Week 15), posted 04/14, demo 05/05
      * - **Weight**
        - 20% of the course grade
      * - **Lectures**
        - L10 to L13
      * - **Team Size**
        - 3 students
      * - **Submission**
        - Canvas + GitHub repository link + code-freeze tag
      * - **Code freeze**
        - Friday, April 30, 2027, at 11:59 pm


.. admonition:: Specification draft
   :class: note

   This page is the specification draft for the final demo. The provided
   code (the course skills package, with its assembly robot and gantry
   welder skills) is released with the project, on the day the final demo
   specification is posted in Week 12. The code freeze is Friday, April 30, 2027, at 11:59 pm.
   The tag name is set in that specification. The grading rubric is at the
   end of this page.


.. admonition:: AI tools
   :class: warning

   AI tools are **required** in the final demo: the system you build calls
   an LLM, a VLM and a hosted embodied-reasoning model. Your team must
   understand, design and debug the code that calls them. You may also use
   AI tools to clarify concepts or look up syntax. Your team is responsible
   for every line you submit, and any member may be asked to explain any
   part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

The final demo integrates GP1 to GP4 into one system that runs a full ARIAC
2025 trial:

- **Task 1:** inspection and kit building, as in GP1 to GP4.
- **Task 2:** module construction.

The trial can contain any of the ARIAC challenges: conveyor malfunction,
voltage tester malfunction, vacuum tool malfunction and high-priority
orders. It is an **unseen trial**: a trial file no team has seen, with its
own ID, seed and challenge start times. Your team practiced on other trials,
so you know the kinds of events, but not when they happen.

Task 2
~~~~~~

Task 2 builds a battery module from a finished kit:

1. Assembly robot 1 (a UR5e) places the four cells in a bottom shell with
   the right polarity.
2. Assembly robot 2 changes to the VG2 vacuum tool and places the top
   shell. The top shell spawns at a random pose on the assembly table, so
   your team needs a sensor to find it.
3. The gantry welder makes four top welds.
4. Assembly robot 2 changes to the VG4 tool and flips the module.
5. The gantry welder makes two bottom welds.
6. Your team submits the module.

The embodied-reasoning step
~~~~~~~~~~~~~~~~~~~~~~~~~~~

One perception step uses a hosted **embodied-reasoning model**: a model
that answers spatial questions about an image. An example is Google's
Gemini Robotics ER (on 2026-10-12 the Gemini API listed it as
``gemini-robotics-er-2-preview``). The model judges cell defects from a
camera image of the inspection conveyor (L13 shows where the course's
camera sits, beside the belt, and why). It is scored with precision and
recall on the same cells as your GP2 lidar detector: learned vision against
classical lidar. Whether defects 0.84 to 2.49 mm deep (ARIAC's training
cells, measured in L5) show in the camera image is part of the result.

Gemini Robotics ER is the course example. Your team may use another
vision-language model instead, a Google model that runs on the course key or
a local model, if it reports the same comparison:
precision and recall per defect type on the same cells, latency and cost.
The instructor runs every team's image with one course API key (see the run
rules), so every team gets the same quota. The course key runs only these
graded evaluations: while it develops, your team uses its own free-tier
Gemini API key.

Lectures L10 to L13 cover what the final demo adds: the motion layer under
the skills package (L10), recovery (L11), evaluation with the ARIAC scoring
formula (L12) and the embodied-reasoning model (L13).


How the Demo Runs
-----------------

The instructor runs every team's system before the Week 15 class. Class time
is for presentations.

Why the run is not in class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARIAC's ``TIME_LIMIT`` counts simulation time. Gazebo ran at about 0.37
times real time in the course's ARIAC container on the instructor's
development PC (measured while building the skills package). So the 900 s
of the ARIAC example trial takes:

1. 900 s / 0.37 = 2432 s of wall clock,
2. 2432 s / 60 = about 41 minutes.

That does not fit a class session with every team. Running every team on
one machine also keeps the run fair: each team gets the same hardware and
the same ratio of simulation time to wall-clock time for its LLM calls.
The instructor times a dry run on the evaluation machine to get its real
figure.

The run rules
~~~~~~~~~~~~~

.. important::

   1. By the code-freeze deadline, your team pushes its code-freeze tag and
      submits the team configuration file.
   2. Before class, the instructor builds your Docker image from that tag,
      on the same machine as every other team, and runs it on the unseen
      trial in the ARIAC App: a new database, recording on, and no testing
      cheat (the App's cheats start a run at a later stage).
   3. The instructor builds every image on Saturday, May 1. If your image
      does not build, the instructor emails your team, and you have 24 hours
      to push a fix tag that changes only build files (the Dockerfile and
      dependency lists), not code. Your team then loses the 10 points of
      "Builds and runs from the Dockerfile"; the rest is graded normally. If
      the fixed image still does not build, the run criteria (75 points)
      score 0.
   4. The run goes until ``TIME_LIMIT`` or until your system ends the
      competition. A crash of your code is part of the graded run, not a
      reason to restart.
   5. If the run fails for a reason outside your code (the evaluation
      machine crashes, or a model provider has an outage), the instructor
      runs a backup trial with the same parameters.
   6. The instructor sends each team its own run results and videos
      privately. Scores are never shown to the class.

Your team never receives the demo trial. Your code learns the trial only
through ARIAC topics and services during the run. **Code that tries to read
a trial file is not allowed**, and the instructor checks the tagged code for
it.

ARIAC evaluates its own competitors the same way: its Submission page says
the Dockerfile "tells the evaluation system how to build and run your code"
and that "NIST will evaluate your code using specific tagged versions."

The Week 15 class
~~~~~~~~~~~~~~~~~

Each team presents with its recorded run. The lesson plan gives each team a
10-minute slot: 6 minutes of talk (5 minimum), 3 minutes of questions (one
for each team member) and 1 minute of change-over. The presentation order is drawn at random and posted
in Week 14. RO01 (online) teams are run on the same machine, and they
present live in the class video meeting, in the posted order.

Each RO01 team also uploads its talk as a 5 to 6 minute video to
ELMS-Canvas by Tuesday, May 4, at 11:59 pm. If the team cannot connect in
its slot, the instructor plays the video, and the team answers the questions
in a video call with the instructor within two days. The video is not graded
unless it is played.


Learning Objectives
-------------------

After completing the final demo, you will be able to:

- Integrate behavior trees, perception, planning and an LLM agent into one
  system that runs Task 1 and Task 2.
- Recover from each ARIAC 2025 challenge.
- Use a hosted embodied-reasoning model to judge cell defects from camera
  images, and compare its precision and recall with your GP2 lidar
  detector on the same cells.
- Evaluate the system with the ARIAC scoring formula before the demo.
- Package a ROS 2 system in a Dockerfile.
- Present the architecture, the design decisions and the failure modes
  met.


Provided Resources
------------------

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - Resource
     - What it gives you
   * - Your team's GP1 to GP4 packages
     - The system you integrate.
   * - Course skills package
     - Now including the assembly robot and gantry welder skills.
   * - Final demo specification
     - Posted in Week 12: the run rules, the trial parameters that may vary
       and their ranges (not their values), the code-freeze tag name, and
       the grading procedure.
   * - An embodied-reasoning model
     - Gemini Robotics ER is the course example; another VLM is allowed if
       it runs on the course key (a Google model) or locally, and your team
       reports the same comparison. The evaluation runs use one course key. See :doc:`/ariac/ai_setup`.


Tasks
-----

.. dropdown:: Task 1: Extend the system to Task 2
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** submitted modules.

   **Requirements:**

   - Insert the bottom shell, place the four cells, change tools, locate
     and place the top shell, make the four top welds, flip the module,
     make the two bottom welds and submit the module.
   - Place the sensor that Task 2 needs to find the top shell, and keep the
     total sensor cost within the $9600 budget.

.. dropdown:: Task 2: Recover from every challenge
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a run that continues after each challenge.

   **Requirements:**

   - Make every challenge recoverable in the integrated system: conveyor,
     voltage tester and vacuum tool malfunctions, and high-priority orders.
   - Vacuum tool malfunction (new in the final demo): a grasp attempt with
     VG2 or VG4 fails, and the grasp service reports the failure. ARIAC's
     expected handling is a local retry: move the gripper away and try the
     grasp again.
   - Log every detection and every recovery with its time stamp.

.. dropdown:: Task 3: Add the embodied-reasoning step
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a measured comparison of learned vision against lidar.

   **Requirements:**

   - Call the embodied-reasoning model on a camera image of each cell on
     the inspection conveyor.
   - Measure it against your GP2 lidar detector on the same cells:
     precision and recall per defect type, latency and cost per call, and
     the number of cells used.
   - The model call must also run during the evaluation run, and show in
     its log.

.. dropdown:: Task 4: Test on trials you have not tuned for
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a system that works on a trial it has not seen.

   **Requirements:**

   - Test on varied trial seeds and challenge mixes, within the ranges the
     specification gives.
   - Compute the ARIAC run score of each test run (L12).

   .. tip::

      **Set the run count first.** Choose the number of runs for each test
      configuration before you run it, from the smallest gap your tests must
      detect.
      :ref:`l12-runs-a-claim-needs` shows how, in L12's frames "Comparing
      Two Systems" and "A 20-Run Batch".

.. dropdown:: Task 5: Write the Dockerfile
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** an image the instructor can build and run with no help.

   **Requirements:**

   - Write the Dockerfile, and confirm that the system builds and runs from
     it on a machine other than the developer's.
   - The image reads API keys at run time. No key is in the repository or
     in the image. For the evaluation run, the instructor passes one course
     key as an environment variable; your README names the variable your
     model's SDK reads (``GEMINI_API_KEY`` for Gemini).
   - Before the code freeze, build the image from your tag and test it on a
     practice trial in the ARIAC App, with a new database and no cheat.

.. dropdown:: Task 6: Prepare the presentation
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a 5 to 6 minute talk that explains your system and your run.

   **Required content:**

   - The architecture on the L2 three-layer diagram: the LLM agent and VLM,
     the behavior tree, the skills package and MoveIt 2, perception.
   - Design decisions and their reasons: for example the sensor choice and
     cost, where the agent decides and where the tree decides, and what the
     GP3 planner still does.
   - The recorded run: the run score and its terms, and one clip showing a
     failure or a challenge and how the system handled it.
   - The embodied-reasoning step: its defect calls, with precision and
     recall against the GP2 lidar detector on the same cells, and its
     latency and cost per call.
   - Failure modes met during development, and how they were caught (L11).


Deliverables
------------

1. The integrated codebase, running from a Dockerfile, in your team's
   repository. Submit the link on Canvas before the demo.
2. The code-freeze tag and the team configuration file, by the code-freeze
   deadline. The instructor runs the image on the unseen trial before class.
3. A presentation (5 to 6 minutes): architecture, design decisions, failure
   modes met and how they were handled.
4. The embodied-reasoning comparison table.
5. The honor pledge, signed by every team member.


Submission Checklist
--------------------

.. admonition:: Before the code freeze, check every item
   :class: tip

   - [ ] The image builds from the tag with the README commands, on a
         machine other than the developer's.
   - [ ] The image ran a practice trial in the ARIAC App, with a new
         database and no cheat.
   - [ ] No API key is in the repository or the image.
   - [ ] No code reads a trial file.
   - [ ] The total sensor cost, top shell sensor included, is within $9600.
   - [ ] The run log shows each challenge's detection and recovery, and the
         embodied-reasoning calls.
   - [ ] The comparison table states the cells used, precision and recall
         per defect type, latency and cost.
   - [ ] Every team member signed the honor pledge.
   - [ ] After the demo, each member fills in the peer-review form (see
         :ref:`peer-evaluation`).


Grading Rubric
--------------

.. admonition:: How the points add up
   :class: note

   The total is 100 points, scaled to 20% of the course grade: 75 points
   for the run and 25 for the class session (presentation and questions).

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Criterion
     - Points
     - How the grader checks it
   * - Builds and runs from the Dockerfile
     - 10
     - Before the demo, the grader builds the image and starts the system
       with the README commands on the grading machine. An image that needs
       a build-only fix (run rules, item 3) loses these 10 points.
   * - Task 1 on the unseen trial
     - 15
     - ARIAC run results. Points = 15 x (kits accepted / kits wanted),
       high-priority kits included. Example: 3 of 4 kits accepted gives
       15 x 3 / 4 = 11.25 points.
   * - Task 2 on the unseen trial
     - 15
     - ARIAC run results. Points = 15 x (modules accepted / modules
       wanted).
   * - Challenges handled
     - 15
     - The grader compares the trial's challenge list with the run log:
       each challenge detected, a recovery action taken, and the run
       continuing. The 15 points are split equally among the challenges in
       the trial. For each challenge, half its share is for detecting it,
       and the other half for the recovery action and the run continuing.
   * - Safe run
     - 5
     - ARIAC penalty table for the run: 5 points minus 1 for each penalty
       event (robot collisions, AGV collisions, objects on invalid surfaces),
       not below 0.
   * - Embodied-reasoning step
     - 15
     - The run log shows the model call during the evaluation run, and the
       grader reads the comparison table with the GP2 lidar detector: same
       cells, precision and recall per defect type, latency and cost, and
       the number of cells used. The points are for doing the step and
       reporting it honestly; the model's precision and recall do not change
       the points.
   * - Presentation
     - 15
     - The grader times the talk (5 to 6 minutes) and checks the four
       required parts: architecture, design decisions, failure modes met,
       how they were handled.
   * - Questions
     - 10
     - Each team member answers a question about a part of the code that
       member did not present.

The points add up to 10 + 15 + 15 + 15 + 5 + 15 + 15 + 10 = 100.


Common Mistakes
---------------

.. danger::

   - **Testing only on the GP trials.** The demo trial is new. Test on
     other seeds and challenge mixes.
   - **An image that only builds on one laptop.** Build and run it on a
     second machine before the code freeze.
   - **A key baked into the image.** Read API keys at run time.
   - **Expecting a restart.** A crash is part of the graded run.
   - **Reading the trial file.** The trial reaches your system only through
     ARIAC topics and services.


Tips for Success
----------------

.. tip::

   **Score every test run.** Compute the ARIAC run score for each practice
   run (L12). Fix first the term that costs you the most points.

.. tip::

   **Start a challenge test matrix in Week 12.** List each challenge, the
   trial that triggers it, and whether your system detected it and
   recovered. Fill it in as you test.
