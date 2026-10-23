====================================================
Lecture
====================================================

.. note::

   These notes follow the L13 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running ``er_demo.py``, ``er_rerun.py`` and
   ``score_er.py`` with Python 3.12.3, ``google-genai`` 2.31.0, ``httpx``
   0.28.1 and ``jsonschema`` 4.26.0. The scripts and how to run them are on
   the :doc:`code page <l13_code>`.

.. admonition:: Class logistics for this week
   :class: warning

   - **There is no quiz this week.** The five quizzes ended in Week 12.
   - **The final demo code freeze is Friday, April 30, at 11:59 pm**, two
     days after this class: push your code-freeze tag ``final-demo`` and submit your team
     configuration file (see :ref:`l13-final-demo`).
   - **The final demo is next week**, Week 15 (Wednesday, May 5). The last
     part of class is for your questions about it.

The quotes below are from the reference pages as of 2026-10-18.


.. _l13-physical-ai:

Physical AI and This Course
---------------------------

- All semester, your team built an agent that reasons about the factory and
  calls classical robot skills.
- Today: systems where learned models produce the robot's motions.
- No quiz this week.
- The final demo code freeze is Friday, April 30, at 11:59 pm, two days
  after this class.


Perform and Orchestrate
~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Physical AI (NVIDIA glossary, used since L1)
   :class: note

   "Physical AI lets autonomous systems like cameras, robots, and self-driving
   cars perceive, understand, reason, and perform or orchestrate complex
   actions in the physical world."

The last two verbs give two kinds of system:

- **Perform:** a learned model produces the robot's actions, as a VLA does.
  Today covers this kind.
- **Orchestrate:** an agent decides what happens next and calls skills that
  carry it out. The course built this kind.

The course's own term, agentic physical AI, is the orchestrate kind (L1,
:ref:`l1-agentic-physical-ai`).


The Stack Your Team Has Now, on the L2 Layers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 82
   :class: compact-table

   * - **Layer**
     - **What your team has**
   * - Deliberative
     - The GP3 PDDL planner, then the GP4 LLM agent with VLM grounding
   * - Executive
     - The ``py_trees_ros`` behavior tree from GP1, which runs the plan or the
       agent's decisions
   * - Reactive
     - The course skills package on MoveIt 2, over ARIAC's joint trajectory
       and gripper actions; plus ARIAC's AGV move action, which your team
       calls itself (it is not a skill)
   * - Perception
     - The GP2 inspection pipeline, which reads lidar point clouds over the
       inspection conveyor

This lecture compares this stack with designs where a learned model
replaces the reactive layer, or the reactive and executive layers together.


More Terms from the Glossary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Reinforcement learning.** The glossary says: "Reinforcement learning
teaches autonomous machines skills in a simulated environment to perform in
the real world."

**Simulation and world foundation models.** The glossary says the two are
used together to create synthetic data for training.


.. _l13-vla:

VLA Models and Robot Foundation Models
--------------------------------------

This section covers what a VLA maps, five examples from the L13 references,
and what a robot foundation model adds.


One ARIAC Step, Done Two Ways
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: vision-language-action (VLA) model
   :class: note

   A **VLA** is a learned model that maps camera images and language straight
   to robot actions.

**The step.** ``inspection_robot_1`` (a UR3e with a Robotiq 2F-85 gripper)
picks a cell off the moving conveyor and places it in a voltage tester.

**Two ways to do it.**

- **GP4:** the agent returns a tool call with typed arguments, checked
  against a JSON schema. The skills package turns it into a MoveIt 2
  trajectory.
- **VLA:** the model reads the camera images and an instruction such as
  "place the cell in tester 1" and outputs the motion itself. No planner and
  no named skill sit in between.


VLA Examples
~~~~~~~~~~~~

**OpenVLA** (`project page <https://openvla.github.io/>`_)

- "a 7B parameter open-source vision-language-action model (VLA), pretrained
  on 970k robot episodes from the Open X-Embodiment dataset."
- It maps image inputs to embeddings and predicts action tokens, which are
  decoded into continuous actions the robot executes.

**pi-0 and pi-0.5** (Physical Intelligence,
`openpi <https://github.com/Physical-Intelligence/openpi>`_)

- pi-0 is "a flow-based vision-language-action model (VLA)".
- pi-0.5 is "an upgraded version of pi0 with better open-world
  generalization." (README, Updates list)
- The base checkpoints are "pre-trained on 10k+ hours of robot data."

**Gemini Robotics** (Google DeepMind,
`model page <https://deepmind.google/models/gemini-robotics/>`_)

- The page calls its VLA a model "that converts vision and language input
  into motor control."
- The current models include Gemini Robotics 2 and Gemini Robotics ER 2.

**NVIDIA Isaac GR00T** (`README <https://github.com/NVIDIA/Isaac-GR00T>`_)

- N1.7 is "an open vision-language-action (VLA) model for generalized
  humanoid robot skills."
- Its architecture is "a combination of vision-language foundation model and
  diffusion transformer head that denoises continuous actions."

**SmolVLA** (Hugging Face, `blog post <https://huggingface.co/blog/smolvla>`_)

- "a compact (450M), open-source Vision-Language-Action model for robotics
  that runs on consumer hardware."
- Inputs: images from several cameras, the robot's sensorimotor state and a
  language instruction. Output: a continuous sequence of actions.


The Dated Events of These Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The timeline places each model by the month of a dated event. Only the
horizontal position carries data; the tags alternate above and below the
line so they do not overlap.

.. image:: /_static/images/l13/model_timeline.svg
   :alt: A horizontal timeline from June 2024 to October 2026 with year marks
         at 2025 and 2026. Seven numbered dots, left to right, each with its
         month: tag 1, Jun 2024; tag 2, Oct 2024; tag 3, Jun 2025; tag 4, Sep
         2025; tag 5, Apr 2026; tag 6, Jul 2026; tag 7, Aug 2026. Tags
         alternate above and below the axis; only the horizontal position
         carries data.
   :width: 90%
   :align: center

