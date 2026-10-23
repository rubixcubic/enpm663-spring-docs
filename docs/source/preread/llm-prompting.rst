====================================================
LLM Prompting and Structured Output
====================================================

.. admonition:: Read this before L8. It takes about 30 minutes.
   :class: important

   This page is **pre-read material**. It covers what
   :doc:`L8 </lectures/lecture8/l8_index>` assumes you already know: what a
   call to a large language model (LLM) looks like, why the model keeps
   nothing between calls, what a token is, where the API key lives, and how
   to read JSON and a JSON Schema.

   L8 then teaches the parts that build on it: the system prompt for a
   planner, validating the model's output against a schema with a bounded
   retry, and tool calling. This page does not cover those.

The examples on this page use Anthropic's Python SDK. The L8 demonstrations
use Google's Gemini (see the :doc:`L8 code page </lectures/lecture8/l8_code>`).
**The course's LLM provider is Google Gemini.** GP4 and the final demo also allow a local
open-weight model (see the :doc:`AI Access </ariac/ai_setup>` page). Every idea here holds
for Gemini and the other providers too; only the field names change.

**What you need to run the examples.** Python 3.10 or newer and a virtual
environment. The outputs on this page come from Python 3.12.3, ``anthropic``
1.13.0 and ``tiktoken`` 0.14.0, run on 2026-10-12:

.. code-block:: bash

   python3 -m venv ~/preread-venv
   source ~/preread-venv/bin/activate
   pip install anthropic==1.13.0 tiktoken==0.14.0

No API key is needed for this page. The one script that calls an API runs
against a local stand-in, described below.


What an LLM API Call Is
-----------------------

A **large language model (LLM)** is a program that reads text and writes
text. A hosted model runs on the provider's computers, and your program sends
it a request over the network through the provider's **API** (application
programming interface): a set of addresses and rules that one program uses to
ask another program for something. A local model, such as one run with
Ollama, answers the same kind of request on your own machine. An LLM call is one **HTTP request**, the
same kind of request a browser sends to a web server, and one reply.

A provider's **SDK** (software development kit) is a Python package that
builds the request for you, sends it, and turns the reply into Python
objects. Here is the smallest call with Anthropic's SDK:

.. code-block:: python

   import anthropic

   client = anthropic.Anthropic()        # reads ANTHROPIC_API_KEY
   reply = client.messages.create(
       model="claude-opus-5-5",
       max_tokens=200,
       messages=[{"role": "user", "content": "Hello, Claude"}],
   )
   print(reply.content[0].text)

The request carries three things:

1. **model**: which model answers. Providers list the model IDs on a models
   page, and they change: read the ID on the day you run.
2. **max_tokens**: the most output the model may write, counted in tokens
   (see :ref:`preread-llm-tokens`).
3. **messages**: a list of messages. Each message is a small record with a
   **role** and a **content**. The role ``user`` marks what your program
   says; the role ``assistant`` marks what the model said earlier.

The reply is also a record. Anthropic's guide prints this example reply. It
comes from the guide, not from a run of ours:

.. code-block:: json

   {
     "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
     "type": "message",
     "role": "assistant",
     "content": [
       {
         "type": "text",
         "text": "Hello!"
       }
     ],
     "model": "claude-opus-5-5",
     "stop_reason": "end_turn",
     "stop_sequence": null,
     "usage": {
       "input_tokens": 12,
       "output_tokens": 6
     }
   }

(`Using the Messages API <https://platform.claude.com/docs/en/build-with-claude/working-with-messages>`__,
read 2026-10-12.) Three fields matter on every call:

- **content** is a list of blocks. A ``text`` block holds the words the
  model wrote. That is why the code above reads ``reply.content[0].text``.
