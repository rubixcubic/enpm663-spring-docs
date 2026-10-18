====================================================
AI Access (LLMs and VLMs)
====================================================

From L8, and for GP4 and the final demo, you need access to a large
language model (LLM) and a vision-language model (VLM). The course default
is Google Gemini: the L8 and L9 demos call ``gemini-3.5-flash-lite``
through ``generateContent``, and the final demo calls Gemini Robotics ER
(``gemini-robotics-er-2-preview``). GP4 and the final demo pages also allow
a local open-weight model; see Option B.

This costs your team nothing. While you develop, you use your own
free-tier Gemini API key, at no charge. The course Gemini key runs only
the graded GP4 and final demo evaluations, also at no charge to your team.

.. note::

   Never commit API keys to your repository. The Gemini API docs put it
   plainly (`API keys <https://ai.google.dev/gemini-api/docs/api-key>`_,
   read 2026-10-18): "Never check API keys into source control systems
   like Git." Store the key outside every repository, the way the lecture
   code reads it (see "Where the key goes" below), or, for your own GP4
   code, in an environment variable or a ``.env`` file listed in
   ``.gitignore``.

Option A: Google Gemini (Course Default)
------------------------------------------

Create a free key in Google AI Studio. Steps from the Gemini API docs
(`API keys <https://ai.google.dev/gemini-api/docs/api-key>`_, read
2026-10-18):

1. Go to `Google AI Studio <https://aistudio.google.com/apikey>`_ and click
   **Get API key**. If you are new to it, Google AI Studio
   "automatically creates a default Google Cloud project and API key
   after you accept the Terms of Service," and your key is ready.
2. To use an existing Google Cloud project instead, "you must import your
   existing projects": open **Dashboard**, select **Projects**, click
   **Import projects**, choose your project, then open **API Keys** and
   click **Create API key**.
3. Install the SDK: ``pip install google-genai``.

Where the key goes
~~~~~~~~~~~~~~~~~~~

The course's L8 code reads the key from a file, not an environment
variable: ``read_key()`` in ``gemini_model.py`` opens the file and refuses
it unless its permissions are exactly mode 600 (only you can read it).
Store your own key the same way, outside every repository:

.. code-block:: bash

   mkdir -p ~/.config/enpm663
   touch ~/.config/enpm663/gemini_key
   chmod 600 ~/.config/enpm663/gemini_key
   # paste the key into the file with an editor

Hand your code the file's path, never the key itself, and never on a
command line. For your own GP4 submission, the GP4 guard rails instead
allow an environment variable or a ``.env`` file listed in ``.gitignore``
(see :doc:`/assignments/gp4`); either way, the key stays out of every
repository.

Free tier: pace and data use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Gemini API's rate-limits page gives no requests-per-minute number for
``gemini-robotics-er-2-preview`` (checked 2026-10-18). In a course
recording on 2026-10-18, Google refused the 9th back-to-back call with HTTP
429 and the message "Rate limit exceeded for model
gemini-robotics-er-2-preview (limit: 5 requests per minute on Free Tier).
Please retry in 35s". The first 8 calls had all been answered within 34 s,
so the limit is not a simple count per minute, and the recording does not
show how it is counted. A second recording started its calls 13 seconds
apart and got 12 answers of 12: pace your calls at least that far apart on
the free tier. Google may
also use what you send on the free tier to improve its products: the
pricing page (read 2026-10-18) lists "Content used to improve our
products" for the free tier, against "not used to improve our products"
for the paid tier.

Option B: Local Open-Weight Models
------------------------------------

A team may run a local open-weight model instead of a hosted one, within
the conditions GP4 and the final demo set:

- **GP4** (see :doc:`/assignments/gp4`) lists "Gemini or a local
  open-weight model" as the LLM and VLM resource. Local models avoid
  per-token cost and keep data on your machine, at the price of hardware
  requirements.
- **Final demo** (see :doc:`/assignments/final_demo`): for the
  embodied-reasoning step, you may use "a Google model that runs on the
  course key or a local model, if it reports the same comparison:
  precision and recall per defect type on the same cells, latency and
  cost."

`Ollama <https://ollama.com/>`_ is the simplest runner:

.. code-block:: bash

   curl -fsSL https://ollama.com/install.sh | sh

   # An LLM for task planning:
   ollama pull llama3.2

   # A VLM for scene grounding:
   ollama pull qwen2.5vl

Check a model's memory needs on its Ollama page before you pull it. Small
VLMs such as Qwen-VL and LLaVA come in sizes meant for a single GPU.

Model Context Protocol (MCP)
----------------------------

Tool and context integration in L8 uses the `Model Context Protocol
<https://modelcontextprotocol.io/>`_ (MCP). MCP's own site (read
2026-10-18) describes it as "an open-source standard for connecting AI
applications to external systems," with support across "a wide range of
clients and servers," naming Claude, ChatGPT, Visual Studio Code and
Cursor among them. No special install is needed to start; the SDK is
introduced in L8 and used in GP4.

Embodied-Reasoning Model (Final Demo)
--------------------------------------

The final demo uses a hosted embodied-reasoning model for one perception
step: Gemini Robotics ER (``gemini-robotics-er-2-preview``) through the
Gemini API. These models answer spatial questions about an image (where a
part is, which cell looks damaged) and are part of what the industry calls
physical AI. Pace your calls as in Option A: about 13 seconds apart on
the free tier. Access and cost details are posted with the final demo
specification.
