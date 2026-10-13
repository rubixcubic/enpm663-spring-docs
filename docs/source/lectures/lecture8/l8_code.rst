====================================================
Code
====================================================

L8 has six Python files and one shell script. They run on their own, with no
ARIAC simulation and no ROS: the factory is a Python dictionary, and
``stub_agv.py`` stands in for ARIAC's ``/agvN/move`` action. The outputs below
come from running the scripts on 2026-10-12 with Python 3.12.3.

.. important::

   **No LLM is called.** ``ScriptedModel`` in ``orchestrator.py`` is a
   scripted stand-in for the model: it returns fixed replies, one per call,
   in the order you give them. A real model's answers vary from run to run,
   so a real model would not reproduce the outputs below. The stand-in makes
   every run repeatable and costs nothing. The last section of this page,
   :ref:`l8-code-real-model`, shows how to put a real model in its place.

.. note::

   **What you need.** Python 3.10 or newer (the outputs come from 3.12.3).
   ``validator.py`` needs the ``jsonschema`` package. The MCP demo needs the
   ``mcp`` package, version 2.3.0, which is not installed system-wide. Make
   your own virtual environment in the folder that holds the scripts:

   .. code-block:: bash

      cd lecture8/code
      python3 -m venv venv
      source venv/bin/activate
      pip install jsonschema mcp==2.3.0

   If ``python3 -m venv`` says that ``ensurepip`` is not available, install
   the venv module first with ``sudo apt install python3-venv``.

   The course machine ran ``orchestrator.py``, ``validator.py`` and
   ``token_growth.py`` with Ubuntu's system Python and its
   ``python3-jsonschema`` package (``jsonschema`` 4.10.3). In a virtual
   environment with ``jsonschema`` 4.26.0 and ``mcp`` 2.3.0, all four outputs
   were the same, character for character (checked 2026-10-12).

   Run every script from inside ``lecture8/code``: the scripts import
   ``stub_agv.py`` from the same folder, and the MCP client starts the server
   by its file name.


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **Script**
     - **What it shows**
     - **Notes section**
   * - :download:`stub_agv.py <code/stub_agv.py>`
     - The stand-in for ``/agvN/move``: the seven ARIAC paths and the example
       factory. Imported by the others; not run on its own.
     - :ref:`l8-agent-loop`
   * - :download:`orchestrator.py <code/orchestrator.py>`
     - An orchestrator loop with a guard, a step limit and an invalid-output
       limit, around a scripted stand-in model.
     - :ref:`l8-agent-loop`
   * - :download:`validator.py <code/validator.py>`
     - Parse, schema and semantic checks on seven outputs, then two runs of a
       bounded retry.
     - :ref:`l8-structured-output`
   * - :download:`agv_mcp_server.py <code/agv_mcp_server.py>`
     - An MCP server with one tool, ``move-agv``. Started by the client.
     - :ref:`l8-tool-calling`
   * - :download:`agv_mcp_client.py <code/agv_mcp_client.py>`
     - An MCP client that lists the server's tools and makes three calls.
     - :ref:`l8-tool-calling`
   * - :download:`token_growth.py <code/token_growth.py>`
     - Input tokens and cost of a ReAct run and of plan-and-execute, for 5,
       10, 20 and 40 steps.
     - :ref:`l8-context-cost-latency`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all of the above and writes their outputs to ``../outputs/``.
     - See the last code section


The AGV Stand-in: ``stub_agv.py``
---------------------------------

``move_agv`` imitates ``/agv{agv}/move``. Its rules come from ARIAC 2025's
``ariac_plugins/src/agv_motion_plugin.cpp``: a goal to the AGV's own station
is rejected, and only the seven paths in ``PATHS`` are accepted. A goal to the
AGV's own station is never in ``PATHS``, so one check covers both rules.
``example_factory`` returns the factory state every L8 demo starts from
(chosen for this example). You do not run this file; the others import it.

.. literalinclude:: code/stub_agv.py
   :language: python
   :caption: stub_agv.py


The Orchestrator: ``orchestrator.py``
-------------------------------------

The script runs the loop twice with the scripted stand-in model. In Run 1 the
model asks for the wrong AGV, then the right one, then says "done". In Run 2
it asks for the wrong AGV twice.

