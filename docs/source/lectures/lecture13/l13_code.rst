====================================================
Code
====================================================

L13 has two Python scripts and a shell script that runs them. They show the
final demo's embodied-reasoning step: ``er_demo.py`` asks Gemini Robotics ER
about 12 cells and checks each answer against a JSON schema, and
``score_er.py`` scores those answers against a GP2 lidar detector. Neither
uses ROS 2 or the ARIAC simulation.

.. warning::

   **The model server is a scripted stand-in.** The client side is the real
   ``google-genai`` SDK, called the way the Gemini API robotics page shows.
   The server side is not a model: an ``httpx`` mock transport catches each
   request before it leaves your machine and returns an answer written in
   advance. No API key and no network are used. The images are synthetic 8
   by 8 gray PNG files, not ARIAC camera images, and the cell IDs, the
   scripted answers, the ground truth and the lidar labels are all chosen
   for this example.

.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it is**
     - **Notes section**
   * - :download:`er_demo.py <code/er_demo.py>`
     - Builds the request, sends it 12 times through the stand-in, and
       checks each answer against the schema.
     - :ref:`l13-demo`
   * - :download:`score_er.py <code/score_er.py>`
     - Precision and recall per defect type for the ER answers and the lidar
       labels, on the same cells.
     - :ref:`l13-demo`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs both scripts and writes their outputs to ``../outputs/``.
     - See the last section


What You Need
-------------

Python 3 with ``google-genai`` (it brings ``httpx``) and ``jsonschema``.
``google-genai`` is not packaged for the Ubuntu 24.04 system Python, so
install both in a virtual environment:

.. code-block:: bash

   python3 -m venv ~/l13-venv
   ~/l13-venv/bin/pip install google-genai jsonschema

The outputs below come from Python 3.12.3, ``google-genai`` 2.29.0, ``httpx``
0.28.1 and ``jsonschema`` 4.10.3:

.. literalinclude:: outputs/versions.txt
   :language: text

A fresh virtual environment made with the two commands above on 2026-10-12
installed ``google-genai`` 2.29.0, ``httpx`` 0.28.1 and ``jsonschema`` 4.26.0,
and both scripts printed the same output.

Download both Python files into one folder, ``code/``. ``score_er.py``
imports ``er_demo.py``, so they must sit side by side. Run each script from
that folder:

.. code-block:: bash

   cd code
   ~/l13-venv/bin/python er_demo.py
   ~/l13-venv/bin/python score_er.py


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
       false) and a list of ``defects``, each with a ``type`` (``DENT``,
       ``SCRATCH`` or ``BULGE``) and a ``point`` of two integers from 0 to
       1000.
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
       prompt and ``thinking_level`` medium. Returns the answer text.
   * - ``check``
     - Parses the text as JSON and lists every schema error, as
       ``path: message``.
   * - ``ask_all``
     - Asks about every cell and keeps, per cell, the text, the parsed answer
       and the errors. ``score_er.py`` calls it too.
   * - ``main``
     - Prints the number of requests, where they went, the first request
       body (image data and prompt shortened), the raw answer for c07, and
       the schema check of every answer.

.. literalinclude:: code/er_demo.py
   :language: python
   :caption: er_demo.py

Output:

.. literalinclude:: outputs/er_demo.txt
   :language: text


Scoring Against GP2: ``score_er.py``
------------------------------------

The script holds two labels per cell, both chosen for this example: ``TRUTH``
(what the cell has) and ``LIDAR`` (the defect type in the team's GP2
inspection report). It calls ``ask_all`` for the ER labels, leaves out every
cell whose answer the schema rejected, and prints TP, FP, FN, precision and
recall per defect type for both detectors, on the same cells. Each defective
cell in this example has one defect. When a detector never calls a type, its
precision has no denominator and the script prints ``no calls``.

.. literalinclude:: code/score_er.py
   :language: python
   :caption: score_er.py

Output:

.. literalinclude:: outputs/score_er.txt
   :language: text

.. admonition:: Where the ground truth comes from in your runs
   :class: important

   In this example ``TRUTH`` is typed in. For your final demo measurement,
   it comes from **practice runs** launched with ``log_cell_info:=true``.
   ARIAC's launch file declares that argument as a "Cheat tool for logging
   the info about the cell when spawned", and ``cheat_tools_plugin.cpp``
   then prints each cell's type, voltage, rotation and defects to the Gazebo
   log. Graded runs use no cheat tool: the instructor starts each final demo
   run with no cheat selected. So you build your comparison table from
   practice runs, never from the graded run.


Running Against the Real Model
------------------------------

The demonstration never contacts Google. To send the same request to the
real model, you need what the Gemini API documentation lists (read
2026-10-12):

1. **A Gemini API key**, created in
   `Google AI Studio <https://aistudio.google.com/>`_ or the Google Cloud
   console. The `API key page <https://ai.google.dev/gemini-api/docs/api-key>`_
   explains both. The robotics page says the Gemini API "does not accept
   requests from unrestricted API keys and returns a 403 Forbidden error",
   so restrict the key to the Gemini API in AI Studio.
2. **The key in an environment variable,** ``GEMINI_API_KEY`` (or
   ``GOOGLE_API_KEY``, which wins if both are set). The client libraries read
   it automatically:

   .. code-block:: bash

      export GEMINI_API_KEY=<YOUR_API_KEY_HERE>

   Never commit the key; in the final demo, pass it to your Docker container
   as an environment variable at run time (course
   :doc:`AI setup page </ariac/ai_setup>`).
3. **The SDK,** ``pip install -U google-genai`` (the quickstart's command).
4. **Access to the model.** The robotics page marks Gemini Robotics ER as a
   preview model. On 2026-10-12 the
   `pricing page <https://ai.google.dev/gemini-api/docs/pricing>`_ lists a
   free tier for ``gemini-robotics-er-2-preview`` and a paid tier billed per
   million tokens. Prices change, so check the page before you run many
   calls.

**What changes in the code.**

- In ``ask_all``, replace ``client = make_client(stand_in)`` with
  ``client = genai.Client()``. With no ``api_key`` argument, the client reads
  ``GEMINI_API_KEY``; without the variable it stops with ``ValueError: No API
  key was provided``.
- Replace ``placeholder_png()`` with the bytes of a real camera image, for
  example ``open("cell.png", "rb").read()``.
- ``main`` prints what the stand-in recorded (``stand_in.requests`` and its
  URL). With a real client the stand-in records nothing, so remove those
  lines.
- ``SCRIPT`` is no longer used: the answers come from the model and vary
  from call to call.

.. note::

   These steps come from the Gemini API documentation; the course did not
   make a real call while writing this page. The instructor shows a real
   call in class only if model access is confirmed.


Run Everything: ``run_all.sh``
------------------------------

``run_all.sh`` records the Python and package versions in ``versions.txt``,
then runs both scripts and writes their outputs to ``../outputs/``. It clears
the environment (``env -i``) so a sourced ROS 2 setup cannot change which
packages load, and runs the Python of the virtual environment named by
``VENV``, which is ``~/l13-venv`` unless you set it. Create the
``outputs/`` folder next to ``code/`` first:

.. code-block:: bash

   mkdir -p outputs
   bash code/run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh
