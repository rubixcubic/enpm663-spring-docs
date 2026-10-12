==============================================================================
L13: The Physical AI Frontier: VLAs, Robot Foundation Models, and World Models
==============================================================================

Overview
--------

**All semester, your team built one side of physical AI: an agent that
reasons about the factory and calls classical robot skills. This lecture
surveys the other side, where learned models produce the robot's motions.**
It is a survey: you train no policy and need no GPU. There is no quiz this
week and nothing is due.

The lecture starts from the NVIDIA definition of **physical AI** used since
L1. Its last two verbs, *perform* and *orchestrate*, give two kinds of
system: a learned model that produces the robot's actions, and an agent that
decides what happens next and calls skills. Your stack is the second kind.

It then covers **vision-language-action (VLA) models**, learned models that
map camera images and language straight to robot actions, with five examples
from the references: OpenVLA, Physical Intelligence's pi-0 and pi-0.5,
Google DeepMind's Gemini Robotics, NVIDIA Isaac GR00T and SmolVLA. A
**robot foundation model** is trained once on data from many tasks and
robots, then adapted to a new one with less data.

Many current VLAs use a **two-system design**: a slow reasoning model above a
fast control policy. Set next to your three layers, the slow model plays the
deliberative role and the policy the reactive one, but no executive layer
checks each step. A **world model**, a learned model that predicts how a
scene will change, generates training data and tests policies before they
reach a robot. The lecture compares a learned policy with your stack on data,
compute (with the GPU memory the sources list), what a person can read after
one step, failure modes and new tasks.

The last part shows the one physical AI step the final demo adds: an
**embodied-reasoning (ER) model** that judges cell defects from a camera
image. A demonstration calls Gemini Robotics ER through the real
``google-genai`` SDK, with a scripted stand-in in place of the server, checks
each answer against a JSON schema, and scores the answers with precision and
recall against a GP2 lidar detector on the same cells. The class ends with
questions about the Week 15 final demo.

.. important::

   **ARIAC tie-in.** ARIAC 2025 has no learned policies, and the final demo
   does not need one. The final demo does use one physical AI model for
   perception: a hosted embodied-reasoning model judges cell defects from
   camera images over the inspection conveyor, and you score it with
   precision and recall on the same cells as your GP2 lidar detector.

.. important::

   **Group project.** The final demo is in Week 15 (Wednesday, May 5). Before
   that class, your team pushes its code-freeze tag. The instructor builds
   every team's Docker image from its tag and runs it on the same unseen
   trial, on one machine, and records each run. Class time is for
   presentations with the recorded runs, 5 to 7 minutes per team. The full
   rules are in the final demo specification posted in Week 12.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain what a VLA model is and how it differs from the modular stack built
  in this course.
- Describe the two-system design used by many current VLAs (a slow reasoning
  model above a fast control policy) and compare it with the course's three
  layers: the slow model plays the deliberative role and the policy the
  reactive one, but no executive layer checks each step.
- Explain what robot foundation models and world models are used for:
  generalizing across tasks, generating training data, and testing policies
  in simulation.
- Compare a learned policy and a skills library for an ARIAC 2025 task on
  data needs, compute, auditability and failure modes.
- Describe how to call a hosted embodied-reasoning model on a camera image of
  a cell and how to score its defect calls against your GP2 lidar detector on
  the same cells, as the final demo requires.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l13_lecture
   l13_code
   l13_exercises
   l13_quiz
   l13_references


Next Steps
----------

- **Week 15 (Wednesday, May 5): final demo presentations.** 5 to 7 minutes
  per team: your architecture, your design decisions, the failure modes you
  met and how you handled them, with your recorded run.
- **Before then:**

  - Run Task 1 and Task 2 together on practice trials with different seeds
    and challenge times.
  - Add the embodied-reasoning step and its measurement against GP2.
  - Build the Docker image from a clean clone.
  - RO01 teams: test sharing slides in the class video meeting.
  - Optional: run the demonstration code (see :doc:`l13_code`), work through
    the :doc:`L13 exercises <l13_exercises>`, take the
    :doc:`self-check quiz <l13_quiz>` (ungraded), and read the
    :doc:`references <l13_references>`.
