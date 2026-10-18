====================================================
Code
====================================================

The L8 code runs in two ways.

- **Offline**, with the system Python and no ARIAC: the validator, the token
  table, and the orchestrator loop on a stand-in factory
  (``orchestrator.py --fake``). These outputs repeat exactly.
- **Against ARIAC**, in the course container: the orchestrator with Gemini
  (``gemini-3.5-flash-lite``), the MCP server and client, and one real model
  output for the Structured Output section. ``run_sim_demo.sh`` starts ARIAC
  and the course skills server, runs one demonstration and copies its output
  back. These outputs were recorded once, on 2026-10-17. A rerun gives
  different answers.

Every output on this page is copied from the files the scripts wrote, the
same files the slides show.

.. important::

   **Two kinds of model.** ``GeminiModel`` in ``gemini_model.py`` calls
   Gemini, a real model, and its answers vary from run to run.
   ``ScriptedModel`` in ``orchestrator.py`` is a stand-in that returns fixed
   replies, one per call, in the order you give them. The lecture uses the
   scripted model where a slide shows a guard or a check (Run 2, the
   validator), because a fixed reply makes the guard fire every time.

.. note::

   **Where to put the files.** Keep the folder layout of the course:
   ``lecture8/code/`` holds the scripts, ``lecture8/code/config/`` the two
   ARIAC configuration files, and ``lecture8/outputs/`` the outputs. The L9
   scripts sit in ``lecture9/code/`` next to it and import the L8 files from
   ``../../lecture8/code``. Run every script from inside ``lecture8/code``.


.. list-table::
   :header-rows: 1
   :widths: 30 50 20
   :class: compact-table

   * - **File**
     - **What it does**
     - **Runs**
   * - :download:`orchestrator.py <code/orchestrator.py>`
     - The agent loop: observe, ask the model, check the call
       (``check_call()`` and ``guard()``), run it, record the result, stop.
       Run 1 uses Gemini, Run 2 a scripted model.
     - ARIAC, or offline with ``--fake``
   * - :download:`skill_tools.py <code/skill_tools.py>`
     - The ten tools: the seven skill actions of the two inspection robots and
       three ARIAC readings, each a declaration (name, description, schema)
       and a method of ``SkillTools``.
     - ARIAC
   * - :download:`fake_tools.py <code/fake_tools.py>`
     - ``FakeTools``: a factory with no ARIAC, with the same tool names,
       arguments and result shapes. Every value in it is chosen for this
       example.
     - offline
   * - :download:`gemini_model.py <code/gemini_model.py>`
     - ``GeminiModel``: the Gemini client, with the same call as
       ``ScriptedModel``. It reads the key from a file and saves every API
       response.
     - ARIAC or offline, with a key
   * - :download:`gemini_prices.py <code/gemini_prices.py>`
     - The model name and its prices, quoted from the Gemini pricing page with
       the date read.
     - imported
   * - :download:`sim_session.py <code/sim_session.py>`
     - Waits for ARIAC and the skills, starts the competition, and stops a
       demo that runs too long.
     - ARIAC
   * - :download:`stub_agv.py <code/stub_agv.py>`
     - A stand-in for ARIAC's ``/agvN/move`` action and the stub factory of
       the Structured Output section.
     - imported
   * - :download:`validator.py <code/validator.py>`
     - Parse, schema and semantic checks on seven scripted outputs, then two
       runs of a bounded retry.
     - offline
   * - :download:`structured_live.py <code/structured_live.py>`
     - One real Gemini output, run through ``validator.check()``.
     - with a key
   * - :download:`skills_mcp_server.py <code/skills_mcp_server.py>`
     - An MCP server for ten tools (7 skills and 3 readings). Started by the client.
     - ARIAC
   * - :download:`skills_mcp_client.py <code/skills_mcp_client.py>`
     - An MCP client that lists the server's tools and makes three calls.
     - ARIAC
   * - :download:`run_cost.py <code/run_cost.py>`
     - Tokens, latency and cost of one recorded run, from its raw API
       responses.
     - offline
   * - :download:`token_growth.py <code/token_growth.py>`
     - Input tokens and cost of a ReAct run and of plan-and-execute, for 5,
       10, 20 and 40 steps, from Run 1's measured tokens.
     - offline
   * - :download:`run_sim_demo.sh <code/run_sim_demo.sh>`
     - Runs one demonstration in the course container and copies its output
       back.
     - host
   * - :download:`demo_inner.sh <code/demo_inner.sh>`
     - Inside the container: starts ARIAC and the skills server, runs the
       demonstration, and stops every process it started.
     - container
   * - :download:`setup_lecture_venv.sh <code/setup_lecture_venv.sh>`
     - Makes the lecture's virtual environment in the container.
     - host
   * - :download:`lecture_requirements.txt <code/lecture_requirements.txt>`
     - The two packages of that environment: ``google-genai`` and ``mcp``.
     - read by the line above
   * - :download:`l8_trial.yaml <code/config/l8_trial.yaml>` and
       :download:`l8_user_config.yaml <code/config/l8_user_config.yaml>`
     - The ARIAC trial file and team configuration file of the L8 runs.
     - ARIAC
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs the offline parts and writes their outputs to ``../outputs/``.
     - offline
   * - :download:`listings.py <code/listings.py>` and
       :download:`listings_l8.json <code/listings_l8.json>`
     - Cut the slide listings out of the outputs, and check that every listing
       on a slide matches its output file byte for byte.
     - offline


Offline: No ARIAC, No Key
-------------------------

.. note::

   **What you need.** Python 3.10 or newer (the outputs come from 3.12.3)
   and the ``jsonschema`` package. The outputs come from Ubuntu's system
   Python with its ``python3-jsonschema`` package (``jsonschema`` 4.10.3):

   .. code-block:: bash

      sudo apt install python3-jsonschema
      cd lecture8/code

The Loop on a Stand-in Factory: ``orchestrator.py --fake``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``--fake`` runs the same loop, the same checks and the same ten tool
declarations on ``FakeTools``. Each skill call adds 20 s of simulation time,
and the cells read 3.61, 3.55, 3.66 and 3.58 V, in that order (chosen for
this example). ``--runs`` takes a comma list: ``2`` is Run 2 of the slides,
``dry`` is the scripted model doing the whole task, and ``1`` is Gemini. With
no key file, Run 1 prints a line that says so and runs the scripted model.

.. code-block:: bash

   python3 orchestrator.py --fake --runs 2
   python3 orchestrator.py --fake --runs dry

The :doc:`exercises <l8_exercises>` change the scripted replies and run the
loop this way.

.. literalinclude:: code/orchestrator.py
   :language: python
   :caption: orchestrator.py

.. literalinclude:: code/fake_tools.py
   :language: python
   :caption: fake_tools.py

``skill_tools.py`` holds the declarations that both ``SkillTools`` (ARIAC)
and ``FakeTools`` offer:

.. literalinclude:: code/skill_tools.py
   :language: python
   :caption: skill_tools.py

The Validator: ``validator.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script checks seven model outputs, one at a time, with ``check``: parse,
schema, then the semantic checks. It then runs ``ask``, the bounded retry,
twice with the scripted model. The factory is the stub of ``stub_agv.py``.

.. code-block:: bash

   python3 validator.py

.. literalinclude:: code/stub_agv.py
   :language: python
   :caption: stub_agv.py

.. literalinclude:: code/validator.py
   :language: python
   :caption: validator.py

Output (scripted model: fixed replies):

.. literalinclude:: outputs/validator.txt
   :language: text

Token Growth: ``token_growth.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`F` (``FIXED``), :math:`h` (``PER_STEP``) and the output per call
(``OUT``) come from Run 1's token counts, which the script reads from
``../outputs/agent_run1_usage.json``. The prices come from
``gemini_prices.py``. ``PLAN_OUT``, 40 output tokens per plan step, is chosen
for this example: no plan-and-execute run was recorded.

.. code-block:: bash

   python3 token_growth.py

.. literalinclude:: code/token_growth.py
   :language: python
   :caption: token_growth.py

.. literalinclude:: code/gemini_prices.py
   :language: python
   :caption: gemini_prices.py

The measured counts it reads (written by ``run_cost.py``):

.. literalinclude:: outputs/agent_run1_usage.json
   :language: json

Output:

.. literalinclude:: outputs/token_growth.txt
   :language: text

Running Everything Offline: ``run_all.sh``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``run_all.sh`` is the script that produced the offline outputs. It runs each
script in a clean environment (``env -i``), which drops the shell's ROS and
Python paths, and writes each output to ``../outputs/``. It also runs the
lecture's tests and checks every slide listing against its output file. The
tests and the slides are in the course's slides repository, not on this page,
so on your machine run the scripts one by one as above. They give the same
outputs.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

The versions it recorded:

.. literalinclude:: outputs/versions.txt
   :language: text

The slide listings are cut from the outputs by ``listings.py``, with the
lines, widths and dropped lines set in ``listings_l8.json``. The notes include
the same listing files.