- **stop_reason** says why the model stopped. The API reference lists, among
  others, ``"end_turn"``: "the model reached a natural stopping point", and
  ``"max_tokens"``: "we exceeded the requested ``max_tokens`` or the model's
  maximum"
  (`Messages API reference <https://platform.claude.com/docs/en/api/messages/create>`__,
  read 2026-10-12). A reply cut off at ``max_tokens`` can end in the middle
  of a sentence, or in the middle of a JSON record.
- **usage** counts the tokens the call read (``input_tokens``) and wrote
  (``output_tokens``). The provider bills you by these two numbers.


The Model Keeps Nothing Between Calls
-------------------------------------

Each call stands alone. The model does not remember the call before it.
Anthropic's guide says: "The Messages API is stateless, which
means that you always send the full conversational history to the API."
(`Using the Messages API <https://platform.claude.com/docs/en/build-with-claude/working-with-messages>`__,
read 2026-10-12.) A chat window that seems to remember you is a program that
keeps the list of messages and sends all of it again on every call.

The script below makes three calls. Call 1 gives a robot name. Call 2 asks
for the name in a new list. Call 3 asks again, but sends the whole history.

.. code-block:: python
   :caption: two_calls.py

   """Two calls to an LLM API: without the history, then with it."""
   import anthropic

   client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
   MODEL = "claude-opus-5-5"       # read the ID from the models page on the day

   first = {"role": "user", "content": "Remember this robot name: R2-K7."}
   question = {"role": "user", "content": "What robot name did I give you?"}


   def ask(messages):
       reply = client.messages.create(model=MODEL, max_tokens=200,
                                      messages=messages)
       print(f"sent {len(messages)} message(s)")
       print("  reply:", reply.content[0].text)
       print("  stop_reason:", reply.stop_reason)
       print("  usage:", reply.usage.input_tokens, "in,",
             reply.usage.output_tokens, "out")
       return reply.content[0].text


   print("=== Call 1 ===")
   answer = ask([first])
   print("=== Call 2: a new list, no history ===")
   ask([question])
   print("=== Call 3: the history sent again ===")
   ask([first, {"role": "assistant", "content": answer}, question])

.. important::

   **No model ran for the output below.** We ran ``two_calls.py`` against a
   **stand-in**: a short local program that answers like the Messages API
   but runs no model. Its reply only reports how many messages it received
   and what the first one says. The stand-in also fills ``usage`` with 0,
   because it counts nothing. The point of the run is what the server
   *receives*, which does not depend on the model.

.. code-block:: text

   === Call 1 ===
   sent 1 message(s)
     reply: [stand-in] I received 1 message(s). The first one says: Remember this robot name: R2-K7.
     stop_reason: end_turn
     usage: 0 in, 0 out
   === Call 2: a new list, no history ===
   sent 1 message(s)
     reply: [stand-in] I received 1 message(s). The first one says: What robot name did I give you?
     stop_reason: end_turn
     usage: 0 in, 0 out
   === Call 3: the history sent again ===
   sent 3 message(s)
     reply: [stand-in] I received 3 message(s). The first one says: Remember this robot name: R2-K7.
     stop_reason: end_turn
     usage: 0 in, 0 out

The stand-in also saved the body of each request it received. This is the
body of call 3, as the SDK sent it (the stand-in added the indentation):

.. code-block:: json

   {
     "max_tokens": 200,
     "messages": [
       {
         "role": "user",
         "content": "Remember this robot name: R2-K7."
       },
       {
         "role": "assistant",
         "content": "[stand-in] I received 1 message(s). The first one says: Remember this robot name: R2-K7."
       },
       {
         "role": "user",
         "content": "What robot name did I give you?"
       }
     ],
     "model": "claude-opus-5-5"
   }

**Reading the run:**

1. Call 2 carried one message, the question. The name R2-K7 was not in it.
   A real model answering call 2 has no way to read the name: it is not in
   anything the server received.
2. Call 3 carried three messages, and the name is in the first one. The
   program, not the model, put the history back together.
