====================================================
Course Skills Package
====================================================

..
   Published since 2026-10-12 (HIDE_SKILLS_PAGE is False in conf.py). Written
   2026-10-12 from the package's v0.1.0 README; checked against v0.2.0
   (6fa0563) on 2026-10-18. Before v1.0.0 (GP1, 2027-02-03):
   - add the assembly robot and gantry welder skills (milestone 2);
   - recheck "A gripper error reports what the fingers hold" against the fixed
     holding check;
   - check the install commands against the published release repo.

ARIAC 2025 gives its robots low-level controls only: a joint trajectory
action for each robot, and a gripper action, vacuum tool services or a weld
service (the table in :ref:`l1-robot-interfaces`). None of them is a pick or
place skill. The course skills package adds them. Each skill
is a ROS 2 action: your behavior tree (GP1 to GP3) or your LLM agent (GP4)
sends a goal, and the skill plans the motion with MoveIt 2, moves the arm,
runs the gripper and reports the result. You never write motion code.

The package moves the robot arms and nothing else. You call ARIAC's factory
services yourself: the cell feeder, inspection reports, AGV moves and kit
submissions.

.. warning::

   **Version 0.2.0.** This page describes version 0.2.0 of the package:
   the skills for the two inspection robots. The repository
   becomes available to students with GP1 on February 3, 2027, as version
   1.0.0. The install commands and some details may change by then, and the
   assembly robot and gantry welder skills for the final demo are added
   later. The :doc:`changelog </changelog/changelog>` announces each
   change.

.. note::

   This page describes the skills for the two inspection robots, which GP1
   to GP4 use. L10 opens the package and shows how a skill becomes a
   trajectory.


Install
-------

The package is in the
`enpm663-spring-2027-skills <https://github.com/rubixcubic/enpm663-spring-2027-skills>`_
repository. Use the release tag the course announces, so your team runs the
same code the instructor tested. Fixes come as new tags, listed in the
:doc:`changelog </changelog/changelog>`.

.. tab-set::

   .. tab-item:: Docker (recommended)

      .. code-block:: bash

         git clone --branch v1.0.0 https://github.com/rubixcubic/enpm663-spring-2027-skills.git
         cd enpm663-spring-2027-skills
         scripts/dev_up.sh

      ``dev_up.sh`` builds the image and opens a shell in the container
      ``enpm663_skills_dev``. The image starts from NIST's ARIAC 2025 image,
      pinned to the version the package was tested on. The container uses the
      NVIDIA runtime, so your PC needs an NVIDIA GPU, its driver and the
      NVIDIA Container Toolkit. Without the runtime, the container does not
      start.

   .. tab-item:: Native (Ubuntu 24.04)

      Clone the repository into the ``src`` folder of the colcon workspace
      where ARIAC 2025 is built, then build:

      .. code-block:: bash

         colcon build --symlink-install
         source install/setup.bash

      Your MoveIt packages must match your ARIAC build. A MoveIt built
      against another ``fastcdr`` version fails when Python imports
      ``moveit.planning``. The Docker image avoids this problem.


Start ARIAC and the Skills
--------------------------

**Step 1: Place the break beam.** ``pick_from_conveyor`` needs a break beam
on the inspection conveyor. It goes under ``SENSORS`` in your team
configuration file. The repository's ``config/team_config.yaml`` has one:

.. code-block:: yaml

   SENSORS:
     - NAME: conveyor_beam
       TYPE: break_beam
       POSE:
         XYZ: [0.6, 0.95, 0.44]
         RPY: [0.0, 0.0, pi/2]
       UPDATE_RATE: 10

ARIAC names the beam's TF frame ``<NAME>_frame`` (here
``conveyor_beam_frame``). It publishes the beam's state on
``/<NAME>/status``, and on ``/<NAME>/change`` each time the reading changes.

**Step 2: Start ARIAC.** Inside the container:

.. code-block:: bash

   scripts/run_ariac.sh <your_trial.yaml>

The script launches ARIAC headless with your trial file and the
repository's team configuration.

**Step 3: Start the skills.** In another shell, with the workspace sourced:

.. code-block:: bash

   ros2 launch enpm663_skills skills.launch.py