.. literalinclude:: code/listings.py
   :language: python
   :caption: listings.py

.. literalinclude:: code/listings_l8.json
   :language: json
   :caption: listings_l8.json


Against ARIAC: The Gemini and MCP Demonstrations
------------------------------------------------

These runs need the course container ``enpm663_skills_dev`` with ARIAC 2025
and the course skills package (see the
:doc:`skills package page </ariac/skills>`), and, for the Gemini runs, an API
key. The model and SDK details in the code come from the Gemini API
documentation; each function in ``gemini_model.py`` names the page and the
date it was read.

Step 1: The Lecture's Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Gemini SDK and ``mcp`` go into their own virtual environment inside the
container, ``/opt/enpm663_lecture_venv``, not into the skills package, its
image or the container's system Python. ``setup_lecture_venv.sh`` makes it
from the host. Run it again after the container is recreated.

.. code-block:: bash

   bash setup_lecture_venv.sh

.. literalinclude:: code/setup_lecture_venv.sh
   :language: bash
   :caption: setup_lecture_venv.sh

.. literalinclude:: code/lecture_requirements.txt
   :language: text
   :caption: lecture_requirements.txt

Step 2: Where the Key Goes
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   For these lecture demos, the Gemini key lives in one file on the host,
   ``~/.config/enpm663/gemini_key``, with mode 600 (only you can read it).
   The demo scripts read it only from there, so for them it never goes on a
   command line or in an environment variable. In any setup, it never goes in
   a repository or an output file. For your own GP4 code, the GP4 guard
   rails allow an environment variable or a ``.env`` file listed in
   ``.gitignore`` (L9).

.. code-block:: bash

   mkdir -p ~/.config/enpm663
   touch ~/.config/enpm663/gemini_key
   chmod 600 ~/.config/enpm663/gemini_key
   # then paste the key into the file with an editor

For a ``--key`` run, ``run_sim_demo.sh`` checks the mode, then copies the
file through standard input to ``/dev/shm/enpm663_gemini_key`` in the
container. ``/dev/shm`` is held in memory, not on disk. The copy is removed
when the demonstration ends, and again when the script ends.
``GeminiModel`` reads the key from that file, and replaces it with ``<key>``
in every error text and every saved response.

Step 3: Run a Demonstration: ``run_sim_demo.sh``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script runs on the host. Before anything starts, it checks that the host
has 2 GB free, that no other simulation runs in the container, and that the
skills package has no uncommitted changes and matches the commit the
recordings used (``SKILLS_BASE``). Set ``SKILLS_REPO`` to your clone of the
skills package; the default is its place in the instructor's folders,
found from the script's folder in the slides repository. On your own clone,
set ``SKILLS_BASE`` to the commit you run, for example
``SKILLS_BASE=$(git -C "$SKILLS_REPO" rev-parse HEAD)``; the skills check
then refuses only uncommitted changes. It copies
``lecture8/code`` and ``lecture9/code`` into the container, runs the
demonstration under three stops (``demo_inner.sh``), and writes
``lecture8/outputs/NAME.txt``: a header (date, the model as the API reports
it, the SDK versions, the ARIAC image and commit, the skills commit), the
demonstration's output and its exit status. It refuses a ``NAME`` that
already exists, so every recording keeps its own file.

The commands that made the L8 recordings:

.. code-block:: bash

   # the agent: Run 2 (scripted), then Run 1 (Gemini)
   bash run_sim_demo.sh --lecture 8 --name agent_rec1 \
       --sim config/l8_trial.yaml config/l8_user_config.yaml 1800 --key \
       -- orchestrator.py --runs 2,1
   # one real output for the Structured Output section (no ARIAC)
   bash run_sim_demo.sh --lecture 8 --name structured_live --key -- structured_live.py
   # the MCP client (no model, no key)
   bash run_sim_demo.sh --lecture 8 --name mcp_live2 \
       --sim config/l8_trial.yaml config/l8_user_config.yaml 1200 -- skills_mcp_client.py

.. literalinclude:: code/run_sim_demo.sh
   :language: bash
   :caption: run_sim_demo.sh

.. literalinclude:: code/demo_inner.sh
   :language: bash
   :caption: demo_inner.sh

.. literalinclude:: code/sim_session.py
   :language: python
   :caption: sim_session.py

.. literalinclude:: code/config/l8_trial.yaml
   :language: yaml
   :caption: config/l8_trial.yaml

.. literalinclude:: code/config/l8_user_config.yaml
   :language: yaml
   :caption: config/l8_user_config.yaml

