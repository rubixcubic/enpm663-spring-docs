====================================================
References
====================================================

These are the sources the L9 slides cite, grouped by topic, in the order the
slides first use them. Every link was checked on 2026-10-12. The ARIAC source
links point to the ``ariac2025`` branch of the ARIAC repository. A last
dropdown lists further reading that the exercises use but no slide cites.


.. dropdown:: VLMs: Hosted, Local and Embodied Reasoning
   :class-container: sd-border-secondary
   :open:

   The three families of VLM on the "What a VLM Is" slide, and the vision
   pages that show each provider's request format (step 3 of "From an Image
   Topic to a Request").

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Claude vision
         :link: https://platform.claude.com/docs/en/build-with-claude/vision
         :class-card: sd-border-secondary

         **Anthropic: Vision**

         How to send images to Claude in a request, and how images count as
         input tokens.

      .. grid-item-card:: OpenAI vision
         :link: https://developers.openai.com/api/docs/guides/images-vision
         :class-card: sd-border-secondary

         **OpenAI: Images and vision**

         How to send images to GPT models in a request.

      .. grid-item-card:: Gemini image understanding
         :link: https://ai.google.dev/gemini-api/docs/image-understanding
         :class-card: sd-border-secondary

         **Google: Image understanding with the Gemini API**

         How to send images to Gemini models in a request.

      .. grid-item-card:: Gemini models list
         :link: https://ai.google.dev/gemini-api/docs/models
         :class-card: sd-border-secondary

         **Google: Gemini models**

         The model list that showed ``gemini-robotics-er-2-preview``, a
         preview model, on 2026-10-12.

      .. grid-item-card:: Gemini Robotics ER
         :link: https://ai.google.dev/gemini-api/docs/robotics-overview
         :class-card: sd-border-secondary

         **Google: Gemini Robotics ER overview**

         The embodied-reasoning model: pointing at a part, drawing a box
         around it. The final demo uses one model of this kind.

      .. grid-item-card:: Gemini Robotics
         :link: https://deepmind.google/models/gemini-robotics/
         :class-card: sd-border-secondary

         **Google DeepMind: Gemini Robotics**

         The model family that Gemini Robotics ER belongs to. L13 places it
         in the physical AI landscape.

      .. grid-item-card:: Qwen-VL on Ollama
         :link: https://ollama.com/library/qwen2.5vl
         :class-card: sd-border-secondary

         **Ollama library: qwen2.5vl**

         The local open-weight VLM behind ``ollama pull qwen2.5vl`` on the
         slide and on the :doc:`AI Access </ariac/ai_setup>` page.

      .. grid-item-card:: LLaVA on Ollama
         :link: https://ollama.com/library/llava
         :class-card: sd-border-secondary

         **Ollama library: llava**

         The other local open-weight VLM the slide names.


.. dropdown:: ARIAC 2025 Documentation
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Sensors page
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/sensors.html
         :class-card: sd-border-secondary

         **ARIAC: Sensors**

         Camera prices ($800 for 1080p, $500 for 720p) and where lidar may
         be placed.

      .. grid-item-card:: Challenges page
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **ARIAC: Challenges**

         The four challenges, their trial-file keys (``START_TIME``,
         ``DURATION``, ``TESTER``, ``ID``) and the expected handling,
         including the high-priority order steps. The slides note two places
         where the 2025 source behaves differently.

      .. grid-item-card:: Scoring page
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **ARIAC: Scoring**

         The trial time bonus, the high-priority speed bonus and the sensor
         cost bonus. It says the targets can change. L12 works the formulas.

      .. grid-item-card:: Configuration page
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/config_files.html
         :class-card: sd-border-secondary

         **ARIAC: Configuration files**

         The trial file (``SEED``, ``DEFECT_RATE``, ``CHALLENGES``) and the
         team file (``SENSORS``, ``CONVEYOR_SPEED``, ``CELL_FEED_RATE``), with
         an example of every challenge. GP4 sets its test cases here.


.. dropdown:: ARIAC 2025 Source: Messages and Plugins
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: scoring_weights.yaml
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         ``SENSOR_BUDGET: 9600`` and
         ``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION: 150``.

      .. grid-item-card:: CellTypes.msg
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         ``LI_ION`` and ``NIMH``, nominal voltages 3.6 V and 1.2 V, cell
         tolerance 0.2 V, kit tolerance 0.15 V.

      .. grid-item-card:: CellDefect.msg
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellDefect.msg
         :class-card: sd-border-secondary

         ``DENT``, ``BULGE`` and ``SCRATCH``, and no value for "no defect".

      .. grid-item-card:: AgvTrayStatus.msg
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/AgvTrayStatus.msg
         :class-card: sd-border-secondary

         Four booleans, ``slot_1_occupied`` to ``slot_4_occupied``, and no
         cell type.

      .. grid-item-card:: cell_feed_plugin.hpp
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/include/ariac_plugins/cell_feed_plugin.hpp
         :class-card: sd-border-secondary

         ``voltage_std_dev = 0.1``: the 0.1 V spread of cell voltages.

      .. grid-item-card:: linear_conveyor_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/linear_conveyor_plugin.cpp
         :class-card: sd-border-secondary

         The conveyor malfunction: it stops the belt.

      .. grid-item-card:: cell_feed_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/cell_feed_plugin.cpp
         :class-card: sd-border-secondary

         The cell feed, which has no malfunction check.

      .. grid-item-card:: voltage_tester_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         Publishes every 0.1 s; voltage -1 and ``MALFUNCTIONING`` during a
         malfunction; 0 V plus noise with no cell.

      .. grid-item-card:: OperationStates.msg
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/OperationStates.msg
         :class-card: sd-border-secondary

         ``OPERATIONAL = 1`` and ``MALFUNCTIONING = 2``.


.. dropdown:: Software Used by the Demonstrations
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: cv_bridge
         :link: https://github.com/ros-perception/vision_opencv/tree/rolling/cv_bridge
         :class-card: sd-border-secondary

         **ros-perception/vision_opencv: cv_bridge**

         ``CvBridge.imgmsg_to_cv2`` converts a ROS image message to an
         OpenCV image (step 2 of "From an Image Topic to a Request").

      .. grid-item-card:: jsonschema for Python
         :link: https://python-jsonschema.readthedocs.io/en/stable/
         :class-card: sd-border-secondary

         **python-jsonschema**

         The ``Draft7Validator`` both scripts use to check replies against a
         schema. The outputs were made with version 4.10.3.


.. dropdown:: Further Reading
   :class-container: sd-border-secondary

   Not cited on a slide; used by the exercises.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ARIAC ROS API
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **ARIAC: API**

         Every ARIAC topic, service and action, including the cell feed
         control service, ``/{agv_name}/move`` and ``/{agv_name}/info``
         (Exercise 5).

      .. grid-item-card:: JSON Schema
         :link: https://json-schema.org/
         :class-card: sd-border-secondary

         **JSON Schema**

         The specification behind the schemas, enums and ``minimum`` checks
         of the lecture.
