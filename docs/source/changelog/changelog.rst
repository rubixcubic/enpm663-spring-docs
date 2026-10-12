====================================================
Changelog
====================================================

All notable changes to the ENPM663 Spring 2027 course documentation are
recorded here.


.. dropdown:: v0.3.0: Lidar Inspection, Instructor-Run Final Demo, Refresher Topics (2026-10-12)
   :icon: tag
   :class-container: sd-border-success
   :open:

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
