====================================================
AI Access (LLMs and VLMs)
====================================================

From L8, and for GP4 and the final demo, you need access to a large language
model (LLM) and a vision-language model (VLM). You may use either a hosted API
or local open-weight models. Group projects accept either; cost guidance is
provided per project.

.. note::

   Never commit API keys to your repository. Store them in environment
   variables or a local ``.env`` file that is listed in ``.gitignore``.


Option A: Hosted APIs
---------------------

Create an account and an API key with one provider, then install its Python
SDK:

.. code-block:: bash

   pip install anthropic        # Anthropic Claude
   pip install openai           # OpenAI
   pip install google-genai     # Google Gemini

Export your key in your shell configuration file (example for Anthropic):

.. code-block:: bash

   echo 'export ANTHROPIC_API_KEY="sk-..."' >> ~/.bashrc
   source ~/.bashrc

All three providers support **structured output** (JSON-schema-constrained
responses), **tool / function calling**, and multimodal (VLM) input, which are
the mechanisms used in L8 and L9.


Option B: Local Open-Weight Models
----------------------------------

Local models avoid per-token cost and keep data on your machine, at the price
of hardware requirements. `Ollama <https://ollama.com/>`_ is the simplest
runner:

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

Tool and context integration in L8 uses the
`Model Context Protocol <https://modelcontextprotocol.io/>`_ (MCP), the
standard way, since 2024, to expose tools to an LLM across the major agent
frameworks. No special install is needed to start; the SDK is introduced in
L8 and used in GP4.


Embodied-Reasoning Model (Final Demo)
-------------------------------------

The final demo uses a hosted embodied-reasoning model for one perception
step, for example Google's Gemini Robotics ER through the Gemini API. These
models answer spatial questions about an image (where a part is, which
cell looks damaged) and are part of what the industry calls physical AI.
Access and cost details are posted with the final demo specification.