The table gives each tag's event and the source of its date (checked
2026-10-18). Gemini Robotics 2 is not on the
line: its page gives no date.

.. list-table::
   :header-rows: 1
   :widths: 5 28 17 50
   :class: compact-table

   * - **Tag**
     - **Event**
     - **Date**
     - **Source**
   * - 1
     - OpenVLA paper, version 1
     - 13 Jun 2024
     - `arXiv 2406.09246 <https://arxiv.org/abs/2406.09246>`_, submission
       date
   * - 2
     - pi-0 paper, version 1
     - 31 Oct 2024
     - `arXiv 2410.24164 <https://arxiv.org/abs/2410.24164>`_, submission
       date
   * - 3
     - SmolVLA blog post
     - 3 Jun 2025
     - Hugging Face blog, publication date
   * - 4
     - pi-0.5 released in openpi
     - Sep 2025
     - openpi README, Updates list
   * - 5
     - GR00T N1.7 release
     - 18 Apr 2026
     - GitHub release ``n1.7-release``, publication date
   * - 6
     - Gemini Robotics ER 2 preview
     - Jul 2026
     - Gemini API robotics page, "Latest update"
   * - 7
     - Gemini Robotics ER 1.6 deprecated
     - 31 Aug 2026
     - Same page: "deprecated on August 31, 2026"

.. note::

   Each date is when something was published or updated, not when the work
   started. A GitHub release can be published after a model was first
   announced.


Robot Foundation Models: Train Once, Adapt with Less Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: robot foundation model
   :class: note

   A **robot foundation model** is trained once on data from many tasks and
   robots, then adapted to a new robot or task with less data.

   **Fine-tuning** is more training of a trained model, on a smaller set of
   data for the new robot or task.

Examples from the references:

- OpenVLA "can be quickly adapted to new robot setups via parameter-efficient
  fine-tuning."
- openpi provides base model checkpoints and examples for fine-tuning them to
  your own datasets.
- GR00T N1.7 is trained on data from several robot bodies: bimanual,
  semi-humanoid and humanoid.


What a VLA Would Need Before It Could Work in ARIAC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A VLA would need demonstrations of the ARIAC robots doing ARIAC tasks
  before it could replace a skill. Fine-tuning needs data from the target
  robot.
- ARIAC 2025 has no learned policies, and the final demo does not need one.
- The final demo uses one physical AI model for perception: a hosted
  embodied-reasoning model judges cell defects from camera images.

.. tip::

   Your skills package needed no demonstrations: it needed the ARIAC geometry
   and a MoveIt 2 configuration. A VLA needs demonstrations in their place.


.. _l13-two-system:

Two-System Designs
------------------

A **two-system design** puts a slow model, for meaning and planning, above a
fast control policy. SmolVLA's authors call a vision-language model combined
with an action prediction module "a common design pattern in recent VLA
systems" (Hugging Face blog).


Two Models, or Two Parts of One Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Two models: Gemini Robotics.**

- The Gemini Robotics page: "Our vision-language-action (VLA) model and
  embodied reasoning (ER) model work together to interact with the physical
  world. Each has a specialist role, but they operate as one powerful and
  versatile system."
- The `Gemini API robotics page
  <https://ai.google.dev/gemini-api/docs/robotics-overview>`_: "Gemini
  Robotics ER is also agentic: it breaks complex tasks into sub-tasks and
  executes them by calling your robot functions or running generated code."

**Two parts of one model.**

- SmolVLA: a pretrained VLM encodes the images, state and instruction; an
  **action expert** (a flow matching transformer) turns those features into
  actions.
- GR00T: a vision-language model with a diffusion transformer head.


A Single VLA, a Two-System VLA and Your Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l13/three_designs.svg
   :alt: Three block diagrams side by side. Panel 1: camera images and a
         language instruction go into one VLA model, which outputs robot
         actions. Panel 2: the same inputs go into a slow reasoning model (an
         ER model or a VLM, blue), whose output goes straight down to a fast
         policy (a VLA or an action expert, orange), marked tag 4, which
         outputs robot actions. A dashed arrow marked tag 5 goes from the
         robot actions back up to the slow model. Panel 3: ARIAC topics and
         services, lidar and camera go into an LLM agent or PDDL planner
         (blue), then through a tool call marked tag 6 to the behavior tree
         (green), then to the skills package and MoveIt 2 (orange), which
         send ARIAC trajectory and gripper actions. Dashed arrows marked tag
         7 go back up from the skills to the tree and from the tree to the
         agent.
   :width: 95%
   :align: center

1. One VLA model, such as OpenVLA.
2. A two-system design: Gemini Robotics (ER model and VLA), or SmolVLA (VLM
   and action expert).
3. Your stack.
4. The slow model's output goes straight to the policy.
5. Gemini Robotics only: the ER model can judge progress and success from
   video. SmolVLA has no such path.
6. A tool call, checked against a JSON schema (L8).
7. Status and failure reasons move up.

Colors: blue is the deliberative role, green the executive role, orange the
reactive role, gray no layer role.


The Two-System Roles in the Course
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 36 48
   :class: compact-table

   * - **Role**
     - **Two-system VLA**
     - **This course**
   * - Deliberative
     - The ER model or VLM: reasons about the scene, calls functions
     - The GP4 agent: reasons about the scene, calls tools
   * - Executive
     - SmolVLA: none, the action expert acts on the VLM's features directly.
       Gemini Robotics: the ER model can judge progress and success (see
       below)
     - The behavior tree: checks each skill result before the next step and
       stops cleanly on failure (L4, L7, L11)
   * - Reactive
     - A learned policy (the VLA or action expert)
     - Classical motion planning: the skills package and MoveIt 2

The slow system matches your agent closely. In the fast system, a learned
policy takes the place of your classical motion planning.


What Checks Each Step, Design by Design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Your stack.** Code in your behavior tree checks each step (L4, L7, L11).

**SmolVLA.** Nothing between the two parts checks each step: the VLM passes
its features straight to the action expert. Helix (L2) works the same way.

