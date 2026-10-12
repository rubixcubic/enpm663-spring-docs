====================================================
References
====================================================

These are the sources the L5 slides cite or take their facts from, in the
order of the slides, grouped by topic. ARIAC source files are on the
``ariac2025`` branch of `usnistgov/ARIAC <https://github.com/usnistgov/ARIAC/tree/ariac2025>`_.
Every link was checked on 2026-10-12.


.. dropdown:: The ARIAC Sensors and the Budget
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Sensors
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/sensors.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Sensors**

         The four sensor types, their grades and costs, and the three
         bounding boxes a lidar must sit in.

      .. grid-item-card:: Configuration files
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/config_files.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Configuration Files**

         The team configuration file, the example lidar (50 by 8 samples), and
         the note that the training defects will change for the competition.

      .. grid-item-card:: How a lidar is billed
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_setup/ariac_setup/structures.py
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_setup/ariac_setup/structures.py``

         ``Lidar.grade``: grade A only at exactly 20 Hz, otherwise by samples
         alone; exactly 200 samples is grade B; more than 400 is refused.

      .. grid-item-card:: Cell spawn point and height
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/include/ariac_plugins/cell_feed_plugin.hpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/include/ariac_plugins/cell_feed_plugin.hpp``

         A cell spawns at :math:`x` = 0.55 m, :math:`z` = 0.422 m: the belt
         surface.

      .. grid-item-card:: The inspection door
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/include/ariac_plugins/physical_inspection_plugin.hpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/include/ariac_plugins/physical_inspection_plugin.hpp``

         Where the door opens (:math:`x` = 1.0 m) and closes (after 1.25 m).

      .. grid-item-card:: The lidar's range
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/sensors/lidar/model.sdf
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/models/sensors/lidar/model.sdf``

         Range 0.04 to 0.2 m, and no noise element.

      .. grid-item-card:: Scenario
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scenario**

         Step 1a (inspection with lidar point clouds, the three defect types
         and the 2 mm statement), Step 1c (voltage), Step 1e (kit check) and
         Step 2c (the Task 2 top shell).

      .. grid-item-card:: Scoring weights
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/config/scoring_weights.yaml``

         The $9600 sensor budget, the 4 s nominal inspection time, and the
         50-point penalty ``GOOD_CELL_IN_INSPECTION_BIN``.

      .. grid-item-card:: Scoring code
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/ariac_db/scoring.py
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/ariac_db/scoring.py``

         The sensor cost bonus and the over-budget penalty.


.. dropdown:: Point Clouds in ROS 2
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The lidar's topic and frame
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/ray_sensor_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/ray_sensor_plugin.cpp``

         ``PointCloud2`` on ``/{lidar_name}/scan`` with frame
         ``{lidar_name}_frame``, and its QoS.

      .. grid-item-card:: PointCloud2
         :link: https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/PointCloud2.html
         :class-card: sd-border-secondary

         **ROS 2 Jazzy: sensor_msgs/msg/PointCloud2**

         The message fields: header, height, width, fields, point_step,
         row_step and data.

      .. grid-item-card:: The point_cloud2 helpers
         :link: https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs_py/sensor_msgs_py/point_cloud2.py
         :class-card: sd-border-secondary

         **sensor_msgs_py source:** ``point_cloud2.py`` (branch ``jazzy``)

         ``create_cloud_xyz32`` and ``read_points_numpy``, used in
         ``pc2_roundtrip.py``.

      .. grid-item-card:: TF2 tutorials
         :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html
         :class-card: sd-border-secondary

         **ROS 2 Jazzy documentation: TF2**

         Static transforms and ``lookup_transform``, for a refresher before
         writing the transform code.


.. dropdown:: Lidar Geometry
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The cell's size
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/battery_cell/model.sdf
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/models/battery_cell/model.sdf``

         The collision cylinder: radius 10.5 mm, length 70 mm.

      .. grid-item-card:: The cell's spawn rotation
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/cell_feed_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/cell_feed_plugin.cpp``

         Each cell spawns turned by a random angle from :math:`-\pi` to
         :math:`\pi`.


.. dropdown:: From Points to Defects
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: A defect's location
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellDefect.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellDefect.msg``

         ``defect_type`` (DENT = 1, BULGE = 2, SCRATCH = 3), ``theta`` and
         ``z`` relative to the cell base.

      .. grid-item-card:: The training defects
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_setup/config/defects.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_setup/config/defects.yaml``

         The ten defect types, each with its mesh file and the type,
         :math:`\theta` and :math:`z` of each defect. Read by
         ``mesh_depths.py``.

      .. grid-item-card:: The cell mesh
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/battery_cell/meshes/li-ion/base.glb
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/models/battery_cell/meshes/li-ion/base.glb``

         The good cell's mesh; its top narrows above about 68 mm, which is why
         the demo crops at 66 mm. The defect meshes are in the same folder.


.. dropdown:: The Inspection Report and the Door
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The report
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/InspectionReport.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/InspectionReport.msg``

         ``bool passed`` and a list of ``CellDefect``.

      .. grid-item-card:: The submit service
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/srv/SubmitInspectionReport.srv
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/srv/SubmitInspectionReport.srv``

         The request holds a timestamp and the report.

      .. grid-item-card:: Matching a report to a cell
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/physical_inspection_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/physical_inspection_plugin.cpp``

         Which cell a report lands on, the door, and the :math:`\theta` check
         with ``abs()`` applied to the comparison.

      .. grid-item-card:: Scoring
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring**

         The inspection speed and inspection classification bonuses.


.. dropdown:: Voltage Readings
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The reading
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/VoltageReading.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/VoltageReading.msg``

         ``voltage`` and ``operation_status``.

      .. grid-item-card:: The voltage ranges
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellTypes.msg``

         Li-Ion: 3.6 V plus or minus 0.2 V. Ni-MH: 1.2 V nominal.

      .. grid-item-card:: The noise
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/voltage_tester/model.sdf
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/models/voltage_tester/model.sdf``

         ``noise_std_dev`` 0.05 V.

      .. grid-item-card:: What the tester publishes
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/voltage_tester_plugin.cpp``

         0 V plus noise with no cell; −1 and MALFUNCTIONING during a
         malfunction; one reading every 0.1 s of wall-clock time.

      .. grid-item-card:: Challenges
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Challenges**

         The voltage tester malfunction. The page says the tester stops
         publishing; the plugin code keeps publishing.


.. dropdown:: GP2 and Ground Truth
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: log_cell_info
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/launch/ariac.launch.py
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/launch/ariac.launch.py``

         The ``log_cell_info`` launch argument, which logs each cell's
         ground truth. GP2 uses it offline only.

      .. grid-item-card:: ARIAC source
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025
         :class-card: sd-border-secondary

         **usnistgov/ARIAC, branch** ``ariac2025``

         The code to check against when your node depends on how ARIAC
         behaves. ``mesh_depths.py`` reads this repository.
