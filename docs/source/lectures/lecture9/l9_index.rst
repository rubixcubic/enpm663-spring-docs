=======================================================
L9: LLM Agents II: VLM Grounding and Agentic Replanning
=======================================================

Overview
--------

This lecture extends the L8 agent in two directions. With VLM grounding, a
vision-language model describes what the cameras see, and the agent uses that
description as its observation. With agentic replanning, the orchestrator
notices that the factory has drifted from the expected state and asks the
LLM again with the new observations. The lecture also draws the boundary
honestly: for a fully specified task, the PDDL planner from L6 is often the
better tool (cheaper, deterministic, auditable). The LLM agent earns its
place when the situation is ambiguous, new, or needs a recovery the PDDL
domain did not plan for. Quiz 4 (L7 and L8) is given at the start of class.
GP3 is due and GP4 is posted.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Use a VLM (a hosted multimodal API or a local model) to describe a cell or a
  tray from an ARIAC camera image.
- Design a prompt that asks a VLM for defects and spatial relations, not only
  labels.
- Implement an agentic closed loop: observe, act, re-observe, replan when the
  state drifts.
- Decide when to retry one action and when to ask for a new plan.
- Judge when a PDDL planner is the right tool and when an LLM agent is, and
  defend the choice for a given situation.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- VLMs in 2026: hosted multimodal APIs (Claude, GPT, Gemini), local models
  (Qwen-VL, LLaVA), and embodied-reasoning models (Gemini Robotics ER) that
  answer spatial questions about an image.
- Scene description prompts: from "describe the image" to "list each cell, its
  defects and its slot".
- The agentic closed loop: act, re-observe, replan when the state drifted; the
  L8 loop closed around feedback.
- Replanning triggers: a failed action, an inconsistent world state, a
  high-priority order.
- When not to use an LLM: for a fully specified task, PDDL is cheaper,
  deterministic and auditable.
- Side by side: PDDL and the LLM agent on the same trial (validity, plan
  length, cost, latency).


ARIAC Tie-in
------------

GP4 builds this loop on ARIAC: a VLM describes the cells for an LLM agent,
and the agent drives GP3's executor. GP4 tests it on the situations GP3's
PDDL domain does not model: a conveyor malfunction, a voltage tester that
stops giving valid readings, a vacuum tool that fails to grasp, and high-priority orders.
The agent calls the course skills package, so GP4 needs no MoveIt 2 code;
L10 opens up the motion layer underneath.


Starting References
-------------------

- Claude vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- OpenAI vision: https://platform.openai.com/docs/guides/vision
- Gemini Robotics: https://deepmind.google/models/gemini-robotics/
- Qwen-VL: TODO link to model card.
- LLaVA: TODO link.
- ARIAC 2025 challenges: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz 4 today (L7 and L8).
- GP3 is due today. **GP4 is posted today** and is due in Week 13.
- In the next lecture, we will cover **motion planning**, the layer below the
  executor.
