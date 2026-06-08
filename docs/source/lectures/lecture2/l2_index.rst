====================================================
Week 2: System Architectures for AI-Augmented Robotics
====================================================

Overview
--------

This lecture establishes the architectural vocabulary used throughout the
course. We begin with the classical architecture taxonomy (reactive,
behavior-based, subsumption, three-layer/hybrid), then introduce the modern
three-layer architecture as the dominant pattern for AI-augmented robotic
systems. The key insight is that AI does not replace the architecture; it
plugs into specific layers (LLM as deliberative planner, VLM as perception,
classical motion). PT1 is handed out at the end of this lecture.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Name and contrast classical robot architectures (reactive, behavior-based,
     subsumption, three-layer/hybrid).
   - Describe the modern three-layer architecture (deliberative, executive,
     reactive) and the data flow between layers.
   - Identify where AI components (LLM, VLM) plug into classical architectures
     and where classical components remain.
   - Map ARIAC's node graph onto a three-layer architecture instance.


Topics
------

- Classical control architectures: reactive, behavior-based, subsumption,
  three-layer (Brooks, Gat).
- The modern three-layer default: deliberative planner, executive (BT),
  reactive control (MoveIt2 + low-level).
- Where AI plugs in: LLM as deliberative planner, VLM as perception
  augmentation, classical components unchanged.
- Case study: ARIAC's component graph as a three-layer instance.


Hands-On Exercise
-----------------

In teams or pairs, sketch a block diagram for an AI-augmented ARIAC kitting
task. Label each block with the layer it belongs to and the data exchanged
with adjacent blocks. Share diagrams; compare design choices.


ARIAC Tie-in
------------

ARIAC's competition kit includes a kitting robot, an AGV, an overhead camera
system, and the order subscriber. Together they form a textbook three-layer
architecture. The exercise traces an ARIAC order from arrival through planning
to execution.


References
----------

- Classical robot architectures (Brooks, Gat): TODO links.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
- Source material: ``Lectures_export/Architectures-2023-Spring.pptx``.


Next Steps
----------

- Week 3 covers Knowledge Representation, the symbolic layer that the
  architecture's blocks exchange.
- Continue PT1 work; due Week 5.
- Form teams of 3 by Week 3.