The launch starts one node per robot. A node rejects every goal until its
robot is ready. When it is, the node logs ``ready`` and publishes ``true``
on ``/<robot>/skills/ready`` (a latched ``std_msgs/Bool``). Wait for it
before you send a goal.

The skills read their settings from ``config/skills.yaml``. To use your own
copy, set ``ENPM663_SKILLS_CONFIG=/path/to/skills.yaml`` before the launch.
A file with a missing key or a value out of range stops the launch, with a
message that names the key.

**Step 4: Send a goal.** From the command line:

.. code-block:: bash

   ros2 action send_goal --feedback /inspection_robot_2/skills/move_home \
     enpm663_skills_interfaces/action/MoveHome "{}"

The command prints each stage the skill goes through, then the result.


The Skills
----------

Every action is served at ``/<robot>/skills/<skill>``. Its type is in
``enpm663_skills_interfaces/action``.

.. list-table::
   :header-rows: 1
   :widths: 22 22 20 36
   :class: compact-table

   * - Robot
     - Skill
     - Goal
     - What it does
   * - ``inspection_robot_1``
     - ``pick_from_conveyor``
     - ``beam`` (a ``std_msgs/Header``)
     - Catches a moving cell from the side. Needs empty hands. Ends holding
       ``CELL``.
   * -
     - ``place_on_tester``
     - ``tester`` (1 or 2)
     - Puts the held cell on a voltage tester. Ends holding ``NOTHING``,
       parked.
   * - ``inspection_robot_2``
     - ``pick_from_tester``
     - ``tester`` (1 or 2)
     - Takes the cell off a tester. Needs empty hands. Ends holding
       ``CELL``, parked.
   * -
     - ``place_in_slot``
     - ``agv`` (1 to 3), ``slot`` (1 to 4)
     - Puts the held cell in a tray slot. The AGV must be at the inspection
       station. Ends holding ``NOTHING``.
   * -
     - ``drop_in_recycling``
     - none
     - Drops the held cell in the recycling bin. Ends holding ``NOTHING``.
   * - both robots
     - ``move_home``
     - none
     - Moves the arm to its park pose, outside the testers.

Each action streams feedback with one field, ``stage``: the step the skill
is in now, such as ``approach``, ``grasp``, ``release`` or ``retreat``. Your
tree can show progress with it, or time a cancel.


The Result
----------

Every skill returns a ``SkillResult``:

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - Field
     - Meaning
   * - ``code``
     - How the skill ended (table below).
   * - ``holding``
     - What the robot holds now: ``NOTHING``, ``CELL``, ``SHELL`` or
       ``MODULE``.
   * - ``message``
     - What happened, in words. Log it.
   * - ``attempts``
     - Planning or execution attempts used. 1 means no fallback was needed.

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Code
     - When
   * - ``SUCCESS``
     - The skill finished.
   * - ``PLANNING_FAILED``
     - MoveIt found no path, even after the fallback planner.
   * - ``EXECUTION_FAILED``
     - The controller rejected or stopped the trajectory, or a step ran past
       its time limit.
   * - ``GRASP_FAILED``
     - The gripper closed on nothing, or the cell was lost before release.
   * - ``PRECONDITION_FAILED``
     - The robot held the wrong thing, the AGV was at the wrong station, or
       the cell could not be caught (see below).
   * - ``PLACE_NOT_FOUND``
     - A place's TF frame could not be found.
   * - ``ZONE_BUSY_TIMEOUT``
     - The other robot kept the tester area for too long.
   * - ``CANCELED``
     - Your code cancelled the goal.

A skill never retries its own task. It does not close the gripper again,
check a precondition again, or resend a cancelled move. Recovery is your
team's job (L7, L11). ``attempts`` above 1 means one of two infrastructure
retries happened: a second planner (Pilz first, then OMPL), or one more try
after MoveIt's "controller is taking too long" error.


Behaviors Your Team Must Know
-----------------------------

.. dropdown:: A cell reaches the robot only with a passing inspection report
   :icon: alert

   The inspection conveyor has a door at x = 1.0 m. It opens only for a
   cell that already has a passing inspection report. Any other cell drops
   into ARIAC's inspection bin before it reaches the catch point, and
   ``pick_from_conveyor`` never sees it. Sending the report is one of the
   factory services your team calls.

