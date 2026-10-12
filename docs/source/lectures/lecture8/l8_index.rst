==============================================================
L8: LLM Agents I: Agent Loops, Tool Use, and Structured Output
==============================================================

Overview
--------

This is the first lecture on LLM-based planning. In industry an LLM is rarely
called once; it is the reasoning core of an *agent*. A program called the
orchestrator runs a loop: it reads the state of the world, asks the LLM what
to do next, runs the tool the LLM chose, feeds the result back, and repeats
until the goal is met or a stop condition fires. This lecture builds that
loop and treats the robot skills that GP3's executor already runs as the
agent's tools. Three mechanisms make the loop reliable: prompting, structured
output checked against a JSON schema, and tool calling through the Model
Context Protocol (MCP).


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the agent loop (observe, reason, act, observe the result) and the
  orchestrator that runs it, as distinct from the LLM itself.
- Contrast plan-and-execute (produce a full plan, then run it) with ReAct
  (interleave reasoning and tool calls).
- Design a system prompt for an LLM planner with a role, a goal format and an
  output format.
- Specify a JSON schema for plans or tool calls and validate LLM output
  against it, with a bounded retry.
- Explain how tool calling and MCP expose robot skills to an LLM, and manage
  the context, token budget, cost and latency of a loop.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- The LLM as a function from a prompt to text; the agent behavior comes from
  the orchestrator loop around it.
- The agent loop: observe, reason, call a tool, observe the result; stop
  conditions and step limits.
- Planning patterns: plan-and-execute and ReAct, and when a robot task wants
  each one.
- Prompt structure: system and user messages, few-shot examples, output
  format.
- JSON schemas as a representation of plans and actions: typed actions,
  required fields, enums.
- Validation and retry: catch malformed output, re-prompt with the error, cap
  the retries.
- Tool calling and MCP: how a schema becomes a callable tool, and how MCP
  standardizes tools across agent frameworks. ROS 2 MCP servers such as
  ``ros-mcp-server`` expose topics and services this way.
- Context and memory: which state to carry between iterations, and the cost
  and latency of a loop.


ARIAC Tie-in
------------

GP4 wraps this loop around the ARIAC factory. The agent's tools are the
actions GP3's executor already runs (pick a cell and place it with the
skills package, move an AGV and submit a kit through the ARIAC interfaces),
so the agent decides the next action and the classical executor carries it
out.


Starting References
-------------------

- Anthropic API tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- OpenAI structured outputs: https://platform.openai.com/docs/guides/structured-outputs
- Model Context Protocol (MCP): https://modelcontextprotocol.io/
- ros-mcp-server: https://github.com/robotmcp/ros-mcp-server
- ReAct (Yao et al.): https://arxiv.org/abs/2210.03629
- JSON Schema: https://json-schema.org/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Read the LLM Prompting and MCP pre-reads before this class (see
  :doc:`Pre-Read </preread/index>`).
- GP3 is due in Week 10.
- In the next lecture, we will add **VLM grounding and agentic replanning** to
  the agent.
