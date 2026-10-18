====================================================
Code
====================================================

L13 has three Python scripts and a shell script that runs the offline parts.
They show the final demo's embodied-reasoning step: ``er_demo.py`` asks
Gemini Robotics ER about each cell image and checks each answer against a
JSON schema, ``er_rerun.py`` sends a recorded session's images to the real
model again, and ``score_er.py`` scores the answers. None of them uses ROS 2
or the ARIAC simulation.

.. warning::

   **Two modes.**

   - **Offline (scripted model: fixed replies).** The client side is the real
     ``google-genai`` SDK, called the way the Gemini API robotics page shows.
     The server side is not a model: an ``httpx`` mock transport catches each
     request before it leaves your machine and returns an answer written in
     advance. No API key and no network are used. The images are synthetic 8
     by 8 gray PNG files, and the cell IDs, the scripted answers, the ground
     truth and the lidar labels are all chosen for this example.
   - **Live.** The same ``ask()`` and ``check()``, with the mock removed: each
     image goes to the real model with your key. The two runs in the
     :ref:`lecture notes <l13-real-runs>` were made this way, each recorded
     once, on 2026-10-18, with ``gemini-robotics-er-2-preview``. A rerun
     gives different answers.

.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it is**
     - **Notes section**
   * - :download:`er_demo.py <code/er_demo.py>`
     - Offline: builds the request, sends it 12 times through the stand-in,
       and checks each answer against the schema. Live: sends your images
       to the model and saves every request and response.
     - :ref:`l13-demo`
   * - :download:`er_rerun.py <code/er_rerun.py>`
     - Run 2: sends a recorded session's 12 images again, with structured
       output, 13 s apart.
     - :ref:`l13-run2-call`
   * - :download:`score_er.py <code/score_er.py>`
     - Precision and recall per defect type: for the scripted example
       (``--scripted``), or for a recorded run against ARIAC's cell log.
     - :ref:`l13-demo`, :ref:`l13-real-runs`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs the offline parts and writes their outputs to ``../outputs/``.
     - See the last section


What You Need
-------------

Python 3 with ``google-genai`` (it brings ``httpx``) and ``jsonschema``.
``google-genai`` is not packaged for the Ubuntu 24.04 system Python, so
install both in a virtual environment:

.. code-block:: bash

   python3 -m venv ~/l13-venv
   ~/l13-venv/bin/pip install google-genai jsonschema

The outputs on these pages come from Python 3.12.3, ``google-genai`` 2.31.0,
``httpx`` 0.28.1 and ``jsonschema`` 4.26.0:

.. literalinclude:: outputs/versions.txt
   :language: text

Download ``er_demo.py`` and ``score_er.py`` into one folder, ``code/``.
``score_er.py`` imports ``er_demo.py``, so they must sit side by side. Run
the offline example from that folder:

.. code-block:: bash

   cd code
   ~/l13-venv/bin/python er_demo.py
   ~/l13-venv/bin/python score_er.py --scripted


The ER Demonstration: ``er_demo.py``
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75
   :class: compact-table

   * - **Part**
     - **What it does**
   * - ``MODEL``, ``CELLS``
     - The API model name, ``gemini-robotics-er-2-preview`` (2026-10-12), and
       the 12 cell IDs ``c01`` to ``c12``.
   * - ``PROMPT``
     - The question: the three ARIAC defect types and the JSON format of the
       answer. Its last sentence is quoted from the Gemini API robotics page.
   * - ``ANSWER_SCHEMA``
     - The JSON schema every answer must match: ``defective`` (true or
       false) and a list of ``defects``, each with a ``type`` (the string
       ``DENT``, ``SCRATCH`` or ``BULGE``) and a ``point`` of two integers
       from 0 to 1000.
   * - ``SCRIPT``
     - The stand-in's 12 answers, one per call, in call order.
   * - ``placeholder_png``
     - Builds the synthetic 8 by 8 gray PNG sent as the image.
   * - ``StandIn``
     - The stand-in for the server: it records each request and returns the
       next scripted answer in the shape of a completed interaction.
   * - ``make_client``
     - A ``genai.Client`` whose HTTP client is an ``httpx`` client with a
       ``MockTransport``, so every request goes to ``StandIn``.
   * - ``ask``
     - One call to ``client.interactions.create``: the image (base64), the
       prompt and ``thinking_level`` medium, plus any ``extra`` arguments.
       Returns the answer text.
   * - ``STRUCTURED``, ``GAP_S``
     - Run 2's two extra arguments (``response_format`` with
       ``ANSWER_SCHEMA``, and ``store=False``) and its 13 s between call
       starts.
   * - ``check``
     - Parses the text as JSON and lists every schema error, as
       ``path: message``. It runs on every answer, in every mode.
   * - ``ask_all``
     - Asks about every cell and keeps, per cell, the text, the parsed answer
       and the errors. ``score_er.py --scripted`` calls it too.
   * - ``main``
     - Prints the number of requests, where they went, the first request
       body (image data and prompt shortened), the raw answer for c07, and
       the schema check of every answer.
   * - ``Recorder``
     - Live mode: saves each request (key and image bytes removed; the image
       is named by its SHA-256) and each response, and blocks a second
       request for the same image, so no call is ever repeated.
   * - ``make_live_client``
     - The SDK client with no stand-in: a plain ``httpx`` client with the
       recorder's hooks.
   * - ``ask_live``
     - Live mode: one call per image, in order, never repeated, with a wall
       limit of 120 s per call. After HTTP 400, 401, 403, 404 or 429, or a
       call with no answer in time, the other images are not sent.
   * - ``live_main``
     - The command line for your own images (next section).

.. literalinclude:: code/er_demo.py
   :language: python
   :caption: er_demo.py

Offline output:

.. literalinclude:: outputs/er_demo.txt
   :language: text


Scoring: ``score_er.py``
------------------------

**The scripted example** (``score_er.py --scripted``). The script holds two
labels per cell, both chosen for this example: ``TRUTH`` (what the cell has)
and ``LIDAR`` (the defect type in the team's GP2 inspection report). It calls
``ask_all`` for the ER labels, leaves out every cell whose answer the schema
rejected, and prints TP, FP, FN, precision and recall per defect type for
both detectors, on the same cells. Each defective cell in this example has
one defect. When a detector never calls a type, its precision has no
denominator and the script prints ``no calls``.

**A recorded run** (``score_er.py RAW_DIR``). It reads the run's files
(``answers.json``, the responses, ``captures.json`` and ARIAC's cell log
``cell_info.txt``) and needs no key and no network. A cell can have two
defects, so each label is a set of types. It prints the deck's check on the
answers as sent, precision and recall per type with 95% Wilson score
intervals and what one cell changes, each logged defect with its depth and
its angle from the camera, the model's points, and the tokens, latency and
cost of every call. The raw recordings are not published, so this mode runs
only in the slides repository; its outputs are below.

.. literalinclude:: code/score_er.py
   :language: python
   :caption: score_er.py

Scripted output:

.. literalinclude:: outputs/score_er.txt
   :language: text

Run 1, scored (``outputs/score_er_rec1.txt``):

.. literalinclude:: outputs/score_er_rec1.txt
   :language: text

Run 2, scored (``outputs/score_er_rec2.txt``):

.. literalinclude:: outputs/score_er_rec2.txt
   :language: text

.. admonition:: Where the ground truth comes from in your runs
   :class: important

   In the scripted example ``TRUTH`` is typed in. In Run 1 and Run 2 it
   comes from ARIAC's cell log. For your final demo measurement, it comes
   from **practice runs** launched with ``log_cell_info:=true``. ARIAC's
   launch file declares that argument as a "Cheat tool for logging the info
   about the cell when spawned", and ``cheat_tools_plugin.cpp`` then prints
   each cell's type, voltage, rotation and defects to the Gazebo log. Graded
   runs use no cheat tool: the instructor starts each final demo run with no
   cheat selected. So you build your comparison table from practice runs,
   never from the graded run.


Run 2: ``er_rerun.py``
----------------------

``er_rerun.py er_rec2 er_rec1`` sends the 12 images that the ``er_rec1``
session saved to the model once more, each with ``STRUCTURED`` and 13 s
between call starts. It runs no simulation. It writes the header and the call
log to ``outputs/er_rec2.txt`` and the requests and responses to
``outputs/raw/er_rec2/``, and refuses to overwrite an earlier recording. The
key is read from ``~/.config/enpm663/gemini_key`` and never printed.

.. literalinclude:: code/er_rerun.py
   :language: python
   :caption: er_rerun.py

Run 1's log (``outputs/er_rec1.txt``; the session ran ARIAC in the course's
simulation container):

