====================================================
Lecture
====================================================

.. note::

   These notes follow the L13 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running ``er_demo.py`` and ``score_er.py`` with Python
   3.12.3, ``google-genai`` 2.29.0, ``httpx`` 0.28.1 and ``jsonschema``
   4.10.3. The scripts and how to run them are on the
   :doc:`code page <l13_code>`.

.. admonition:: Class logistics for this week
   :class: warning

   - **There is no quiz this week and nothing is due.** The five quizzes
     ended in Week 12.
   - **The final demo is next week**, Week 15 (Wednesday, May 5). The last
     part of class is for your questions about it.

The reference pages quoted below were read on 2026-10-12. They change often,
so the quotes are checked again the week before class.


.. _l13-physical-ai:

Physical AI and This Course
---------------------------

- All semester, your team built one side of physical AI: an agent that
  reasons about the factory and calls classical robot skills.
- This lecture surveys the other side, where learned models produce the
  robot's motions.
- It is a survey: no policy training and no GPU. No quiz this week and
  nothing is due.


Two Kinds of Physical AI System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Physical AI (NVIDIA glossary, used since L1)
   :class: note

   "Physical AI lets autonomous systems like cameras, robots, and self-driving
   cars perceive, understand, reason, and perform or orchestrate complex
   actions in the physical world."

The last two verbs give two kinds of system:

- **Perform:** a learned model produces the robot's actions. This is the VLA
  side, the subject of this lecture.
- **Orchestrate:** an agent decides what happens next and calls skills that
  carry it out. This is the side the course built.


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

.. admonition:: The question for this lecture
   :class: hint

   What changes if a learned model replaces the reactive layer, or the
   reactive and executive layers together?


Two More Technologies the Same Glossary Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Reinforcement learning.** The glossary says: "Reinforcement learning
teaches autonomous machines skills in a simulated environment to perform in
the real world."

**Simulation and world foundation models.** The glossary says the two are
used together to create synthetic data for training. The section
:ref:`l13-world-models` returns to both.

**The lecture, in order:**

1. VLA models and robot foundation models.
2. Two-system designs, next to your three layers.
3. World models and simulation.
4. What learned policies cost and how they fail.
5. Agentic manufacturing in industry.
6. A demonstration of the embodied-reasoning step from the final demo, then
   final demo questions.


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
   to robot actions. The course surveys VLAs; it does not build one.

**The step.** ``inspection_robot_1`` (a UR3e with a Robotiq 2F-85 gripper)
picks a cell off the moving conveyor and places it in a voltage tester.

**Two ways to do it.**

- **GP4:** the agent returns a tool call with typed arguments, checked
  against a JSON schema. The skills package turns it into a MoveIt 2
  trajectory.
- **VLA:** the model reads the camera images and an instruction such as
  "place the cell in tester 1" and outputs the motion itself. No planner and
  no named skill sit in between.


Five VLAs
~~~~~~~~~

**OpenVLA** (`project page <https://openvla.github.io/>`_)

- "a 7B parameter open-source vision-language-action model (VLA), pretrained
  on 970k robot episodes from the Open X-Embodiment dataset."
- It maps image inputs to embeddings and predicts action tokens, which are
  decoded into continuous actions the robot executes.

**pi-0 and pi-0.5** (Physical Intelligence,
`openpi <https://github.com/Physical-Intelligence/openpi>`_)

- pi-0 is "a flow-based vision-language-action model (VLA)".
- pi-0.5 is "an upgraded version of :math:`\pi_0` with better open-world
  generalization."
- The base checkpoints are "pre-trained on 10k+ hours of robot data."
- The README writes the names with Greek letters: :math:`\pi_0` and
  :math:`\pi_{0.5}`.

**Gemini Robotics** (Google DeepMind,
`model page <https://deepmind.google/models/gemini-robotics/>`_)

- The page calls its VLA a model "that converts vision and language input
  into motor control."
- On 2026-10-12 the current versions are Gemini Robotics 2 and Gemini
  Robotics ER 2, written with no hyphen.

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
horizontal position carries data; the labels alternate above and below the
line so they do not overlap.

.. image:: /_static/images/l13/model_timeline.svg
   :alt: A horizontal timeline from June 2024 to October 2026 with year marks
         at 2025 and 2026. Dots, left to right: OpenVLA, Jun 2024; pi-0, Oct
         2024; SmolVLA, Jun 2025; pi-0.5 in openpi, Sep 2025; GR00T N1.7, Apr
         2026; Gemini Robotics ER 2, Jul 2026; ER 1.6 deprecated, Aug 2026.
         Labels alternate above and below the axis; only the horizontal
         position carries data.
   :width: 90%
   :align: center

