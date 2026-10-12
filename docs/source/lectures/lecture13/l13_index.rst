==============================================================================
L13: The Physical AI Frontier: VLAs, Robot Foundation Models, and World Models
==============================================================================

Overview
--------

All semester, your team has built one side of physical AI: an agent that
reasons about the factory and calls classical robot skills. This lecture
surveys the other side, where learned models produce the robot's actions.
It covers vision-language-action (VLA) models, robot foundation models,
embodied-reasoning models, and world models used to generate training data
and test policies in simulation. It compares them with the modular stack you
built, on data, compute, auditability and how each one fails, and looks at
how manufacturers are combining agents and robots today. The final
demo questions are answered at the end of class.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain what a VLA model is and how it differs from the modular stack built
  in this course.
- Describe the two-system design (a slow reasoning model above a fast control
  policy) used by many current VLAs.
- Explain what robot foundation models and world models are used for:
  generalizing across tasks, generating training data, testing in simulation.
- Compare a learned policy and a skills library for a factory task on data
  needs, compute, auditability and failure modes.
- Use a hosted embodied-reasoning model for one perception step, as the final
  demo requires.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- What the industry calls physical AI, and where this course sits in it.
- VLA models: OpenVLA, Physical Intelligence's pi-0 and pi-0.5, Google
  DeepMind's Gemini Robotics, NVIDIA GR00T; small open models such as SmolVLA.
- Two-system designs: an embodied-reasoning model that plans and calls tools
  above a VLA that moves the robot.
- World models and simulation: generating training data and testing policies
  before they reach a robot.
- What it costs: demonstration data, GPU memory for running and fine-tuning,
  and testing.
- Agentic manufacturing in industry: agents that coordinate machines and
  robots on the factory floor.
- Final demo questions.


ARIAC Tie-in
------------

ARIAC 2025 has no learned policies, and the final demo does not need one. The
final demo does use one physical AI model: a hosted embodied-reasoning model
for one perception step, measured against your GP2 pipeline.


Starting References
-------------------

- NVIDIA glossary, physical AI: https://www.nvidia.com/en-us/glossary/generative-physical-ai/
- OpenVLA: https://openvla.github.io/
- Physical Intelligence openpi (pi-0, pi-0.5): https://github.com/Physical-Intelligence/openpi
- Gemini Robotics: https://deepmind.google/models/gemini-robotics/
- NVIDIA Isaac GR00T: https://github.com/NVIDIA/Isaac-GR00T
- SmolVLA: https://huggingface.co/blog/smolvla


Next Steps
----------

- **The final demo is in Week 15.** Bring a tested system and a working
  Dockerfile.
