====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 4,
   at the start of L9, covers L7 and L8. Working through this page is good
   preparation for it. Memorizing the answers below is not.

This quiz covers Lecture 8: where the LLM goes in the stack, the LLM as a
function, the agent loop and the orchestrator, plan-and-execute and ReAct,
prompt structure, JSON Schema validation with a bounded retry, tool calling
and MCP, and context, cost and latency. Every question can be answered from
the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 11)
===================================

.. admonition:: Question 1
   :class: hint

   Between two calls, what does an LLM keep about the factory?

   A. The result of the last tool call

   B. Nothing; the program sends the state and the earlier turns again on
      every call

   C. The system message, but not the user messages

   D. The latest state it read from ROS

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   An LLM call takes a list of messages and returns text, and between calls
   it keeps nothing. The program, not the model, keeps the conversation and
   sends it again on every call. **D** is wrong twice: the model keeps
   nothing, and it never reads ROS; the orchestrator does.


.. admonition:: Question 2
   :class: hint

   The model replies "done". Who decides that the goal is reached?

   A. The model: "done" ends the run

   B. The executor, when its last subtree succeeds

   C. The orchestrator, by checking the state in code

   D. The operator, by reading the log

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The model can say "done"; only the orchestrator decides, by checking the
   state in code. In the demo, ``shipped()`` checks that ``agv1`` is at
   ``SHIPPING``. If the check fails, the orchestrator sends back
   "goal not reached" and the loop goes on.


.. admonition:: Question 3
   :class: hint

   In Run 1 of the orchestrator demo, the characters sent were 666, then 839,
   then 1025. Why do they grow?

   A. The model's replies get longer

   B. Each call sends the whole history again, and every step adds a tool
      call and its result to it

   C. The system message grows with every step

   D. The tool list gains a tool after every call

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each call sends the system message, the tool list and every message so
   far. Each step adds one model reply and one result: 839 − 666 = 173 more,
   then 1025 − 839 = 186 more. The system message and the tool list stay the
   same.


.. admonition:: Question 4
   :class: hint

   The validator gets ``{"agv": 2, "station": "SHIPPING"}`` while ``agv2``
   holds 3 cells. Which step refuses it?

   A. Step 1, parsing the JSON

   B. Step 2, the schema

   C. Step 3, the semantic checks

   D. None: the output is valid

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The text is valid JSON, ``agv`` 2 is inside 1 to 3 and ``SHIPPING`` is in
   the enum, so it passes steps 1 and 2. Only code that knows the factory's
   state sees that ``agv2`` holds 3 of 4 cells: "semantic: agv2 holds 3 of 4
   cells".


.. admonition:: Question 5
   :class: hint

   The validator refuses ``{"agv": 1, "station": "SHIPPING", "speed": 2}``.
   Which schema keyword does the output break?

   A. ``required``

   B. ``enum``

   C. ``maximum``

   D. ``additionalProperties``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   The schema sets ``"additionalProperties": False``, so a field not listed
   in ``properties`` is refused: "Additional properties are not allowed
   ('speed' was unexpected)". The required fields are present and their
   values are valid.


.. admonition:: Question 6
   :class: hint

   A provider holds the model's output to your schema while it is generated
   (constrained output, such as ``strict: true`` on a tool). Which errors
   does that remove?

   A. Parse and schema errors only

   B. Semantic errors only

   C. All errors, so the orchestrator's checks can go

   D. No errors

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   Constrained output removes parse and schema errors (steps 1 and 2), not
   semantic errors. A schema-perfect output can still ship a tray with 3
   cells, so the semantic checks, the error feedback and the retry cap
   (steps 3 to 5) stay.


.. admonition:: Question 7
   :class: hint

   How does an MCP client find out which tools a server offers?

   A. It reads the server's Python source

   B. It sends a ``tools/list`` request

   C. It sends a ``tools/call`` request with no arguments

   D. The LLM tells it

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   MCP messages are JSON-RPC 2.0. A client finds the tools with
   ``tools/list`` and runs one with ``tools/call``. In the demo, the client's
   ``list_tools()`` printed the ``move-agv`` tool and its input schema.


.. admonition:: Question 8
   :class: hint

   In the MCP demo, ``agv1`` is at ``SHIPPING`` and the client calls
   ``move-agv`` with ``{"agv": 1, "station": "ASSEMBLY"}``. What comes back?

   A. ``is_error`` ``True``, because the move failed

   B. ``is_error`` ``False``, with ``"status": "REJECTED"`` and the reason in
      the result

   C. An exception in the client

   D. ``is_error`` ``False``, with ``"status": "SUCCEEDED"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ARIAC has no path from ``SHIPPING`` to ``ASSEMBLY``. The tool ran and
   reported the failure in its result, so ``is_error`` is ``False``. The call
   with AGV 4 is the other case: it failed the server's own argument check,
   the tool never ran, and ``is_error`` was ``True``.


.. admonition:: Question 9
   :class: hint

   With the lecture's values (:math:`F` = 2000 tokens on every call,
   :math:`h` = 250 tokens per earlier step), how many input tokens does call
   10 of a ReAct run send?

   A. 2250

   B. 4250

   C. 4500

   D. 31,250

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Call :math:`k` sends :math:`F + (k - 1)\,h`: 2000 + 9 × 250 = 4250. It is
   the "last call" value for 10 steps in the ``token_growth.py`` table.
   **D**, 31,250, is the total over all 10 calls.


.. admonition:: Question 10
   :class: hint

   Which ARIAC decision should stay classical because of time?

   A. Which cells go in which kit

   B. When to switch the cell feed

   C. The inspection report for a cell on the moving conveyor

   D. How to respond to a challenge

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ARIAC's target for an inspection report is 4 s, and the report must arrive
   before the cell reaches the door. At 0.1 m/s a cell moves 0.4 m in 4 s,
   and every second spent waiting for a model moves it another 0.1 m. Loops
   tied to the moving conveyor stay classical; **A**, **B** and **D** are the
   slower decisions the agent can own.


.. admonition:: Question 11
   :class: hint

   A voltage tester reports ``MALFUNCTIONING`` in the middle of a kit. Which
   pattern did the lecture choose?

   A. Plan-and-execute: write a full plan at once

   B. ReAct-style steps, then a new plan

   C. ReAct for the rest of the trial

   D. No LLM call: retry the tester until it works

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   What still works is unclear until a few results come back, so the agent
   takes ReAct-style steps, then writes a new plan. This is the common
   hybrid: plan-and-execute with ReAct-style recovery when a trigger fires,
   which matches the L7 executor.


----


True or False (Questions 12 to 17)
==================================

.. admonition:: Question 12
   :class: hint

   With ``MAX_RETRIES`` = 2, the bounded retry makes 2 attempts in all.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   It makes 3 attempts: the first one and 2 retries. In retry run 2 all three
   failed, and after the third failure nothing was sent back; the
   orchestrator fell back.


.. admonition:: Question 13
   :class: hint

   With the ``mcp`` package 2.3.0, the server class is imported with
   ``from mcp.server.fastmcp import FastMCP``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   In ``mcp`` 2.x the class that 1.x tutorials call ``FastMCP`` is
   ``MCPServer``, imported from ``mcp.server.mcpserver``. The 1.x import
   fails with "FastMCP was renamed to MCPServer".


.. admonition:: Question 14
   :class: hint

   The input schema that the MCP server generated for ``move-agv`` refuses
   extra fields, like the hand-written schema in ``validator.py``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The generated schema has ``minimum``, ``maximum``, the ``enum`` and the
   ``required`` list, but no ``additionalProperties``. The hand-written
   schema is stricter. Check what your server generates.


.. admonition:: Question 15
   :class: hint

   ARIAC itself checks each team configuration file against a JSON schema,
   with the Python ``jsonschema`` package, before the simulation starts.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The schema is ``ariac_setup/config/user_config_schema.json`` (draft-07).
   In it ``CONVEYOR_SPEED`` must be above 0 and at most 0.1, and a sensor's
   ``TYPE`` must be one of ``break_beam``, ``distance``, ``lidar`` or
   ``camera``. A bad file is refused before the simulation starts.


.. admonition:: Question 16
   :class: hint

   A low enough temperature makes an LLM's output safe to run without checks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Settings such as temperature change how much the answers vary. No setting
   makes the output safe to run without checks, so the orchestrator checks
   every output before anything moves.


.. admonition:: Question 17
   :class: hint

   For GP4, the lecture recommends giving the LLM raw publish access to ROS
   topics through ros-mcp-server.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ros-mcp-server lets an LLM publish and subscribe to topics, call services
   and actions, and set parameters: wide access to the robot system.
   Task-level tools behind the executor's guards are safer. Each team may
   choose whether to use MCP at all; the tool schemas are the same either
   way.


----


Short Answer (Questions 18 to 20)
=================================

.. admonition:: Question 18
   :class: hint

   Three Li-Ion cells on a tray measure 3.55 V, 3.62 V and 3.70 V. What does
   the orchestrator put in the prompt about the fourth cell, how does it get
   that, and why not just send the three voltages?

.. dropdown:: Answer
   :class-container: sd-border-success

   The three cells total 3.55 + 3.62 + 3.70 = 10.87 V. The kit window is
   14.25 V to 14.55 V, so the fourth cell must be at least 14.25 − 10.87 =
   3.38 V, raised to the cell minimum of 3.40 V, and at most 14.55 − 10.87 =
   3.68 V. The prompt says "the fourth cell must be from 3.40 V to 3.68 V".
   LLMs make arithmetic slips, so code does the sums and the model only
   chooses among cells.


.. admonition:: Question 19
   :class: hint

   The slides say the orchestrator owns the loop and the LLM only proposes.
   Name what the orchestrator owns, and what happens to a tool call that
   fails the checks.

.. dropdown:: Answer
   :class-container: sd-border-success

   The orchestrator owns the loop, the list of tools, the checks and the
   logs; the LLM never sends a ROS goal itself. A call that fails checks 1 to
   4 (parse, schema, semantic checks, executor guards) is not run. It goes
   back to the LLM as an error message, and the loop goes on until a stop
   condition fires, such as too many invalid outputs in a row.


.. admonition:: Question 20
   :class: hint

   From 20 to 40 steps, the ReAct input grows from 87,500 to 275,000 tokens,
   about 3.1 times, while the slides say the history grows about four times.
   Explain the difference with the formula :math:`nF + h\,n(n - 1)/2`.

.. dropdown:: Answer
   :class-container: sd-border-success

   The total has two parts. The fixed part :math:`nF` only doubles: 40,000
   to 80,000. The history part :math:`h\,n(n - 1)/2` grows with the square
   of :math:`n`: 47,500 to 195,000, about 4.1 times. The total,
   275,000 / 87,500 = 3.1 times, sits between the two. The longer the run,
   the more the history part dominates, which is why the slides suggest
   summarizing old steps.
