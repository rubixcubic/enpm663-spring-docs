====================================================
Pre-Read Material
====================================================

Some material this course depends on is **assumed knowledge** rather than
lecture content: either it comes from a prerequisite course, or it is a
supporting topic broad enough that covering it in class would crowd out the
agentic and physical AI material it supports.

That material lives here. **Each page states when to read it.** Each one is
read *before* the lecture that assumes it.

.. list-table::
   :widths: 30 15 55
   :header-rows: 1
   :class: compact-table

   * - Page
     - When
     - Why it is here
   * - :doc:`ROS 2 Refresher </preread/ros2-refresher>`
     - Before L1
     - The ROS 2 the syllabus assumes: workspaces and packages, nodes and
       topics, the ``ros2`` tools, parameters, services, actions, launch
       files and reading C++ code, plus lifecycle nodes for reference. L1
       then teaches QoS, executors, actions in depth and TF2.
   * - :doc:`PDDL Primer </preread/pddl-primer>`
     - Before L6
     - What a planning problem is, on a two-room toy world: facts, actions
       with preconditions and effects, a goal, and a plan by hand. L6 builds
       the ARIAC domain and runs Fast Downward.
   * - :doc:`LLM Prompting and Structured Output </preread/llm-prompting>`
     - Before L8
     - What an LLM API call sends and returns, why the history is resent on
       every call, tokens, the API key, and JSON basics. L8 teaches system
       prompts, schemas with validation and retry, and tool calling.
   * - :doc:`Model Context Protocol (MCP) </preread/mcp>`
     - Before L8
     - Why a standard protocol for tools, host, client and server, the three
       primitives, the messages and the two transports. L8 builds and calls
       an MCP server.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   ros2-refresher
   pddl-primer
   llm-prompting
   mcp
