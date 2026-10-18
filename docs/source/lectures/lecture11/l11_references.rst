====================================================
References
====================================================

These are the sources the L11 slides cite, grouped by topic, in the order the
slides first use them. Every link was checked on 2026-10-12. The ARIAC source
links point to commit 0c3e722 of the ARIAC repository, the commit the slides
quote line numbers from. A last dropdown lists further reading that the
exercises use but no slide cites.


.. dropdown:: The Final Demo Specification
   :class-container: sd-border-secondary
   :open:

   The sources behind "What Your System Must Do" and the run-time
   arithmetic on "What Is Set".

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Gemini Robotics ER
         :link: https://ai.google.dev/gemini-api/docs/robotics-overview
         :class-card: sd-border-secondary

         **Google: Gemini Robotics ER overview**

         The example of a hosted embodied-reasoning model. The final demo
         page says which other models your team may use. The course key runs
         the graded runs only; your team uses its own free-tier key while
         you develop.

      .. grid-item-card:: ARIAC configuration files
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/config_files.html
         :class-card: sd-border-secondary

         **ARIAC 2025 docs: Configuration Files**

         The example trial file (``TIME_LIMIT`` 900, the malfunction start
         times and durations) and the example team file
         (``CELL_FEED_RATE`` 0.1, one cell every ten seconds).

      .. grid-item-card:: ARIAC submission
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/submission.html
         :class-card: sd-border-secondary

         **ARIAC 2025 docs: Submission**

         How ARIAC itself evaluates teams: a Dockerfile at the repository
         root and a tag created before the deadline. The final demo runs the
         same way.


.. dropdown:: Behavior Tree Recovery: py_trees 2.6.0
   :class-container: sd-border-secondary
   :open:

   The classes on "The Building Blocks" and the Retry behavior on "What Retry
   Does on Each Tick". The slides read the signatures and the source from
   the ``py_trees`` 2.6.0 installed with ROS 2 Jazzy.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Composites
         :link: https://py-trees.readthedocs.io/en/devel/composites.html
         :class-card: sd-border-secondary

         **py_trees: Composites**

         ``Selector`` (with and without memory), ``Sequence`` and
         ``Parallel``.

      .. grid-item-card:: Decorators
         :link: https://py-trees.readthedocs.io/en/devel/decorators.html
         :class-card: sd-border-secondary

         **py_trees: Decorators**

         ``Retry``, ``Timeout`` and ``EternalGuard``.

      .. grid-item-card:: Module reference
         :link: https://py-trees.readthedocs.io/en/devel/modules.html
         :class-card: sd-border-secondary

         **py_trees: Module API**

         Every class with its arguments, including
         ``py_trees.timers.Timer``, the wait for a backoff.

      .. grid-item-card:: Retry source
         :link: https://github.com/splintered-reality/py_trees/blob/release/2.6.x/py_trees/decorators.py
         :class-card: sd-border-secondary

         **py_trees release 2.6.x: decorators.py**

         ``Retry.update()``: ``RUNNING`` before the n-th failure,
         ``FAILURE`` on it, and the feedback messages the demonstration
         prints.


.. dropdown:: Checking LLM Output: the L8 Checks and the Course Skills
   :class-container: sd-border-secondary
   :open:

   Check 2 of L8's ``check_call()`` (``Draft202012Validator`` in
   ``lecture8/code/orchestrator.py``), and the skill rules behind the failure
   results table and Runs C and D.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: jsonschema
         :link: https://python-jsonschema.readthedocs.io/en/stable/validate/
         :class-card: sd-border-secondary

         **python-jsonschema documentation: Schema Validation**

         The Python package the demonstration ran with (4.10.3):
         ``Draft202012Validator`` and ``iter_errors()``, as in L8.

      .. grid-item-card:: Course Skills Package
         :link: /ariac/skills
         :link-type: doc
         :class-card: sd-border-secondary

         **The course skills package page**

         The result codes in ``SkillResult.msg``, "One goal per arm" and
         "Cancel stops the arm", from the README of v0.2.0, the version
         you get.


