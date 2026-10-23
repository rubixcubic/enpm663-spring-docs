====================================================
Changelog
====================================================

All notable changes to the ENPM663 Spring 2027 course documentation are
recorded here.


.. dropdown:: v0.4.23: New L6 Planner Timings (2026-10-23)
   :icon: tag
   :class-container: sd-border-success
   :open:

   - **L6:** ``fd_summary.txt`` comes from a new run of the Fast Downward
     example. The plans and the expanded-state counts are unchanged; the
     search times are new measurements. The exercise answer that quotes the
     large problem's search time now says 12.539839 s.


.. dropdown:: v0.4.22: The Code-Freeze Tag Is final-demo (2026-10-23)
   :icon: tag
   :class-container: sd-border-success

   - **Final demo:** the code-freeze tag is named ``final-demo``, and a team
     whose image does not build on May 1 pushes ``final-demo-fix``. The final
     demo page, the L13 pages and the syllabus say so.


.. dropdown:: v0.4.21: Wording Revised; Quizzes Are 20 Minutes (2026-10-23)
   :icon: tag
   :class-container: sd-border-success

   - **Every lecture page** follows its revised slides: shorter sentences, each
     caveat stated once, and some slide titles renamed (for example L6's
     "Where PDDL Strains" is now "Limits of PDDL").
   - **Corrections:** L8's step limit is 15, as in ``orchestrator.py``; L9
     names the three challenges GP4 tests.
   - **Quizzes:** every quiz, the Week 1 diagnostic included, is 20 minutes.
     The diagnostic also covers Git and GitHub.
   - **GP3:** the reflection asks what PDDL modeled well and what was hard to
     model.
   - **Glossary:** "Bonus gate" is now **Aborted run (ARIAC)**.
   - **Syllabus:** the course description, prerequisites and email line are
     shorter; the facts are unchanged.


.. dropdown:: v0.4.20: GP4 Due Friday, April 23 (2026-10-22)
   :icon: tag
   :class-container: sd-border-success

   - **GP4** is now due Friday, April 23, 2027, at 11:59 pm (it was due
     Wednesday, April 21). The syllabus, the schedule, the GP4 page and the L9
     to L12 pages say so.
   - **Lecture 1:** the diagnostic quiz also covers Git and GitHub
     (branches, merge conflicts and pull requests).


.. dropdown:: v0.4.19: Inspection Door, L5 Bonus, L9 Recap (2026-10-22)
   :icon: tag
   :class-container: sd-border-success

   - **Inspection door:** without a passing report the door stays closed and
     the cell drops into the inspection bin; the door does not push it. Fixed
     in L1, L2, L3, L5, L7 and L13, GP1, GP2 and the syllabus.
   - **Lecture 5:** a new slide, "The $9600 Budget and the Sensor Cost
     Bonus", gives the bonus formula with a worked line.
   - **Lecture 9:** the recap now says what the L8 agent did: after every
     call it read the testers, the conveyor and agv1, and ``guard()`` checked
     the next call. No code picks between retry, wait and replan; the model
     chooses.
   - **LLM prompting pre-read:** it names Google Gemini, or a local open-weight
     model, as the course's choice.


.. dropdown:: v0.4.18: Git and GitHub Are Prerequisites (2026-10-20)
   :icon: tag
   :class-container: sd-border-success

   - The syllabus and the home page list Git and GitHub under Prerequisites:
     clone, branch, commit, push and pull, resolve a merge conflict, and open
     and review a pull request. The course does not teach them.


.. dropdown:: v0.4.17: Lecture Pages Corrected After Independent Checks (2026-10-18)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 1

   - **Robot interfaces:** a new table, "What ARIAC Gives Each Robot". Only
     the inspection robots and assembly robot 1 have a gripper action;
     assembly robot 2 uses vacuum tool services, and the gantry welder a
     weld service. Quiz Q2 follows.
   - **Cancel:** the action demo cancels because it runs on a multi-threaded
     executor. On a single-threaded executor the goal ends SUCCEEDED.
   - **API keys:** your team uses its own free-tier Gemini key while it
     develops; the course key runs only the graded GP4 and final demo
     evaluations.
   - The meaning of each word in "agentic physical AI", and why the QoS demo
     shows 19 of 20.

   .. rubric:: Lecture 2

   - The react-only rule says which rules fire in one pass.
   - Helix is named as the two-system VLA, and the page says why the course
     keeps the modular stack.
   - The recovery row, the Brooks and Universal Robots quotes with their
     sources, and the Next Class wording are corrected.
   - Larger text in the figures.

   .. rubric:: Lecture 3

   - **Expanded:** definitions at first use (JSON, JSON record, PDDL fact,
     4D/RCS node), the JSON world-model record, four figures and worked
     examples.
   - **Fourth cell:** five readings per average, as in L4, and GP1 Task 4's
     rule decides cell c4 (it is recycled). The kit check is cited from
     ``validate_kit()``.
   - Inspection results: your team submits ``InspectionReport.msg``; ARIAC
     sends none. Seven exercises.

   .. rubric:: Lecture 4

   - **Pattern 3** checks the kit before every place, as GP1 does, with the
     three-cell window 10.45 V to 11.15 V.
   - **Chance:** a new section works out whether a 3.75 V reading can be
     trusted (``kit_spread.py``).
   - Larger figure text; the repeat-sets output is measured again (3 to 6
     of 10).

   .. rubric:: Lecture 5

   - **Update rates:** ARIAC accepts lidar at 10 or 20 Hz, cameras at 30 Hz,
     and break beam and distance sensors at 10 or 30 Hz. The GP2 page says
     the same.
   - The L1 result is 50 of 50. The two missed dents are 0.82 and 0.91 mm
     deep, with the reason each is missed.
   - Three slides moved to the exercises: Exercise 2 Part 6 (what a cheaper
     lidar gives up) and a new Exercise 6 (what the four-lidar layout costs).
   - **Inspection door:** without a report, the door stays closed and the cell
     drops into the inspection bin. The L2 quiz says the same.
   - Larger figure text.

   .. rubric:: Lecture 6

   - **Translator:** Fast Downward drops only the actions a relaxed test
     rules out, so some that can never apply stay (232 of 256 in the
     example).
   - **Look-ahead kit:** a 14.50 V kit is in range by the averages, but
     ARIAC would reject it about 1 time in 7 to 1 in 11
     (``kit_margin.py``).
   - Kit examples follow GP1's check. "Cost" in L6 means plan length; in GP4
     it means tokens or dollars. LM-cut and LAMA are defined.
   - Larger figure text; the objects and the timeline are split in two.

   .. rubric:: Lecture 7

   - **Common bugs:** a misspelled blackboard key stops the tick with an
     error, or the reader gets an old value.
   - ``check-voltage`` and queued cells are marked as new in L7.
   - GP3's Timeout, ``SyncActionNode`` (it must never return RUNNING), the
     0.52 s arithmetic, the limit margin and a GP1 window note.
   - Ten slides moved to this page, among them the factory function, the
     PDDL-to-ROS mapping and the BehaviorTree.CPP comparison. The slides point
     to each one.
   - Larger figure text.

   .. rubric:: Lecture 10

   - **Robot interfaces:** the L1 table, so not every robot has a gripper.
   - **Conveyor pick:** the page now teaches what ``pick_from_conveyor``
     does in v0.2.0: a fixed side catch, its refusals, and the stop on a
     belt change. New demo runs A to D and a new Exercise 5.
   - **Pilz:** a course measurement replaces a ROS 1 test. Execution
     retries, and one zone lock (the tester area).
   - Larger figure text.

   .. rubric:: Lecture 11

   - **LLM output checks** use L8's ten tools and its check order: tool,
     schema, guard.
   - The recovery rule has L9's three cases (retry, wait, replan), and the
     seven skill results from L10 each get a response.
   - Runs C and D follow the skills' one-goal-per-arm and cancel rules.
     Local and global recovery are defined before first use.
   - Larger figure text.

   .. rubric:: Lecture 12

   - **Standard error:** the spread of one success rate. Two sets of runs
     differ by about 1.41 times it.
   - **How many runs a claim needs:** two new sections, Comparing Two
     Systems (126 runs per system for a 0.10 gap) and A 20-Run Batch
     (``batch_bar.py``, whose simulation of 1,000,000 batches matches the
     exact numbers).
   - GP4's required columns, the price of a false negative (GP1's check kit
     quality call), the inspection door and the angle test are corrected.
   - Larger figure text.

   .. rubric:: Lecture 13

   - **Final demo:** the code freeze is Friday, April 30; new sections give
     the dates, deliverables and grading.
   - Xia et al. and DeepFleet now say what their sources say, and the
     two-system claim is scoped to SmolVLA (Gemini Robotics can judge
     progress and success).
   - Bonuses are maxima that the run scales down. Larger figure text.
   - **Embodied-reasoning demo:** two runs recorded with
     ``gemini-robotics-er-2-preview`` on 12 ARIAC camera images. In Run 1 the
     schema check rejects every answer (each is inside a code fence), and the
     free tier's 5 requests per minute stops the run at call 9. Run 2 asks for
     structured output and scores all 12 cells. The scripted run stays as
     the offline mode. Four slides moved to this page.

   .. rubric:: Glossary

   - New entries: **JSON**, **JSON record**, **Fact (PDDL)**, **Node
     (4D/RCS)**, **Class, relation and instance (ontology)**.
   - Updated: **Fast Downward**, **Executor (plan)**, **Inspection report**,
     **4D/RCS**, **Parameterized grasp**, **Local recovery**, **Global
     recovery**, **Standard error** and **Inspection door**.

   .. rubric:: Projects and syllabus

   - **API keys:** the syllabus, GP4 and the final demo say who pays: your
     team's own free-tier Gemini key while it develops, the course key for
     the graded GP4 and final demo evaluations.
   - **GP3 Task 6:** the trigger is "a queued cell fails inspection".
   - **Models:** GP4 and the final demo accept Gemini or a local open-weight
     model. The AI Access page is rewritten for Gemini: how to create a free
     key, where to keep it, and the free tier's limits.
   - **Final demo Task 4:** a tip on choosing the runs per test configuration
     from L12's "How Many Runs a Claim Needs".
   - **Course Skills Package:** the page describes v0.2.0, lists the robots'
     real controls, and says when a stopped belt refuses a catch.