**Gemini Robotics.** The `Gemini API robotics page
<https://ai.google.dev/gemini-api/docs/robotics-overview>`_ says Gemini
Robotics ER 2 "specializes in embodied reasoning capabilities,
such as agentic orchestration of robots (e.g. using VLAs), robot video
understanding including progress understanding and success detection,
instrument reading, pointing, and spatial reasoning."

So the ER model can do executive work: it can judge from the robot's video
whether a step succeeded. That judgment comes from a learned model, not from
a coded check of a skill result.


What Crosses the Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Course:** a named tool call with arguments checked against a JSON schema
  (L8). A person can read it.
- **SmolVLA:** the VLM passes learned features (lists of numbers) to the
  action expert. A person cannot read them.

.. admonition:: Your stack against a two-system VLA
   :class: important

   - Your architecture has the deliberative and reactive roles of a
     two-system VLA, plus an executive layer that SmolVLA lacks.
   - They differ in what sits in the fast layer, what crosses the interface,
     and what checks each step.


.. _l13-world-models:

World Models and Simulation
---------------------------

This section is about training data and testing, before a policy reaches a
robot.


What a World Model Is, and Why Physical AI Needs One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: world model (learned)
   :class: note

   A **world model** is a learned model that predicts how a scene will
   change. It is used to generate training data and to test robot policies
   in simulation before they reach a robot.

.. warning::

   The same words meant something else in L3: a 4D/RCS world model is the
   knowledge each layer keeps about the factory. In this lecture, "world
   model" means the learned predictor above.

**Why (NVIDIA glossary).**

- "Training physical AI models requires large, diverse, and physically
  accurate data about the spatial relationships and physical rules of the
  real world."
- Simulation and world foundation models are used together to create
  synthetic data for training.


How Much Data the References Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 48 30
   :class: compact-table

   * - **Model**
     - **Training data**
     - **Source**
   * - OpenVLA
     - 970k robot episodes
     - OpenVLA page
   * - openpi base models
     - 10k+ hours of robot data
     - openpi README
   * - GR00T N1.7
     - 20K hours of EgoScale human video data in pretraining, with robot
       demonstrations
     - Isaac-GR00T README

Collecting that much on real robots is slow. Simulation and world models can
make synthetic data in its place (NVIDIA glossary).


ARIAC and a World Model
~~~~~~~~~~~~~~~~~~~~~~~

**ARIAC 2025** is a physics simulation in Gazebo Harmonic whose rules
engineers wrote: the conveyor, the inspection door that stays closed without a
passing report (the cell then drops into the inspection bin), the voltage
testers that publish a noisy voltage, the scoring formula.

**A world model** learns its rules from data, so neither its scenes nor its
errors come from a written rule.

**The same purpose:** both let you test a system before it runs on hardware.
Every GP was tested in ARIAC.


A Learned Policy Is Judged by Outcomes over Many Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A learned policy has no readable plan to check, so you judge it by what
  happens over many runs.
- L12's run-count rule applies ("How Many Runs a Claim Needs"): how many
  runs, and how much the result varies between runs.
- A rate from a few runs can only take a few values. With 4 runs (chosen for
  this example), one run moves a success rate by 1 / 4 = 0.25, so the rate
  can only be 0, 0.25, 0.50, 0.75 or 1.

.. tip::

   A learned policy has only its outcomes as evidence, so it needs more runs
   than your stack before you trust a number.


.. _l13-cost:

What Learned Policies Cost
--------------------------

This section compares your stack with a learned policy (a VLA) row by row:
data, compute, auditability, failure modes and new tasks.


Rows 1 and 2: Data and Compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 12 38 50
   :class: compact-table

   * -
     - **Your stack**
     - **A learned policy (VLA)**
   * - Data
     - No demonstrations. It needs the ARIAC geometry (frames, tray slot
       offsets) and a MoveIt 2 configuration.
     - The training data from :ref:`l13-world-models`, plus demonstrations
       on the target robot for fine-tuning.
   * - Compute
     - A hosted LLM and VLM API, or small local models. GPU access is not
       assumed.
     - OpenVLA was trained "on a cluster of 64 A100 GPUs for 15 days".
       Running and fine-tuning need the GPU memory in the next figure.
       SmolVLA runs on consumer hardware.


GPU Memory Each Step Needs, as the Sources List It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The chart shows the GPU memory each source lists for running a model and for
fine-tuning it. Five values are lower bounds ("more than" or "or more"), so
their bars show the least memory the source asks for. The GR00T fine-tuning
value is what its README calls "recommended", not a minimum.

.. image:: /_static/images/l13/gpu_memory.svg
   :alt: A horizontal bar chart. The horizontal axis is the GPU memory the
         source lists, in GB, from 0 to 80. The vertical axis lists six steps.
         Course stack (hosted API): no bar, no GPU assumed. openpi, run the
         model: more than 8 GB. GR00T, run the model: 16 GB or more. openpi,
         LoRA fine-tuning: more than 22.5 GB. GR00T, fine-tuning: 40 GB or
         more, recommended. openpi, full fine-tuning: more than 70 GB.
   :width: 90%
   :align: center

- **openpi README:** more than 8 GB to run, more than 22.5 GB for LoRA
  fine-tuning (example GPU RTX 4090), more than 70 GB for full fine-tuning
  (A100 80GB or H100), on one GPU. The README spells LoRA out as low-rank
  adaptation. Its lower bound is about a third of the full fine-tuning one:
  22.5 / 70 = 0.32.
- **Isaac-GR00T README:** "1 GPU with 16 GB+ VRAM" to run; "1 or more GPUs
  with 40 GB+ VRAM recommended" to fine-tune.


Row 3: What a Person Can Read After One Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The step: place a cell in voltage tester 1.

.. image:: /_static/images/l13/audit_trace.svg
   :alt: Two rows for the step: place a cell in voltage tester 1. Row 1, the
         course stack, has four records joined by arrows: the agent's tool
         call with its name and arguments (blue); the schema check, valid or
         the rule it broke (blue); the behavior tree's status of each node
         (green); the skill result, success or a failure reason (orange). Row
         2, a VLA: camera images and the instruction go into one VLA model,
         drawn with a dashed border and marked as learned features, not
         readable; it outputs robot actions, and the last box is the outcome:
         placed, dropped, or a collision penalty.
   :width: 95%
   :align: center

