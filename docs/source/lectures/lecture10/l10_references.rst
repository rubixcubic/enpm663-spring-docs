====================================================
References
====================================================

These are the sources the L10 slides cite, grouped by topic, in the order the
slides first use them. Every link was checked on 2026-10-12. The ARIAC source
links point to the ``ariac2025`` branch of the ARIAC repository.

.. note::

   **MoveIt versions.** The slides use MoveIt 2.12 on ROS 2 Jazzy. The MoveIt
   documentation site has no Jazzy edition (checked 2026-10-12), so the MoveIt
   links below go to its current edition, which is built for ROS 2 Rolling.


.. dropdown:: ARIAC 2025: Robots, Services and Tasks
   :class-container: sd-border-secondary
   :open:

   What ARIAC gives each robot, the five robots, and the Task 2 steps.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ARIAC ROS API
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **ARIAC 2025: ROS API**

         The joint trajectory action, the gripper action, and the tool changer
         and vacuum services of assembly robot 2 ("What ARIAC 2025 Gives Each
         Robot").

      .. grid-item-card:: ARIAC scenario
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **ARIAC 2025: Scenario**

         The five robots and their jobs, the top shell's random pose
         (Step 2c), and the Task 2 motion of the final demo.

      .. grid-item-card:: ARIAC repository
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025
         :class-card: sd-border-secondary

         **usnistgov/ARIAC, branch ariac2025**

         The source behind the slides' ARIAC numbers. The robot description
         files are in ``ariac_description/urdf``.


.. dropdown:: TF2 and Frames
   :class-container: sd-border-secondary
   :open:

   Static and moving transforms, the frames ARIAC publishes, and the axis
   conventions.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: tf_publisher_plugin.cpp
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/tf_publisher_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC: the TF publisher plugin**

         Which frames ARIAC publishes (``<model>_frame``, then
         ``<model>_<child>``), and which go on the moving broadcaster.

      .. grid-item-card:: AGV model
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/agv/model.sdf
         :class-card: sd-border-secondary

         **ARIAC: agv/model.sdf**

         The tray and slot offsets that ``tf_agv_moves.py`` uses.

      .. grid-item-card:: ARIAC world
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/world/ariac.world
         :class-card: sd-border-secondary

         **ARIAC: ariac.world**

         AGV 1's pose at the inspection station.

      .. grid-item-card:: AGV motion plugin
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/include/ariac_plugins/agv_motion_plugin.hpp
         :class-card: sd-border-secondary

         **ARIAC: agv_motion_plugin.hpp**

         The AGV's pose at the assembly station.

      .. grid-item-card:: tf2 tutorial (Jazzy)
         :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html
         :class-card: sd-border-secondary

         **ROS 2 Jazzy: Introducing tf2**

         ``ros2 run tf2_tools view_frames``: "To view the tree, open the
         resulting frames.pdf with your favorite PDF viewer."

      .. grid-item-card:: REP 103
         :link: https://www.ros.org/reps/rep-0103.html
         :class-card: sd-border-secondary

         **ROS REP 103: Standard Units of Measure and Coordinate Conventions**

         x forward, y left, z up; meters and radians; the ``_optical`` frame
         of a camera (z forward, x right, y down).


.. dropdown:: From a Camera Pixel to a Robot Target
   :class-container: sd-border-secondary
   :open:

   The top shell's pose, the camera's topics and intrinsics, and the camera
   frame.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Shell insertion plugin
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/include/ariac_plugins/shell_insertion_plugin.hpp
         :class-card: sd-border-secondary

         **ARIAC: shell_insertion_plugin.hpp**

         The top shell's random offset (up to 0.05 m in x, up to 0.1 m in y,
         any yaw) and the spot it starts from.

      .. grid-item-card:: Image plugin
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/image_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC: image_plugin.cpp**

         The camera's ``image`` and ``info`` topics, stamped in
         ``{camera_name}_frame``.

      .. grid-item-card:: CameraInfo
         :link: https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CameraInfo.html
         :class-card: sd-border-secondary

         **sensor_msgs/CameraInfo (Jazzy)**

         The message that carries :math:`K`, nine numbers row by row in
         ``k``.

      .. grid-item-card:: Image
         :link: https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/Image.html
         :class-card: sd-border-secondary

         **sensor_msgs/Image (Jazzy)**

         The message on ``/{camera_name}/image``.

      .. grid-item-card:: Camera resolutions
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_setup/ariac_setup/structures.py
         :class-card: sd-border-secondary

         **ARIAC: ariac_setup/structures.py**

         720p is 1280 × 720 pixels, 1080p is 1920 × 1080.

      .. grid-item-card:: ARIAC configuration files
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/config_files.html
         :class-card: sd-border-secondary

         **ARIAC 2025: Configuration Files**

         The example configuration: a camera FOV of 1.57 rad, a conveyor
         speed of 0.1 m/s and a feed of 0.1 cells per second.

      .. grid-item-card:: gz-rendering Utils.cc
         :link: https://github.com/gazebosim/gz-rendering/blob/gz-rendering8/src/Utils.cc
         :class-card: sd-border-secondary

         **Gazebo: gz-rendering, src/Utils.cc**

         With gz-sensors below, the intrinsics Gazebo computes when the SDF
         gives no lens values. Both links go to the Gazebo Harmonic branches,
         the Gazebo release paired with ROS 2 Jazzy.

      .. grid-item-card:: gz-sensors CameraSensor.cc
         :link: https://github.com/gazebosim/gz-sensors/blob/gz-sensors8/src/CameraSensor.cc
         :class-card: sd-border-secondary

         **Gazebo: gz-sensors, src/CameraSensor.cc**

         Fills the camera info message, including :math:`K`.

      .. grid-item-card:: sdformat issue 425
         :link: https://github.com/gazebosim/sdformat/issues/425
         :class-card: sd-border-secondary

         **"Missing documentation for what concerns camera sensors frame"**

         A Gazebo camera looks along its frame's +x axis, with z up.

      .. grid-item-card:: Assembly table
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/assembly_table/model.sdf
         :class-card: sd-border-secondary

         **ARIAC: assembly_table/model.sdf**

         A 0.43 m tall box: the table top is at z = 0.43 m.


