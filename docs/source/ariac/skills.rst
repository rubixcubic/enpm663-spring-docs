====================================================
Course Skills Package
====================================================

..
   Published since 2026-10-12 (HIDE_SKILLS_PAGE is False in conf.py). Written
   2026-10-12 from the package's v0.1.0 README; rewritten 2026-11-11 from the
   v0.3.1 README (9a2197d), all five robots. Before v1.0.0 (GP1, 2027-02-03):
   - check the install commands against the published release repo.
   v1.0.0 ships all five robots' skills (user decision 2026-11-15, todo 35).

ARIAC 2025 gives its robots low-level controls only: a joint trajectory
action for each robot, and a gripper action, vacuum tool services or a weld
service (the table in :ref:`l1-robot-interfaces`). None of them is a pick or
place skill. The course skills package adds them. Each skill
is a ROS 2 action: your behavior tree (GP1 to GP3) or your LLM agent (GP4)
sends a goal, and the skill plans the motion with MoveIt 2, moves the arm,
runs the gripper, vacuum tool or welder, and reports the result. You never
write motion code.

The package moves the robot arms and nothing else. You call ARIAC's factory
services yourself: the cell feeder, inspection reports, AGV moves and kit
submissions.

.. warning::

   **Version 0.3.1.** This page describes version 0.3.1 of the package. The
   repository becomes available to students with GP1 on February 3, 2027, as
   version 1.0.0. The install commands and some details may change by then.
   The :doc:`changelog </changelog/changelog>` announces each change.

.. note::

   The skills come in two groups. The **Task 1 skills** move the two
   inspection robots; GP1 to GP4 use them. The **Task 2 skills** move the two
   assembly robots and the gantry welder; the
   :doc:`final demo </assignments/final_demo>` uses them. Both groups come in
   version 1.0.0 with GP1. L10 opens the package and shows how a skill becomes
   a trajectory.


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

The launch starts five nodes, one per robot. A node rejects every goal until
its robot is ready. When it is, the node logs ``ready`` and publishes
``true`` on ``/<robot>/skills/ready`` (a latched ``std_msgs/Bool``). Wait for
it before you send a goal.

The skills read their settings from ``config/skills.yaml``. To use your own
copy, set ``ENPM663_SKILLS_CONFIG=/path/to/skills.yaml`` before the launch.
A file with a missing key or a value out of range stops the launch, with a
message that names the key.

**Step 4: Send a goal.** From the command line:

.. code-block:: bash

   ros2 action send_goal --feedback /inspection_robot_2/skills/move_home \
     enpm663_skills_interfaces/action/MoveHome "{}"

The command prints each stage the skill goes through, then the result.

In your own node, create each action client once, when the node starts, and
send every goal for that action through it. Give every goal your own
deadline. If the deadline passes, cancel the goal. If the cancel gets no
answer either, restart ARIAC and the skills server.


The Skills
----------

Every action is served at ``/<robot>/skills/<skill>``. Its type is in
``enpm663_skills_interfaces/action``. Every robot also has ``move_home``
(no goal fields), which moves the arm to its park pose.

**Task 1 skills: the inspection robots**

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

**Task 2 skills: the assembly robots and the gantry welder**

.. list-table::
   :header-rows: 1
   :widths: 22 22 20 36
   :class: compact-table

   * - Robot
     - Skill
     - Goal
     - What it does
   * - ``assembly_robot_1``
     - ``pick_from_slot``
     - ``agv`` (1 to 3), ``slot`` (1 to 4)
     - Grips the cell lying in a tray slot from above, at its middle. Needs
       empty hands and the AGV at the assembly station. Ends holding
       ``CELL``.
   * -
     - ``stand_cell``
     - ``orientation`` (``UP`` or ``DOWN``)
     - Stands the held cell on end in the tray's center hole, lets go, and
       grips it again from above. ``UP`` puts the base end down. Ends
       holding ``CELL``.
   * -
     - ``place_in_shell``
     - ``shell_slot`` (1 to 4)
     - Lowers the standing cell into a bottom shell slot. Slots 1 and 3 take
       ``UP``, slots 2 and 4 take ``DOWN``. Ends holding ``NOTHING``,
       parked.
   * - ``assembly_robot_2``
     - ``change_tool``
     - ``tool`` (``NONE``, ``VG_2`` or ``VG_4``)
     - Returns the attached tool to its holder, then attaches the named one.
       Needs empty hands.
   * -
     - ``pick_top_shell``
     - ``pose`` (a ``PoseStamped`` from your sensor)
     - Picks the top shell off the assembly table with vg_2. Uses the pose's
       x, y and yaw. Ends holding ``SHELL``.
   * -
     - ``place_top_shell``
     - ``module`` (a ``PointStamped`` from your sensor)
     - Lowers the held top shell onto the module on conveyor section 3. Ends
       holding ``NOTHING``.
   * -
     - ``flip_module``
     - ``module`` (a ``PointStamped`` from your sensor)
     - Grips the module with vg_4, turns it upside down on section 3, and
       lets go. Ends holding ``NOTHING``, parked.
   * - ``gantry_welder``
     - ``weld_bead``
     - ``shell`` (``TOP`` or ``BOTTOM``), ``bead``, ``module`` (a
       ``PointStamped``)
     - Welds one bead: 1 to 4 on the top shell, 1 or 2 on the bottom shell.
       Always raises the electrodes again afterward.

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
     - The controller rejected or stopped the trajectory, a step ran past
       its time limit, or the simulation stopped responding.
   * - ``GRASP_FAILED``
     - The gripper closed on nothing, the cell was lost before release, or
       the vacuum tool's grasp was refused.
   * - ``PRECONDITION_FAILED``
     - The robot held the wrong thing, the AGV was at the wrong station, the
       cell could not be caught, the module point was out of range or too
       old, or a conveyor section moved (see below).
   * - ``PLACE_NOT_FOUND``
     - A place's TF frame could not be found.
   * - ``ZONE_BUSY_TIMEOUT``
     - The other robot kept the tester area for too long.
   * - ``CANCELED``
     - Your code cancelled the goal.
   * - ``WELD_FAILED``
     - ARIAC refused the weld. The message gives ARIAC's reply, for example
       that the bead was already welded.
   * - ``TOOL_CHANGE_FAILED``
     - ARIAC refused to attach or detach a tool, or the tool changer's
       status did not follow in time.

A skill never retries its own task. It does not close the gripper again,
check a precondition again, or resend a cancelled move. Recovery is your
team's job (L7, L11). ``attempts`` above 1 means one of two infrastructure
retries happened: a second planner (Pilz first, then OMPL), or one more try
after MoveIt's "controller is taking too long" error. ``pick_top_shell`` also
reads 2 when it turned the tool 180 degrees to find a plan before touching
the shell.


Behaviors Your Team Must Know
-----------------------------

**For every robot**

.. dropdown:: One goal per arm
   :icon: info

   Each robot runs one goal at a time, across all of its skills. A second
   goal sent while the first is running is rejected when it arrives. Different
   robots can run goals at the same time.

.. dropdown:: Cancel stops the arm
   :icon: info

   Cancelling a goal stops the trajectory at once. If the skill was inside
   the tester area, the robot then lifts, parks and gives up the lock. The
   result's code is ``CANCELED``, and ``holding`` says what the robot
   holds.

.. dropdown:: move_home parks the arm
   :icon: info

   ``move_home`` moves the arm to a park pose, not to the "home" pose in the
   robot's MoveIt configuration. For ``inspection_robot_2``, that home pose
   is above voltage tester 1, inside the tester area.

.. dropdown:: If the simulation stops responding
   :icon: alert

   If Gazebo freezes during a motion, its clock stops too. After 30 s
   without the clock moving, the skill stops the arm and ends
   ``EXECUTION_FAILED`` with "restart ARIAC and the skills server" in its
   message, about 35 s after the freeze. From then on, every motion of that
   robot is refused at once. Restart ARIAC and the skills server. Your own
   deadline on every goal still matters: it covers the cases the skill
   cannot see.

**Task 1 skills**

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

.. dropdown:: A gripper error reports what the fingers hold
   :icon: info

   If a gripper command itself fails (the close of a catch or a tester pick,
   or the open of a release), the result's ``holding`` comes from the finger
   position. It says ``CELL`` only when the fingers are closed on a cell.
   Fingers closed past it, or stopped open, read as ``NOTHING``.

**Task 2 skills**

