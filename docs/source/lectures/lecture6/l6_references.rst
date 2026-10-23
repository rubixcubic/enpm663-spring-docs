====================================================
References
====================================================

These are the sources the L6 slides cite or take their facts from, in the
order of the slides, grouped by section. The slide deck has no bibliography:
the sources below are the paper, the documentation pages, the ARIAC source
files and the packages that the slides name. Every link was checked on
2026-10-12.


.. dropdown:: Classical Planning
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Where the model comes from
         :link: https://doi.org/10.1016/0004-3702(71)90010-5
         :class-card: sd-border-secondary

         **R. E. Fikes and N. J. Nilsson, STRIPS: A New Approach to the
         Application of Theorem Proving to Problem Solving**

         *Artificial Intelligence* 2(3 to 4):189 to 208, 1971. States as
         sets of facts, and actions with preconditions and effects: the
         model that you write in two PDDL files.

      .. grid-item-card:: The four challenges
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Challenges**

         The conveyor malfunction, the voltage tester malfunction, the vacuum
         tool malfunction and the high-priority order: where the factory
         breaks the deterministic and static-world assumptions.

      .. grid-item-card:: A malfunctioning tester in code
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/voltage_tester_plugin.cpp``

         During a malfunction the tester publishes a voltage of −1 with the
         status ``MALFUNCTIONING``.


.. dropdown:: A PDDL Domain for Task 1
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Task 1, Steps 1b to 1e
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scenario**

         Which robot does each step, the check kit quality call before the
         AGV moves, "Cells lock to the tray after they are placed", the
         recycling station for a rejected kit, and the cell and kit voltage
         tolerances.

      .. grid-item-card:: Types as frame classes
         :link: /lectures/lecture3/l3_index
         :link-type: doc
         :class-card: sd-border-secondary

         **L3: frames, relations and instances**

         The frame classes whose role PDDL types play in the domain header.

      .. grid-item-card:: Four slots per tray
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/AgvTrayStatus.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/AgvTrayStatus.msg``

         ``slot_1_occupied`` to ``slot_4_occupied``: why ``s1`` to ``s4``
         are domain constants, and where ``slot-free`` comes from.

      .. grid-item-card:: Four AGV stations
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/AgvStations.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/AgvStations.msg``

         ``INSPECTION``, ``ASSEMBLY``, ``SHIPPING`` and ``RECYCLING``; the
         L6 domain uses two of them.

      .. grid-item-card:: The ARIAC calls behind the actions
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: ROS API**

         ``/{agv_name}/check_kit_quality``, the ``/{agv_name}/move`` action,
         and ``/submit_kitting_order`` ("AGV at shipping required").

      .. grid-item-card:: The AGV move rejects a cancel
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/agv_motion_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/agv_motion_plugin.cpp``

         The move action's cancel callback returns
         ``CancelResponse::REJECT``.


.. dropdown:: A PDDL Problem
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Where the AGV is
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/AgvStatus.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/AgvStatus.msg``

         The ``station_id`` published on ``/{agv_name}/info``, the source of
         ``agv-at``.

      .. grid-item-card:: The topics a generator reads
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: ROS API**

         ``/{agv_name}/info``, ``/{agv_name}/tray_status``, and
         ``/voltage_tester_1/voltage`` and ``/voltage_tester_2/voltage``.