3. The ``assistant`` message in call 3 is whatever the program wrote into
   the list. Here it is the stand-in's reply. The guide says the same thing:
   "Earlier conversational turns don't necessarily need to actually
   originate from Claude."
4. Each call sends everything again, so a longer conversation means a longer
   request on every call. L8 measures how fast that grows.

.. dropdown:: Run it yourself, without a key

   Save this as ``stand_in.py`` next to ``two_calls.py``. It uses only
   Python's standard library.

   .. code-block:: python
      :caption: stand_in.py

      """A local stand-in for the Messages API. No model runs here.

      It answers POST /v1/messages with a fixed reply that says how many
      messages it received, and logs each request body to requests.log.
      """
      import json
      from http.server import BaseHTTPRequestHandler, HTTPServer


      class StandIn(BaseHTTPRequestHandler):
          def do_POST(self):
              body = json.loads(self.rfile.read(int(self.headers["content-length"])))
              with open("requests.log", "a") as log:
                  log.write(json.dumps(body, indent=2) + "\n")
              msgs = body["messages"]
              text = (f"[stand-in] I received {len(msgs)} message(s). "
                      f"The first one says: {msgs[0]['content']}")
              reply = {
                  "id": "msg_standin", "type": "message", "role": "assistant",
                  "model": body["model"],
                  "content": [{"type": "text", "text": text}],
                  "stop_reason": "end_turn", "stop_sequence": None,
                  "usage": {"input_tokens": 0, "output_tokens": 0},
              }
              data = json.dumps(reply).encode()
              self.send_response(200)
              self.send_header("content-type", "application/json")
              self.send_header("content-length", str(len(data)))
              self.end_headers()
              self.wfile.write(data)

          def log_message(self, *args):
              pass


      HTTPServer(("127.0.0.1", 8765), StandIn).serve_forever()

   Start it in one terminal, then run the script in a second terminal. The
   SDK reads two environment variables: ``ANTHROPIC_BASE_URL`` sends the
   request to the stand-in in place of Anthropic's server, and the stand-in
   accepts any text as the key.

   .. code-block:: bash

      # Terminal 1
      python3 stand_in.py

      # Terminal 2, in the virtual environment
      export ANTHROPIC_BASE_URL=http://127.0.0.1:8765
      export ANTHROPIC_API_KEY=not-a-real-key
      python3 two_calls.py
      cat requests.log

   Stop the stand-in with ``Ctrl+C``. Before you call a real model, close
   that terminal or run ``unset ANTHROPIC_BASE_URL``.


.. _preread-llm-tokens:

Tokens
------

A model does not read letters or words. It reads **tokens**: pieces of text
from a fixed list the model was built with. Anthropic's glossary says tokens
"can correspond to words, subwords, characters, or even bytes", and that "the
number of characters a token represents depends on the model and the
language"
(`Glossary <https://platform.claude.com/docs/en/about-claude/glossary>`__,
read 2026-10-12). The program that cuts text into tokens is a
**tokenizer**.

To see real pieces, the script below uses ``o200k_base``, an open tokenizer
from OpenAI's ``tiktoken`` package. **Each model family has its own
tokenizer**, so a Claude or Gemini model cuts the same text differently. The
script shows the idea, not the count any one provider bills.

.. code-block:: python
   :caption: tokens.py

   """Split text into tokens with one open tokenizer (OpenAI's o200k_base)."""
   import tiktoken

   enc = tiktoken.get_encoding("o200k_base")
   for text in ["Move the robot to the charging dock.",
                "INSPECTION",
                '{"agv": 1, "station": "SHIPPING"}']:
       ids = enc.encode(text)
       pieces = [enc.decode([i]) for i in ids]
       print(f"{len(text):3} characters, {len(ids):2} tokens: {pieces}")

The first run downloads the tokenizer's table from the internet. Output
(run 2026-10-12):

