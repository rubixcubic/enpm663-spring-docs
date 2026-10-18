====================================================
Model Context Protocol (MCP)
====================================================

.. admonition:: Read this before L8. It takes about 20 minutes.
   :class: important

   This page is **pre-read material**: a short overview of the Model
   Context Protocol (MCP), so that the MCP part of
   :doc:`L8 </lectures/lecture8/l8_index>` starts from a picture you already
   have. It answers four questions: why a standard protocol for tools, who
   talks to whom, what a server can offer, and how the messages travel.

   L8 builds an MCP server for ten tools (7 skills and 3 readings), with a client that calls
   three of them against ARIAC, and discusses what GP4 should expose this way.
   This page does not.

Read the :doc:`LLM Prompting and Structured Output <llm-prompting>` pre-read
first: this page uses JSON and JSON Schema from it.


Why a Standard Protocol for Tools
---------------------------------

An LLM only reads and writes text. To read a file, query a database or move
a robot, an AI application gives the model **tools**: functions the
application runs when the model asks for them. L8 explains how the model
asks.

Someone has to connect each application to each source of tools. Without a
shared way to do it, every pair needs its own code. Anthropic named this
problem when it released MCP on November 25, 2024: "Every new data source
requires its own custom implementation, making truly connected systems
difficult to scale." MCP is its answer: "a universal, open standard for
connecting AI systems with data sources, replacing fragmented integrations
with a single protocol."
(`Introducing the Model Context Protocol <https://www.anthropic.com/news/model-context-protocol>`__,
read 2026-10-12.)

A **protocol** is a set of rules for the messages two programs exchange.
If both sides follow the same rules, neither needs to know how the other is
written.

**A worked example** (numbers chosen for this example). Three AI
applications each want tools from four sources.

1. **Without a standard**, each application needs its own connector for
   each source: 3 × 4 = 12 connectors, each written and kept up to date by
   someone.
2. **With MCP**, each application learns the protocol once, and each source
   is wrapped once: 3 + 4 = 7 pieces.
3. A fifth source adds 3 connectors without the standard (one per
   application), but only 1 piece with it.

For GP4 this means: if your team writes its robot tools as an MCP server,
any agent program that speaks MCP can use them, whichever model it calls.


Host, Client and Server
-----------------------

MCP names three participants.

.. list-table::
   :widths: 16 44 40
   :header-rows: 1
   :class: compact-table

   * - Participant
     - What it is, in plain words
     - In a GP4 agent that uses MCP
   * - **Host**
     - The AI application the user runs. It talks to the LLM and decides
       what to do with the tools.
     - Your team's agent program, with its orchestrator
   * - **Client**
     - A part inside the host that holds the connection to one server. The
       host makes one client for each server.
     - An object in your program, made by the ``mcp`` package
   * - **Server**
     - A separate program that offers tools and data to clients.
     - A program that offers robot actions, such as moving an AGV

The architecture page says it this way: "The MCP host accomplishes this by
creating one MCP client for each MCP server. Each MCP client maintains a
dedicated connection with its corresponding MCP server."
(`Architecture overview <https://modelcontextprotocol.io/docs/learn/architecture>`__,
read 2026-10-12.) A host connected to three servers holds three clients.

The picture below shows one host with two servers. Lines are connections,
not distances.

.. code-block:: text

   +------------------- host: your agent program --------------------+
   |                                                                 |
   |   LLM calls          orchestrator         client 1   client 2   |
   |                                              |          |       |
   +----------------------------------------------|----------|-------+
                                                  |          |
                                              server A   server B
                                             (AGV tools)  (a file reader)

.. note::

   The LLM is not one of the three. The model never connects to a server.
   The host reads the server's tool list, shows it to the model, and when
   the model asks for a tool, the host's client makes the call. MCP
   "does not dictate how AI applications use LLMs or manage the provided
   context" (architecture overview).


What a Server Offers: Three Primitives
--------------------------------------

A **primitive** is one kind of thing a server can offer. MCP defines three
for servers. They differ in **who decides when they are used**, and the
specification states that for each one:

.. list-table::
   :widths: 14 36 22 28
   :header-rows: 1
   :class: compact-table

   * - Primitive
     - What it is
     - Who decides when it is used
     - A robot cell example
   * - **Tools**
     - Functions that do something, with a name, a description and an
       input schema
     - The model: "model-controlled"
     - Move AGV 1 to a station
   * - **Resources**
     - Data the server can hand over, each at an address (a URI)
     - The host application: "application-driven"
     - The current state of each AGV, read only
   * - **Prompts**
     - Ready-made message templates the server offers
     - The user: "user-controlled"
     - A template "plan the next kit" that the operator picks from a menu

Quotes from the specification's
`tools <https://modelcontextprotocol.io/specification/2026-07-28/server/tools>`__,
`resources <https://modelcontextprotocol.io/specification/2026-07-28/server/resources>`__
and `prompts <https://modelcontextprotocol.io/specification/2026-07-28/server/prompts>`__
pages, revision 2026-07-28, read 2026-10-12.

Clients can offer one primitive back to servers in this revision:
**elicitation**, which lets a server ask the user for more information. You
will not need it in this course.


How the Messages Travel
-----------------------

**JSON-RPC 2.0.** Every MCP message is a JSON object in the JSON-RPC 2.0
format. **RPC** means remote procedure call: one program asks another to run
a named function and send back the result. A JSON-RPC request has four
fields:

- ``jsonrpc``: always ``"2.0"``.
- ``id``: a number the client picks. The response carries the same ``id``,
  so the client knows which request it answers.
- ``method``: the name of what to run, such as ``tools/list`` or
  ``tools/call``.
- ``params``: the arguments.

A **notification**, a message that needs no answer, has no ``id``. The
response to a request has the same ``id`` and either a ``result`` or an
``error``.
(`JSON-RPC 2.0 specification <https://www.jsonrpc.org/specification>`__,
read 2026-10-12.)

**A captured exchange.** To see real messages, we wrote a toy server,
``lamp-demo``, with one tool (``set-lamp``, which switches a room's lamp on
or off) and one resource (``lamp://state``). We connected the Python ``mcp``
package's own client to it (``mcp`` 2.3.0, Python 3.12.3, 2026-10-12) and
logged every line between them. The client sent four requests:

.. list-table::
   :widths: 8 26 66
   :header-rows: 1
   :class: compact-table

   * - ``id``
     - ``method``
     - What the client asked
   * - 1
     - ``server/discover``
     - Which protocol versions and primitives do you support?
   * - 2
     - ``tools/list``
     - Which tools do you have? (The reply holds each tool's name,
       description and input schema.)
   * - 3
     - ``tools/call``
     - Run ``set-lamp`` with these arguments.
   * - 4
     - ``resources/read``
     - Send the data at ``lamp://state``.

Request 3 and its response, as logged. On the wire each message is one
line; we added the indentation.

.. code-block:: json
   :caption: Client to server

   {
     "jsonrpc": "2.0",
     "id": 3,
     "method": "tools/call",
     "params": {
       "name": "set-lamp",
       "arguments": {
         "room": "lab",
         "on": true
       },
       "_meta": {
         "io.modelcontextprotocol/protocolVersion": "2026-07-28",
         "io.modelcontextprotocol/clientInfo": {
           "name": "mcp",
           "version": "0.1.0"
         },
         "io.modelcontextprotocol/clientCapabilities": {}
       }
     }
   }

.. code-block:: json
   :caption: Server to client

   {
     "jsonrpc": "2.0",
     "id": 3,
     "result": {
       "content": [
         {
           "text": "{\n  \"room\": \"lab\",\n  \"on\": true\n}",
           "type": "text"
         }
       ],
       "isError": false,
       "resultType": "complete",
       "_meta": {
         "io.modelcontextprotocol/serverInfo": {
           "name": "lamp-demo",
           "version": ""
         }
       }
     }
   }

**Reading the exchange:**

1. The request names the tool and gives its arguments as a JSON object.
   They are the same arguments a model would put in a tool call.
2. ``_meta`` carries the protocol version on **every** request. Revision
   2026-07-28 made MCP stateless, in the same sense as the LLM API in the
   other pre-read: "Every request carries the protocol version and the
   capabilities relevant to that request in its ``_meta`` field, so the
   server can process each request on its own." (architecture overview)
3. The response carries ``id`` 3, so the client matches it to request 3.
   The tool's return value comes back as text inside ``content``.

.. warning::

   **Older tutorials start differently.** "Earlier protocol revisions
   established a connection-scoped session with an ``initialize``
   handshake"
   (`Transports <https://modelcontextprotocol.io/specification/2026-07-28/basic/transports>`__,
   read 2026-10-12). A tutorial whose first message is ``initialize`` was
   written for an earlier revision. The ``mcp`` package 2.3.0 sent
   ``server/discover`` first in our run. Check which ``mcp`` version a
   tutorial uses before you copy its code; L8 uses 2.3.0.


Two Transports
--------------

A **transport** is how the messages get from one program to the other. The
messages are the same on both; only the delivery changes.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * -
     - **stdio**
     - **Streamable HTTP**
   * - Who starts the server
     - The client starts it as a child process on the same machine.
     - The server runs on its own, on this machine or another, and waits
       for clients.
   * - How messages travel
     - Through the server's standard input and standard output, one JSON
       message per line.
     - The client sends each message as an HTTP POST to one address, the
       server's MCP endpoint. The reply comes back in the HTTP response.
   * - Typical use
     - A local server for one host, such as robot tools on the robot's
       computer.
     - A shared server that many clients reach over the network.

The stdio rules include: "Messages are delimited by newlines, and **MUST
NOT** contain embedded newlines," and "The server **MUST NOT** write
anything to its ``stdout`` that is not a valid MCP message."
(`stdio transport <https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio>`__,
read 2026-10-12.) So in a stdio server, ``print()`` writes into the message
channel. We tried it: we added ``print("switching", room)`` to the toy
server's tool. With ``mcp`` 2.3.0 the calls still returned, but the client
logged ``Failed to parse JSONRPC message from server`` and a validation
error for the text ``switching lab``. The specification forbids that line,
so do not count on a client tolerating it. Log to standard error instead,
which the same page allows.

The captured exchange above used stdio, and so does the L8 demonstration.


Where L8 Takes Over
-------------------

L8's :ref:`Tool calling and MCP <l8-tool-calling>` section starts from this
picture. It shows what a tool is in an LLM API, how to design tools for the
factory, an MCP server for ten tools (7 skills and 3 readings) written with ``mcp`` 2.3.0,
a client that lists them and calls three against ARIAC, and why GP4 exposes
task-level tools behind the executor's guards instead of raw ROS topics. Whether to use MCP in GP4
is each team's choice.


Check Yourself
--------------

.. admonition:: Question 1
   :class: hint

   Five AI applications each need tools from six sources. How many pieces
   does each approach need, without a standard and with MCP?

.. dropdown:: Answer
   :class-container: sd-border-success

   1. Without a standard: one connector per pair, 5 × 6 = 30.
   2. With MCP: one client side per application and one server per source,
      5 + 6 = 11.

.. admonition:: Question 2
   :class: hint

   Your agent program connects to an AGV server and to a camera server. How
   many MCP clients does it hold, and which participant is your program?

.. dropdown:: Answer
   :class-container: sd-border-success

   Two clients, one per server. Your program is the host.

.. admonition:: Question 3
   :class: hint

   Name the primitive for each:

   1. ``place-in-slot``, which the model asks to run when it decides a cell
      goes in a slot.
   2. The list of cells on each tray, which your program reads and adds to
      the model's messages.
   3. A "recover from a tester malfunction" template that the operator
      chooses from a menu.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. A **tool**: the model decides when to call it.
   2. A **resource**: data, and the application decides when to use it.
   3. A **prompt**: a template, and the user decides when to use it.

.. admonition:: Question 4
   :class: hint

   True or false: in MCP, the LLM opens a connection to each server and
   calls the tools itself.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.** The host holds the connections, through its clients. The
   model only asks for a tool call in its reply; the host decides whether to
   run it and makes the call.

.. admonition:: Question 5
   :class: hint

   Which transport fits each case? (a) Your agent starts the AGV tool server
   on the same computer. (b) The whole team's agents share one server that
   runs on a lab machine.

.. dropdown:: Answer
   :class-container: sd-border-success

   (a) **stdio**: the client starts the server as a child process on the
   same machine. (b) **Streamable HTTP**: the server runs on its own and
   many clients reach it over the network.

.. admonition:: Question 6
   :class: hint

   You add ``print("moving agv", agv)`` inside a tool of a stdio server, and
   the client starts reporting errors. Why?

.. dropdown:: Answer
   :class-container: sd-border-success

   On stdio, the server's standard output carries the MCP messages, and the
   specification says the server must not write anything else there. The
   client reads the printed line as a message, and it is not valid JSON-RPC.
   In our test the ``mcp`` 2.3.0 client logged a parse error and went on;
   another client may not. Print to standard error instead, for example
   ``print(..., file=sys.stderr)``.


Further Reading
---------------

- `What is the Model Context Protocol? <https://modelcontextprotocol.io/docs/getting-started/intro>`__:
  the one-page introduction.
- `Architecture overview <https://modelcontextprotocol.io/docs/learn/architecture>`__:
  participants, layers, primitives, and a full example exchange.
- `Server concepts <https://modelcontextprotocol.io/docs/learn/server-concepts>`__:
  tools, resources and prompts, with examples.
- `Specification, revision 2026-07-28 <https://modelcontextprotocol.io/specification/2026-07-28>`__,
  with its `transports <https://modelcontextprotocol.io/specification/2026-07-28/basic/transports>`__,
  `stdio <https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio>`__
  and `Streamable HTTP <https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http>`__
  pages: the rules themselves.
- `JSON-RPC 2.0 specification <https://www.jsonrpc.org/specification>`__: the
  message format MCP uses.
- `Introducing the Model Context Protocol <https://www.anthropic.com/news/model-context-protocol>`__:
  Anthropic's announcement, November 25, 2024.
- `MCP Python SDK <https://github.com/modelcontextprotocol/python-sdk>`__ and
  its `PyPI page <https://pypi.org/project/mcp/>`__: the ``mcp`` package L8
  uses.