.. dropdown:: MoveIt 2 and the Example Team
   :class-container: sd-border-secondary
   :open:

   The MoveIt 2 parts, the planning pipeline, and what the ARIAC example team
   ships.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: MoveIt motion planning
         :link: https://moveit.picknik.ai/main/doc/concepts/motion_planning.html
         :class-card: sd-border-secondary

         **MoveIt: Motion Planning (concepts)**

         The planning pipeline: request adapters, a planner plugin, and
         response adapters.

      .. grid-item-card:: MoveIt Python API
         :link: https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html
         :class-card: sd-border-secondary

         **MoveIt: Motion Planning Python API**

         How a MoveItPy instance plans and executes from Python.

      .. grid-item-card:: ARIAC example team
         :link: https://github.com/usnistgov/ariac_example_team
         :class-card: sd-border-secondary

         **usnistgov/ariac_example_team**

         MoveIt configurations for the five robots, ``robot_interface.py``
         and the Move Robots demo.

      .. grid-item-card:: Example team planners
         :link: https://github.com/usnistgov/ariac_example_team/blob/main/moveit_configs/inspection_robot_1_moveit_config/config/moveit_cpp.yaml
         :class-card: sd-border-secondary

         **moveit_cpp.yaml (inspection robot 1)**

         The three planner settings: ``pilz_ptp``, ``pilz_lin`` and
         ``ompl_rrts``.

      .. grid-item-card:: Move Robots demo
         :link: https://github.com/usnistgov/ariac_example_team/blob/main/example_team/example_team/examples/move_robots.py
         :class-card: sd-border-secondary

         **move_robots.py**

         One MoveItPy instance per robot, 20 short Pilz LIN moves each.

      .. grid-item-card:: ARIAC demos
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/demos.html
         :class-card: sd-border-secondary

         **ARIAC 2025: Demos**

         How to run the example team's demos, including Move Robots.