.. code-block:: text

    36 characters,  8 tokens: ['Move', ' the', ' robot', ' to', ' the', ' charging', ' dock', '.']
    10 characters,  3 tokens: ['INS', 'PE', 'CTION']
    33 characters, 14 tokens: ['{"', 'ag', 'v', '":', ' ', '1', ',', ' "', 'station', '":', ' "', 'SH', 'IPPING', '"}']

**Reading the output:**

1. The English sentence: 36 characters in 8 tokens, so 36 / 8 = 4.5
   characters per token. Most common words are one token, with the space in
   front.
2. ``INSPECTION`` in capitals has no single token in this tokenizer's list,
   so it is cut into 3 pieces.
3. The JSON record: 33 characters in 14 tokens, so 33 / 14 = 2.4 characters
   per token. Quotes, colons and short names each cost a token. The same
   number of characters costs more tokens as JSON than as plain English.

**Why tokens matter for your code:**

- **Cost.** Providers price input tokens and output tokens per million,
  each at its own price. L8 works out what an agent run costs.
- **The output cap.** ``max_tokens`` stops the model after that many output
  tokens. If ``stop_reason`` is ``"max_tokens"``, the text was cut off.
- **The input limit.** A model reads at most a fixed number of tokens per
  call, its **context window**. The models page lists it for each model.

For an exact count, do not estimate from characters. Read ``usage`` in the
reply, or use the provider's token counting service. The glossary says: "To
get exact counts, use token counting with the model you plan to use."


The API Key
-----------

The provider needs to know who sends each request, so it can bill the right
account. An **API key** is a long secret string that identifies your
account. Anyone who has your key can make calls that you pay for.

**Where the key lives: in an environment variable.** An **environment
variable** is a name and a value that your shell hands to every program it
starts. Programs read it at run time, so the key never appears in your code.
The SDK looks for ``ANTHROPIC_API_KEY`` by itself; other providers use their
own names. (The L8 demonstrations keep the Gemini key in a file that only
its owner can read; the :doc:`L8 code page </lectures/lecture8/l8_code>` shows
how.)

.. code-block:: bash

   export ANTHROPIC_API_KEY="your key here"   # this terminal only
   echo ${ANTHROPIC_API_KEY:+the key is set}   # prints a note, not the key

``export`` sets the variable for that terminal and the programs it starts.
The :doc:`AI Access </ariac/ai_setup>` page shows how to set it in
``~/.bashrc`` for every new terminal. Your own Python code reads a variable
with ``os.environ``:

.. code-block:: python

   import os

   key = os.environ.get("ANTHROPIC_API_KEY")   # None if it is not set

**What the SDK does with it.** It puts the key in a header of each HTTP
request. When we ran ``two_calls.py`` against the stand-in, the stand-in saw
the header ``X-Api-Key: not-a-real-key``. Anthropic's
`API overview <https://platform.claude.com/docs/en/api/overview>`__ lists
``x-api-key`` and ``Authorization`` as the two headers that can carry it.

**What happens without it.** We ran ``two_calls.py`` with no key set. It
printed ``=== Call 1 ===`` and then stopped at the first call with a
traceback whose last line is:

.. code-block:: text

   TypeError: "Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"

If you see this, the terminal that runs the script has no key. A new
terminal does not see a variable you exported in another one.

.. warning::

   **Never write the key into a file that Git tracks.** Anyone who can read
   the repository can copy the key, and the calls are billed to you. Deleting
   the line later does not help: the key stays in the Git history. If you keep the key in a ``.env`` file, list ``.env`` in
   ``.gitignore`` before your first commit. If a key leaks, delete it in the
   provider's console and make a new one.


JSON Basics
-----------

**JSON** (JavaScript Object Notation) is a text format for data. LLM APIs
send their requests and replies as JSON, and in L8 you ask the model to
answer in JSON so that code can read the answer. The standard, RFC 8259,
says: "JSON can represent four primitive types (strings, numbers, booleans,
and null) and two structured types (objects and arrays)."
(`RFC 8259 <https://www.rfc-editor.org/rfc/rfc8259>`__, read 2026-10-12.)