1. Your stack leaves four records, one from each part: the agent's tool call,
   the schema check, the behavior tree's node status and the skill result.
2. A VLA leaves its inputs, its actions and the outcome. What passes inside
   the model cannot be read.

.. admonition:: Auditability
   :class: important

   The instructor's view: an LLM-based plan leaves a trace a person can
   inspect, and a learned policy's failure leaves no readable reason.


Rows 4 and 5: Failure Modes and New Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 14 44 42
   :class: compact-table

   * -
     - **Your stack**
     - **A learned policy (VLA)**
   * - Failure modes
     - Each failure comes from a named part: a skill returns failure, a schema
       check rejects the agent's output, the VLM misreads a cell. L11 gives a
       check or a recovery for each one.
     - No step returns failure. You find the failure from the outcome, for
       example a dropped cell or a collision penalty in the ARIAC score.
   * - A new task
     - An engineer writes or changes a skill and the PDDL domain or tool list.
     - The foundation models aim to generalize to new tasks (pi-0.5: "better
       open-world generalization"), with fine-tuning when they do not.

On new tasks, a learned policy has the advantage: your stack can only do what
its skills cover.


Class Discussion: Which Part Would You Replace with a VLA?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Prompt
   :class: hint

   ``inspection_robot_1`` must pick each cell off the moving conveyor and
   place it in one of two voltage testers. Which part of your system would
   you replace with a VLA, and what would you need first?

What you would need first:

- Demonstrations of the UR3e picking cells at your conveyor speed.
- A GPU of the size in the GPU memory chart.
- A test plan with many runs, and a way to detect a failed pick, since the
  policy will not report one.
- The ARIAC penalties a bad policy would trigger: a cell in the conveyor bin
  (25), an object on an invalid surface (25), a robot collision (100 for
  every 5 s).


Why the Course Grades a Skills Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The course grades engineering judgment on unseen trials: the final demo
  runs your system on a trial you have never seen.
- To grade judgment, the grader must see why the system did what it did. The
  readable traces of rows 3 and 4 make that possible.
- A learned policy would add GPU needs and demonstration data, and would
  replace those traces with outcomes only.

.. tip::

   This lecture surveys learned policies so you can judge when one fits: when a task
   has no skill, when demonstrations exist, and when outcomes over many runs
   are enough evidence.


.. _l13-industry:

Agentic Manufacturing in Industry
---------------------------------

This section is about agents that coordinate robots: two lab examples and
one industry example.


Lab Example 1: An LLM Reassigns Tasks After a Robot Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Lim and Kovalenko, Penn State <https://arxiv.org/abs/2505.22804>`__ (arXiv
preprint, May 2025):

- Two arms (UFactory xArm6 and Lite6) work in two cells. The LLM is GPT-4o.
- The LLM decides: when a robot fails, it writes a new task assignment.
- A central controller (CCA in the paper) checks it: "If the response fails
  validation, the CCA provides structured feedback and re-prompts the LLM
  until a feasible configuration is obtained or the maximum retry limit is
  reached."
- Each robot's own controller runs the motion.

**Measured by the authors (20 trials):** a valid reassignment in 20 of 20
trials, 12 of them on the first try, and 19.36 s on average to adapt.


Lab Example 2: LLM Agents Run a Modular Production Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Xia, Jazdi, Zhang, Shah and Weyrich, University of Stuttgart
<https://arxiv.org/abs/2409.18009>`__ (IEEE ETFA 2025): a manager agent turns
an order into a production plan, and operator agents control the automation
modules, which do the physical work. Each operator agent's LLM output holds a
function call, "the concrete command that will be executed on the automation
module" (p. 3 of the arXiv version). The command goes straight to the module.

