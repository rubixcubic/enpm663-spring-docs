====================================================================================
Week 9: LLM-Based Task Planning I (Agent Loops, Tool Use, and Structured Output)
====================================================================================

Overview
--------

This is the first lecture on the AI-augmented planning thread. In industry, an
LLM is rarely deployed as a one-shot function; it is the reasoning core of an
*agent*: an orchestrator runs a loop that reads the world state, asks the LLM
what to do next, executes the tool the LLM chose, feeds the observation back,
and repeats until the goal is met or a stop condition fires. We introduce that
loop here and treat the LLM planner as an agent whose "tools" are the robot
actions PT3's BT executor already exposes. The mechanics that make this
reliable are prompting (system messages, few-shot examples), structured output
(JSON schemas, validation, retry), and tool/function calling standardized
through the Model Context Protocol (MCP).


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Describe the agent loop (observe, reason, act, observe result) and the
     role of the orchestrator that runs it, as distinct from the LLM itself.
   - Contrast two dominant planning patterns: plan-and-execute (produce a full
     plan, then run it, the LLM analog of the W6 PDDL planner) and ReAct
     (interleave reasoning and tool calls step by step).
   - Design a system prompt for an LLM-as-planner with a clear role, a goal
     format, and a structured output format.
   - Specify a JSON schema for plans or tool calls and validate LLM output
     against it, with a bounded re-prompt-on-error retry loop.
   - Explain how tool/function calling and MCP expose robot actions to an LLM,
     and manage context (what state persists across loop iterations), token
     budget, cost, and latency.


Topics
------

- LLM mental model: a stateless function from prompt to text; the agent
  behavior comes from the orchestrator loop wrapped around it, not the model.
- The agent loop: observe, reason, act (call a tool), observe the result,
  decide the next step; stop conditions and step caps.
- Planning patterns: plan-and-execute vs. ReAct; when a robot task wants a full
  plan up front (auditable, cheaper) vs. step-by-step reasoning (adapts to
  surprises). Reflexion-style self-critique as an extension.
- Prompt structure: system + user; few-shot examples; output format
  constraints.
- JSON schemas as plan/action KR: typed actions, required fields, enums for
  action names.
- Validation and retry: catch malformed output, re-prompt with the error,
  cap retries.
- Tool/function calling and MCP: how a schema becomes a callable tool, and how
  MCP has become the industry-standard protocol (2024 onward) for exposing
  tools and context to LLMs across frameworks (LangGraph, the OpenAI Agents
  SDK, the Claude Agent SDK).
- Context and memory: what world state to carry across iterations, and the
  token-budget, cost, and latency consequences of a multi-step loop.


Hands-On Exercise
-----------------

Two small steps on a toy scene (3 colored parts, 2 kit slots):

1. Write a one-shot LLM call (Claude, GPT, or local Llama/Qwen) that takes a
   scene description and a goal (kit each slot with a specific part) and
   returns a JSON plan. Validate against a provided JSON schema and add a
   single re-prompt-on-invalid retry.
2. Turn it into a minimal agent loop: expose one ``place_part(part, slot)``
   tool via function calling, and let the LLM place parts one at a time,
   receiving a short "result" observation after each call, until both slots
   are filled. (TODO: starter prompt, schema, and tool stub.)


ARIAC Tie-in
------------

Forward-looking: PT4 (handed out next week) wraps this agent loop around
ARIAC's real robot actions. The tools the LLM calls are the same pick and
place actions PT3's BT executor already drives, so the agent produces a plan
(or a next action) and the classical executor carries it out. Today's exercise
is a toy version of the PT4 agent.


References
----------

- Anthropic API tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- OpenAI structured outputs: https://platform.openai.com/docs/guides/structured-outputs
- Model Context Protocol (MCP): https://modelcontextprotocol.io/
- ReAct (Yao et al., reason + act): https://arxiv.org/abs/2210.03629
- JSON Schema specification: https://json-schema.org/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Week 10 covers VLM grounding and agentic closed-loop replanning, completing
  the PT4 toolkit.
- Continue PT3 work; due Week 10.