.. list-table::
   :widths: 18 34 24 24
   :header-rows: 1
   :class: compact-table

   * - JSON type
     - What it holds
     - JSON example
     - Python after ``json.loads``
   * - object
     - name and value pairs; each name is a string in double quotes
     - ``{"agv": 1}``
     - ``dict``
   * - array
     - an ordered list of values
     - ``["lab", "night"]``
     - ``list``
   * - string
     - text in **double** quotes
     - ``"rover1"``
     - ``str``
   * - number
     - an integer or a decimal
     - ``87.5``
     - ``int`` or ``float``
   * - boolean
     - ``true`` or ``false``, lowercase
     - ``false``
     - ``bool``
   * - null
     - no value
     - ``null``
     - ``None``

Objects and arrays can hold each other, to any depth. Python's ``json``
module turns JSON text into Python objects (``json.loads``) and back
(``json.dumps``):

.. code-block:: python
   :caption: json_basics.py

   """JSON to Python and back, and three common mistakes."""
   import json

   text = ('{"name": "rover1", "battery": 87.5, "docked": false, '
           '"mode": "IDLE", "tags": ["lab", "night"], "fault": null}')
   record = json.loads(text)                  # JSON text -> Python objects
   for key, value in record.items():
       print(f"{key:8} {type(value).__name__:9} {value!r}")

   # Python -> JSON text
   print(json.dumps({"ok": True, "pose": (1, 2), "note": None}))

   for bad in ["{'name': 'rover1'}",          # single quotes
               '{"name": "rover1",}',         # trailing comma
               '{"docked": False}']:          # Python's False, not JSON's false
       try:
           json.loads(bad)
       except json.JSONDecodeError as err:
           print(f"{bad:22} -> {err.msg} (column {err.colno})")

Output (system Python 3.12.3, run 2026-10-12):

.. code-block:: text

   name     str       'rover1'
   battery  float     87.5
   docked   bool      False
   mode     str       'IDLE'
   tags     list      ['lab', 'night']
   fault    NoneType  None
   {"ok": true, "pose": [1, 2], "note": null}
   {'name': 'rover1'}     -> Expecting property name enclosed in double quotes (column 2)
   {"name": "rover1",}    -> Expecting property name enclosed in double quotes (column 19)
   {"docked": False}      -> Expecting value (column 12)

**Reading the output:**

1. Each JSON type became the Python type in the table: ``false`` became
   ``False`` and ``null`` became ``None``.
2. Going back, ``json.dumps`` wrote ``True`` as ``true`` and ``None`` as
   ``null``. JSON has no tuple, so the tuple ``(1, 2)`` became the array
   ``[1, 2]``.
3. The three mistakes are the ones you will see most from hand-written or
   model-written JSON. A Python ``dict`` printed with ``print`` uses single
   quotes, and that is not JSON. A comma after the last pair is not allowed.
   ``False`` with a capital F is Python, not JSON. The error message names
   the column where the parser gave up.

.. tip::

   To turn a Python object into JSON text, use ``json.dumps``. Never build
   JSON with ``str()`` or an f-string: ``str({"a": True})`` gives
   ``{'a': True}``, which is not JSON.


JSON Schema at a Glance
-----------------------

A JSON record can be well formed and still wrong for your program: a missing
field, a word your code does not know, a number out of range. A **JSON
Schema** is a JSON document that describes which records are allowed: which
fields, of which types, with which values. Here is a schema for a robot's
status report:

.. code-block:: json

   {
     "type": "object",
     "required": ["name", "battery", "mode"],
     "additionalProperties": false,
     "properties": {
       "name":    {"type": "string"},
       "battery": {"type": "number", "minimum": 0, "maximum": 100},
       "docked":  {"type": "boolean"},
       "mode":    {"enum": ["IDLE", "DRIVING", "CHARGING"]},
       "tags":    {"type": "array", "items": {"type": "string"}}
     }
   }

