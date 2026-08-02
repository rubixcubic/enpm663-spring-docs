====================================================================================
PT4: LLM Agent for Task Planning with VLM Grounding (Extends PT3)
====================================================================================

.. list-table::
   :widths: 25 25 25 25
   :class: compact-table

   * - **Hand out:** Week 10
     - **Due:** Week 13
     - **Weight:** 10%
     - **Extends:** PT3

Goal
----

Swap the PDDL planner for an LLM agent that consumes a VLM-grounded scene
description and the order, and that outputs a structured plan (JSON schema) or
per-step tool calls which the same BT executor from PT3 runs unchanged. The
agent replans in a closed loop when execution drifts from the expected state.
The classical-to-AI contrast with PT3 is the point of this project.

ARIAC Tie-in
------------

Same kitting scenarios as PT3, plus at least one scenario PT3's PDDL domain
cannot handle without code changes (for example, a new part type or an unusual
ordering constraint). The LLM agent should adapt at prompt time; PDDL would
need a domain rewrite. Motion is still executed through ARIAC's action servers
(MoveIt2 underneath); the AI complexity lives in planning and grounding.

Deliverable
-----------

- An LLM agent module (agent loop, tools, structured output, validation and
  retry; tool exposure via MCP where applicable).
- A VLM grounding module that produces the scene description.
- Executor modifications for closed-loop replanning.
- A side-by-side comparison of PDDL vs. LLM plans on identical inputs (validity,
  plan length, cost, latency).
- A demo and a reflection on LLM failure modes and how they were caught.

Relevant Lectures
-----------------

- Week 9: LLM-Based Task Planning I (Agent Loops, Tool Use, Structured Output).
- Week 10: LLM-Based Task Planning II (VLM Grounding and Agentic Replanning).
