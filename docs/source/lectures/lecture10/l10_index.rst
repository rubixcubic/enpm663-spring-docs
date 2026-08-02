====================================================================================
Week 10: LLM-Based Task Planning II (VLM Grounding and Agentic Replanning)
====================================================================================

Overview
--------

This lecture extends the Week 9 agent in two directions: VLM grounding, where a
vision-language model produces the scene description the agent observes; and
agentic closed-loop replanning, where the orchestrator detects that execution
drifted from the expected state and re-invokes the LLM with updated
observations. This is the agent loop from Week 9 closed around real feedback.
We also draw the honest boundary: for a fully specified kitting order the
classical PDDL planner from Week 6 is often the better tool (cheaper,
deterministic, auditable). The LLM agent earns its place when the order is
ambiguous, the scene is novel, or recovery requires reasoning the PDDL domain
did not anticipate. Quiz #4 (covering W7 BT execution and W9 LLM I) is
administered at the start of class. PT3 is due today; PT4 is handed out.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Use a VLM (hosted multimodal API or local Qwen-VL/LLaVA) to produce a
     scene description from an ARIAC camera image.
   - Design a prompt that asks the VLM for spatial relations (above,
     left-of, in-slot) rather than just object labels.
   - Implement an agentic closed loop: observe, plan/act, execute, re-observe,
     replan on drift.
   - Decide when to retry a single action vs. when to ask for a full re-plan.
   - Judge when a classical PDDL planner is the right tool and when an LLM
     agent is, and defend the choice per scenario.


Topics
------

- VLM landscape (2026): hosted multimodal APIs (Claude, GPT, Gemini), local
  options (Qwen-VL, LLaVA), and embodied-reasoning VLMs (e.g., Gemini
  Robotics-ER) that emit spatial relations; tradeoffs.
- Scene description prompts: from "describe the image" to "list parts with
  positions and slot assignments."
- Agentic closed loop: execute one action, re-observe, replan if the state
  drifted from expected; this is the Week 9 agent loop closed around feedback.
- Replan triggers: action failure, world-state inconsistency, new order.
- When NOT to use an LLM: for a fully specified kitting order, PDDL is cheaper,
  deterministic, and auditable. The LLM agent pays off on ambiguous orders,
  novel scenes, and recovery the domain did not anticipate.
- Side-by-side: PDDL vs. LLM agent on the same scenario (validity, plan length,
  cost, latency).


Hands-On Exercise
-----------------

Take a static ARIAC scene image, prompt a VLM for a JSON scene description,
then feed that description into Week 9's agent loop. Compare the output plan to
the PDDL plan you wrote in Week 6 on a similar problem, and note the case where
each approach is the better fit. (TODO: starter notebook with API-key
handling.)


ARIAC Tie-in
------------

PT4 (handed out today) builds exactly this loop on ARIAC: VLM grounding feeding
an LLM agent feeding PT3's executor. The closed-loop replan handles faulty-part
scenarios that PT3's PDDL domain may not cover elegantly.

.. note::

   PT4's executor calls the robot through ARIAC's provided action servers (the
   same pick and place actions PT3 already uses); teams do not need to write
   MoveIt2 code to complete PT4. The motion layer itself (MoveIt2, TF2 in
   depth, parameterized grasps) is covered next week (W11) for teams that want
   to customize grasping or debug motion failures. In other words, the agent
   and executor sit above a motion layer you can treat as a black box for PT4
   and open up in W11.


References
----------

- Claude Vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- GPT-4o vision: https://platform.openai.com/docs/guides/vision
- Gemini Robotics-ER (embodied reasoning VLM): TODO link to model card.
- Qwen-VL: TODO link to model card.
- LLaVA: TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz #4 today (W7 BT execution, W9 LLM I).
- PT3 due today; PT4 (LLM Agent + VLM Grounding) is handed out and due
  Week 13.
- Week 11 covers motion planning, the layer below the executor.
