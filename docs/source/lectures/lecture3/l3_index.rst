======================================================
L3: Knowledge Representation for Agentic Robotics
======================================================

Overview
--------

**This lecture covers what crosses the interfaces between L2's layers: a
representation of the world, the task and the robot.** **Knowledge representation** is the study of how to write
that model down so programs can use it.

Three programs in this course read the same world model, each in its own
form: a PDDL planner (GP3) needs typed objects and true or false facts, an LLM
agent (GP4) reads text and must answer in a form a JSON schema can check, and
the executor (from GP1 on) needs typed action arguments. The lecture starts
with what goes wrong when they do not share one model.

It then covers two formalisms. **Frames**, from Minsky's 1974 memo, describe a
kind of object as named slots with fillers and defaults, and more specific
frames inherit the slots of general ones; the lecture builds frames for ARIAC
cells, kits, modules, AGVs and high-priority orders. An **ontology** adds the
classes, the relations between them and the instances that exist now, so
software can check that a statement makes sense.

Next come two ideas from NIST's **4D/RCS** reference model, used inside L2's
three layers: each layer keeps only the detail it decides with, and an error
is handled where it is seen, with status passed up. Then one kit state is
written three ways (PDDL facts, a JSON record checked by a JSON schema, and
text), all printed by one script. A worked example picks the voltage range of
the kit's fourth cell, then checks it against chance: the tester readings are
noisy, so the range keeps a margin inside each limit. The lecture ends with
what the GP1 tree must know: which facts are observed, which are inferred and
which are unknown, and one cell tracked from events, step by step.

.. important::

   **ARIAC tie-in.** One kit representation serves three readers later in the
   semester: GP3's planner reads it as facts, GP4's agent reads it as a record
   checked by a JSON schema, and the final demo's recovery logic updates it
   when a cell fails inspection or a tester stops giving valid readings.

.. important::

   **Group project.** GP1 is under way. Its world model lives on the
   ``py_trees`` blackboard, so decide your key names and types now, and give
   each key an owner in your team charter, due before this class.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain what goes wrong when a PDDL planner, an LLM agent and an executor
  keep separate copies of one world model.
- Apply frames (slots, fillers, defaults, inheritance) to ARIAC cells, kits,
  modules and AGVs.
- Describe an ontology, and trace one dented cell from perception to planning
  with it.
- Explain two ideas from NIST's 4D/RCS reference model, and apply them to
  the three layers of the ARIAC stack.
- Write one kit as PDDL facts, as a JSON record checked by a JSON schema, and
  as text.
- Identify which facts about a cell are observed, inferred or unknown at a
  step of Task 1.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l3_lecture
   l3_code
   l3_exercises
   l3_quiz
   l3_references


Next Steps
----------

- **Quiz 1** is next week (Wednesday, February 17), at the start of class:
  closed notes, on ELMS-Canvas or paper, covering L1 to L3. Review the ARIAC
  2025 tasks, challenges and how ARIAC scores a run; QoS, executors, actions
  and TF2 and their demo results; the classical and three-layer architectures
  and AI in the three layers; frames, ontologies, the two 4D/RCS ideas and the
  three views of a kit.
- In the next lecture we cover **L4: Behavior Trees for Task Execution**, the
  executive layer, which reads and writes the blackboard. After L4, your team
  writes the GP1 tree.
- **Before next class:**

  - Run ``kit_views.py``, ``ontology_check.py`` and ``track_cell.py`` (see
    :doc:`l3_code`) and compare your output with the notes.
  - Work through the :doc:`L3 exercises <l3_exercises>` and the
    :doc:`self-check quiz <l3_quiz>`.
  - Continue GP1 setup, and agree on your blackboard key names.