.. dropdown:: Cells stand up in the tray's center hole
   :icon: info

   ``pick_from_slot`` grips every cell at its middle, so the skill cannot
   tell which end is up. You name it at ``stand_cell``: ``UP`` puts the base
   end down (shell slots 1 and 3), ``DOWN`` the other end (slots 2 and 4).
   ``place_in_shell`` refuses a cell whose orientation does not match the
   slot, before the arm moves.

   ARIAC's ``/agvN/tray_status`` shows every slot empty once the AGV reaches
   the assembly station, so ``pick_from_slot`` cannot check a slot first. An
   empty slot ends ``GRASP_FAILED``.

.. dropdown:: What the module skills need from your sensor
   :icon: alert

   ``place_top_shell``, ``flip_module`` and ``weld_bead`` take the module's
   center as a ``PointStamped``. Its ``header.stamp`` must be in simulation
   time. While the module has not moved since ARIAC put it on section 3, it
   is at the wait point, world (4.2, 5.55).

   The point must be in range, or the skill refuses before the arm moves:

   - ``place_top_shell``: x from 4.18 to 4.22, y from 5.47 to 6.00;
   - ``flip_module``: x from 4.18 to 4.22, y from 5.47 to 5.555;
   - ``weld_bead``: the bead must be under the electrodes, x from 3.95 to
     4.45 and y from 6.275 to 6.575. Run section 3 until the module's center
     is in that y range first.

   A weld needs the point within 2 mm across the module (x) and 3 mm along
   it (y). That budget includes where your top shell landed: the top shell
   locks where it falls, and falling does not center it.

.. dropdown:: Measure again after every belt move
   :icon: alert

   A module skill refuses a point stamped before conveyor section 3 last
   stopped, and refuses any goal while the section moves.
   ``place_in_shell`` does the same for section 1. If the section starts
   while the skill works, the goal ends ``PRECONDITION_FAILED``, and the
   message says what the arm did: it stopped before moving, it stopped and
   retreated, or its retreat failed (then send ``move_home`` before the next
   goal). The message also names the last stage the goal reached. After
   ``release``, the part was already let go.

.. dropdown:: The vacuum retry is yours
   :icon: info

   In ARIAC's vacuum malfunction challenge, the grasp is refused and
   ``pick_top_shell`` ends ``GRASP_FAILED``. Its retreat lifts the pads off
   the shell, which clears the fault. Send the same goal again.

   Give ``pick_top_shell`` the shell's yaw within 90 degrees. Off by 180
   degrees, the shell is still picked, but it lands turned on the module,
   and its bead numbers then run the other way.

.. dropdown:: Change tools only with change_tool
   :icon: info

   ARIAC's ``attach_tool`` service can "attach" a tool that is still in its
   holder, after the pin has left the tool. ``change_tool`` attaches only at
   the holder and waits for ``/assembly_robot_2/tool_changer/status`` to
   agree. Use it instead of calling the services yourself.

.. dropdown:: Mistakes no skill can see
   :icon: alert

   ARIAC reports none of these, and none can be undone. Each skill still
   reports ``SUCCESS`` when its motion and device calls worked:

   - a cell that locks ``UP`` when ``DOWN`` was wanted, or in a neighboring
     slot;
   - a top shell that does not lock;
   - a top weld made before the top shell locked. The bead is marked done and
     can never be welded again. Weld the top beads only after
     ``place_top_shell``, and only if your sensor shows the top shell
     seated;
   - a ``weld_bead`` with the wrong ``shell``. ``BOTTOM`` bead 1 on a module
     that was not flipped welds top bead 3 and reports success.

.. dropdown:: Two failures that only a trial restart clears
   :icon: alert

   - ``stand_cell`` ends ``GRASP_FAILED`` after its regrasp failed: the cell
     stands ungripped in the tray's center hole, and no skill removes it.
   - ``flip_module`` ends ``EXECUTION_FAILED`` with "the module is still
     held": vg_4 holds the turned module, and every skill that needs empty
     hands refuses.

   Restarting the trial (a fresh ARIAC run) clears both.

.. dropdown:: Harmless log lines
   :icon: info

   - After a flip, Gazebo logs ``DetachableJoint's parent link entity [...]
     not found in link map`` and ``Failed to find joint [...]``. Measure the
     module again before the bottom welds anyway.
   - At every launch, the ``gantry_welder`` node logs ``Semantic description
     is not specified for the same robot as the URDF``. ARIAC's URDF names
     the gantry ``assembly_robot_1``, a leftover upstream; ``move_home`` and
     ``weld_bead`` work normally.
