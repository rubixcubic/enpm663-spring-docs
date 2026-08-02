====================================================================================
Week 3: Knowledge Representation for AI-Augmented Robotics
====================================================================================

Overview
--------

This lecture covers the foundational knowledge-representation (KR) techniques
that AI-augmented robotic systems rely on. Every architecture's blocks
exchange representations of the world, the task, and the robot's own state;
this lecture introduces the formalisms that make those representations
precise: frames, ontologies, and hierarchical task and world models (4D/RCS).
Examples are anchored in ARIAC (orders, parts, kits as frame-based
representations). Teams of 3 are formed at the start of class.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Explain why knowledge representation matters for AI-augmented robotic
     systems (LLMs, VLMs, and classical planners all consume some KR).
   - Apply frame-based representations to model ARIAC orders, parts, and kits.
   - Describe ontologies and their role in connecting perception to planning.
   - Distinguish hierarchical KR (4D/RCS) from flat representations.
   - Map a KR design onto consumers: PDDL predicates, LLM JSON schemas, VLM
     scene descriptions.


Topics
------

- Why KR matters in AI-augmented systems: the LLM needs to "see" the world
  as text; the planner needs structured predicates; the executor needs typed
  action arguments.
- Frame-based representations: slots, fillers, default values, inheritance.
- Ontologies: classes, relations, instances.
- Hierarchical task and world models (4D/RCS): time-varying attribute tables.
- ARIAC representations: orders, products, parts, kit slots, faulty parts,
  priority levels.


Hands-On Exercise
-----------------

In teams, design a frame-based representation for an ARIAC kit (slots,
expected parts per slot, faulty-part handling). Express the same kit as a
JSON schema for an LLM. Compare what is preserved and what is lost in each
form.


ARIAC Tie-in
------------

The same kit representation will be consumed by PT3's PDDL planner (as typed
predicates), PT4's LLM planner (as JSON schema), and PT5's recovery logic
(as state to update when a fault is detected). A coherent KR design across
these consumers is the difference between an integrated and a brittle system.


References
----------

- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
- ARIAC order interface and configuration files: TODO links into ARIAC docs.
- Source material: ``Lectures_export/KR-Lecture-Spring2023.pptx`` (NIST 4D/RCS
  examples to be re-anchored to ARIAC for the new lecture).


Next Steps
----------

- Teams formed today; one team contract per team (TODO: template) signed
  before next class.
- Week 4 covers behavior trees, the executive layer that will consume the KR
  designed today.
- Continue PT1 work; due Week 5.