.. list-table:: GPT-4o on 100 test points (the paper's Table II)
   :header-rows: 1
   :widths: 40 30 30

   * - GPT-4o
     - Routine steps
     - Unexpected events
   * - As released
     - 100%
     - 41%
   * - Fine-tuned on their data
     - 100%
     - 100%

The authors write: "An accuracy of less than 100% means that the results are
not fully reliable for directly controlling an automation system" (p. 7).
Human approval is something the authors propose: "they can be developed as an
assistant system, proposing next actions for human supervisors to approve"
(p. 7).


Industry Example: Amazon DeepFleet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Amazon Science blog
<https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination>`__
(August 11, 2025):

- A foundation model trained on data from Amazon fulfillment and sortation
  centers. It is a learned model, not an LLM agent.
- Amazon reports that DeepFleet "can already help assign tasks to our robots
  and route them around potential congestion, increasing the efficiency of
  our robot deployments by 10%".
- The models are still being developed: Amazon is "initially using them to
  predict congestion, with the longer-term goal of using them to produce
  outputs like assignments of robots to specific retrieval tasks and target
  locations".



Lab and Industry Examples Compared
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The two LLM examples are lab work. DeepFleet, a learned model,
  is the one example that Amazon reports already helping in its robot
  deployments.
- In both lab examples, the LLM decides and classical controllers do the
  motion: each robot's own controller (Lim and Kovalenko) or the automation
  modules (Xia et al.).
- The Gemini Robotics page says Gemini Robotics 2 "can coordinate multiple
  robots to work together in shared spaces."

**The same problem in ARIAC.**

- Two inspection robots, two assembly robots, a gantry welder and three AGVs
  share one workspace and one set of tasks.
- L2 treated this as a multi-agent problem: one decision maker, or one per
  robot.


Class Discussion: A High-Priority Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Question 1
   :class: hint

   A high-priority order arrives while a Li-Ion kit is half built. The team
   must switch the feed to Ni-MH, build a Ni-MH kit and submit it with the
   order ID. Which robots does that change, and who decides the order of
   their work?

.. admonition:: Question 2
   :class: hint

   What must the system log so a plant engineer can later check why the
   agent made each decision?


.. _l13-demo:

Demonstration: an Embodied-Reasoning Model
------------------------------------------

This section shows the call the final demo requires, once, before your team
makes it. In class you watch only; you make the call yourselves in the final
demo.

.. warning::

   - The first parts run offline. A scripted stand-in answers instead of the
     model server, and no API key is used. The client code is the
     ``google-genai`` SDK itself; only the server's answers are scripted.
   - **Run 1 and Run 2** use ``gemini-robotics-er-2-preview`` on 12 ARIAC
     camera images.

   Code: ``lecture13/code/er_demo.py``, ``er_rerun.py`` and ``score_er.py``;
   ``run_all.sh`` runs the offline parts (see :doc:`l13_code`). Versions:
   Python 3.12.3, ``google-genai`` 2.31.0, ``httpx`` 0.28.1, ``jsonschema``
   4.26.0.


What an Embodied-Reasoning Model Is, and Which One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: embodied-reasoning (ER) model
   :class: note

   An **embodied-reasoning model** is a vision-language model trained to
   answer spatial questions about a scene, such as where a part is or which
   cell looks damaged.

**The course example** (Gemini API robotics page):

- Google's Gemini Robotics ER, through the Gemini API and the
  ``google-genai`` Python SDK.
- API model: ``gemini-robotics-er-2-preview``, a preview model that supports
  structured output and function calling.
- "Gemini Robotics ER 1.6 was deprecated on August 31, 2026."


The Final Demo's ER Step
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Capture** one image from an RGB camera placed through your team config,
   beside the inspection conveyor: a cell stands upright, and its defects are
   on its side.
2. **Ask:** send the image and one question to the model, and ask for the
   answer in a JSON format (L8).
3. **Check** the answer against a JSON schema, as GP4 does for the agent.
4. **Locate**, when the answer is a point: turn its image position into a
   position in a robot frame with the camera model (L10) and TF2.
5. **Measure** against GP2: on the same cells, compare with your lidar
   detector and with the ground truth. Report precision and recall per
   defect type, latency and cost per call.

The same call also finds the top shell over the assembly table in Task 2 (it
spawns at a random pose). Whether defects
0.84 to 2.49 mm deep show in a camera image is part of what your team
measures.


Step 2: The Question
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/er_demo.py
   :language: python
   :lines: 41-48
   :caption: lecture13/code/er_demo.py (excerpt)

- The prompt names the three ARIAC defect types and describes each one in
  simpler words than the ARIAC scenario page: a dent and a scratch are inset
  (a scratch is long and narrow), a bulge sticks out.
- The last sentence is quoted from the Python example on the Gemini API
  robotics page. Each point is an image position, rows first (``[y, x]``),
  scaled to 0 to 1000.


Step 2: The Call
~~~~~~~~~~~~~~~~

.. literalinclude:: code/er_demo.py
   :language: python
   :lines: 134-145
   :caption: lecture13/code/er_demo.py (excerpt)

- ``client.interactions.create`` with a model, an input list and a generation
  config follows the Python example on the Gemini API robotics page. The
  example uploads the image file; this code sends the bytes in the request
  instead (base64 text in the ``data`` field).
- "For thinking level use medium for a good balance between latency and
  performance" (same page).
- ``extra`` is empty offline and in Run 1. Run 2 passes two arguments through
  it (see :ref:`l13-run2-call`).


How the Stand-In Replaces the Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   This part is in the notes only. The slides keep one line for it.

.. literalinclude:: code/er_demo.py
   :language: python
   :lines: 115-131
   :caption: lecture13/code/er_demo.py (excerpt)

- ``httpx.MockTransport`` catches each request before it leaves the machine
  and returns the next scripted answer. ``httpx`` is the HTTP library the SDK
  uses to send requests.
- With a real key, you drop the mock client: the rest of the code stays the
  same. Run 1 and Run 2 do this with ``make_live_client``, a plain ``httpx``
  client that saves each request and response with the key removed. The
  :doc:`code page <l13_code>` lists what you need for that.


The Request the SDK Sends
~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   This part is in the notes only. The slides keep one line for it.

Scripted model: fixed replies. The body of the first call, from
``outputs/er_demo.txt``:

.. literalinclude:: outputs/er_demo.txt
   :language: text
   :lines: 2-16

The first line of the file says ``Requests sent: 12``, one per cell. The
image is a synthetic 8 by 8 gray PNG; the script shortens the image data and
the prompt when it prints them.


Step 3: The Answer and the Schema Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answers come from the scripted stand-in, and the cell IDs are chosen for
this example:

.. literalinclude:: outputs/er_demo.txt
   :language: text
   :lines: 18-

The schema allows only ``DENT``, ``SCRATCH`` and ``BULGE``, the three types in
ARIAC's ``CellDefect.msg``. The answer for c10 names ``CRACK``, so it is
rejected before it can reach a report.


Step 5: How the Final Demo's ER Step Is Scored
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l13/er_scoring.svg
   :alt: A flow diagram. One cell on the inspection conveyor feeds three
         rows. Row 1, tag 1: a lidar scan and the GP2 detector give an
         inspection report with a defect type. Row 2, tag 2: a camera image
         goes to the ER model; tag 3: its JSON answer goes through a schema
         check, and a rejected answer goes to a dashed box: left out,
         counted. Row 3, tag 4: ground truth from a practice run log
         (log_cell_info:=true). All three rows lead to tag 5: compare on the
         same cells, per defect type, true positives, false positives and
         false negatives. That leads to tag 6: precision and recall per type,
         latency and cost per call, and the number of cells used.
   :width: 95%
   :align: center

1. The GP2 lidar report.
2. A camera image to the ER model.
3. The schema check. A rejected cell is left out of both scores, and counted.
4. Ground truth. ARIAC prints each cell's defects to the Gazebo log when it
   is launched with ``log_cell_info:=true`` (``cheat_tools_plugin.cpp``).
5. Compare on the same cells, per type.
6. The table the final demo asks for.


Precision and Recall per Defect Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For one defect type, over the cells used:

- **TP** (true positive): the detector and the ground truth both say the cell
  has this type.
- **FP** (false positive): the detector says this type; the ground truth does
  not.
- **FN** (false negative): the ground truth has this type; the detector does
  not say it.

.. admonition:: Precision and recall
   :class: note

   **Precision** = TP / (TP + FP): of the cells the detector called this
   type, the share that have it.

   **Recall** = TP / (TP + FN): of the cells that have this type, the share
   the detector found.

.. literalinclude:: code/score_er.py
   :language: python
   :lines: 58-63
   :caption: lecture13/code/score_er.py (excerpt)


The Comparison Table for 12 Cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/score_er.txt
   :language: text
   :caption: outputs/score_er.txt

The ground truth and the lidar labels are chosen for this example, and the
ER labels come from the scripted stand-in. The table shows how to score; it
does not measure Gemini Robotics ER or your lidar detector.


Reading the Table, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. c10's answer broke the schema, so c10 is left out for both detectors: 11
   of 12 cells are used.
2. **DENT, ER:** c02 is right (TP). c05 has no defect but was called a dent
   (FP). c07 is a dent called a bulge (FN). Precision 1 / (1 + 1) = 0.50;
   recall 1 / (1 + 1) = 0.50.
3. **BULGE, ER:** c06 and c11 are right (TP 2), and c07 is the FP. Precision
   2 / 3 = 0.67; recall 2 / 2 = 1.00. The one mistake on c07 counts twice: an
   FN for DENT and an FP for BULGE.
4. **SCRATCH:** both detectors have recall 1 / 2 = 0.50, but lidar missed c09
   and the stand-in missed c04. The same recall comes from different cells;
   the labels agree on only 7 of 11 cells.

.. warning::

   Each type has 2 defective cells here, so one cell moves recall by
   1 / 2 = 0.50. With so few cells, a difference between the two detectors can be
   one cell. Use many more cells (L12).


.. _l13-real-runs:

Gemini Robotics ER: Two Runs on 12 ARIAC Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- One ARIAC session (trial ``LEC13001``, seed 2) fed 12 Li-Ion cells past a
  1080p camera and saved one image per cell. ARIAC's cell log
  (``log_cell_info:=true``) is the ground truth: 8 cells have 9 defects in
  all, and 4 have none.
- The camera sits beside the belt, 0.20 m from the cell, looking 20 degrees
  down (``code/config/l13_user_config.yaml`` in the slides repository).
- The instructor chose the seed and the camera's side after replaying ARIAC's
  random draws. The seed is the smallest one whose 12 cells have each defect
  type 3 or more times and 3 or more good cells (``code/config/l13_trial.yaml``).
  The side makes the side defects face the camera: 5 of the 9 point within 60
  degrees of the direction to the camera (the angle between the defect's
  outward direction and the line to the camera, ``angle_from_camera`` in
  ``score_er.py``). Your team's camera would likely see fewer.
- Two separate runs sent the same 12 images to the model, one call per image,
  with no retry. Run 1 uses the call shown in :ref:`l13-demo` (Step 2). Run 2
  adds structured output.

.. note::

   Recorded once, on 2026-10-18, with ``gemini-robotics-er-2-preview``. A
   rerun gives different answers.


Run 1: The Schema Check Rejects Every Answer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From ``outputs/er_rec1.txt``, then ``outputs/score_er_rec1.txt``:

.. literalinclude:: outputs/er_rec1.txt
   :language: text
   :lines: 28-30

c02 to c08 (lines 31 to 51 of the file) carry the same fence. Then:

.. literalinclude:: outputs/er_rec1.txt
   :language: text
   :lines: 52-54

.. literalinclude:: outputs/score_er_rec1.txt
   :language: text
   :lines: 18-19

- All 8 answers came inside a Markdown code fence (c01 is shown; c02 to c08
  are the same in ``er_rec1.txt``), although the prompt says "Answer only
  with JSON". ``json.loads`` fails at the first character, so the deck's
  check rejects all 8, and 0 of 12 cells are scored: no answer that is not
  JSON reaches the scores.
- Call 9 got HTTP 429. Google's message, in the error body
  (``outputs/raw/er_rec1/c09.response.json``): "Rate limit exceeded for model
  gemini-robotics-er-2-preview (limit: 5 requests per minute on Free Tier).
  Please retry in 35s or upgrade your tier at https://ai.dev/rate-limit."
- The recording does not fit a simple count per minute: the first 8 calls were
  all answered within 34 s (their ``created`` times run from 09:29:48 to
  09:30:22 UTC), and call 9 was refused. So the recording does not show how
  the limit is counted.
- The SDK waited and sent the call again. The recorder blocks every second
  request, so c09 has no answer, and the run stopped: c10 to c12 were not
  sent.
- Both events matter to your team. You develop on your own free-tier key, so
  you meet the same limit, and a schema check that rejects every answer
  scores nothing.


.. _l13-run2-call:

Run 2: The Same Call, with Structured Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/er_demo.py
   :language: python
   :lines: 154-161
   :caption: lecture13/code/er_demo.py (excerpt)

- Each call is ``ask(client, png, **STRUCTURED)``. The model, the prompt and
  the thinking level stay as in Run 1. The other two changes are the pacing
  (calls start 13 s apart) and ``store``. 13 s is a choice, slower than 5
  calls a minute; Run 2 shows it worked once (12 of 12 answered), not that a
  shorter gap fails.
- ``response_format`` "Enforces that the generated response is a JSON object
  that complies with the JSON schema specified in this field"
  (`Interactions API reference <https://ai.google.dev/api/interactions-api>`_). The schema is the deck's own ``ANSWER_SCHEMA``. Its
  ``type`` field is a string ``enum``, which the
  `structured output page <https://ai.google.dev/gemini-api/docs/structured-output>`_
  lists among the supported keywords for strings.
- The deck's check still runs on every answer, because the structured
  output page says: "While output is syntactically
  correct JSON, always validate values in your application."
- ``store``: "Whether to store the response and request for later retrieval"
  (API reference). The
  `Interactions overview <https://ai.google.dev/gemini-api/docs/interactions-overview>`_
  (read 2026-10-18) says: "By default, the API stores all Interaction
  objects (store=true)", and "Free tier: The system retains interactions for
  1 day." Run 2 sets it to ``False``; Run 1 used the default, so its 8
  answered calls were stored. Run 2's responses carry no interaction ``id``,
  and Run 1's do.

.. warning::

   **What you send on the free tier.** The
   `pricing page <https://ai.google.dev/gemini-api/docs/pricing>`_ (read
   2026-10-18) answers "Used to improve our products" with "Yes" for the free
   tier of ``gemini-robotics-er-2-preview`` and "No" for the paid tier. Send
   only images you may share.


Run 2: All 12 Answers Pass the Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From ``outputs/score_er_rec2.txt``:

.. literalinclude:: outputs/score_er_rec2.txt
   :language: text
   :lines: 5-18

- All 12 calls were answered with no fence, and the check accepted all 12.
  With 13 s between call starts, no call got HTTP 429.
- The model named a defect on 6 cells, and all 6 have one. It said none on
  c03 and c07. Neither scratch shows in the images: c03's faces away from
  the camera, and c07's falls on the cell's dark side.
- It named the right type only on the 3 bulges. c02 and c12 are dents called
  bulges, and c04 is a scratch called a dent. On c10 it found the bulge, not
  the dent that faces away (152 degrees from the camera).
- c10 has two defects, so ``score_er.py`` scores each label as a set of types
  (``set_counts``), not as the single label that ``counts`` compares on the
  scripted example.


Run 2: Precision and Recall per Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each rate below comes with a 95% interval (Wilson score): the range of true
rates that these counts fit, at 95% confidence. It stays inside 0 to 1. L12's
2 x SE rule would give a range of zero width at 0 of 3 or 3 of 3, because the
SE of such a count is 0. The formula is in the footnote [#wilson]_.

From ``outputs/score_er_rec2.txt``:

.. literalinclude:: outputs/score_er_rec2.txt
   :language: text
   :lines: 20-34

.. warning::

   Each type is on 3 cells, so one cell moves its recall by 1 / 3 = 0.33, and
   DENT's precision comes from 1 call (one cell moves it by 1.00). Every
   per-type 95% interval (Wilson score) is 0.56 to 0.79 wide. 12 cells are too
   few to rank this model against your lidar detector or another model; see
   :ref:`l12-runs-a-claim-needs` in L12.

.. [#wilson] Wilson score interval for :math:`k` of :math:`n`, with
   :math:`\hat p = k / n` and :math:`z = 1.96`: center
   :math:`(\hat p + z^2 / 2n) / (1 + z^2 / n)`, half width
   :math:`\frac{z}{1 + z^2 / n} \sqrt{\hat p (1 - \hat p) / n + z^2 / 4n^2}`
   (``wilson`` in ``score_er.py``). For 0 of 3: 0.00 to 0.56.


Run 2: Where the Model Pointed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l13/er_points.png
   :alt: Six close-up photo crops side by side, each of part of a blue Li-Ion
         cell, with a black and white ring at the center and a numbered tag under it.
         Tag 1: the ring sits on a bump in the cell's left outline. Tag 2:
         the ring sits on a lighter, smeared patch near the bottom of the
         cell, beside the label text. Tag 3: on a tilted cell, the ring sits
         on a horizontal groove. Tag 4: the ring sits on a bump in the left
         outline. Tag 5: the ring sits on a small lighter patch in the upper
         part of the cell. Tag 6: the ring sits on a faint small patch
         beside the label text.
   :width: 95%
   :align: center

The model's type, then ARIAC's log:

1. c01: BULGE (a bulge).
2. c02: BULGE (a dent).
3. c04: DENT (a scratch).
4. c06: BULGE (a bulge).
5. c10: BULGE (a bulge; its dent faces away).
6. c12: BULGE (a dent).

- Each ring is the model's point in pixels: row = y x 1080 / 1000, column =
  x x 1920 / 1000. Each crop is 240 by 320 px of the 1920 by 1080 image,
  centered on the point.
- The instructor checked each ring by eye on the full image: every ring sits
  on a bump, a patch or a groove.
- The rings are not checked against a projected position. The camera model
  puts the cell about 80 px (about 8 mm) off, so those positions are only
  approximate. To locate a defect, your team finds the cell in the image
  itself.


Run 2: Tokens, Latency and Cost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   This part is in the notes only. The slides keep one line for it.

From ``outputs/score_er_rec2.txt``:

.. literalinclude:: outputs/score_er_rec2.txt
   :language: text
   :lines: 62-77

- Every call had 1203 input tokens: 103 of text and 1100 for the image.
  Thinking tokens are billed as output: for c01, 1203 + 51 + 332 = 1586, the
  ``total_tokens`` the API reported.
- The `pricing page <https://ai.google.dev/gemini-api/docs/pricing>`_ (read
  2026-10-18) gives two price sets for the paid tier, per million tokens:
  input "$1.00 (text / image / video / audio) through December 31, 2026" and
  "$2.00 (text / image / video / audio) starting January 1, 2027"; output
  (including thinking tokens) "$5.00 through December 31, 2026" and "$10.00
  starting January 1, 2027".
- The 12 calls cost $0.0307 at the 2026 prices and $0.0614 at the 2027
  prices (the last line of the output above). The Spring 2027 semester runs
  under the 2027 prices, so use those for your cost per call. The key is on
  the free tier ("Free of charge"), so the run cost $0.
- A call took 3.77 s on average. With 13 s between call starts, the whole run
  took 147 s.


Practical Points from the Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   This part is in the notes only. The slides keep one line for it.

**Gemini API robotics page.**

- "Crop or zoom into small or unclear objects before sending the image."
- "Query multiple times and average results for high-precision tasks." Each
  extra call adds latency and cost.
- The page warns that the models can occasionally "hallucinate" or provide
  incorrect information. Your schema check and your comparison with GP2 are
  how you catch it.

**Camera cost (ARIAC sensors page).**

- An RGB camera costs $800 at 1080p or $500 at 720p. It counts toward the
  sensor cost bonus, which pays only under the $9600 budget.


.. _l13-final-demo:

Final Demo Questions
--------------------

This section covers the procedure, rules and grading for Week 15 (Wednesday,
May 5). The full rules are in the final demo specification posted in Week 12.


The Procedure
~~~~~~~~~~~~~

1. **Code freeze:** your team pushes the git tag ``final-demo``
   before the deadline. The demo runs that commit.
2. **The unseen trial:** no team ever receives it. Before class, the
   instructor runs every team's Docker image on it, one after another on one
   machine, and records each run.
3. **Class time:** presentations with the recorded runs, 5 to 6 minutes per
   team, in an order drawn at random and posted this week.
4. **RO01 teams:** your image runs on the same machine as every other team's,
   so you need no connection during the run. You present live in the class
   video meeting.


Dates and Deliverables
~~~~~~~~~~~~~~~~~~~~~~

From the :doc:`final demo page </assignments/final_demo>`:

.. list-table::
   :header-rows: 1
   :widths: 24 76
   :class: compact-table

   * - **When**
     - **What**
   * - Fri, Apr 30, 11:59 pm
     - Code freeze: push your code-freeze tag ``final-demo`` and submit your team
       configuration file.
   * - Sat, May 1
     - The instructor builds every team's image. If yours does not build,
       the instructor emails your team, and you have 24 hours to push a fix
       tag, ``final-demo-fix``, that changes only build files (the Dockerfile
       and dependency lists). That fix costs the 10 points of "Builds and
       runs from the Dockerfile". If the fixed image still does not build,
       the run
       criteria (75 points) score 0.
   * - Tue, May 4, 11:59 pm
     - RO01 teams: upload your talk as a 5 to 6 minute video to ELMS-Canvas.
   * - Wed, May 5
     - Each team has a 10-minute slot: 6 minutes of talk (5 minimum), 3
       minutes of questions (one for each team member), 1 minute of
       change-over.
   * - After the demo
     - Each team member fills in the peer-review form.


The Run Rules
~~~~~~~~~~~~~

**How each run starts.** The ARIAC App, with the demo trial, your team
config, a fresh database, Record set to True and no cheat selected.

**After the launch.**

- No code edits, parameter changes or manual robot commands.
- Your code must not read the trial file. It learns the trial only through
  ARIAC topics and services.

**The Dockerfile** (ARIAC submission page).

- It sits in the repository root. It installs the dependencies, builds the
  ROS workspace, sources it in ``.bashrc``, and sets ``TEAM_CONFIG`` and
  ``TEAM_COMMAND``.
- For the evaluation run, the instructor passes one course API key as an
  environment variable. Your README names the variable your model's SDK
  reads (``GEMINI_API_KEY`` for Gemini). No key is ever committed
  (:doc:`final demo page </assignments/final_demo>`, Task 5).
- While developing, your team uses its own free-tier key (L1).


How the Run Is Scored (ARIAC Scoring Page)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Run score
   :class: note

   R = B + (sum of bonuses) - (sum of penalties), with

   B = 5000 × (kits done / kits wanted) + 12000 × (modules done / modules
   wanted).

.. list-table::
   :widths: 16 84
   :class: compact-table

   * - Bonuses
     - Each value is a maximum, which the run scales down: trial time (up to
       1000), inspection speed (up to 500), high-priority speed (up to 600),
       sensor cost (up to 1000), inspection classification (up to 500).
       They count only if every kit and module was submitted.
   * - Penalties
     - Good cell in the inspection bin 50, cell in the conveyor bin 25,
       object on an invalid surface 25, AGV collision 100, robot collision
       100 for every 5 s.
   * - Sensor cost
     - Under the $9600 budget, the bonus is 1000 × (1 - cost / 9600). Over
       it, the penalty is 1000 × (cost / 9600 - 1). Both from ARIAC's
       ``scoring.py``.

**Example.** A sensor cost of $10560, chosen for this example, gives:

1. 10560 / 9600 = 1.1,
2. 1.1 - 1 = 0.1,
3. 1000 × 0.1 = 100 points of penalty.


How the Final Demo Is Graded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the :doc:`final demo page </assignments/final_demo>` (Grading Rubric):

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - **Criterion**
     - **Points**
     - **How it is checked**
   * - Builds and runs from the Dockerfile
     - 10
     - The image builds and starts with your README commands
   * - Task 1 on the unseen trial
     - 15
     - 15 × (kits accepted / kits wanted)
   * - Task 2 on the unseen trial
     - 15
     - 15 × (modules accepted / modules wanted)
   * - Challenges handled
     - 15
     - Each challenge detected, a recovery action, the run continuing
   * - Safe run
     - 5
     - 5 minus 1 for each penalty event, not below 0
   * - Embodied-reasoning step
     - 15
     - The call in the run log and your comparison table; the model's
       scores do not change the points
   * - Presentation
     - 15
     - 5 to 6 minutes, with the four required parts
   * - Questions
     - 10
     - Each member answers a question about code that member did not present

- 10 + 15 + 15 + 15 + 5 + 15 = 75 points for the run, and 15 + 10 = 25 for
  the class session: 100 points, 20% of the course grade.
- The ARIAC run score R above is not the grade.


Your Questions
~~~~~~~~~~~~~~

- The rest of this segment is for your team's questions about the procedure,
  the rules and the grading.
- RO01 teams: ask by voice or in the meeting chat; the instructor reads chat
  questions aloud.
- RO01 teams: confirm how you will present in Week 15: live in the class
  video meeting, sharing your own slides.


.. _l13-next-class:

Next Class
----------

**Week 15 (Wednesday, May 5): final demo presentations.** 5 to 6 minutes per
team: architecture, design decisions, failure modes met and how they were
handled, with your recorded run.

**Before then:**

- Run Task 1 and Task 2 together on practice trials with different seeds and
  challenge times.
- Add the embodied-reasoning step and its measurement against GP2.
- Build the Docker image from a clean clone.
- RO01 teams: test sharing slides in the class video meeting.
- Optional: the :doc:`L13 references <l13_references>` and the
  :doc:`L13 self-check quiz <l13_quiz>` (ungraded).
