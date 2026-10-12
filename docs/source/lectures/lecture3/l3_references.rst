====================================================
References
====================================================

These are the sources the L3 slides cite or take their facts from, in the
order of the slides, grouped by topic. Every link was checked on 2026-10-12.


.. dropdown:: Frames
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Frames
         :link: https://www.mit.edu/~dxh/marvin/web.media.mit.edu/~minsky/papers/Frames/frames.html
         :class-card: sd-border-secondary

         **Minsky, M. (1974)**

         "A Framework for Representing Knowledge." MIT AI Laboratory Memo
         306, June 1974.

         The source of the frame definition: slots (Minsky's terminals),
         fillers and default assignments.

      .. grid-item-card:: The message definitions behind the frames
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025/ariac_interfaces/msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg`` (branch ``ariac2025``)

         ``CellTypes.msg`` (types, nominal voltages, tolerances),
         ``CellDefect.msg`` (defect type, θ and z), ``AgvStations.msg``,
         ``AgvTrayStatus.msg`` and ``HighPriorityOrder.msg``: the slots of
         the cell, AGV and order frames.

         +++

         Read them before you name your blackboard keys.


.. dropdown:: Ontologies
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Ontologies for robotics
         :link: https://standards.ieee.org/ieee/1872/5354/
         :class-card: sd-border-secondary

         **IEEE 1872-2015**

         *IEEE Standard Ontologies for Robotics and Automation.* IEEE, 2015.

         Defines the core ontology CORA. Inactive (reserved) since
         2026-03-26; IEEE is drafting a revision, P1872.

      .. grid-item-card:: A language for ontologies
         :link: https://www.w3.org/OWL/
         :class-card: sd-border-secondary

         **W3C Web Ontology Language (OWL)**

         The W3C standard language for writing ontologies. The course does
         not require it.


.. dropdown:: A World Model at Each Layer
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: 4D/RCS
         :link: https://doi.org/10.6028/NIST.IR.6910
         :class-card: sd-border-secondary

         **Albus, J., et al. (2002)**

         *4D/RCS: A Reference Model Architecture for Unmanned Vehicle
         Systems, Version 2.0.* NISTIR 6910, NIST.

         The two ideas the course uses, quoted from page 31 and page 55
         (a world model at each layer, at the detail that layer needs) and
         page 19 and page 45 (errors handled where they are seen, status
         passed up), and the eight levels of Table 1 (page 55).


.. dropdown:: One Kit, Three Views
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: JSON Schema
         :link: https://json-schema.org/draft-07
         :class-card: sd-border-secondary

         **JSON Schema, Draft 7**

         The version ``kit_views.py`` checks against
         (``Draft7Validator``). The site's
         `guide <https://json-schema.org/understanding-json-schema>`_
         explains each keyword the schema uses.

      .. grid-item-card:: The validator
         :link: https://python-jsonschema.readthedocs.io/en/v4.10.3/
         :class-card: sd-border-secondary

         **jsonschema 4.10.3** (Python package)

         The package and version that produced the outputs in the notes.

      .. grid-item-card:: The kit voltage window
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scenario**

         Step 1d gives the kit tolerance, the total within 4 × the nominal
         cell voltage plus or minus 0.15 V, used in the fourth-cell example.


.. dropdown:: What the GP1 Tree Must Know
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The ARIAC interfaces
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: ROS API**

         The topics and services your system reads: the source of every
         observed fact in Task 1.

      .. grid-item-card:: ARIAC source
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025
         :class-card: sd-border-secondary

         **usnistgov/ARIAC, branch** ``ariac2025``

         The code to check against when you design your world model, for
         example which models ARIAC publishes TF frames for (AGVs and their
         tray slots do; the lecture says individual cells and shells do
         not).