.. dropdown:: v0.4.16: L8 and L9 Run a Real Gemini Agent on ARIAC (2026-10-17)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Real agent:** Run 1 is now Google's Gemini (``gemini-3.5-flash-lite``)
     running the course skills on ARIAC. It filled AGV 1 slot 1 in five
     calls. Run 2 and the validator stay scripted, so you can see each
     guard refuse a bad call.
   - **MCP:** the server serves ten tools (7 skills and 3 readings) against
     ARIAC, and the client lists them and calls three.
   - **Numbers:** the token growth and the cost table use the tokens Run 1
     measured. Every real output says when it was recorded and with which
     model; a rerun gives different answers.
   - **Code page:** how the demonstrations run (the key file, the container,
     ``run_sim_demo.sh``), every script, and a section on using another model.
   - New exercises 2 and 4; the quiz follows the new slides.

   .. rubric:: Lecture 9

   - **Real VLM check:** Gemini reads a real camera image of the kit tray. Its
     answer is checked against the schema, then compared with the tray sensor
     and the agent's own voltage record.
   - **Closed loop:** two recordings on ARIAC with tester 1 malfunctioning, one
     that replans and one that waits. Both fill the tray. The cells add to
     about 14.09 V, under ARIAC's kit minimum of 14.25 V, and the page shows
     why the VLM check alone does not catch it.
   - New exercises 2, 3 and 5; the quiz follows the new slides.

   .. rubric:: Pre-reads

   - **MCP** and **LLM Prompting** say what the L8 demonstrations use.


.. dropdown:: v0.4.15: Agentic Physical AI Defined (2026-10-17)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 1

   - **Definition:** the course's title term, agentic physical AI, is defined
     on the lecture page and in the overview: a robot system in which an AI
     agent decides what the robots do next, and robot skills carry out each
     decision in the physical world. The learning objective uses the new
     wording.

   .. rubric:: Glossary

   - New entry: **Agentic physical AI** (L1, L13).

   .. rubric:: Syllabus

   - The Course Description has the same sentence, on the home page, in
     ``syllabus.md`` and in ``syllabus.pdf``.