.. dropdown:: How the conveyor catch works
   :icon: info

   The arm waits beside the belt with the gripper pointing upstream, fingers
   open across the belt. The upright cell rides into the fingers. A cell
   gripped from the top could not be laid flat in a tester afterward.

   When a ``/<NAME>/change`` message says ``object_detected: true``, a cell
   has just reached the beam. Copy that message's ``header`` into the goal's
   ``beam`` field. The skill reads where the beam is from the header's frame,
   and when the cell crossed it from the stamp. With the belt speed, it
   predicts when the cell reaches the catch point and closes the gripper
   just before then.

.. dropdown:: When the catch is refused
   :icon: alert

   ``pick_from_conveyor`` ends ``PRECONDITION_FAILED`` before the arm moves
   if:

   - the beam header is older than ``max_trigger_age`` (8.0 s in
     ``skills.yaml``, set for a beam at x = 0.6 m and a belt at 0.1 m/s), or
     its stamp is in the future;
   - the belt is stopped and the beam is not at the catch point (within
     ``stopped_tolerance``, 0.005 m). The beam only saw the cell cross, so
     the skill cannot know where a stopped cell is;
   - the cell would reach the catch point before the arm can get there. The
     arm needs up to ``side_lead_time`` (3.925 s of simulation time) from any
     starting pose.

   Send the goal as soon as the beam fires. If a goal is refused, catch the
   next cell. A beam placed farther upstream needs a larger
   ``max_trigger_age`` in your copy of ``skills.yaml``.

.. dropdown:: A conveyor malfunction ends a catch
   :icon: alert

   In ARIAC's conveyor malfunction challenge, ``/inspection_conveyor/status``
   reports ``MALFUNCTIONING`` and the belt stops. If that happens, or the
   speed changes, while ``pick_from_conveyor`` waits for the cell, the skill
   stops waiting, does not close the gripper, moves away, and ends
   ``PRECONDITION_FAILED``, holding ``NOTHING``. The beam only saw the cell
   cross, so after a stop the skill cannot know where the cell is.

   What to do: wait until the status is no longer ``MALFUNCTIONING``, then
   send a new goal with the header of a cell that crosses the beam after the
   restart. Do not reuse a header from before the stop. A cell that stopped
   on the belt cannot be caught by this skill.

.. dropdown:: The tester area is shared
   :icon: info

   ``place_on_tester`` and ``pick_from_tester`` take a lock on the tester
   area before the arm enters it, so the two robots are never there at the
   same time. A skill that waits too long for the lock ends
   ``ZONE_BUSY_TIMEOUT``.

   A skill that fails or is cancelled inside the tester area lifts the arm,
   moves to its park pose, and only then gives up the lock. If that retreat
   does not finish, the robot keeps the lock, and every later result from
   that robot says so in its ``message``. Send ``move_home`` to clear it: a
   successful ``move_home`` is the only thing that gives up a lock left held
   this way.

.. dropdown:: Every release checks the cell first
   :icon: info

   Before ``place_on_tester``, ``place_in_slot`` or ``drop_in_recycling``
   opens the gripper, it checks that the cell is still held. If the cell
   slipped out on the way, the skill ends ``GRASP_FAILED``, holding
   ``NOTHING``, instead of opening on empty space and reporting success.

.. dropdown:: One goal per arm
   :icon: info

   Each robot runs one goal at a time, across all of its skills. A second
   goal sent while the first is running is rejected when it arrives. The two
   robots can run goals at the same time.

.. dropdown:: Cancel stops the arm
   :icon: info

   Cancelling a goal stops the trajectory at once. If the skill was inside
   the tester area, the robot then lifts, parks and gives up the lock. The
   result's code is ``CANCELED``, and ``holding`` says what the gripper
   holds.

.. dropdown:: move_home parks the arm
   :icon: info

   ``move_home`` moves the arm to a park pose outside the tester area, not
   to the "home" pose in the robot's MoveIt configuration. For
   ``inspection_robot_2``, that home pose is above voltage tester 1, inside
   the tester area.