.. code-block:: bash

   python3 orchestrator.py

.. literalinclude:: code/orchestrator.py
   :language: python
   :caption: orchestrator.py

Output:

.. literalinclude:: outputs/orchestrator.txt
   :language: text

The character counts (666, 839, 1025) are the length of the JSON text the
loop would send. They are not token counts; a provider's API reports tokens
in its ``usage`` fields.

.. tip::

   ``ScriptedModel`` raises ``IndexError`` when it runs out of replies. When
   you change a script (as in the exercises), give it at least as many
   replies as the loop will ask for.


The Validator: ``validator.py``
-------------------------------

The script checks seven model outputs, one at a time, with ``check``: parse,
schema, then the semantic checks. It then runs ``ask``, the bounded retry,
twice with the scripted stand-in. It imports ``ScriptedModel`` from
``orchestrator.py``.

.. code-block:: bash

   python3 validator.py

.. literalinclude:: code/validator.py
   :language: python
   :caption: validator.py

Output:

.. literalinclude:: outputs/validator.txt
   :language: text


The MCP Demo: ``agv_mcp_server.py`` and ``agv_mcp_client.py``
-------------------------------------------------------------

The server wraps ``stub_agv.move_agv`` as one MCP tool, ``move-agv``. The
client starts the server as a process (``sys.executable agv_mcp_server.py``),
talks to it over stdio, lists its tools and makes three calls. No LLM is
involved: the client makes the calls a model would ask for. Both files need
the ``mcp`` package, so run the client from the virtual environment:

.. code-block:: bash

   source venv/bin/activate
   python3 agv_mcp_client.py

The client starts the server with the same Python that runs the client, so the
server also sees the ``mcp`` package. You never start the server by hand.

.. literalinclude:: code/agv_mcp_server.py
   :language: python
   :caption: agv_mcp_server.py

.. literalinclude:: code/agv_mcp_client.py
   :language: python
   :caption: agv_mcp_client.py

Output:

.. literalinclude:: outputs/mcp_demo.txt
   :language: text

The server also writes one log line to the terminal (standard error) when it
refuses the arguments of the third call:

.. literalinclude:: outputs/mcp_demo_stderr.txt
   :language: text

.. _l8-code-fastmcp:

``FastMCP`` is ``MCPServer`` in ``mcp`` 2.x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many MCP tutorials were written for ``mcp`` 1.x and start with
``from mcp.server.fastmcp import FastMCP``. In ``mcp`` 2.3.0 that import
fails. This is the last line of the error the course machine printed (the
traceback above it is left out):

.. literalinclude:: outputs/fastmcp_import.txt
   :language: text

The message names both ways out: use ``MCPServer`` (as
``agv_mcp_server.py`` does), or pin ``mcp<2`` to keep running 1.x code. The
L8 code is written for 2.3.0, so install that version.


Token Growth: ``token_growth.py``
---------------------------------

Every number in this script is an assumption chosen for this example, not a
measurement and not a provider's price: 2000 tokens sent on every call, 250
tokens added by each earlier step, 100 output tokens per ReAct call, 40 per
plan step, $2 per million input tokens and $10 per million output tokens.

.. code-block:: bash

   python3 token_growth.py

.. literalinclude:: code/token_growth.py
   :language: python
   :caption: token_growth.py

Output:

.. literalinclude:: outputs/token_growth.txt
   :language: text


Running Everything: ``run_all.sh``
----------------------------------

``run_all.sh`` is the script that produced the outputs above. It runs each
example in a clean environment (``env -i``), which drops the shell's ROS and
Python paths, and writes each output to ``../outputs/``. It also writes the
versions it used:

.. literalinclude:: outputs/versions.txt
   :language: text

You do not need it: the commands in the sections above give the same results.
To run it yourself, install ``python3-jsonschema`` for the system Python
(``sudo apt install python3-jsonschema``) and make a virtual environment with
``mcp``. The script looks for it in ``~/l8-venv`` unless you set ``VENV``. It
overwrites the files in ``../outputs/``.

.. code-block:: bash

   python3 -m venv ~/l8-venv
   ~/l8-venv/bin/pip install mcp==2.3.0
   bash run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh


.. _l8-code-real-model:

Using a Real Model in Place of ``ScriptedModel``
------------------------------------------------

``run()`` calls the model as ``model(SYSTEM, messages, TOOLS)`` and expects
back either ``{"tool": ..., "args": ...}`` or ``{"text": ...}``. Any object
with that call signature can replace ``ScriptedModel``, and the loop, the
guard and the stop conditions stay as they are.

.. important::

   **The course has not chosen an LLM provider.** Any provider whose API
   supports tool calling works, hosted or a local open-weight model. Google
   calls the same feature "function calling". The two examples below use two
   providers so you can compare them. The course requires neither one.

The object that replaces ``ScriptedModel`` is an *adapter*: a class that
translates between the loop's format and one provider's API. Each provider
has its own message format for tools, so the adapter keeps the conversation
in that format next to the loop's own ``messages`` list. For any provider,
the adapter does three jobs:

1. **Send the tools in the provider's format.** ``TOOLS`` describes
   ``move-agv`` with three fields: ``name``, ``description`` and
   ``input_schema`` (a JSON Schema for the arguments). If the provider uses
   other field names, the adapter converts ``TOOLS``; ``orchestrator.py``
   stays as it is.
2. **Turn the model's reply into the loop's format.** A tool call becomes
   ``{"tool": name, "args": arguments}``, and a plain answer becomes
   ``{"text": ...}``.
3. **Send each result back.** The loop appends the guard's error or the
   tool's result as the last message. The adapter sends it to the provider
   as the result of the tool call it answers, with the ID the provider gave
   that call.

The table compares the two examples. The versions are the ones tested for
these notes; every other entry comes from the provider's documentation, read
on 2026-10-12, and each example lists its sources.

.. list-table::
   :header-rows: 1
   :widths: 28 36 36
   :class: compact-table

   * - **Job**
     - **Example 1: Anthropic**
     - **Example 2: Google Gemini**
   * - Python package (version tested)
     - ``anthropic`` (1.13.0)
     - ``google-genai`` (2.30.0)
   * - Environment variable for the key
     - ``ANTHROPIC_API_KEY``
     - ``GEMINI_API_KEY`` or ``GOOGLE_API_KEY``
   * - Tool definition
     - ``name``, ``description``, ``input_schema``: ``TOOLS`` as it is
     - ``type``, ``name``, ``description``, ``parameters``: converted from
       ``TOOLS``
   * - The model's tool call
     - a ``tool_use`` block with ``id``, ``name`` and ``input``
     - a ``function_call`` step with ``id``, ``name`` and ``arguments``
   * - The result sent back
     - a ``tool_result`` block with ``tool_use_id``
     - a ``function_result`` step with ``call_id``
   * - Marking a result as an error
     - ``is_error``
     - ``is_error``
   * - At most one tool call per reply
     - ``disable_parallel_tool_use``
     - no such setting found; the adapter answers any extra call with an
       error

.. warning::

   A real model costs money on every call, and its answers vary. Run it with
   a small ``MAX_STEPS`` first. Keep your API key in an environment variable
   in your terminal, never in a file in your repository.

Example 1: Anthropic's Claude API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TOOLS`` in ``orchestrator.py`` already uses the three fields of an
Anthropic tool definition, so this adapter passes it unchanged. Everything in
this example comes from Anthropic's documentation, read on 2026-10-12:
`tool use overview <https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview>`_,
`handle tool calls <https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls>`_,
`models overview <https://platform.claude.com/docs/en/about-claude/models/overview>`_
and the `Python SDK README <https://github.com/anthropics/anthropic-sdk-python>`_.

Step 1: Install the SDK and Set Your Key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The SDK needs Python 3.10 or newer. Install it in the same virtual
environment (these notes were checked with version 1.13.0):

.. code-block:: bash

   pip install anthropic

The client reads its key from the ``ANTHROPIC_API_KEY`` environment
variable. The README's example passes
``api_key=os.environ.get("ANTHROPIC_API_KEY")`` with the comment "This is the
default and can be omitted". Set the variable in the terminal that runs the
script:

.. code-block:: bash

   export ANTHROPIC_API_KEY="your key here"

Step 2: Choose a Model
^^^^^^^^^^^^^^^^^^^^^^

On 2026-10-12 the models overview page suggests starting with Claude Opus 5.5,
whose API ID is ``claude-opus-5-5``. It also lists ``claude-sonnet-5-5`` and
``claude-haiku-5-5``, which cost less per token. Model IDs and prices change:
read them from the models overview and pricing pages on the day you run.

Step 3: Write the Adapter
^^^^^^^^^^^^^^^^^^^^^^^^^

- The model's tool call arrives as a ``tool_use`` block with an ``id``, a
  ``name`` and an ``input`` (the arguments). The response's ``stop_reason``
  is then ``"tool_use"``.
- The result goes back in a ``user`` message that holds a ``tool_result``
  block with the same ``tool_use_id``. The documentation lists ``is_error``
  as optional: "Set to ``true`` if the tool execution resulted in an error."
  The class sets it for the guard's errors, and leaves it ``false`` for a
  ``REJECTED`` move, where the tool ran and reported a failure (the same rule
  as ``is_error`` in the MCP demo).
- ``tool_choice={"type": "auto", "disable_parallel_tool_use": True}`` is the
  setting the official example uses to "ask for at most one tool call per
  turn", which matches the loop: one call, one check, one result.

.. code-block:: python

   import json

   import anthropic


   class ClaudeModel:
       """Calls Claude in place of ScriptedModel; same call signature."""

       def __init__(self, model="claude-opus-5-5"):
           self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
           self.model = model
           self.history = []        # the conversation in the API's format
           self.tool_use_id = None  # id of the last tool_use block

       def __call__(self, system, messages, tools):
           latest = messages[-1]["content"]  # the goal, or the last result
           if self.tool_use_id is None:
               text = latest if isinstance(latest, str) else json.dumps(latest)
               self.history.append({"role": "user", "content": text})
           else:
               self.history.append({"role": "user", "content": [{
                   "type": "tool_result",
                   "tool_use_id": self.tool_use_id,
                   "content": json.dumps(latest),
                   "is_error": "error" in latest,
               }]})
           response = self.client.messages.create(
               model=self.model,
               max_tokens=16000,
               system=system,
               tools=tools,
               tool_choice={"type": "auto", "disable_parallel_tool_use": True},
               messages=self.history,
           )
           self.history.append({"role": "assistant", "content": response.content})
           self.tool_use_id = None
           for block in response.content:
               if block.type == "tool_use":
                   self.tool_use_id = block.id
                   return {"tool": block.name, "args": block.input}
           return {"text": " ".join(b.text for b in response.content
                                    if b.type == "text")}

Then, in the ``__main__`` block of a copy of ``orchestrator.py``, replace the
scripted model:

.. code-block:: python

   model = ClaudeModel()
   print("stop:", run(model, example_factory(), shipped))

.. note::

   **How this was checked.** No API call was made for these notes, and no
   API key was used. On 2026-10-12 the class above was run with
   ``anthropic`` 1.13.0 and Python 3.12.3, in two ways:

   - With a fake client in place of ``anthropic.Anthropic`` that returned
     ``tool_use`` and ``text`` blocks in the order of Run 1. The orchestrator
     printed the same lines as Run 1. The requests the class built had 1, 3
     and 5 messages, and each result was in a ``tool_result`` block that
     named the matching ``tool_use_id``.
   - With the real ``anthropic.Anthropic`` client, whose network layer was
     replaced by a local stand-in that answered without leaving the
     computer. This checked that the SDK accepts the requests, including the
     earlier replies stored in ``self.history``, and reads the replies.

   A real model's replies, and so its output, will differ.

Example 2: Google's Gemini API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final demo's embodied-reasoning step uses Gemini Robotics ER, a Google
model, so this example uses Google's API. It uses the Interactions API, the
one Google's function calling page uses. The Interactions page says: "As of
June 2026, it is Generally Available and recommended for all new projects."
Everything in this example comes from Google's documentation, read on
2026-10-12:
`function calling <https://ai.google.dev/gemini-api/docs/function-calling>`_,
`Interactions API <https://ai.google.dev/gemini-api/docs/interactions-overview>`_,
`Interactions API reference <https://ai.google.dev/api/interactions-api>`_,
`models <https://ai.google.dev/gemini-api/docs/models>`_,
`API keys <https://ai.google.dev/gemini-api/docs/api-key>`_,
`structured output <https://ai.google.dev/gemini-api/docs/structured-output>`_
and the Python SDK reference
(`overview <https://googleapis.github.io/python-genai/>`_ and
`genai module <https://googleapis.github.io/python-genai/genai.html>`_).

Step 1: Install the SDK and Set Your Key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Interactions page says the Python SDK supports the Interactions API "from
2.3.0 version onwards". The installed package (2.30.0) declares Python 3.10
or newer. Install it in the same virtual environment:

.. code-block:: bash

   pip install google-genai

The SDK reference says: "Set the GEMINI_API_KEY or GOOGLE_API_KEY. It will
automatically be picked up by the client." If both are set,
``GOOGLE_API_KEY`` wins, so set only one:

.. code-block:: bash

   export GEMINI_API_KEY="your key here"

The first security rule on the API keys page is: "Never check API keys
into source control systems like Git." The same page says the Gemini API rejects
requests from unrestricted standard keys, and explains how to restrict one.

Step 2: Choose a Model
^^^^^^^^^^^^^^^^^^^^^^

On 2026-10-12 the models page lists Gemini 3.8 Flash as a stable model, and
the function calling page's examples use its ID, ``gemini-3.8-flash``. The
Interactions page lists the other models that the Interactions API accepts.
Model IDs and prices change: read them from the models and pricing pages on
the day you run.

Step 3: Convert ``TOOLS`` to Function Declarations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The function calling page defines a function with four fields: ``"type":
"function"``, ``name``, ``description`` and ``parameters`` (a JSON Schema). So
the adapter converts each tool in ``TOOLS``, without changing
``orchestrator.py``:

- ``input_schema`` becomes ``parameters``, and ``"type": "function"`` is
  added.
- The ``station`` property has an ``enum`` but no ``type``. The structured
  output page lists ``enum`` under string values, so the converter adds
  ``"type": "string"`` (the four station names are strings).
- The name ``move-agv`` stays. The SDK reference's ``FunctionDeclaration``
  says a name "Must be a-z, A-Z, 0-9, or contain underscores, dots, colons
  and dashes, with a maximum length of 128."

Step 4: Write the Adapter
^^^^^^^^^^^^^^^^^^^^^^^^^

- The model's tool call arrives as a ``function_call`` step with an ``id``, a
  ``name`` and ``arguments``.
- The result goes back as a ``function_result`` step with the call's
  ``name``, a ``call_id`` equal to the call's ``id``, and a ``result``. The
  function calling page sends the result as one text block,
  ``[{"type": "text", "text": json.dumps(result)}]``. The API reference
  lists ``is_error`` as optional: "Whether the tool call resulted in an
  error." The class sets it by the same rule as the Anthropic example.
- By default the API stores every interaction on Google's servers (55 days
  on the paid tier, 1 day on the free tier), and a later call can continue
  from it with ``previous_interaction_id``. This adapter uses the
  function calling page's stateless mode instead, ``store=False``: "you must
  pass the full history of the conversation in the input field of each
  subsequent request." The history holds the first ``user_input`` step, every
  step the model returned "exactly as received", and each
  ``function_result`` step. Like the Anthropic adapter, it resends the whole
  conversation on every call.
- The system prompt goes in ``system_instruction``.
- The function calling page says the model can call "multiple functions in a
  single turn (parallel function calling)". Its ``tool_choice`` modes are
  ``auto`` (the default), ``any``, ``none`` and ``validated``, and none of
  them limits a reply to one call. So the class gives the loop only the
  first call, and answers any other call in the same reply with an error
  result, so the model sees that those calls did not run.
- When the reply has no function call, ``interaction.output_text`` holds the
  model's text.

