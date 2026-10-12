====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   No graded quiz covers L13: the five in-class quizzes listed in the
   :doc:`syllabus </syllabus/index>` ended in Week 12, and L11 to L13 are
   graded through the final demo. Working through this page is good
   preparation for the final demo's embodied-reasoning step. Memorizing the
   answers below is not.

This quiz covers Lecture 13: the two kinds of
physical AI system, VLAs and robot foundation models, two-system designs,
world models, what learned policies cost, the embodied-reasoning
demonstration with its scoring, and the final demo procedure. Every question
can be answered from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 8)
==================================

.. admonition:: Question 1
   :class: hint

   The NVIDIA definition of physical AI ends with "perform or orchestrate
   complex actions". Which kind of system did the course build?

   A. Perform: a learned model produces the robot's actions

   B. Orchestrate: an agent decides what happens next and calls skills

   C. Both, through a VLA in the reactive layer

   D. Neither: the course builds only perception

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The course built an agent (GP3 planner, then GP4 LLM agent) that decides
   what happens next and calls classical skills. "Perform", where a learned
   model produces the actions, is the VLA side the lecture surveys.


.. admonition:: Question 2
   :class: hint

   What does a VLA output for the step "place the cell in tester 1"?

   A. A tool call with typed arguments, checked against a JSON schema

   B. A PDDL plan

   C. The motion itself, with no planner and no named skill in between

   D. A defect label in JSON

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A VLA maps camera images and language straight to robot actions. Answer A
   is what the GP4 agent returns; the skills package then turns it into a
   MoveIt 2 trajectory.


.. admonition:: Question 3
   :class: hint

   Which model does its own reference page describe as "a compact (450M),
   open-source Vision-Language-Action model for robotics that runs on
   consumer hardware"?

   A. OpenVLA

   B. pi-0

   C. NVIDIA Isaac GR00T N1.7

   D. SmolVLA

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   That is the Hugging Face blog's description of SmolVLA. OpenVLA is a 7B
   parameter model, pi-0 is "a flow-based vision-language-action model", and
   GR00T N1.7 is a VLA "for generalized humanoid robot skills".


.. admonition:: Question 4
   :class: hint

   In a two-system VLA mapped onto the course's three layers, which layer
   has no counterpart?

   A. Deliberative

   B. Executive

   C. Reactive

   D. Perception

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The slow model (an ER model or VLM) plays the deliberative role and the
   learned policy the reactive one. The policy acts on the slow model's
   output directly, so nothing plays the behavior tree's role of checking
   each step and stopping cleanly on failure.


.. admonition:: Question 5
   :class: hint

   Inside SmolVLA, what passes from the VLM to the action expert?

   A. A named tool call with schema-checked arguments

   B. Learned features: lists of numbers a person cannot read

   C. A PDDL plan

   D. A JSON answer with points in [y, x] format

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   This is one of the three differences the lecture names: in the course, a
   named tool call a person can read crosses the interface; in SmolVLA,
   learned features do.


.. admonition:: Question 6
   :class: hint

   A learned policy is tested over 4 runs. Which of these success rates can
   it **not** report?

   A. 0.25

   B. 0.50

   C. 0.60

   D. 0.75

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With 4 runs, one run moves the rate by 1 / 4 = 0.25, so the rate can only
   be 0, 0.25, 0.50, 0.75 or 1. A rate of 0.60 would need 2.4 successes.


.. admonition:: Question 7
   :class: hint

   In the demonstration, why was the answer for cell c10 rejected?

   A. It was not valid JSON

   B. Its point was outside 0 to 1000

   C. It named the defect type CRACK, which the schema does not allow

   D. The stand-in returned no answer for it

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The output line is ``defects.0.type: 'CRACK' is not one of ['DENT',
   'SCRATCH', 'BULGE']``. The schema allows only the three types in ARIAC's
   ``CellDefect.msg``, so c10 is left out of both detectors' scores and
   counted as rejected.


.. admonition:: Question 8
   :class: hint

   Where does the ground truth for the final demo's ER comparison come
   from?

   A. The graded run, launched with every cheat tool on

   B. Practice runs launched with ``log_cell_info:=true``, which prints each
      cell's defects to the Gazebo log

   C. The ER model's own answers

   D. ARIAC's ``defects.yaml``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ARIAC prints each cell's defects when launched with
   ``log_cell_info:=true`` (``cheat_tools_plugin.cpp``). The graded run uses
   no cheat: the instructor starts it with no cheat selected.


----


True or False (Questions 9 to 14)
=================================

.. admonition:: Question 9
   :class: hint

   True or false: ARIAC 2025 has no learned policies, and the final demo
   does not need one.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   The final demo uses one physical AI model, for perception only: a hosted
   embodied-reasoning model judges cell defects from camera images.


.. admonition:: Question 10
   :class: hint

   True or false: in this lecture, "world model" means the knowledge each
   layer keeps about the factory, as in L3's 4D/RCS.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The slides warn about exactly this. In L13 a world model is a learned
   model that predicts how a scene will change, used to generate training
   data and to test robot policies in simulation. The 4D/RCS meaning is
   L3's.


.. admonition:: Question 11
   :class: hint

   True or false: according to the openpi README, full fine-tuning needs
   more than 70 GB of GPU memory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   The README lists more than 70 GB for full fine-tuning (A100 80GB or H100),
   more than 22.5 GB for LoRA fine-tuning and more than 8 GB to run the
   model, on one GPU. The course stack assumes no GPU.


.. admonition:: Question 12
   :class: hint

   True or false: when a VLA drops a cell, the policy returns a failure
   status that the system can act on.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   No step of a VLA returns failure. You find the failure from the outcome,
   for example a dropped cell or a collision penalty in the ARIAC score. In
   your stack, a failure has a named place: the skill returns failure.


.. admonition:: Question 13
   :class: hint

   True or false: the demonstration's comparison table shows that the GP2
   lidar detector is better than Gemini Robotics ER.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The ground truth and the lidar labels are chosen for the example, and the
   ER labels come from a scripted stand-in, not a model. The table shows how
   to score; it says nothing about how a real model or a real detector does.


.. admonition:: Question 14
   :class: hint

   True or false: in the final demo, each team runs its own system live in
   class on the unseen trial.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   Before class, the instructor runs every team's Docker image on the unseen
   trial, one after another on one machine, and records each run. Class
   time is for presentations with the recorded runs, 5 to 7 minutes per
   team.


----


Short Answer (Questions 15 to 18)
=================================

.. admonition:: Question 15
   :class: hint

   Name the three differences between your architecture and a two-system
   VLA.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. **What sits in the fast layer:** classical motion planning (the skills
      package and MoveIt 2) against a learned policy.
   2. **What crosses the interface:** a named tool call checked against a
      JSON schema, which a person can read, against learned features, which
      a person cannot.
   3. **Whether anything checks each step:** your behavior tree does; a
      two-system VLA has no executive layer.


.. admonition:: Question 16
   :class: hint

   In the demonstration, ER called cell c07 a bulge. Its truth is a dent.
   Which counts does this one answer change, and why is that worth knowing?

.. dropdown:: Answer
   :class-container: sd-border-success

   It adds an FN to DENT (a dented cell not called a dent) and an FP to
   BULGE (a bulge called where there is none). So one mistake lowers DENT
   recall and BULGE precision at once: ER's DENT recall is 1 / 2 = 0.50 and
   its BULGE precision 2 / 3 = 0.67. When you read a table, a wrong type
   shows up in two rows.


.. admonition:: Question 17
   :class: hint

   In the demonstration, both detectors have SCRATCH recall 1 / 2 = 0.50.
   Does that mean they behave the same on scratches? What should you do
   before you compare them in your final demo?

.. dropdown:: Answer
   :class-container: sd-border-success

   No. Lidar missed c09 and the stand-in missed c04: the same number hides
   different cells, and the labels agree on only 7 of 11 cells. Each type
   has 2 defective cells, so one cell moves recall by 0.50, and a difference
   between the detectors can be one cell. Use many more cells (L12).


.. admonition:: Question 18
   :class: hint

   Give two reasons the course keeps classical skills instead of a learned
   policy, and one situation where the lecture says the learned side fits.

.. dropdown:: Answer
   :class-container: sd-border-success

   The course grades engineering judgment on unseen trials, and the grader
   must see why the system did what it did: your stack leaves readable
   traces, a learned policy only outcomes. A learned policy would also add
   GPU needs and demonstration data. The learned side fits when a task has no
   skill, when demonstrations exist, or when outcomes over many runs are
   enough evidence.
