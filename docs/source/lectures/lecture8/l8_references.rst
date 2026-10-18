====================================================
References
====================================================

These are the sources the L8 slides cite or take their facts from, in the
order of the slides, grouped by section. A last dropdown lists the
documentation behind the Gemini client on the :doc:`code page <l8_code>`.
The links were checked on 2026-10-12, and the Gemini links on 2026-10-17.
Provider documentation changes often; read it again on the day you build on
it.


.. dropdown:: Where the LLM Goes
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Physical AI
         :link: https://www.nvidia.com/en-us/glossary/generative-physical-ai/
         :class-card: sd-border-secondary

         **NVIDIA Glossary: "What is Physical AI?"**

         The definition from L1: physical AI lets autonomous systems
         "perceive, understand, reason, and perform or orchestrate complex
         actions in the physical world." The agent in GP4 does the
         "orchestrate" part.


.. dropdown:: The LLM as a Function
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Messages API
         :link: https://platform.claude.com/docs/en/api/messages/create
         :class-card: sd-border-secondary

         **Anthropic, Messages API reference: Create a Message**

         The source of the quote on alternating ``user`` and ``assistant``
         turns: the program sends the prior turns on every call, because the
         model keeps nothing.


.. dropdown:: The Agent Loop
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ARIAC interfaces
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: ROS API**

         The topics the orchestrator reads in step 1
         (``/competition_status``, ``/inspection_conveyor/status``, the
         voltage topics, ``/{agv_name}/info``, ``/{agv_name}/tray_status``),
         the ``/submit_kitting_order`` service and the ``/{agv_name}/move``
         action.

      .. grid-item-card:: AGV move rules
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/agv_motion_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/agv_motion_plugin.cpp``

         ``goal_recieved_cb`` rejects a goal to the AGV's own station and
         accepts only seven paths. ``stub_agv.py`` copies these rules.


.. dropdown:: Plan-and-Execute and ReAct
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ReAct
         :link: https://arxiv.org/abs/2210.03629
         :class-card: sd-border-secondary

         **S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan and
         Y. Cao**

         *ReAct: Synergizing Reasoning and Acting in Language Models.*
         ICLR 2023; arXiv:2210.03629, 2022.

         The source of the ReAct pattern and of the quote on interleaving
         reasoning traces and actions.

      .. grid-item-card:: Conveyor speed
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_setup/config/user_config_schema.json
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_setup/config/user_config_schema.json``

         ``CONVEYOR_SPEED`` has ``exclusiveMinimum`` 0 and ``maximum`` 0.1:
         the conveyor moves at up to 0.1 m/s.

      .. grid-item-card:: Inspection and high-priority targets
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/config/scoring_weights.yaml``

         ``NOMINAL_INSPECTION_TIME`` (4 s) and
         ``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION`` (150 s), used in this
         section and in Context, Cost and Latency.


.. dropdown:: Prompt Structure for a Planner
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Cell types and tolerances
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellTypes.msg``

         The Li-Ion nominal voltage (3.6 V) and the tolerances (0.2 V per
         cell, 0.15 V per kit) behind the kit rule and the window for the
         fourth cell.

      .. grid-item-card:: Three AGVs
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/world/ariac.world
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/world/ariac.world``

         The world file with the three AGVs, ``agv1`` to ``agv3``, named in
         the example system message and in the schema's ``agv`` range.

      .. grid-item-card:: Four stations
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/AgvStations.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/AgvStations.msg``

         ``INSPECTION`` = 1, ``ASSEMBLY`` = 2, ``SHIPPING`` = 3,
         ``RECYCLING`` = 4: the ``station_id`` values a valid move maps to.


.. dropdown:: Structured Output
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: JSON Schema
         :link: https://json-schema.org/
         :class-card: sd-border-secondary

         **JSON Schema**

         The specification and learning pages for the schema keywords used
         in the lecture: ``type``, ``required``, ``enum``, ``minimum``,
         ``maximum`` and ``additionalProperties``.

      .. grid-item-card:: ARIAC's configuration check
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_setup/ariac_setup/yaml_validation.py
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_setup/ariac_setup/yaml_validation.py``

         Where ARIAC validates a team configuration file against
         ``user_config_schema.json`` (draft-07) with the ``jsonschema``
         package, before the simulation starts.

      .. grid-item-card:: jsonschema
         :link: https://python-jsonschema.readthedocs.io/en/stable/validate/
         :class-card: sd-border-secondary

         **python-jsonschema documentation: Schema Validation**

         ``jsonschema.validate`` raises ``ValidationError``, and "If no
         $schema property is found, the default validator class is the latest
         released draft" (2020-12 in versions 4.10.3 and 4.26.0, checked).

      .. grid-item-card:: Pydantic
         :link: https://docs.pydantic.dev/latest/
         :class-card: sd-border-secondary

         **Pydantic documentation**

         The other validation library named in step 2. The MCP server of
         Exercise 4 uses Pydantic's ``Field`` to write its argument limits.

      .. grid-item-card:: Structured outputs (OpenAI)
         :link: https://developers.openai.com/api/docs/guides/structured-outputs
         :class-card: sd-border-secondary

         **OpenAI, Structured Outputs guide**

         The quotes on output held to a supplied JSON Schema, and on a
         refusal that "does not necessarily follow the schema".

      .. grid-item-card:: Strict tool use (Anthropic)
         :link: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
         :class-card: sd-border-secondary

         **Anthropic, Tool use with Claude**

         The quote on ``strict: true``, which makes tool calls "always match
         your schema exactly".


.. dropdown:: Tool Calling and MCP
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Gemini API reference
         :link: https://ai.google.dev/api/generate-content
         :class-card: sd-border-secondary

         **Google, Gemini API reference: generateContent**

         The fields of a function declaration (``name``, ``description``,
         ``parameters``) quoted on the What a Tool Is slide, and the schema
         subset ``parameters`` takes, which has no ``additionalProperties``
         and allows ``enum`` for strings only.

      .. grid-item-card:: Gemini function calling
         :link: https://ai.google.dev/gemini-api/docs/generate-content/function-calling
         :class-card: sd-border-secondary

         **Google, Function calling with the Gemini API**

         The ``function_call`` part, the function response sent back with
         the call's ID, and the advice to name functions "without spaces,
         periods, or dashes".

      .. grid-item-card:: MCP architecture
         :link: https://modelcontextprotocol.io/docs/learn/architecture
         :class-card: sd-border-secondary

         **Model Context Protocol: Architecture overview**

         Spec version 2026-07-28. The definitions of host, client and
         server, the three primitives (tools, resources, prompts),
         JSON-RPC 2.0, ``tools/list`` and ``tools/call``, and the stdio and
         Streamable HTTP transports.

      .. grid-item-card:: MCP Python SDK
         :link: https://github.com/modelcontextprotocol/python-sdk
         :class-card: sd-border-secondary

         **Model Context Protocol, Python SDK** (``mcp``)

         The package the demo uses, version 2.3.0
         (`PyPI <https://pypi.org/project/mcp/2.3.0/>`_, released
         2026-10-02, Python 3.10 or newer). Its
         `v2 migration guide <https://py.sdk.modelcontextprotocol.io/v2/migration/>`_
         covers the rename of ``FastMCP`` to ``MCPServer``, which
         ``mcp/server/fastmcp.py`` in 2.3.0 also names.

      .. grid-item-card:: ros-mcp-server
         :link: https://github.com/robotmcp/ros-mcp-server
         :class-card: sd-border-secondary

         **robotmcp, ros-mcp-server**

         An MCP server that connects an LLM to a robot through rosbridge, to
         "publish & subscribe to topics, call services & actions, set
         parameters". The example of raw ROS access on the GP4 choice slide.


.. dropdown:: Context, Cost and Latency
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: 4D/RCS
         :link: https://doi.org/10.6028/NIST.IR.6910
         :class-card: sd-border-secondary

         **J. Albus et al.**

         *4D/RCS: A Reference Model Architecture For Unmanned Vehicle
         Systems, Version 2.0.* NISTIR 6910, NIST, August 2002.

         The source of L3's idea 1, a world model at each layer at the
         detail that layer needs, which decides what goes in the agent's
         context.

      .. grid-item-card:: ARIAC scoring
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring**

         The page that says the nominal targets (150 s for a high-priority
         order, 4 s for an inspection report) can change.


.. dropdown:: The Gemini Client (Code Page)
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Gemini pricing
         :link: https://ai.google.dev/gemini-api/docs/pricing
         :class-card: sd-border-secondary

         **Google, Gemini API pricing page**

         The prices in ``gemini_prices.py`` and on The Cost of Run 1 slide:
         $0.30 per million input tokens and $2.50 per million output tokens
         for ``gemini-3.5-flash-lite``, read 2026-10-17.

      .. grid-item-card:: Google GenAI SDK for Python
         :link: https://googleapis.github.io/python-genai/
         :class-card: sd-border-secondary

         **googleapis/python-genai**

         The ``google-genai`` package (2.31.0 in the lecture's virtual
         environment) that ``gemini_model.py`` uses.

      .. grid-item-card:: Gemini API keys
         :link: https://ai.google.dev/gemini-api/docs/api-key
         :class-card: sd-border-secondary

         **Google, Using Gemini API keys**

         How the key reaches the client, and "Never check API keys into
         source control systems like Git."
