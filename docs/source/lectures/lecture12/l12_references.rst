====================================================
References
====================================================

These are the sources the L12 slides cite or take their facts from, in the
order of the slides, grouped by topic. The ARIAC source files are linked at
commit 0c3e722 of the ``ariac2025`` branch, the commit the lecture read
(still the head of the branch on 2026-10-12). Every link was checked on
2026-10-12.


.. dropdown:: Measuring a System
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ARIAC documentation
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation**

         The home page says the competition's results guide "standards
         efforts in robot agility", the quote on the slide "Claims and
         Measurements".


.. dropdown:: Plan-Level Metrics
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Plan validation
         :link: https://unified-planning.readthedocs.io/en/latest/operation_modes.html
         :class-card: sd-border-secondary

         **Unified Planning Framework: Operation Modes**

         Defines plan validation: deciding, given a planning problem and a
         plan, whether the plan is a valid solution. The ``PlanValidator``
         of the "Checking Validity" part comes from this framework (L6).


.. dropdown:: Perception Metrics
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Penalties and weights
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/config/scoring_weights.yaml``

         The 50-point ``GOOD_CELL_IN_INSPECTION_BIN`` penalty, the price of a
         false positive. The same file gives every weight of the scoring
         section.

      .. grid-item-card:: Kit acceptance
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring**

         An accepted kit needs four good cells, so a kit with a defective
         cell is refused at shipping.

      .. grid-item-card:: Check kit quality
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/agv_tray_interface_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/agv_tray_interface_plugin.cpp``

         The check kit quality service, which :doc:`GP1 </assignments/gp1>`
         requires before the AGV moves, reports "Cell in slot N is defective"
         at the AGV inspection station (line 423). With it, a false negative
         costs a recycled tray and the rebuild time, and the kit only if the
         rebuild misses the time limit.

      .. grid-item-card:: ARIAC's classification check
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/physical_inspection_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/physical_inspection_plugin.cpp``

         Checks each inspection report: the number of defects, and each
         defect's type and height against thresholds. The angle test (line
         387) is one-sided. It also measures a cell's report time from the
         moment the cell is created.

      .. grid-item-card:: Ground truth for cells
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/cheat_tools_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/cheat_tools_plugin.cpp``

         With ``log_cell_info:=true``, prints each spawned cell's type,
         voltage, rotation, defective flag and defects to the Gazebo log. The
         launch argument is read in
         `ariac_gz/launch/ariac.launch.py <https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_gz/launch/ariac.launch.py>`_.

      .. grid-item-card:: Defect shapes
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_setup/config/defects.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_setup/config/defects.yaml``

         Holds only the shape of each defect type (type, angle, height), not
         which cells are defective.


.. dropdown:: How Many Runs
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Five runs, best two averaged
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring** (Execution Score)

         Teams complete five runs per trial; the two best run scores of each
         trial are averaged, and the trial averages are summed.


.. dropdown:: The ARIAC 2025 Scoring Formula
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The scoring page
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring**

         The run score, the base score, the five bonuses and the penalties,
         with the note that the weights may change and live in
         ``scoring_weights.yaml``.

      .. grid-item-card:: The scorer
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_db/ariac_db/scoring.py
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/ariac_db/scoring.py``

         ``score_bonuses`` (every bonus set to 0 when an order is missing, and which bonuses are clamped),
         ``score_penalties`` (the over-budget penalty) and
         ``get_run_score_table`` (the table printed at the end of a run).
         ``score_calculator.py`` follows it.

      .. grid-item-card:: The aborted flag
         :link: https://github.com/usnistgov/ARIAC/blob/0c3e722/ariac_plugins/src/competition_manager_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/competition_manager_plugin.cpp``

         Sets ``run.aborted = !orders_complete()``, which makes
         ``score_bonuses`` set every bonus to 0.


.. dropdown:: Worked Example: Two Runs
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Sensor prices
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/sensors.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Sensors**

         The prices used in the worked example and the exercises: lidar
         grade B $1250 (grade A $1500), break beam grade A $400, 1080p
         camera $800 (720p $500), distance sensor grade A $600 (grade B
         $300).

      .. grid-item-card:: The 900 s time limit
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/config_files.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Configuration Files**

         The example trial configuration file, with ``TIME_LIMIT: 900``,
         ``NUM_KITS: 3`` and ``NUM_MODULES: 2``.

      .. grid-item-card:: ARIAC repository
         :link: https://github.com/usnistgov/ARIAC
         :class-card: sd-border-secondary

         **usnistgov/ARIAC on GitHub**

         The source of every file above. Use the ``ariac2025`` branch.