.. dropdown:: ARIAC 2025 Documentation
   :class-container: sd-border-secondary
   :open:

   The topics and services the lecture names, the voltage averaging step,
   the kit check, and the challenge descriptions.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ARIAC ROS API
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **ARIAC 2025 docs: ROS API**

         ``/high_priority_orders``, ``/inspection_conveyor/status``,
         ``/inspection_conveyor/cell_feed/control``, ``/agvN/tray_status``,
         ``/agvN/check_kit_quality``, ``/vacuum_tool/vg_2/grasp`` and
         ``/submit_high_priority_order``.

      .. grid-item-card:: ARIAC scenario
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **ARIAC 2025 docs: Scenario**

         Step 1c (average the noisy tester readings), the kit quality check
         before you move the AGV, and the rejected kit that must go to the
         recycling station.

      .. grid-item-card:: ARIAC challenges
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **ARIAC 2025 docs: Challenges**

         The four challenges. Its voltage tester text ("will stop publishing
         data") and conveyor text (the cell feed pauses) differ from the
         code, as the lecture shows.


.. dropdown:: ARIAC 2025 Source (Commit 0c3e722)
   :class-container: sd-border-secondary
   :open:

   What the simulator does, as opposed to what the docs say. The slides
   quote line numbers from these files at this commit.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: voltage_tester_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         **The voltage tester plugin**

         The 0.1 s publish timer (line 88), voltage -1 with
         ``MALFUNCTIONING`` (lines 126 and 127), and the empty tester's
         noise around 0 V with ``OPERATIONAL`` (line 144).

      .. grid-item-card:: Voltage tester model.sdf
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_gz/models/voltage_tester/model.sdf
         :class-card: sd-border-secondary

         **The voltage tester model**

         ``noise_std_dev`` 0.05, the standard deviation of the synthetic
         readings.

      .. grid-item-card:: CellTypes.msg
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **Cell types and tolerances**

         Nominal voltages (Li-Ion 3.6 V, NiMH 1.2 V), the cell tolerance
         (0.2 V) and the kit tolerance (0.15 V).

      .. grid-item-card:: OperationStates.msg
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_interfaces/msg/OperationStates.msg
         :class-card: sd-border-secondary

         **Operation states**

         The ``OPERATIONAL`` and ``MALFUNCTIONING`` values that
         ``tester_watcher.py`` copies.

      .. grid-item-card:: linear_conveyor_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/linear_conveyor_plugin.cpp
         :class-card: sd-border-secondary

         **The inspection conveyor plugin**

         Sets the speed to 0 and the status to ``MALFUNCTIONING`` during a
         conveyor malfunction.

      .. grid-item-card:: cell_feed_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/cell_feed_plugin.cpp
         :class-card: sd-border-secondary

         **The cell feed plugin**

         Spawns a cell every 1 / feed rate seconds, with no malfunction
         check.

      .. grid-item-card:: vacuum_tool_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/vacuum_tool_plugin.cpp
         :class-card: sd-border-secondary

         **The vacuum tool plugin**

         The "Vacuum gripper is malfunctioning" response, and the malfunction
         that clears only after every suction pad has lost contact.

      .. grid-item-card:: scoring_weights.yaml
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **Scoring weights**

         ``GOOD_CELL_IN_INSPECTION_BIN``: 50 points for each good cell in
         the inspection bin.


.. dropdown:: Local or Global Recovery: 4D/RCS
   :class-container: sd-border-secondary
   :open:

   The order of recovery on "The Rule for Choosing", first quoted in L3.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: NISTIR 6910
         :link: https://doi.org/10.6028/NIST.IR.6910
         :class-card: sd-border-secondary

         **Albus et al., 4D/RCS: A Reference Model Architecture for Unmanned
         Vehicle Systems, Version 2.0 (NIST, 2002)**

         Commands flow down and status feedback flows up (p. 19, Figure 1);
         an executor that senses an error may modify the commanded action to
         cope with it (p. 45).


.. dropdown:: Further Reading (Used by the Exercises)
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: py_trees TickCounter
         :link: https://py-trees.readthedocs.io/en/devel/modules.html#py_trees.behaviours.TickCounter
         :class-card: sd-border-secondary

         **py_trees: behaviours.TickCounter**

         The tick-based wait in Exercise 3. The same page documents
         ``behaviours.Running``, the ``hold_cell`` last resort.