.. dropdown:: v0.4.14: Model Rule, Peer Score Formula, Demo Questions (2026-10-17)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Final demo

   - **Model:** another vision-language model is allowed only if it runs on
     the course key (a Google model) or locally, because the evaluation runs
     use one course key. Updated on the final demo page and in L11.

   .. rubric:: Syllabus

   - **Peer score:** score = 80 + 10 x (mean - 3), so a mean rating of 1
     gives 60, 3 gives 80 and 5 gives 100.
   - **Final demo:** each 5 to 6 minute presentation is followed by 3
     minutes of questions, one for each team member.
   - Lectures include instructor demonstrations. Shorter wording in a few
     places; no other policy changes.


.. dropdown:: v0.4.13: Accessible Syllabus PDF (2026-10-13)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Syllabus

   - ``syllabus.pdf`` is now a tagged PDF: a screen reader gets its
     headings, tables, links, language and title, as accessibility checkers
     such as Ally expect. It is built with ``tools/build_syllabus_pdf.sh``.
   - The old ``syllabus_spring2027_enpm663.pdf``, a June draft with the
     earlier course title, is removed. Nothing linked to it.


.. dropdown:: v0.4.12: Final Demo Model and Evaluation Key (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Final demo

   - **Model:** Gemini Robotics ER is the course example for the
     embodied-reasoning step. Your team may use another vision-language
     model if it reports the same comparison: precision and recall on the
     same cells, latency and cost.
   - **Evaluation key:** the instructor runs every team's image with one
     course API key, passed as an environment variable at run time. Who pays
     for model calls while you develop is still to be announced.


.. dropdown:: v0.4.11: Skills Package Page Marked as a Preview (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: ARIAC Testbed

   - The Course Skills Package page says it describes the first version
     (v0.1.0, the inspection robot skills), and that the repository opens to
     students with GP1 on February 3, 2027, as version 1.0.0.


.. dropdown:: v0.4.10: All Pages Published, Pre-Reads Written (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Published

   - **Lectures L1 to L13**, **GP1 to GP4**, the **final demo** page and the
     **Course Skills Package** page are now on the site. Each project still
     opens for work in the week the syllabus gives. The glossary's lecture
     tags are links, so its lecture filter works.

   .. rubric:: Pre-Read

   - Four pre-read pages: the **ROS 2 Refresher** (before L1), the **PDDL
     Primer** (before L6), **LLM Prompting and Structured Output** and
     **Model Context Protocol (MCP)** (before L8). Each covers what its
     lecture assumes, and points to the lecture for the rest. Their terms are
     in the glossary.

   .. rubric:: Fixes

   - L2: the GP1 timeline follows the GP1 page (Week 2: install the
     packages and run the trial; Week 3: blackboard keys).
   - L9: GP3 is due at the start of L9; only its peer review comes later.
   - L12: the GP4 peer-review form is filled in after the deadline.
   - The exercise pages count the final demo with the graded work.


.. dropdown:: v0.4.9: Syllabus PDF Rebuilt (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Syllabus

   - ``syllabus.pdf`` is rebuilt from the current ``syllabus.md``. It now
     has the "Agentic" lecture titles, the April 30 code freeze and the
     5 to 6 minute final demo talk.


.. dropdown:: v0.4.8: L13 Industry and Lab Examples, Provider-Neutral L8 Code (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **L13:** the industry segment has three sourced examples: an LLM that
     reassigns tasks after a robot fails (Penn State), LLM agents that run a
     modular production line (Stuttgart, IEEE ETFA 2025), and Amazon's
     DeepFleet. The notes now say that published work is pilots and research
     so far, and that motion and control stay classical.
   - **L8 code page:** the real-model section shows Anthropic and Gemini as
     two examples; the course requires neither provider.


.. dropdown:: v0.4.7: Final Demo Talk, Build Check and Online Backup (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Final demo

   - **Talk and questions:** each team talks for 5 to 6 minutes, then
     answers 3 minutes of questions, one for each team member. The slot stays
     10 minutes.
   - **Build check:** the instructor builds every image on Saturday, May 1.
     A team whose image does not build gets 24 hours for a fix that changes
     only build files, and loses the 10 build points.
   - **RO01 teams** upload their talk as a backup video by Tuesday, May 4.
     It is played only if the team cannot connect.

   .. rubric:: Site

   - The browser-tab title shows the changelog version.


.. dropdown:: v0.4.6: Final Demo Rubric Set (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Final demo

   - **Rubric:** 75 points for the run and 25 for the presentation and
     questions, scaled to 20% of the course grade. Task 1 and Task 2 points
     are 15 x accepted / wanted. Each challenge gives half its share for
     detecting it and half for recovering. A safe run loses 1 point per
     penalty event. The embodied-reasoning step is graded on doing it and
     reporting it, not on its precision or recall.


.. dropdown:: v0.4.5: Agentic in the Lecture Titles (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - Four lecture titles now say "Agentic", the first word of the course
     title, instead of "AI-Augmented" or "AI-Driven": L2 System
     Architectures for Agentic Robotics, L3 Knowledge Representation for
     Agentic Robotics, L11 Recovery, Robustness, and Failure Handling for
     Agentic Systems, and L12 Evaluation and Measurement Science for Agentic
     Systems. The syllabus and the lecture schedule match.


.. dropdown:: v0.4.4: Final Demo Code Freeze Set (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Final demo

   - **Code freeze:** Friday, April 30, 2027, at 11:59 pm. The syllabus, the
     final demo page and the L11 pages give the date. The grading rubric and
     the embodied-reasoning model are still to be announced.


.. dropdown:: v0.4.3: Lecture Notes Follow the Trimmed Decks (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **L2, L6, L10 and L11:** the slide decks were shortened, and the lecture
     notes now follow them. Slides that repeated other slides are gone; their
     points sit where the decks now have them. The full code and outputs stay
     on each code page, and the exercises point there where they need them.
   - **L10:** the notes add why Pilz cannot go around an obstacle, from
     MoveIt's own Pilz test.


.. dropdown:: v0.4.2: GP4 Checks the VLM Against a Second Source (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Group projects

   - **GP4, Task 3:** before the agent uses a VLM field, the team checks it
     against its second source, as L9 teaches: slot occupancy against
     ``/agvN/tray_status``, and cell type against the recorded tester
     voltage. A disagreement is logged as a flag. The VLM grounding
     criterion of the draft rubric now asks for that log entry; its points
     are unchanged.


.. dropdown:: v0.4.1: Project Page Corrections (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Group projects

   - **GP3:** Fast Downward is the planner; the Unified Planning Framework is
     the Python library that calls it.
   - **Final demo:** one run of 900 s of simulation takes 900 / 0.37 = 2432 s
     of wall clock (the page said 2430 s).


.. dropdown:: v0.4.0: Lecture Pages, Project Pages and Glossary (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **L1 to L13** each have lecture notes, the lecture code with its
     outputs, take-home exercises with worked solutions (not graded), a
     self-check quiz (not graded) and references. The pages stay hidden
     until each lecture opens.
   - **Defect depth:** the ARIAC documentation says every defect is at least
     2 mm from the cell surface. ARIAC's training cell meshes measure 0.84 to
     2.49 mm. The pages now give the measured range.

   .. rubric:: Group projects

   - The GP1 to GP4 pages and the final demo page are written in full. They
     stay hidden until each project is posted.

   .. rubric:: Glossary

   - The glossary covers every lecture, with 186 terms. Fixed: ARIAC 2025
     has three AGVs, and AGVs are moved with ARIAC's own action, not a
     course skill. Lifecycle nodes are tagged with the pre-read, where they
     moved in v0.3.0.

   .. rubric:: Site

   - ``tools/check_figures.py`` checks SVG figures too.


.. dropdown:: v0.3.0: Lidar Inspection, Instructor-Run Final Demo, Refresher Topics (2026-10-12)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Group projects

   - **GP2 uses lidar.** Teams find dents, scratches and bulges from lidar
     point clouds, as ARIAC 2025 requires, instead of RGB cameras and OpenCV.
   - **Inspection reports for every cell, from GP1 on.** A cell reaches the
     inspection robot only after a passing report; a cell with a failing
     report, or none, goes into the inspection bin.
   - **GP1 comes with a starter tree.** Weeks 2 and 3 go to setup, the skills
     package and the ARIAC services; the tree work follows L4.
   - **AGV moves:** teams call ARIAC's AGV move action themselves. The skills
     package covers the robot arms.
   - **GP4** tests the conveyor and voltage tester malfunctions and
     high-priority orders. The vacuum tool malfunction is tested in the final
     demo, where Task 2 runs.
   - **Final demo:** before the Week 15 class, the instructor runs every team's
     Docker image on the same unseen trial, on one machine. Class time is for
     presentations with the recorded runs. The embodied-reasoning model judges
     cell defects from camera images and is scored against the GP2 lidar
     detector on the same cells.

   .. rubric:: Lectures

   - **L1:** the ROS 2 refresher covers QoS, executors, actions and TF2.
     Lifecycle nodes move to the pre-read. The scoring formula is taught in
     L12.
   - **L3:** two ideas from NIST's 4D/RCS reference model (a world model at
     each layer; errors handled where they are seen), used inside the
     three-layer architecture from L2.
   - **L5 and L10:** the camera model moves from L5 to L10; L5 covers lidar
     point clouds for GP2.
   - **Facts checked against the ARIAC 2025 source:** three AGVs, six welds,
     and a voltage tester that keeps publishing (voltage -1, status
     MALFUNCTIONING) when it malfunctions.

   .. rubric:: Syllabus and site

   - The syllabus, project pages, lecture pages and setup pages are updated to
     match.


.. dropdown:: v0.2.0: New Title, New Site Layout, ARIAC 2025 Factory (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Course

   - **New title:** "Agentic Physical AI for Manufacturing Robotics".
   - **Projects:** four group projects (GP1 to GP4) and a final demo make up
     the final project. They replace PT1 to PT5. The weights are unchanged:
     10% for each GP and 20% for the final demo.
   - **Lectures are exposition only.** The in-class exercises are removed.
   - **New L13: the physical AI frontier** (VLA models, robot foundation
     models, world models). It replaces the Week 14 lab. Lectures are now
     numbered L1 to L13; the final demo is in Week 15.
   - **ARIAC 2025:** the group projects and lectures now describe the ARIAC
     2025 EV battery factory (cell inspection, kits, modules) instead of the
     earlier ARIAC kitting setup.
   - **Robot skills:** a course skills package, built on MoveIt 2, provides
     pick, place and AGV skills from GP1 on.
   - **Teams form in Week 2**, when GP1 is posted, and write a team charter.

   .. rubric:: Syllabus and site

   - **Dates:** Wednesdays, Jan 27 to May 5, 2027, 7:00 to 9:40 pm; spring
     break Mar 14 to 21.
   - The site uses the same layout as the ENPM818Z site: a full syllabus page,
     an ARIAC Testbed section (the former Setup), Pre-Read (the former
     Reading Material), a lecture schedule, a Final Project section and a
     searchable glossary.
   - New logo.
   - Lecture and group project pages open one at a time as they are
     finished.


.. dropdown:: v0.1.0: Redesign In Progress (2026-08)
   :icon: tag
   :class-container: sd-border-success

   ENPM663 rebuilt as "Building AI-Augmented Robotic Systems" (Spring 2027),
   redesigned from the earlier manufacturing-robotics offering.

   - Course structure: 15 weeks (Week 8 spring break), 5 team projects (PT1
     to PT5), 5 quizzes plus an ungraded Week 1 diagnostic.
   - AI direction: LLM agents for task planning (agent loop, tool use via
     MCP, structured output) and VLM grounding with agentic closed-loop
     replanning; classical motion planning (MoveIt 2). The VLA frontier is
     surveyed, not built.
   - Stack: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + ARIAC 2025.
   - Grading: 60% team projects / 25% quizzes / 15% peer-review
     contribution.
   - Lecture stubs authored for all 15 weeks; W9 and W10 framed around the
     agent loop; a VLA survey segment added to W2.
   - Team Project pages (PT1 to PT5) and an ENPM663 setup, reading-material,
     and glossary section replacing the previous C++ course content.
