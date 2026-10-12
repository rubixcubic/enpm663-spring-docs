====================================================
L2: System Architectures for AI-Augmented Robotics
====================================================

Overview
--------

This lecture sets up the architecture vocabulary used for the rest of the
course. It starts with the classical robot architectures (reactive,
behavior-based, subsumption, three-layer) and then the modern three-layer
architecture that agentic robot systems use. AI does not replace the
architecture: it plugs into specific layers (an LLM agent as the
deliberative planner, a VLM in perception) while motion stays classical. The
lecture contrasts this modular approach with end-to-end
vision-language-action (VLA) models, so you know the design space and why
this course builds the modular stack. L13 returns to VLAs in depth. Teams are
formed and GP1 is posted.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Name and contrast the classical robot architectures: reactive,
  behavior-based, subsumption and three-layer.
- Describe the modern three-layer architecture (deliberative, executive,
  reactive) and the data that flows between the layers.
- Identify where AI components (LLM, VLM) plug into a classical architecture
  and where classical components remain.
- Map the ARIAC 2025 interfaces and the course skills package onto a
  three-layer architecture.
- Summarize the end-to-end VLA alternative and the tradeoffs that lead this
  course to the modular stack.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- Classical robot architectures: reactive, behavior-based, subsumption,
  three-layer (Brooks, Gat).
- The modern three-layer architecture: deliberative planner, executive
  (behavior tree), reactive control (MoveIt 2 and the controllers).
- Where AI plugs in: an LLM agent as the deliberative planner, a VLM in
  perception, classical components unchanged.
- The end-to-end alternative: VLA models that map camera images and language
  straight to robot actions (OpenVLA, Physical Intelligence's pi-0, Gemini
  Robotics, Figure's Helix). Many current VLAs are two-system designs, a slow
  VLM for reasoning above a fast control policy. That matches the
  deliberative and reactive layers of this course, with no executive layer
  between them. Tradeoffs: data and GPU
  cost, failure modes that are hard to inspect, and auditability.
- Multi-robot coordination as a multi-agent problem: ARIAC's two inspection
  robots, two assembly robots, gantry welder and three AGVs share one workspace
  and one set of tasks.
- Case study: ARIAC 2025 as a three-layer instance.


ARIAC Tie-in
------------

ARIAC 2025 gives each robot a joint trajectory action and a gripper action,
each AGV a move action, and the factory a set of conveyors, sensors and
submission services. Those form the reactive layer. The course skills
package wraps them into skills such as picking a cell or moving an AGV. Your
behavior tree (GP1) is the executive layer, and your planner (GP3) or agent
(GP4) is the deliberative layer.


Starting References
-------------------

- Classical robot architectures (Brooks, Gat): TODO links.
- OpenVLA (open 7B vision-language-action model): https://openvla.github.io/
- Physical Intelligence pi-0: https://www.physicalintelligence.company/blog/pi0
- Gemini Robotics: https://deepmind.google/models/gemini-robotics/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
- Source material: ``Lectures_export/Architectures-2023-Spring.pptx``.


Next Steps
----------

- **Teams are formed today.** Post your team charter on ELMS before L3 (see
  the :doc:`syllabus </syllabus/index>`).
- **GP1 is posted today** and is due in Week 5.
- In the next lecture, we will cover **knowledge representation**: the
  symbolic models the architecture's layers exchange.
