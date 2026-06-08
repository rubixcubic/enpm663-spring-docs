====================================================
Week 10: LLM-Based Task Planning II (VLM Grounding and Robust Replanning)
====================================================

Overview
--------

This lecture extends the LLM planner from Week 9 in two directions: VLM
grounding, where a vision-language model produces the scene description that
the LLM planner consumes; and closed-loop replanning, where the system
detects execution failure and re-prompts the planner with updated state.
Quiz #4 (covering W7 BT execution and W9 LLM I) is administered at the
start of class. PT3 is due today; PT4 is handed out.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Use a VLM (hosted multimodal API or local Qwen-VL/LLaVA) to produce a
     scene description from an ARIAC camera image.
   - Design a prompt that asks the VLM for spatial relations (above,
     left-of, in-slot) rather than just object labels.
   - Implement a closed-loop plan-execute-detect-replan cycle.
   - Decide when to retry a single action vs. when to ask for a full re-plan.
   - Compare LLM-planner output to PDDL-planner output on the same scene
     (validity, plan length, cost).


Topics
------

- VLM landscape: hosted multimodal APIs (Claude Vision, GPT-4o, Gemini),
  local options (Qwen-VL, LLaVA), tradeoffs.
- Scene description prompts: from "describe the image" to "list parts with
  positions and slot assignments."
- Closed-loop replanning loop: execute one action, re-observe, replan if the
  state drifted from expected.
- Replan triggers: action failure, world-state inconsistency, new order.
- Side-by-side: PDDL vs. LLM on the same scenario.


Hands-On Exercise
-----------------

Take a static ARIAC scene image, prompt a VLM for a JSON scene description,
then feed that description into Week 9's LLM planner. Compare the output
plan to the PDDL plan you wrote in Week 6 on a similar problem. (TODO:
starter notebook with API keys handling.)


ARIAC Tie-in
------------

PT4 (handed out today) builds exactly this loop on ARIAC: VLM grounding
feeding an LLM planner feeding PT3's executor. The closed-loop replan
handles faulty-part scenarios that PT3's PDDL domain may not cover
elegantly.


References
----------

- Claude Vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- GPT-4o vision: https://platform.openai.com/docs/guides/vision
- Qwen-VL: TODO link to model card.
- LLaVA: TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz #4 today (W7 BT execution, W9 LLM I).
- PT3 due today; PT4 (LLM Planner + VLM Grounding) is handed out and due
  Week 13.
- Week 11 covers motion planning, the layer below the executor.
