====================================================
References
====================================================

These are the sources the L13 slides cite or take their facts from, in the
order of the slides, grouped by topic. The last group holds the Gemini API
pages the two recorded runs and the :doc:`code page <l13_code>` use for
running the demonstration against the real model. Every link was checked on
2026-10-12; the last group was read again on 2026-10-18. The model pages
change often, so check a quote against its page before you rely on it.


.. dropdown:: Physical AI
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: What physical AI is
         :link: https://www.nvidia.com/en-us/glossary/generative-physical-ai/
         :class-card: sd-border-secondary

         **NVIDIA glossary:** "What is Physical AI?"

         The definition used since L1 ("perform or orchestrate complex
         actions in the physical world"), the reinforcement learning
         sentence, and why physical AI needs large, physically accurate
         training data from simulation and world foundation models.


.. dropdown:: VLA Models and Robot Foundation Models
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: OpenVLA
         :link: https://openvla.github.io/
         :class-card: sd-border-secondary

         **OpenVLA project page**

         A 7B parameter open VLA, pretrained on 970k robot episodes from the
         Open X-Embodiment dataset; adapted to new robots with
         parameter-efficient fine-tuning; trained on 64 A100 GPUs for 15
         days.

      .. grid-item-card:: pi-0 and pi-0.5
         :link: https://github.com/Physical-Intelligence/openpi
         :class-card: sd-border-secondary

         **Physical Intelligence:** ``openpi`` repository (README)

         pi-0, a flow-based VLA, and pi-0.5, with better open-world
         generalization; base checkpoints pre-trained on 10k+ hours of robot
         data; the GPU memory table for running, LoRA and full fine-tuning.

      .. grid-item-card:: Gemini Robotics
         :link: https://deepmind.google/models/gemini-robotics/
         :class-card: sd-border-secondary

         **Google DeepMind:** Gemini Robotics model page

         The VLA and ER models that "work together", Gemini Robotics 2 and
         Gemini Robotics ER 2, and the coordination of several robots in
         shared spaces.

      .. grid-item-card:: NVIDIA Isaac GR00T
         :link: https://github.com/NVIDIA/Isaac-GR00T
         :class-card: sd-border-secondary

         **NVIDIA:** ``Isaac-GR00T`` repository (README)

         GR00T N1.7, an open VLA for humanoid robot skills: a
         vision-language model with a diffusion transformer head, 20K hours
         of human video in pretraining, and its GPU requirements.

      .. grid-item-card:: SmolVLA
         :link: https://huggingface.co/blog/smolvla
         :class-card: sd-border-secondary

         **Hugging Face blog,** 3 June 2025

         A compact (450M) open VLA that runs on consumer hardware: a
         pretrained VLM and an action expert.


.. dropdown:: The Dates on the Timeline
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: OpenVLA paper
         :link: https://arxiv.org/abs/2406.09246
         :class-card: sd-border-secondary

         **Kim, M. J. et al.**

         "OpenVLA: An Open-Source Vision-Language-Action Model."
         arXiv:2406.09246. Version 1 submitted 13 June 2024.

      .. grid-item-card:: pi-0 paper
         :link: https://arxiv.org/abs/2410.24164
         :class-card: sd-border-secondary

         **Black, K. et al.**

         "π0: A Vision-Language-Action Flow Model for General Robot
         Control." arXiv:2410.24164. Version 1 submitted 31 October 2024.

      .. grid-item-card:: GR00T N1.7 release
         :link: https://github.com/NVIDIA/Isaac-GR00T/releases/tag/n1.7-release
         :class-card: sd-border-secondary

         **NVIDIA:** GitHub release ``n1.7-release``

         Published 18 April 2026.


.. dropdown:: Two-System Designs and the ER Model
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Gemini Robotics ER in the Gemini API
         :link: https://ai.google.dev/gemini-api/docs/robotics-overview
         :class-card: sd-border-secondary

         **Google:** Gemini API docs, "Gemini Robotics ER"

         The API model ``gemini-robotics-er-2-preview`` (latest update July
         2026), the deprecation of ER 1.6 on August 31, 2026, the agentic
         ER model, the Python example the demonstration follows, and the best
         practices and limitations quoted in the notes.


.. dropdown:: The Demonstration Code
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The Google GenAI SDK for Python
         :link: https://github.com/googleapis/python-genai
         :class-card: sd-border-secondary

         **Google:** ``python-genai`` repository

         The ``google-genai`` package that ``er_demo.py`` uses
         (version 2.31.0 for the outputs in the notes).

      .. grid-item-card:: HTTPX transports
         :link: https://www.python-httpx.org/advanced/transports/
         :class-card: sd-border-secondary

         **HTTPX documentation:** Transports

         ``httpx.MockTransport``, which the stand-in uses to answer each
         request without the network.


.. dropdown:: ARIAC 2025
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The defect types
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellDefect.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellDefect.msg`` (branch
         ``ariac2025``)

         DENT, BULGE and SCRATCH: the three types the answer schema allows.

      .. grid-item-card:: The scenario
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **ARIAC documentation:** Scenario

         How each defect type looks on a cell, which the prompt describes in
         simpler words.

      .. grid-item-card:: Ground truth for practice runs
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/cheat_tools_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/cheat_tools_plugin.cpp``

         With ``log_cell_info:=true``, prints each cell's type, voltage,
         rotation and defects to the Gazebo log.

         +++

         The launch argument is declared in
         `ariac.launch.py <https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/launch/ariac.launch.py>`_
         as a "Cheat tool".

      .. grid-item-card:: Sensors and their cost
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/sensors.html
         :class-card: sd-border-secondary

         **ARIAC documentation:** Sensors

         The RGB camera ($800 at 1080p, $500 at 720p) and the sensor budget.

      .. grid-item-card:: The Dockerfile
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/submission.html
         :class-card: sd-border-secondary

         **ARIAC documentation:** Submission

         What the Dockerfile in the repository root must do, including
         ``TEAM_CONFIG`` and ``TEAM_COMMAND``.

      .. grid-item-card:: The run score
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **ARIAC documentation:** Scoring

         The run score, its bonuses and penalties.

         +++

         The over-budget penalty is computed in
         `scoring.py <https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/ariac_db/scoring.py>`_.


.. dropdown:: Agentic Manufacturing in Industry
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: An LLM reassigns tasks after a robot fails
         :link: https://arxiv.org/abs/2505.22804
         :class-card: sd-border-secondary

         **Lim and Kovalenko, Penn State, arXiv 2505.22804 (2025)**

         GPT-4o writes a new task assignment when a robot fails; a central
         controller checks it and re-prompts. Two arms, 20 trials.

      .. grid-item-card:: LLM agents run a modular production line
         :link: https://arxiv.org/abs/2409.18009
         :class-card: sd-border-secondary

         **Xia, Jazdi, Zhang, Shah and Weyrich, IEEE ETFA 2025**

         Manager and operator agents send function calls that go straight
         to the automation modules. Table II gives the accuracy on routine
         steps and on unexpected events; human approval is the authors'
         proposal.

      .. grid-item-card:: Amazon DeepFleet
         :link: https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination
         :class-card: sd-border-secondary

         **Amazon Science blog, August 11, 2025**

         A foundation model for multirobot coordination, used first to
         predict congestion; the 10% efficiency figure.


.. dropdown:: Running Against the Real Model
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Gemini API keys
         :link: https://ai.google.dev/gemini-api/docs/api-key
         :class-card: sd-border-secondary

         **Google:** Gemini API docs, "Using Gemini API keys"

         Creating a key in Google AI Studio or the Cloud console, and the
         ``GEMINI_API_KEY`` environment variable.

      .. grid-item-card:: Quickstart
         :link: https://ai.google.dev/gemini-api/docs/quickstart
         :class-card: sd-border-secondary

         **Google:** Gemini API docs, "Getting started"

         ``pip install -U google-genai`` and a first call with
         ``client.interactions.create``.

      .. grid-item-card:: Pricing
         :link: https://ai.google.dev/gemini-api/docs/pricing
         :class-card: sd-border-secondary

         **Google:** Gemini API docs, "Pricing"

         The free and paid tiers of ``gemini-robotics-er-2-preview``, their
         prices, and whether Google uses the content to improve its
         products.

      .. grid-item-card:: Interactions API reference
         :link: https://ai.google.dev/api/interactions-api
         :class-card: sd-border-secondary

         **Google:** Gemini API reference, "Gemini Interactions API"

         The ``response_format`` and ``store`` fields of Run 2, and the
         ``usage`` fields the token counts come from.

      .. grid-item-card:: Structured output
         :link: https://ai.google.dev/gemini-api/docs/structured-output
         :class-card: sd-border-secondary

         **Google:** Gemini API docs, "Structured outputs"

         How ``response_format`` takes a JSON schema, the supported schema
         keywords, and the advice to validate every answer.

      .. grid-item-card:: Interactions overview
         :link: https://ai.google.dev/gemini-api/docs/interactions-overview
         :class-card: sd-border-secondary

         **Google:** Gemini API docs, "Interactions API"

         Storage by default (``store=true``), and how long each tier keeps
         an interaction.
