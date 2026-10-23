=======================================================
L9: LLM Agents II: VLM Grounding and Agentic Replanning
=======================================================

Overview
--------

After every call, the L8 agent read the testers, the conveyor and agv1 from
ROS 2 topics, and ``guard()`` checked the next call against that reading. It
had no camera, and in its run nothing failed. This lecture adds two things to
it.

The first is **grounding**. A **vision-language model (VLM)** takes a camera
image and a text prompt, and returns text. You ask it for a JSON record that
your code checks against a schema: for each tray slot, whether it is occupied,
the cell type, any visible damage and a confidence. Your code then checks each
field against a second source. Tray occupancy comes from ARIAC's
``/agvN/tray_status`` topic. The cell type comes from the voltage your team
recorded for the cell on a voltage tester. A field where the two disagree is a
flag, and the agent does not act on it.

The second is **replanning**. After every call, the agent compares the new
observation with what the action should have done. On a mismatch there are three
moves: **retry** the action, **wait** for a device to come back, or ask for a
**new plan**. A decision chart sorts ARIAC 2025's four challenges among the three.
No code picks the move: Gemini chooses, and ``guard()`` refuses a call that
breaks a rule.

Two demonstrations show both ideas. In the first, Gemini reads an ARIAC
camera image of agv1's tray, and its record is cross-checked slot by
slot; a scripted stand-in VLM with mistakes written in then shows the checker
catching them. In the second, Gemini chooses the skill calls that fill agv1's tray in
ARIAC while voltage tester 1 malfunctions, once with a replan policy
and once with a wait policy. The Gemini runs were recorded once; a rerun gives
different answers.

The lecture ends with a limit: for a fully specified task, such as the normal
Task 1 flow, the PDDL planner from GP3 is the better tool. It costs nothing per
call, gives the same plan for the same input, and plans from a domain file
your team wrote and can read. The LLM agent helps on ambiguity, on cases the
domain has no action for, and on recovery the domain did not plan for.

.. important::

   **ARIAC tie-in.** Your team places the cameras the VLM reads, and each
   one costs money from the sensor budget. Lidar still finds the defects
   (GP2). The agent observes the conveyor and voltage tester status topics,
   the AGV tray status and the high-priority order topic, and it reacts to
   the conveyor malfunction, the voltage tester malfunction and the
   high-priority order. The demonstration runs a real voltage tester
   malfunction from an ARIAC trial file.

.. important::

   **Group project.** GP3 (PDDL planner and behavior tree executor) is due
   today. **GP4 (LLM agent with VLM grounding) is posted today** and is due
   Friday, April 23, at 11:59 pm. GP4 replaces the GP3 planner with an LLM agent, adds a
   VLM, and tests the agent on a conveyor malfunction, a voltage tester
   malfunction and high-priority orders. The vacuum tool malfunction happens
   only in Task 2; the final demo tests it.

.. admonition:: This week
   :class: warning

   - **Quiz 4** (L7 and L8) opens the class.
   - **GP3 is due**, with its peer-review form.
   - **GP4 is posted.**


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe how a call to a VLM differs from a text-only LLM call (image input,
  prompt, structured output), and name hosted, local and embodied-reasoning
  options.
- Design a VLM prompt and JSON schema that ask for the cell type, tray slot
  and visible damage of each cell in an ARIAC camera image.
- Check a VLM's record against a second source, and decide what to do when
  they disagree.
- Explain the agentic closed loop: act, observe again, compare the observed
  state with the expected state, and replan when they differ.
- Classify an ARIAC failure as a case for retrying one action, waiting, or
  asking for a new plan, and justify the choice.
- Compare a PDDL planner and an LLM agent on validity, plan length, cost and
  latency, and describe the GP4 deliverables.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l9_lecture
   l9_code
   l9_exercises
   l9_quiz
   l9_references


Next Steps
----------

- In the next lecture we cover **L10: Frames, Transforms, and Motion
  Planning** (Wednesday, April 7):

  - TF2.
  - The camera model: from a pixel to a pose.
  - MoveIt 2, and how the course skills package works.

- **Quiz 5** (Wednesday, April 14, start of class) covers L9 and L10.

- **Before next class:**

  - Fill in the GP3 peer-review form on ELMS-Canvas (GP3 was due today).
  - Read the GP4 specification, and agree on who owns the agent, the VLM
    module and the comparison.
  - Set up LLM and VLM access (a free-tier Gemini API key or a local model
    with Ollama) with the :doc:`AI Access </ariac/ai_setup>` page.
  - Rerun the scripted VLM check: on your copy, ``python3 vlm_check.py`` in
    ``lecture9/code`` (see :doc:`l9_code`), and compare its output with the
    notes. The Gemini runs need ARIAC and an API key.
  - Work through the :doc:`L9 exercises <l9_exercises>` and the
    :doc:`self-check quiz <l9_quiz>`.