Read it one keyword at a time:

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Keyword
     - What it says in this schema
   * - ``"type": "object"``
     - The record is a JSON object.
   * - ``"required"``
     - ``name``, ``battery`` and ``mode`` must be present. ``docked`` and
       ``tags`` may be left out.
   * - ``"additionalProperties": false``
     - No field other than the five listed under ``properties``.
   * - ``"properties"``
     - The rule for each field, by name.
   * - ``"minimum"``, ``"maximum"``
     - ``battery`` is a number from 0 to 100, both ends included.
   * - ``"enum"``
     - ``mode`` must be one of the three listed strings, spelled exactly.
   * - ``"items"``
     - Every element of the ``tags`` array is a string.

Two records, checked against it by eye:

.. code-block:: json

   {"name": "rover1", "battery": 87.5, "mode": "IDLE", "tags": ["lab"]}

This one fits. The three required fields are there, 87.5 is from 0 to 100,
``IDLE`` is in the list, and ``tags`` holds strings.

.. code-block:: json

   {"name": "rover2", "battery": 120, "mode": "SLEEP", "speed": 2}

This one breaks three rules, and it is still valid JSON:

1. ``battery`` is 120, above the maximum of 100.
2. ``SLEEP`` is not one of the three modes.
3. ``speed`` is not a listed field, and ``additionalProperties`` is false.

We checked both verdicts with the Python ``jsonschema`` package (4.26.0): it
accepted the first record and listed exactly these three errors for the
second. Running that check in code, and deciding what to do when it fails,
is what L8 teaches.


Where L8 Takes Over
-------------------

You now know what goes into a call, what comes back, and how to read the
JSON on both sides. L8 builds on it:

- :ref:`The LLM as a function <l8-llm-as-function>`: what "nothing kept"
  means for a program that moves robots.
- :ref:`Prompt structure for a planner <l8-prompt-structure>`: the system
  message and the user message.
- :ref:`Structured output <l8-structured-output>`: a schema for one AGV move,
  validation in five steps, semantic checks and a bounded retry.
- :ref:`Tool calling and MCP <l8-tool-calling>`: how the model asks to run a
  tool. The :doc:`MCP pre-read <mcp>` comes before it.
- :ref:`Context, cost and latency <l8-context-cost-latency>`: how the tokens
  of each call add up over an agent run.


Check Yourself
--------------

.. admonition:: Question 1
   :class: hint

   Your program sends call 1 with "My robot is R2-K7." and gets a reply.
   Call 2 sends a new list with one message: "What is my robot's name?" What
   can the model use to answer call 2?

.. dropdown:: Answer
   :class-container: sd-border-success

   Only the one message in call 2. The API is stateless, so the name from
   call 1 is not part of call 2, and the model cannot read it. To give the
   model the name, the program sends call 1's message and the reply again,
   before the question.

.. admonition:: Question 2
   :class: hint

   Which of these strings can ``json.loads`` read?

   A. ``{'mode': 'IDLE'}``

   B. ``{"mode": "IDLE", "docked": False}``

   C. ``{"mode": "IDLE", "docked": false}``

   D. ``{"mode": "IDLE", "docked": false,}``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** only. A uses single quotes. B uses Python's ``False``; JSON's
   boolean is lowercase ``false``. D has a comma after the last pair.

.. admonition:: Question 3
   :class: hint

   Which of these records fit the robot status schema above? For each one
   that does not, name the rule it breaks.

   1. ``{"name": "rover3", "mode": "CHARGING"}``
   2. ``{"name": "rover4", "battery": "87", "mode": "IDLE"}``
   3. ``{"name": "rover5", "battery": 0, "mode": "DRIVING", "docked": true, "tags": []}``
   4. ``{"name": "rover6", "battery": 55, "mode": "IDLE", "tags": ["lab", 7]}``
   5. The record in ``json_basics.py``, with its ``fault`` field.