.. dropdown:: Running a Planner
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Installing UPF
         :link: https://unified-planning.readthedocs.io/en/latest/getting_started/installation.html
         :class-card: sd-border-secondary

         **Unified Planning Framework: Installation**

         Lists Python 3.8, 3.9, 3.10 and 3.11; the L6 demos ran on Python
         3.12.3.

      .. grid-item-card:: The Fast Downward engine for UPF
         :link: https://github.com/aiplan4eu/up-fast-downward
         :class-card: sd-border-secondary

         **aiplan4eu/up-fast-downward**

         The package that brings a built Fast Downward into UPF. Its README
         recommends ``pip install unified-planning[fast-downward]``, which
         installed version 0.5.2; the notes install ``up-fast-downward``
         directly (1.0.0).

      .. grid-item-card:: The planner
         :link: https://www.fast-downward.org/
         :class-card: sd-border-secondary

         **Fast Downward**

         The classical planner used in L6 and GP3 (version 26.6 in the
         notes).

      .. grid-item-card:: Translate, then search
         :link: https://www.fast-downward.org/latest/documentation/planner-usage/
         :class-card: sd-border-secondary

         **Fast Downward: Planner Usage**

         The translator and the search, ``--search "astar(lmcut())"`` and
         the ``--alias`` option (``lama-first``).

      .. grid-item-card:: The LM-cut heuristic
         :link: https://www.fast-downward.org/latest/documentation/search/Evaluator/
         :class-card: sd-border-secondary

         **Fast Downward: Evaluator**

         The heuristics, ``lmcut`` among them, and which ones are
         admissible.

      .. grid-item-card:: Planning and validating from Python
         :link: https://unified-planning.readthedocs.io/en/latest/operation_modes.html
         :class-card: sd-border-secondary

         **Unified Planning Framework: Operation Modes**

         ``OneshotPlanner``, used to solve the problems, and
         ``PlanValidator``, used to check the plans.


.. dropdown:: Checking a Plan
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The stand-alone validator
         :link: https://github.com/KCL-Planning/VAL
         :class-card: sd-border-secondary

         **KCL-Planning/VAL**

         "Tools for AI Planning plans and planning models": the standard
         validator for PDDL plans.

      .. grid-item-card:: The validator used in L6
         :link: https://unified-planning.readthedocs.io/en/latest/operation_modes.html
         :class-card: sd-border-secondary

         **Unified Planning Framework: Operation Modes**

         ``PlanValidator``, which reported ``INAPPLICABLE_ACTION`` and the
         unmet precondition for the plan with two steps swapped.


.. dropdown:: Limits of PDDL
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The voltage limits
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellTypes.msg``

         ``LI_ION_NOMINAL_VOLTAGE`` 3.6, ``CELL_VOLTAGE_TOLERANCE`` 0.2 and
         ``KIT_VOLTAGE_TOLERANCE`` 0.15: the limits in ``select_cells.py``.

      .. grid-item-card:: The kit rule
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scenario**

         A completed kit's total must be within 4 times the cell voltage,
         plus or minus 0.15 V; a rejected kit goes to the recycling station.

      .. grid-item-card:: What Fast Downward supports
         :link: https://www.fast-downward.org/latest/documentation/pddl-support/
         :class-card: sd-border-secondary

         **Fast Downward: PDDL Support**

         Fast Downward "aims to support PDDL 2.2 level 1 plus the
         :action-costs requirement from PDDL 3.1"; "All aspects of numerical
         planning" are listed as not supported, except the numeric features
         of :action-costs.

      .. grid-item-card:: What the translator keeps
         :link: https://www.fast-downward.org/latest/for-developers/problem-transformations/
         :class-card: sd-border-secondary

         **Fast Downward: Problem transformations performed by the planner**

         "The translator can prune facts and actions that are not relaxed
         reachable from the initial state or that are not relevant to the
         goal in the sense that they never contribute to an irreducible
         plan."

      .. grid-item-card:: A numeric planner
         :link: https://unified-planning.readthedocs.io/en/latest/engines/01_available_engines.html
         :class-card: sd-border-secondary

         **Unified Planning Framework: Available Engines**

         The engines UPF can call, ENHSP among them, which handles numeric
         planning. The course does not use it.


.. dropdown:: PDDL in GP3
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Running the plan
         :link: /lectures/lecture7/l7_index
         :link-type: doc
         :class-card: sd-border-secondary

         **L7: Plan Execution Patterns with Behavior Trees**

         The plan-to-BT factory that turns each step of an L6 plan into one
         behavior tree subtree.
