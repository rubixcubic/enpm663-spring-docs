====================================================
AI Access (LLMs and VLMs)
====================================================

Starting in Week 9 and for PT4 and PT5, you need access to a large language
model (LLM) and a vision-language model (VLM). You may use either a hosted API
or local open-weight models. Team projects accept either; cost guidance is
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
the mechanisms used in Weeks 9 and 10.


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

Smaller VLMs such as Qwen-VL and LLaVA are chosen so they fit on typical
student GPUs.


Model Context Protocol (MCP)
----------------------------

Tool and context integration in Week 9 uses the
`Model Context Protocol <https://modelcontextprotocol.io/>`_, the 2024-onward
standard supported across the major agent frameworks. No special install is
needed to start; the relevant SDK is introduced with the Week 9 exercise.
