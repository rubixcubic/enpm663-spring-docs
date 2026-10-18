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
   state in code. In the demo, ``one_cell_in_slot()`` checks that agv1 slot 1
   is occupied and that the record holds a voltage from 3.4 to 3.8 V for it.
   If the check fails, the orchestrator sends back "goal not reached" and the
   loop goes on.


.. admonition:: Question 3
   :class: hint

   In Run 1 of the orchestrator demo, Gemini's five calls sent 1264, 1535,
   1788, 2045 and 2309 input tokens. Why do they grow?

   A. The model's replies get longer

   B. Each call sends the whole history again, and every step adds a tool
      call and its result to it

   C. The system message grows with every step

   D. The tool list gains a tool after every call

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each call sends the system message, the tool list and every message so
   far. Each step adds one model call and its result, with the new
   observation and the record: 1535 − 1264 = 271, 1788 − 1535 = 253,
   2045 − 1788 = 257 and 2309 − 2045 = 264 tokens more. The system message
   and the tool list stay the same. (The output was 16 to 24 tokens per call,
   and 1 for "done".)


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
   ``list_tools()`` printed the ten tools (7 skills and 3 readings) and one line per argument.


.. admonition:: Question 8
   :class: hint

   In the MCP demo, the client calls ``robot2_place_in_slot`` with
   ``{"agv": 4, "slot": 1}``. What comes back?

   A. ``is_error`` ``False``, with ``"code": "PRECONDITION_FAILED"``, because
      robot 2 holds nothing

   B. ``is_error`` ``True``: the server's own argument check refuses AGV 4,
      and the tool never runs

   C. An exception in the client

   D. ``is_error`` ``False``, with ``"code": "SUCCESS"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   MCP wrote the schema of ``agv`` from the type hint ``Literal[1, 2, 3]``,
   so 4 fails the argument check ("Input should be 1, 2 or 3"). The tool
   never ran, so the skill gave no result code, and ``is_error`` was
   ``True``. The call to ``robot2_move_home`` is the other case: the tool
   ran, returned ``SUCCESS``, and ``is_error`` was ``False``.


.. admonition:: Question 9
   :class: hint

   With the values measured in Run 1 (:math:`F` = 1264 tokens on every
   call, :math:`h` = 261 tokens per earlier step), how many input tokens does
   call 10 of a ReAct run send?

   A. 1525

   B. 3613

   C. 3874

   D. 24,385

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Call :math:`k` sends :math:`F + (k - 1)\,h`: 1264 + 9 × 261 = 1264 + 2349
   = 3613. It is the "last call" value for 10 steps in the
   ``token_growth.py`` table. **C** uses 10 earlier steps instead of 9, and
   **D**, 24,385, is the total over all 10 calls.


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
   ``MCPServer``, imported from ``mcp.server.mcpserver``. In 2.3.0 the 1.x
   import raises ``ModuleNotFoundError``, with a message that says
   "FastMCP was renamed to MCPServer".


.. admonition:: Question 14
   :class: hint

   MCP wrote the ``agv`` argument of ``robot2_place_in_slot`` as an integer
   ``enum`` of 1, 2 and 3. The Gemini declarations of the same tool use the
   same ``enum``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The Gemini declarations use ``minimum`` and ``maximum`` instead, because
   Gemini's ``parameters`` schema allows ``enum`` for strings only. The same
   tool can have two schemas, one written by MCP from the type hints and one
   written for Gemini, so check what each one says.


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

   From 20 to 40 steps, the ReAct input grows from 74,870 to 254,140 tokens,
   about 3.4 times, while the slides say the history grows about four times.
   Explain the difference with the formula :math:`nF + h\,n(n - 1)/2`
   (:math:`F` = 1264, :math:`h` = 261).

.. dropdown:: Answer
   :class-container: sd-border-success

   The total has two parts. The fixed part :math:`nF` only doubles: 25,280
   to 50,560. The history part :math:`h\,n(n - 1)/2` grows with the square
   of :math:`n`: 261 × 20 × 19 / 2 = 49,590 to 261 × 40 × 39 / 2 = 203,580,
   about 4.1 times. The total, 254,140 / 74,870 = 3.4 times, sits between
   the two. The longer the run,
   the more the history part dominates, which is why the slides suggest
   summarizing old steps.