The Agent: ``orchestrator.py`` on ARIAC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The full recording behind the Agent Loop section. Run 2 (scripted model:
fixed replies) ran first, then Run 1. Run 1 is recorded once, on 2026-10-17,
with gemini-3.5-flash-lite. A rerun gives different answers.

.. literalinclude:: outputs/agent_rec1.txt
   :language: text

The Gemini client:

.. literalinclude:: code/gemini_model.py
   :language: python
   :caption: gemini_model.py

Tokens, Latency and Cost: ``run_cost.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``run_cost.py`` reads Run 1's raw API responses and writes the cost table of
the slides and ``agent_run1_usage.json``. The raw responses stay in the
course repository and are not on this page.

.. literalinclude:: code/run_cost.py
   :language: python
   :caption: run_cost.py

Output (recorded once, on 2026-10-17, with gemini-3.5-flash-lite):

.. literalinclude:: outputs/agent_run1_cost.txt
   :language: text

One Real Output: ``structured_live.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model gets the example system message of the Prompt Structure section,
the stub factory's state and one tool, ``move_agv``, whose parameters are
``validator.SCHEMA``. Its call's arguments then go through
``validator.check()``. No ARIAC runs.

.. literalinclude:: code/structured_live.py
   :language: python
   :caption: structured_live.py

Output, recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun
gives different answers.

.. literalinclude:: outputs/structured_live.txt
   :language: text

The system message it sends, written by ``run_all.sh``:

.. literalinclude:: outputs/system_message.txt
   :language: text

The MCP Demonstration: ``skills_mcp_server.py`` and ``skills_mcp_client.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The server serves ten tools (7 skills and 3 readings). The client starts the server as a
process with the same Python, talks to it over stdio, lists its tools and
makes three calls. No LLM is involved: the client makes the calls a model
would ask for. Both files need the ``mcp`` package 2.3.0, from the lecture's
virtual environment.

In ``mcp`` 2.x, the class that 1.x tutorials call ``FastMCP`` is
``MCPServer``, imported from ``mcp.server.mcpserver``. In 2.3.0 the old
import, ``from mcp.server.fastmcp import FastMCP``, raises
``ModuleNotFoundError`` with a message that names the rename (read in
``mcp/server/fastmcp.py``, 2026-10-17).

.. literalinclude:: code/skills_mcp_server.py
   :language: python
   :caption: skills_mcp_server.py

.. literalinclude:: code/skills_mcp_client.py
   :language: python
   :caption: skills_mcp_client.py

The full recording (a real run against ARIAC, on 2026-10-17; no model runs;
recording 2 of 2, recording 1 used a client that printed 3 lines per
result):

.. literalinclude:: outputs/mcp_live2.txt
   :language: text

``outputs/mcp_demo.txt`` holds its tool and call lines, which the slides
show. The server also wrote one line to standard error when it refused the
arguments of the third call:

.. literalinclude:: outputs/mcp_demo_stderr.txt
   :language: text


.. _l8-code-real-model:

Using Another Model
-------------------

``run()`` calls the model as ``model(SYSTEM, messages, declarations)``. It
accepts a ``Reply`` from ``gemini_model.py``, or a plain dictionary:
``{"tool": name, "args": arguments}`` for a tool call, or ``{"text": ...}``
for a reply with no tool call (``as_reply()`` in ``orchestrator.py``). Any
object with that call can take the place of ``GeminiModel``, and the loop,
the guard and the stop conditions stay as they are.

.. important::

   **GP4 does not require Gemini.** Any provider whose API supports tool
   calling works, hosted or a local open-weight model (see the
   :doc:`AI Access </ariac/ai_setup>` page). Google calls the feature
   "function calling".

An adapter for another provider does the jobs ``GeminiModel`` does in
``gemini_model.py``:

1. **Send the tools in the provider's format.** ``to_declaration()`` turns
   each entry of ``DECLARATIONS`` into Gemini's format and drops the schema
   keywords Gemini does not take, such as ``additionalProperties``.
   ``check_call()`` still checks every call against the full schema.
2. **Turn the model's reply into the loop's format.** ``parse_raw()`` takes
   the first tool call, counts any others, and keeps the reply's finish
   reason, so the loop can stop on a reply cut off at the output cap.
3. **Send each result back** as the answer to the call it belongs to, with
   the call's ID (``build_request()``).
4. **Read the token counts** from the response's usage fields, and time each
   call. ``run_cost.py`` turns them into a cost.

.. warning::

   A real model costs money on every call, and its answers vary. Run it with
   a small ``MAX_STEPS`` first, and keep the key in a file only you can read,
   as in Step 2 above.
