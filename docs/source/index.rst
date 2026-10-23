ENPM663: Agentic Physical AI for Manufacturing Robotics
=======================================================

Course Description
------------------

ENPM663 teaches how to build **agentic physical AI**: robot systems where AI
agents decide what a factory cell does next and robot skills carry out each
decision. An **agent** is a program that runs a loop around a language model:
it observes the state of the world, asks the model what to do, calls a tool
(here, a robot skill), checks the result, and repeats.

The course is built on the **ARIAC 2025** testbed from NIST, a simulated
EV battery factory in which robots inspect battery cells, build kits and
assemble modules. You start from a classical stack and add AI at the
layers where it earns its place:

- Behavior trees that run robot skills and recover from failures
- Perception of battery cells from camera images
- Classical task planning with PDDL, as the baseline
- LLM agents that plan with tool calls (MCP) and structured output
- Vision-language models that describe what the cameras see
- Replanning when the factory does not behave as planned
- Vision-language-action models, robot foundation models and world models

Motion planning and grasping stay classical (MoveIt 2). By the end of the
semester, your team will have built an agentic system that runs a full
ARIAC trial it has never seen before.


Prerequisites
-------------

Students enrolling in ENPM663 must have:

- Working knowledge of **ROS 2**: packages and workspaces; publishers,
  subscribers, services and actions in Python; launch files, parameters and
  the ``ros2`` command-line tools.
- Strong **Python** programming skills.
- The ability to **read** C++ ROS 2 code. Writing C++ is not required.
- Good command of **Git and GitHub**: clone, branch, commit, push and pull,
  resolve a merge conflict, and open and review a pull request. The course
  does not teach them.

.. note::

   L1 includes a short refresher on the ROS 2 topics this course uses most
   (QoS, executors, actions and TF2), and an ungraded diagnostic
   quiz so you can check your own ROS 2, Git and GitHub background.


Learning Outcomes
-----------------

Upon successful completion of this course, students will be able to:

- **Design Agentic Robot Architectures:** Combine classical components
  (perception, planning, control) with AI components (LLMs, VLMs) and say
  which layer each one belongs to.
- **Represent Factory Knowledge:** Build symbolic models of an ARIAC scene
  and its tasks that both a PDDL planner and an LLM agent can use.
- **Execute Tasks with Behavior Trees:** Implement behavior trees in
  ``py_trees_ros`` that run robot skills and handle failures.
- **Plan with PDDL:** Generate executable plans for a robot cell with a
  classical task planner.
- **Build LLM Agents:** Build an agent that plans in an observe, act,
  observe loop, returns structured output checked against a JSON schema, and
  calls robot skills as tools through MCP.
- **Ground Plans in What the Cameras See:** Use vision-language models to
  describe a scene for the agent and to catch perception failures.
- **Recover from Failures:** Design recovery and replanning for systems
  where LLM and VLM outputs can be wrong.
- **Plan Robot Motion:** Plan and execute pick and place motions with
  MoveIt 2.
- **Explain the Physical AI Landscape:** Compare the modular stack built in
  this course with vision-language-action models and robot foundation
  models, and use a hosted embodied-reasoning model for one perception step.
- **Evaluate Agentic Systems:** Measure plan validity, grounding accuracy,
  execution success and end-to-end task performance.


How to Navigate This Website
----------------------------

This website contains all course materials for ENPM663. Use the **top
navigation bar** to access the main sections:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Changelog
      :class-card: sd-border-secondary

      Track all updates to the course documentation. Check here after each
      lecture for newly released materials.

   .. grid-item-card:: Syllabus
      :class-card: sd-border-secondary

      Course schedule, grade breakdown, group project timeline, and required
      software. **Start here** to understand the course structure.

   .. grid-item-card:: ARIAC Testbed
      :class-card: sd-border-secondary

      Setup guides for Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, ARIAC
      2025, the robotics tools, and access to LLMs and VLMs.

   .. grid-item-card:: Pre-Read
      :class-card: sd-border-secondary

      Assumed-knowledge pages to read *before* the lecture they support:
      the ROS 2 refresher (before L1), PDDL (before L6), and prompting and
      MCP (before L8).

   .. grid-item-card:: Lectures
      :class-card: sd-border-secondary

      13 lectures, from robot architectures to the physical AI frontier.
      Each lecture includes:

      - **Lecture notes:** detailed content with code examples, diagrams,
        and tables.
      - **Quiz:** practice questions (multiple choice, true/false, essay)
        with **hidden answers** you can reveal by clicking the dropdown.
      - **References:** papers, tools, and further reading.

   .. grid-item-card:: Final Project
      :class-card: sd-border-secondary

      Four cumulative group projects (GP1 to GP4) and a final demo that
      build an agentic system for the ARIAC factory. Each GP includes
      detailed instructions, provided code, grading rubrics, and submission
      checklists.

   .. grid-item-card:: Glossary
      :class-card: sd-border-secondary

      Course terms, searchable and filterable by lecture. Use this as a
      quick reference while studying or working on projects.

.. tip::

   **Practice quizzes** are available at the end of each lecture. Click the
   dropdown below each question to reveal the answer and explanation. These
   are not graded. Use them to test your understanding before the in-class
   quizzes.


Course Resources
----------------

**Required Software and Tools**

- Ubuntu 24.04 LTS (Noble Numbat)
- ROS 2 Jazzy Jalisco and Gazebo Harmonic
- ARIAC 2025
- MoveIt 2, ``py_trees_ros``, OpenCV, and a PDDL planner (Unified Planning
  Framework or Fast Downward)
- An LLM and VLM: Gemini (a free-tier API key) or local open-weight models
- Visual Studio Code or preferred IDE
- Git and GitHub for version control

**Course Code**

The course skills package (Python ROS 2 actions for picking and placing parts
with MoveIt 2) and the GP starter code are published with GP1.
The :doc:`ARIAC Testbed </ariac/ariac>` pages show how to install
everything else.


Course Structure
----------------

ENPM663 meets once a week for a lecture. Each week builds on prior
material, from a behavior tree that runs one kit to an agent that runs a
whole factory trial. Students complete four group projects (GP1 to GP4)
that build the system step by step, then integrate them in a final demo on
an unseen ARIAC trial.


Evaluation
----------

.. list-table::
   :header-rows: 1
   :widths: 60 20
   :class: compact-table

   * - Component
     - Percentage
   * - Final Project (GP1 to GP4 at 10% each, final demo at 20%)
     - 60%
   * - Quizzes (5)
     - 25%
   * - Peer-review contribution
     - 15%
   * - **Total**
     - **100%**

Late submissions incur a 10% deduction per day (maximum 3 days). Beyond
3 days, submissions receive zero credit.


.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   changelog/changelog
   syllabus/index
   ariac/ariac
   preread/index
   lectures/index
   assignments/index
   glossary/glossary