.. code-block:: python

   import copy
   import json

   from google import genai


   def to_gemini(tools):
       """TOOLS (name, description, input_schema) as Gemini functions."""
       functions = []
       for tool in tools:
           schema = copy.deepcopy(tool["input_schema"])
           for prop in schema["properties"].values():
               if "enum" in prop and "type" not in prop:
                   prop["type"] = "string"  # the station names are strings
           functions.append({
               "type": "function",
               "name": tool["name"],
               "description": tool["description"],
               "parameters": schema,
           })
       return functions


   def result_step(call, result):
       """A function_result step that answers one function_call step."""
       return {
           "type": "function_result",
           "name": call.name,
           "call_id": call.id,
           "result": [{"type": "text", "text": json.dumps(result)}],
           "is_error": "error" in result,
       }


   class GeminiModel:
       """Calls Gemini in place of ScriptedModel; same call signature."""

       def __init__(self, model="gemini-3.8-flash"):
           self.client = genai.Client()  # reads GEMINI_API_KEY
           self.model = model
           self.history = []  # the conversation as Interactions API steps
           self.calls = []    # function_call steps of the last reply

       def __call__(self, system, messages, tools):
           latest = messages[-1]["content"]  # the goal, or the last result
           if not self.calls:
               text = latest if isinstance(latest, str) else json.dumps(latest)
               self.history.append({
                   "type": "user_input",
                   "content": [{"type": "text", "text": text}],
               })
           else:
               first, *others = self.calls
               self.history.append(result_step(first, latest))
               for call in others:  # the loop runs one call per reply
                   self.history.append(result_step(
                       call, {"error": "not run: one call per reply"}))
           interaction = self.client.interactions.create(
               model=self.model,
               store=False,
               system_instruction=system,
               tools=to_gemini(tools),
               input=self.history,
           )
           self.history += [step.model_dump() for step in interaction.steps]
           self.calls = [step for step in interaction.steps
                         if step.type == "function_call"]
           if self.calls:
               call = self.calls[0]
               return {"tool": call.name, "args": call.arguments}
           return {"text": interaction.output_text}

Then, in the ``__main__`` block of a copy of ``orchestrator.py``, replace the
scripted model:

.. code-block:: python

   model = GeminiModel()
   print("stop:", run(model, example_factory(), shipped))

.. note::

   **How this was checked.** No API call was made for these notes, and no
   API key was used. On 2026-10-12 the code above was run with
   ``google-genai`` 2.30.0 and Python 3.12.3, in two ways:

   - With a fake client in place of ``genai.Client`` that returned
     ``function_call`` and ``model_output`` steps in the order of Run 1. The
     orchestrator printed the same lines as Run 1. The requests had 1, 3 and
     5 steps in ``input``, each result was a ``function_result`` step whose
     ``call_id`` matched the call's ``id``, and every request had
     ``store=False``.
   - With the real ``genai.Client``, whose network layer was replaced by a
     local stand-in that answered without leaving the computer. This checked
     that the SDK accepts the request and reads the replies into steps. A
     reply with two function calls got two ``function_result`` steps back:
     the first with the guard's result, the second with the "not run" error.

   A real model's replies, and so its output, will differ.

What the Sketches Leave Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Other endings.** The Anthropic SDK's ``stop_reason`` can also be, for
  example, ``"max_tokens"`` or ``"refusal"``. A Gemini interaction has a
  ``status``, which the API reference lists as ``completed``,
  ``requires_action``, ``failed``, ``incomplete`` and others. Check it before
  you read the reply.
- **The schema check before the guard.** ``guard`` reads
  ``call["args"]["agv"]`` directly, so a call with a missing field raises
  ``KeyError``. Run ``validator.py``'s parse and schema steps on the
  arguments first. Both providers offer a stricter mode: Anthropic's
  overview says ``strict: true`` on a tool definition makes Claude's tool
  calls "always match your schema exactly", and Google's function calling
  page describes the ``validated`` mode as "Model ensures function schema
  adherence." The semantic checks and the guard still stay (see
  :ref:`l8-structured-output`).
- **Cost and latency.** Each response reports its token counts: Anthropic's
  ``response.usage`` has ``input_tokens`` and ``output_tokens``, and a Gemini
  interaction's ``usage`` has ``total_input_tokens`` and
  ``total_output_tokens``. Time each call with ``time.monotonic()`` before
  and after it. GP4 reports both per trial.
- **API errors.** A failed call, for example a network error or a rate
  limit, makes the SDK raise an exception; the loop must catch it and stop
  safely. In the offline checks above, a stand-in reply with HTTP status 429
  (rate limit) made each SDK raise a ``RateLimitError``.