Gemini Robotics 2 is not on the line: its page gives no date. The table gives
the source of each date (all read on 2026-10-12).

.. list-table::
   :header-rows: 1
   :widths: 30 17 53
   :class: compact-table

   * - **Event**
     - **Date**
     - **Source**
   * - OpenVLA paper, version 1
     - 13 Jun 2024
     - `arXiv 2406.09246 <https://arxiv.org/abs/2406.09246>`_, submission
       date
   * - pi-0 paper, version 1
     - 31 Oct 2024
     - `arXiv 2410.24164 <https://arxiv.org/abs/2410.24164>`_, submission
       date
   * - SmolVLA blog post
     - 3 Jun 2025
     - Hugging Face blog, publication date
   * - pi-0.5 released in openpi
     - Sep 2025
     - openpi README, Updates list
   * - GR00T N1.7 release
     - 18 Apr 2026
     - GitHub release ``n1.7-release``, publication date
   * - Gemini Robotics ER 2 preview
     - Jul 2026
     - Gemini API robotics page, "Latest update"
   * - Gemini Robotics ER 1.6
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

The references show this pattern:

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
  embodied-reasoning model judges cell defects from camera images. The
  section :ref:`l13-demo` shows it.

.. tip::

   Your skills package needed no demonstrations: it needed the ARIAC geometry
   and a MoveIt 2 configuration. A VLA trades that engineering for data.


.. _l13-two-system:

Two-System Designs
------------------

A **two-system design** puts a slow model, for meaning and planning, above a
fast control policy. The 2026 VLA web check recorded in the course design log
found this to be the dominant VLA design.


Two Forms of the Split
~~~~~~~~~~~~~~~~~~~~~~

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
         ER model or a VLM, blue), whose output goes straight to a fast policy
         (a VLA or an action expert, orange), marked tag 4, which outputs
         robot actions. Panel 3: ARIAC topics and services, lidar and camera
         go into an LLM agent or PDDL planner (blue), then through a tool call
         marked tag 5 to the behavior tree (green), then to the skills package
         and MoveIt 2 (orange), which send ARIAC trajectory and gripper
         actions. Dashed arrows marked tag 6 go back up from the skills to the
         tree and from the tree to the agent.
   :width: 95%
   :align: center

1. One VLA model, such as OpenVLA.
2. A two-system design: Gemini Robotics (ER model and VLA), or SmolVLA (VLM
   and action expert).
3. Your stack.
4. The slow model's output goes straight to the policy.
5. A tool call, checked against a JSON schema (L8).
6. Status and failure reasons move up.

Colors: blue is the deliberative role, green the executive role, orange the
reactive role, gray no layer role.


Mapping the Split onto the Course
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - None: the policy acts on the slow model's output directly
     - The behavior tree: checks each skill result before the next step and
       stops cleanly on failure (L4, L7, L11)
   * - Reactive
     - A learned policy (the VLA or action expert)
     - Classical motion planning: the skills package and MoveIt 2

The slow system matches your agent closely. The fast system does not: yours
is classical motion planning, not a learned policy.


What Crosses the Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Course:** a named tool call with arguments checked against a JSON schema
  (L8). A person can read it.
- **SmolVLA:** the VLM passes learned features (lists of numbers) to the
  action expert. A person cannot read them.

.. admonition:: Conclusion
   :class: important

   - Your architecture has the deliberative and reactive roles of a
     two-system VLA, plus an executive layer the VLA lacks.
   - The differences are three: what sits in the fast layer, what crosses
     the interface, and whether anything checks each step.
   - These three differences are where the auditability comparison in
     :ref:`l13-cost` starts.


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

Collecting that much on real robots is slow. That is why synthetic data from
simulation and world models matters for the learned side.


ARIAC Has Written Rules; a World Model Learns Its Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**ARIAC 2025** is a physics simulation in Gazebo Harmonic whose rules
engineers wrote: the conveyor, the inspection door that pushes a cell into
the inspection bin without a passing report, the voltage testers that publish
a noisy voltage, the scoring formula.

**A world model** learns its rules from data. It can produce scenes no one
programmed. It can also be wrong in ways no one programmed.

**The same purpose:** test before hardware. Every GP was tested in ARIAC
before anyone would trust it on a real cell.


A Learned Policy Is Judged by Outcomes over Many Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A learned policy has no readable plan to check, so you judge it by what
  happens over many runs.
- L12's sample-size rule applies: how many runs, and how much the result
  varies between runs.
- A rate from a few runs can only take a few values. With 4 runs (chosen for
  this example), one run moves a success rate by 1 / 4 = 0.25, so the rate
  can only be 0, 0.25, 0.50, 0.75 or 1.

.. tip::

   Your stack is checked at each step and by its outcomes. A learned policy
   is checked only by its outcomes, so it needs more runs before you trust a
   number.


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
fine-tuning it. Each value is a lower bound ("more than" or "or more"), so a
bar shows the least memory the source asks for.

.. image:: /_static/images/l13/gpu_memory.svg
   :alt: A horizontal bar chart. The horizontal axis is the GPU memory the
         source lists, in GB, from 0 to 80, as a lower bound. The vertical
         axis lists six steps. Course stack (hosted API): no bar, no GPU
         assumed. openpi, run the model: more than 8 GB. GR00T, run the model:
         16 GB or more. openpi, LoRA fine-tuning: more than 22.5 GB. GR00T,
         fine-tuning: 40 GB or more per GPU. openpi, full fine-tuning: more
         than 70 GB.
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

   The course design log puts it this way: LLM-based plans produce
   inspectable traces; learned-policy failures are opaque. With a VLA, you
   see what the robot did, not a readable reason.


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
     - A failure has a named place: a skill returns failure, a schema check
       rejects the agent's output, the VLM misreads a cell. L11's recovery
       structures catch each one.
     - No step returns failure. You find the failure from the outcome, for
       example a dropped cell or a collision penalty in the ARIAC score.
   * - A new task
     - An engineer writes or changes a skill and the PDDL domain or tool list.
     - The foundation models aim to generalize to new tasks (pi-0.5: "better
       open-world generalization"), with fine-tuning when they do not.

The last row favors the learned side: your stack can only do what its skills
cover.


Class Discussion: Which Part Would You Replace with a VLA?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Prompt
   :class: hint

   ``inspection_robot_1`` must pick each cell off the moving conveyor and
   place it in one of two voltage testers. Which part of your system would
   you replace with a VLA, and what would you need first?

Points the discussion covered:

- Demonstrations of the UR3e picking cells at your conveyor speed.
- A GPU of the size in the GPU memory chart.
- A test plan with many runs, and a way to detect a failed pick, since the
  policy will not report one.
- The ARIAC penalties a bad policy would trigger: a cell in the conveyor bin
  (25), an object on an invalid surface (25), a robot collision (100 for
  every 5 s).


Why the Course Keeps Its Scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The course grades engineering judgment on unseen trials: the final demo
  runs your system on a trial you have never seen.
- To grade judgment, the grader must see why the system did what it did. The
  readable traces of rows 3 and 4 make that possible.
- A learned policy would add GPU needs and demonstration data, and would
  replace those traces with outcomes only.

.. tip::

   The learned side is surveyed so you can judge when it fits: when a task
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
an order into a production plan, and operator agents send function calls to
the automation modules, which do the physical work.

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
not fully reliable for directly controlling an automation system". They
propose an assistant whose actions human supervisors approve.


Industry Example: Amazon DeepFleet, at Production Scale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Amazon Science blog
<https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination>`__
(August 11, 2025):

- A foundation model trained on data from Amazon fulfillment and sortation
  centers. It is a learned model, not an LLM agent.
- Amazon reports it helps assign tasks and route robots around congestion,
  "increasing the efficiency of our robot deployments by 10%".
- Today it advises the existing fleet planner: Amazon is "initially using
  them to predict congestion, with the longer-term goal of using them to
  produce outputs like assignments of robots to specific retrieval tasks and
  target locations".

.. note::

   Production scale today: a learned model advises a classical planner. The
   two LLM examples are lab work, and both keep a check between the LLM and
   the robots.


What the Examples Show
~~~~~~~~~~~~~~~~~~~~~~

- Published work so far is pilots and research. In each case, the LLM or
  model proposes, and a check, a planner or a person decides. Motion and
  control stay classical.
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

   **The model in this section is a scripted stand-in.** A real model's
   answers vary. No API key was used. The client code is the real
   ``google-genai`` SDK; only the server's answers are scripted.

   Code: ``lecture13/code/er_demo.py`` and ``score_er.py``, run with
   ``run_all.sh`` (see :doc:`l13_code`). Versions: Python 3.12.3,
   ``google-genai`` 2.29.0, ``httpx`` 0.28.1, ``jsonschema`` 4.10.3.


What an Embodied-Reasoning Model Is, and Which One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: embodied-reasoning (ER) model
   :class: note

   An **embodied-reasoning model** is a vision-language model trained to
   answer spatial questions about a scene, such as where a part is or which
   cell looks damaged.

**The course example** (Gemini API robotics page, read 2026-10-12):

- Google's Gemini Robotics ER, through the Gemini API and the
  ``google-genai`` Python SDK.
- API model: ``gemini-robotics-er-2-preview``, a preview model that supports
  structured output and function calling.
- "Gemini Robotics ER 1.6 was deprecated on August 31, 2026." The model name
  is checked again the week before class.


The Final Demo's ER Step, in Five Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Capture** one image from an RGB camera placed through your team config,
   over the inspection conveyor.
2. **Ask:** send the image and one question to the model, and ask for the
   answer in a JSON format (L8).
3. **Check** the answer against a JSON schema, as GP4 does for the agent.
4. **Locate**, when the answer is a point: turn its image position into a
   position in a robot frame with the camera model (L10) and TF2.
5. **Measure** against GP2: on the same cells, compare with your lidar
   detector and with the ground truth. Report precision and recall per
   defect type, latency and cost per call.

The same call also finds the top shell over the assembly table in Task 2 (it
spawns at a random pose). This lecture's example is defects. Whether defects
0.84 to 2.49 mm deep show in a camera image is part of what your team
measures.


Step 2: The Question
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/er_demo.py
   :language: python
   :lines: 29-36
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
   :lines: 121-131
   :caption: lecture13/code/er_demo.py (excerpt)

- ``client.interactions.create`` with a model, an input list and a generation
  config follows the Python example on the Gemini API robotics page. The
  example uploads the image file; this code sends the bytes in the request
  instead (base64 text in the ``data`` field).
- "For thinking level use medium for a good balance between latency and
  performance" (same page).


How the Stand-In Replaces the Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/er_demo.py
   :language: python
   :lines: 102-118
   :caption: lecture13/code/er_demo.py (excerpt)

- ``httpx.MockTransport`` catches each request before it leaves the machine
  and returns the next scripted answer. ``httpx`` is the HTTP library the SDK
  uses to send requests.
- With a real key, you drop the mock client: the rest of the code stays the
  same. The :doc:`code page <l13_code>` lists what you need for that.


The Request the SDK Sends
~~~~~~~~~~~~~~~~~~~~~~~~~

The body of the first call, from ``outputs/er_demo.txt``:

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
   :lines: 39-44
   :caption: lecture13/code/score_er.py (excerpt)


The Comparison Table for 12 Cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/score_er.txt
   :language: text
   :caption: outputs/score_er.txt

The ground truth and the lidar labels are chosen for this example, and the ER
labels come from the scripted stand-in. The table shows how to score; it says
nothing about how a real model or a real detector does.


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
   and the stand-in missed c04. The same number hides different cells; the
   labels agree on only 7 of 11 cells.

.. warning::

   Each type has 2 defective cells here, so one cell moves recall by 1 / 2 =
   0.50. With so few cells, a difference between the two detectors can be
   one cell. Use many more cells (L12).


Practical Points from the Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
- Your API key is passed as an environment variable at run time, never
  committed.

In class, if model access is confirmed, the same code runs against the real
model, and its real answer is shown, mistakes included.


.. _l13-final-demo:

Final Demo Questions
--------------------

This section covers the procedure, rules and grading for Week 15 (Wednesday,
May 5). The full rules are in the final demo specification posted in Week 12.


The Procedure
~~~~~~~~~~~~~

1. **Code freeze:** your team pushes the git tag named in the specification
   before the deadline. The demo runs that commit.
2. **The unseen trial:** no team ever receives it. Before class, the
   instructor runs every team's Docker image on it, one after another on one
   machine, and records each run.
3. **Class time:** presentations with the recorded runs, 5 to 6 minutes per
   team, in an order drawn and posted before Week 15.
4. **RO01 teams:** your image runs on the same machine as every other team's,
   so you need no connection during the run. You present live in the class
   video meeting.


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
- API keys are passed as environment variables at run time and never
  committed (course :doc:`AI setup page </ariac/ai_setup>`).


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
     - Trial time (1000), inspection speed (500), high-priority speed (600),
       sensor cost under budget (1000), inspection classification (500).
       They count only if every kit and module was submitted.
   * - Penalties
     - Good cell in the inspection bin 50, cell in the conveyor bin 25,
       object on an invalid surface 25, AGV collision 100, robot collision
       100 for every 5 s.
   * - Sensor cost
     - Over the $9600 budget, the penalty is 1000 × (cost / 9600 - 1), from
       ARIAC's ``scoring.py``.

**Example.** A sensor cost of $10560, chosen for this example, gives:

1. 10560 / 9600 = 1.1,
2. 1.1 - 1 = 0.1,
3. 1000 × 0.1 = 100 points of penalty.


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