.. dropdown:: Planners
   :class-container: sd-border-secondary
   :open:

   Sampling-based planners, the RRT-Connect toy, and the Pilz industrial
   motion planner.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: RRT-Connect
         :link: https://doi.org/10.1109/ROBOT.2000.844730
         :class-card: sd-border-secondary

         **Kuffner, J. J. and LaValle, S. M. (2000)**

         *RRT-Connect: An Efficient Approach to Single-Query Path Planning.*
         ICRA 2000, vol. 2, pages 995 to 1001.

         The algorithm behind ``rrt_connect_toy.py``.

      .. grid-item-card:: OMPL RRTConnect
         :link: https://ompl.kavrakilab.org/classompl_1_1geometric_1_1RRTConnect.html
         :class-card: sd-border-secondary

         **OMPL: RRTConnect class**

         The RRT-Connect planner as OMPL implements it.

      .. grid-item-card:: OMPL PRM
         :link: https://ompl.kavrakilab.org/classompl_1_1geometric_1_1PRM.html
         :class-card: sd-border-secondary

         **OMPL: PRM class**

         The probabilistic roadmap planner.

      .. grid-item-card:: OMPL RRTstar
         :link: https://ompl.kavrakilab.org/classompl_1_1geometric_1_1RRTstar.html
         :class-card: sd-border-secondary

         **OMPL: RRTstar class**

         "RRT* (optimal RRT) is an asymptotically-optimal incremental
         sampling-based motion planning algorithm."

      .. grid-item-card:: MoveIt OMPL interface
         :link: https://moveit.picknik.ai/main/doc/examples/ompl_interface/ompl_interface_tutorial.html
         :class-card: sd-border-secondary

         **MoveIt: OMPL Planner**

         "A feasible path is smoothened and shortened in a post-processing
         stage": the setting on the "Five Runs" slide.

      .. grid-item-card:: Pilz planner
         :link: https://moveit.picknik.ai/main/doc/how_to_guides/pilz_industrial_motion_planner/pilz_industrial_motion_planner.html
         :class-card: sd-border-secondary

         **MoveIt: Pilz Industrial Motion Planner**

         The PTP, LIN and CIRC motions, and their joint and Cartesian limits.

      .. grid-item-card:: MoveIt planners
         :link: https://moveit.ai/documentation/planners/
         :class-card: sd-border-secondary

         **MoveIt: Planners Available in MoveIt**

         "Pilz industrial motion planner is a deterministic generator for
         circular and linear motions." Also lists STOMP and CHOMP, the
         trajectory optimizers.


.. dropdown:: The Moving Conveyor and Scoring
   :class-container: sd-border-secondary
   :open:

   The belt speed limit, a stopped belt, the course skill's conveyor catch,
   and what a collision costs.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Course Skills Package
         :link: /ariac/skills
         :link-type: doc
         :class-card: sd-border-secondary

         **ENPM663: Course Skills Package (v0.2.0)**

         The actions, goals and result codes; how the conveyor catch works,
         when it is refused, and why a conveyor malfunction ends it; the
         tester area lock.

      .. grid-item-card:: Team configuration schema
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_setup/config/user_config_schema.json
         :class-card: sd-border-secondary

         **ARIAC: user_config_schema.json**

         The largest conveyor speed a team may set, 0.1 m/s.

      .. grid-item-card:: Conveyor plugin
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/linear_conveyor_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC: linear_conveyor_plugin.cpp**

         A stopped belt reports speed 0 during the conveyor malfunction.

      .. grid-item-card:: ARIAC scoring
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **ARIAC 2025: Scoring**

         The collision penalty: 100 points for every 5 s in contact, charged
         to each robot.

      .. grid-item-card:: Scoring weights
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **ARIAC: scoring_weights.yaml**

         The weights behind the scoring page's numbers. L12 works through the
         formula.
