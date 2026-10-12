======================================================
L3: Knowledge Representation for AI-Augmented Robotics
======================================================

Overview
--------

Every layer of an agentic robot system exchanges a model of the world, the
task and the robot's own state. This lecture covers the formalisms that make
those models precise: frames, ontologies, and hierarchical task and world
models (4D/RCS). The examples use the ARIAC 2025 factory: battery cells,
kits, modules, AGV stations and high-priority orders.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why knowledge representation matters when LLMs, VLMs and classical
  planners all consume the same world model.
- Apply frame-based representations to ARIAC cells, kits and modules.
- Describe ontologies and their role in connecting perception to planning.
- Distinguish hierarchical representations (4D/RCS) from flat ones.
- Map one representation onto its consumers: PDDL predicates, a JSON schema
  for an LLM, and a VLM scene description.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- Why representation matters: the LLM reads the world as text, the planner
  needs predicates, the executor needs typed action arguments.
- Frame-based representations: slots, fillers, default values, inheritance.
- Ontologies: classes, relations, instances.
- Hierarchical task and world models (4D/RCS).
- ARIAC representations: a cell (Li-Ion or Ni-MH, voltage, defects), a kit
  (four cells on a tray, the kit voltage tolerance), a module (shells, cells,
  welds), AGV stations, high-priority orders.


ARIAC Tie-in
------------

One kit representation serves three consumers later in the semester: GP3's
PDDL planner reads it as typed predicates, GP4's LLM agent reads it as a JSON
schema, and the final demo's recovery logic updates it when a cell fails
inspection or a tester stops reporting. A representation that all three can
use is the difference between an integrated system and a brittle one.


Starting References
-------------------

- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
- ARIAC 2025 scenario: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
- Source material: ``Lectures_export/KR-Lecture-Spring2023.pptx`` (NIST 4D/RCS examples to be re-anchored to ARIAC).


Next Steps
----------

- Continue GP1; it is due in Week 5.
- In the next lecture, we will cover **behavior trees**, the executive layer
  that runs on today's representation.