.. dropdown:: Answer
   :class-container: sd-border-success

   Only **3** fits. ``minimum`` includes 0, an empty array has no element
   that breaks ``items``, and ``docked`` is a boolean.

   - Record 1: ``battery`` is missing, and it is in ``required``.
   - Record 2: ``"87"`` in quotes is a string, not a number.
   - Record 4: ``7`` is a number, and ``items`` says every tag is a string.
   - Record 5: ``fault`` is not a listed field, and
     ``additionalProperties`` is false.

   We checked all five with ``jsonschema`` 4.26.0; it gave the same
   verdicts.

.. admonition:: Question 4
   :class: hint

   A teammate pastes the API key into ``planner.py`` "just for testing" and
   pushes the branch to a public repository. What can go wrong, and what
   should the team do?

.. dropdown:: Answer
   :class-container: sd-border-success

   Anyone who finds the key can make calls billed to that account, and the
   key stays in the Git history even after the line is deleted. The team
   should delete the key in the provider's console at once and make a new
   one. The new key goes in an environment variable, and the code reads it
   with ``os.environ`` (or lets the SDK read it).

.. admonition:: Question 5
   :class: hint

   A prompt has 700 characters of plain English and another prompt has 700
   characters of JSON. Using the two ratios measured with ``o200k_base`` on
   this page, about how many tokens is each? Why is the answer only an
   estimate?

.. dropdown:: Answer
   :class-container: sd-border-success

   1. English, 36 characters in 8 tokens: 700 × 8 / 36 = 155.6, so about
      156 tokens.
   2. JSON, 33 characters in 14 tokens: 700 × 14 / 33 = 297.0, so about
      297 tokens.

   Each ratio comes from one short line of text and one tokenizer. Another
   model's tokenizer cuts the same text differently, and other text has
   another ratio. The exact count for your model is in the reply's
   ``usage`` fields, or comes from the provider's token counting service.

.. admonition:: Question 6
   :class: hint

   You ask a model for a JSON record and set ``max_tokens`` to 20. The reply's
   ``stop_reason`` is ``"max_tokens"``, and ``json.loads`` fails on the text.
   What happened?

.. dropdown:: Answer
   :class-container: sd-border-success

   The model reached the 20-token cap and stopped in the middle of the
   record, so the closing quotes or braces are missing. Raise ``max_tokens``
   and check ``stop_reason`` before you parse the text.


Further Reading
---------------

- `Using the Messages API <https://platform.claude.com/docs/en/build-with-claude/working-with-messages>`__:
  Anthropic's guide to requests, replies and multi-turn conversations.
- `Messages API reference <https://platform.claude.com/docs/en/api/messages/create>`__:
  every request and reply field, including the ``stop_reason`` values.
- `API overview <https://platform.claude.com/docs/en/api/overview>`__: the
  headers that carry the key and the API version.
- `Glossary <https://platform.claude.com/docs/en/about-claude/glossary>`__ and
  `Token counting <https://platform.claude.com/docs/en/build-with-claude/token-counting>`__:
  what a token is, and how to count them exactly for a Claude model.
- `tiktoken <https://github.com/openai/tiktoken>`__: the open tokenizer used
  on this page.
- `Introducing JSON <https://www.json.org/json-en.html>`__ and
  `RFC 8259 <https://www.rfc-editor.org/rfc/rfc8259>`__: the JSON format,
  first with diagrams, then as the standard.
- `json module <https://docs.python.org/3/library/json.html>`__ and
  `os.environ <https://docs.python.org/3/library/os.html>`__: Python's
  documentation.
- `JSON Schema: getting started step by step <https://json-schema.org/learn/getting-started-step-by-step>`__
  and `type-specific keywords <https://json-schema.org/understanding-json-schema/reference/type>`__:
  how to write a schema, one keyword at a time.