.. literalinclude:: outputs/er_rec1.txt
   :language: text

Run 2's log (``outputs/er_rec2.txt``):

.. literalinclude:: outputs/er_rec2.txt
   :language: text


Running Against the Real Model
------------------------------

To send your own images to the real model, you need what the Gemini API
documentation lists (read 2026-10-12 and 2026-10-18):

1. **A Gemini API key**, created in
   `Google AI Studio <https://aistudio.google.com/>`_ or the Google Cloud
   console. The `API key page <https://ai.google.dev/gemini-api/docs/api-key>`_
   explains both. The robotics page says the Gemini API "does not accept
   requests from unrestricted API keys and returns a 403 Forbidden error",
   so restrict the key to the Gemini API in AI Studio.
2. **The key in a file,** the way the course code reads it:
   ``~/.config/enpm663/gemini_key``, mode 600 (the
   :doc:`AI setup page </ariac/ai_setup>` shows the commands). ``read_key()``
   in L8's ``gemini_model.py`` refuses any other mode. Never commit the key.
   In the final demo, your image reads the key at run time as an
   environment variable, and your README names it (``GEMINI_API_KEY`` for
   Gemini; :doc:`final demo page </assignments/final_demo>`, Task 5).
3. **The SDK,** ``pip install -U google-genai`` (the quickstart's command).
4. **Access to the model, and what the free tier means.** The robotics page
   marks Gemini Robotics ER as a preview model. On 2026-10-18 the
   `pricing page <https://ai.google.dev/gemini-api/docs/pricing>`_ lists for
   ``gemini-robotics-er-2-preview`` a free tier ("Free of charge") and a paid
   tier billed per million tokens, and answers "Used to improve our
   products" with "Yes" for the free tier and "No" for the paid tier. The
   `Interactions overview <https://ai.google.dev/gemini-api/docs/interactions-overview>`_
   (read 2026-10-18) says: "By default, the API stores all Interaction
   objects (store=true)", and "Free tier: The system retains interactions
   for 1 day." Set ``store=False`` (Run 2's ``STRUCTURED`` does) if you do
   not want your calls kept. In Run 1, Google refused the 9th call with
   "Rate limit exceeded for model gemini-robotics-er-2-preview (limit: 5
   requests per minute on Free Tier)", after 8 calls answered within 34 s,
   so the limit is not a simple count per minute. Run 2 started its calls
   13 s apart and got 12 answers of 12; pace yours the same way. The paid
   prices double on January 1, 2027, during the semester ($2.00 and $10.00
   per million input and output tokens, from $1.00 and $5.00). Prices
   change, so check the page before you run many calls.

**The command.** With L8's ``gemini_model.py`` in ``lecture8/code/`` next to
``lecture13/code/`` (as in the slides repository; ``er_demo.py`` adds that
folder to its import path):

.. code-block:: bash

   cd lecture13/code
   ~/l13-venv/bin/python er_demo.py --live-structured \
       ~/.config/enpm663/gemini_key raw/mine cell1.png cell2.png

``--live-structured`` makes Run 2's calls (structured output,
``store=False``, 13 s apart); ``--live`` makes Run 1's call, with neither.
Each image is sent once. ``raw/mine/`` gets each request (key removed), each
response and ``answers.json``, with the schema check of every answer.

.. note::

   These steps come from the Gemini API documentation and from the two
   recorded runs. Each run was recorded once, so your answers can differ
   from the recordings. The recordings do not show call-to-call variation
   by themselves: c02 was a DENT inside Run 1's code fence and a BULGE in
   Run 2, but Run 2 also changed the output format (structured output), so
   that change cannot be told apart from the format change.


Run Everything Offline: ``run_all.sh``
--------------------------------------

``run_all.sh`` records the Python and package versions in ``versions.txt``,
then runs the scripted example and writes its outputs to ``../outputs/``. In
the slides repository it also scores the two recorded runs, cuts the slide
listings from the outputs, and runs the tests. It clears the environment
(``env -i``) so a sourced ROS 2 setup cannot change which packages load, and
runs the Python of the virtual environment named by ``VENV``, which is
``~/l13-venv`` unless you set it. It needs no key and no network. Create the
``outputs/`` folder next to ``code/`` first:

.. code-block:: bash

   mkdir -p outputs
   bash code/run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh
