==============================================================
L8: LLM Agents I: Agent Loops, Tool Use, and Structured Output
==============================================================

Overview
--------

This is the first of two lectures on planning with a large language model
(LLM), and the first class after spring break. GP4 replaces GP3's PDDL
planner with an **LLM agent**. The lecture answers one question: what must the
code around the LLM do so that the robots stay safe?

It starts with where the LLM goes in the GP3 stack. Only the decision part
changes. The world model, the plan-to-BT executor, the skills package and the
GP2 lidar detector stay. An LLM call takes a list of messages and returns
text, keeps nothing between calls, and can return a different answer to the
same messages. So the program around it must send the state on every call,
check every output before anything moves, and limit the cost.

That program is the **orchestrator**. It runs the **agent loop**: read the
state, ask the LLM, check and run the tool call it returns, record the
result, and stop when a stop condition fires. A live demonstration runs an
orchestrator with Gemini driving the ARIAC inspection robots through the
course skills, and a scripted model shows the guard refusing a call. The
lecture then compares **plan-and-execute** with **ReAct**
on ARIAC situations, shows how to write a system message for a planner, and
keeps the arithmetic (the kit voltage window) in code.

The second half covers **structured output**: a JSON schema for one AGV
move, validation in five steps with semantic checks and a bounded retry, and
what constrained output from a provider does and does not remove, with one
real model output run through the same check. Next comes **tool calling**
and the **Model Context Protocol (MCP)**, with ten tools (7 skills and 3 readings) served
from an MCP server, listed and called from a client against ARIAC. The last
section measures how the input grows with each loop step, from the Gemini
run's token counts, what a run costs, and how a model's latency compares with
the factory's clocks.

.. important::

   **ARIAC tie-in.** The agent's tools are the course skills of the two
   inspection robots and three ARIAC readings, and the demonstration runs
   them in ARIAC 2025. The guard checks what each robot holds, the tester
   readings and the AGV's tray before any call runs. The factory's clocks
   (the conveyor at up to 0.1 m/s, a 4 s target for each inspection report)
   decide which loops stay classical.

.. important::

   **Group project.** GP3 is due next week (Week 10, March 31), and GP4, the
   LLM agent with VLM grounding, is posted then. GP4 uses everything in this
   lecture: the loop, the guards, the schemas and the cost report.

.. note::

   **Not in this lecture.** VLM grounding, replanning around feedback and the
   comparison of the planner with the agent on the same trial are
   :doc:`L9 </lectures/lecture9/l9_index>`. The pre-reads for this lecture,
   LLM Prompting and Structured Output and Model Context Protocol (MCP), are
   listed on the :doc:`Pre-Read </preread/index>` page.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the agent loop (observe, reason, act, observe the result) and the
  orchestrator that runs it, as distinct from the LLM itself.
- Compare plan-and-execute with ReAct, and choose one for a given ARIAC
  situation with a reason.
- Design a system prompt for an LLM planner with a role, the factory facts,
  rules and an output format.
- Write a JSON schema for an agent decision and validate LLM output against
  it, with semantic checks and a bounded retry.
- Explain how tool calling and MCP expose robot actions to an LLM, and what
  guards the orchestrator keeps between the LLM and the robots.
- Estimate how context size, cost and latency grow with the number of loop
  steps, and say which ARIAC decisions are too time-critical for an LLM.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l8_lecture
   l8_code
   l8_exercises
   l8_quiz
   l8_references


Next Steps
----------

- In the next lecture we cover **L9: LLM Agents II: VLM Grounding and
  Agentic Replanning** (Wednesday, March 31):

  - A VLM describes the camera images for the agent.
  - The loop closes around feedback for replanning.
  - The class compares the PDDL planner and the agent on the same trial.
  - **Quiz 4** at the start of class covers L7 and L8. GP3 is due, and GP4
    is posted.

- **Before next class:**

  - Set up LLM access: a hosted API account or a local open-weight model.
  - Run the offline L8 scripts (see :doc:`l8_code`): ``validator.py`` and
    ``token_growth.py`` print the tables of the notes, and
    ``python3 orchestrator.py --fake --runs 2`` runs the loop without ARIAC.
    The ARIAC and Gemini demos need the course container.
  - Work through the :doc:`L8 exercises <l8_exercises>` and the
    :doc:`self-check quiz <l8_quiz>`.
  - Finish GP3: the executor and the replanning demo.
