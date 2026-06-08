====================================================
Week 9: LLM-Based Task Planning I (Prompting, Structured Output, Tool Use)
====================================================

Overview
--------

This is the first lecture on the AI-augmented planning thread. We treat the
LLM as a swappable replacement for the PDDL planner: given a scene
description and a goal, the LLM produces a structured plan that PT3's BT
executor runs unchanged. The mechanics that make this reliable are
prompting (system messages, few-shot examples), structured output (JSON
schemas, validation, retry), and tool/function calling.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Design a system prompt for an LLM-as-planner with a clear role, a goal
     format, and a structured output format.
   - Specify a JSON schema for plans and validate LLM output against it.
   - Implement a retry loop that re-prompts the LLM on malformed output.
   - Use tool/function calling to let the LLM invoke explicit "actions"
     (defined in JSON Schema) instead of free-text plan steps.
   - Reason about token budgets, cost, and latency in a planning loop.


Topics
------

- LLM mental model: stateless function from prompt to text, with structured
  output extensions.
- Prompt structure: system + user; few-shot examples; output format
  constraints.
- JSON schemas as plan KR: typed actions, required fields, enums for action
  names.
- Validation and retry: catch malformed output, re-prompt with the error,
  cap retries.
- Tool/function calling: the modern alternative to free-text plans; how
  schemas become callable tools.


Hands-On Exercise
-----------------

Write a one-shot LLM call (Claude, GPT, or local Llama/Qwen) that takes a
scene description (3 colored parts, 2 kit slots) and a goal (kit each slot
with a specific part) and returns a JSON plan. Validate against a provided
JSON schema. (TODO: starter prompt + schema file.)


ARIAC Tie-in
------------

Forward-looking: PT4 (handed out next week) uses this exact mechanism on
ARIAC scenarios. Today's exercise is a toy version of the PT4 planner.


References
----------

- Anthropic API tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- OpenAI structured outputs: https://platform.openai.com/docs/guides/structured-outputs
- JSON Schema specification: https://json-schema.org/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Week 10 covers VLM grounding and closed-loop replanning, completing the
  PT4 toolkit.
- Continue PT3 work; due Week 10.
