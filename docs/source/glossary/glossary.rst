====================================================
Glossary
====================================================

:ref:`0 to 9 <glossary-num>` · :ref:`A <glossary-a>` · :ref:`B <glossary-b>` · :ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`E <glossary-e>` · :ref:`F <glossary-f>` · :ref:`G <glossary-g>` · :ref:`H <glossary-h>` · :ref:`I <glossary-i>` · :ref:`J <glossary-j>` · :ref:`K <glossary-k>` · :ref:`L <glossary-l>` · :ref:`M <glossary-m>` · :ref:`N <glossary-n>` · :ref:`O <glossary-o>` · :ref:`P <glossary-p>` · :ref:`Q <glossary-q>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` · :ref:`T <glossary-t>` · :ref:`U <glossary-u>` · :ref:`V <glossary-v>` · :ref:`W <glossary-w>` · :ref:`Z <glossary-z>`

.. only:: html

   .. raw:: html

      <div id="glossary-search-wrap" style="margin: 1.2em 0 0.6em 0;">
        <input
          id="glossary-search"
          type="search"
          placeholder="Filter terms..."
          autocomplete="off"
          spellcheck="false"
          style="
            width: 100%;
            max-width: 480px;
            padding: 0.45em 0.75em;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
          "
        />
        <span
          id="glossary-search-count"
          style="margin-left: 0.8em; font-size: 0.88em; color: #666;"
        ></span>
      </div>

      <div id="glossary-lecture-filter"
           style="margin: 0 0 1.4em 0; display: flex; flex-wrap: wrap; gap: 0.35em; align-items: center;">
        <span style="font-size: 0.88em; color: #666; margin-right: 0.3em;">Lecture:</span>
        <button type="button" data-lecture="all"
                style="padding: 0.25em 0.7em; font-size: 0.85em; border: 1px solid #888;
                       background: #444; color: #fff; border-radius: 3px; cursor: pointer;">
          All
        </button>
        <!-- one button per published lecture, inserted by JS -->
      </div>

      <script>
      (function () {
        /* Run after the DOM is ready. */
        function initGlossarySearch() {
          var input  = document.getElementById('glossary-search');
          var count  = document.getElementById('glossary-search-count');
          var filterBar = document.getElementById('glossary-lecture-filter');
          if (!input || !filterBar) return;

          var activeLecture = null;  /* null = "All" */

          /* Cache lecture tags per <dt> so we don't rescan the DOM on every keystroke.
             A "tag" is the visible text of any link inside the dd block matching ^L\d+$. */
          var dtIndex = [];  /* { dt, dds, tags: Set<string>, text: lowercased dt text } */
          document.querySelectorAll('dl.glossary dt').forEach(function (dt) {
            var dds = [];
            var node = dt.nextElementSibling;
            while (node && node.tagName === 'DD') {
              dds.push(node);
              node = node.nextElementSibling;
            }
            var tags = new Set();
            dds.forEach(function (dd) {
              dd.querySelectorAll('a').forEach(function (a) {
                var t = a.textContent.trim();
                if (/^L\d+$/.test(t)) tags.add(t);
              });
            });
            dtIndex.push({ dt: dt, dds: dds, tags: tags, text: dt.textContent.toLowerCase() });
          });

          /* One button per lecture that has at least one linked entry. Tags
             for hidden lectures are plain text, not links, so their lectures
             get no button until they are published. */
          var lectures = new Set();
          dtIndex.forEach(function (e) { e.tags.forEach(function (tag) { lectures.add(tag); }); });
          Array.from(lectures)
            .sort(function (a, b) { return parseInt(a.slice(1)) - parseInt(b.slice(1)); })
            .forEach(function (lec) {
              var btn = document.createElement('button');
              btn.type = 'button';
              btn.dataset.lecture = lec;
              btn.textContent = lec;
              btn.style.cssText =
                'padding: 0.25em 0.6em; font-size: 0.85em; ' +
                'border: 1px solid #ccc; background: #fff; color: #333; ' +
                'border-radius: 3px; cursor: pointer;';
              filterBar.appendChild(btn);
            });

          function getLetterSection(el) {
            var node = el;
            while (node && node !== document.body) {
              if (node.id && /^glossary-[a-z]$/i.test(node.id)) return node;
              node = node.parentElement;
            }
            return null;
          }

          function paintButtons() {
            filterBar.querySelectorAll('button').forEach(function (b) {
              var isActive = (b.dataset.lecture === 'all' && activeLecture === null) ||
                             (b.dataset.lecture === activeLecture);
              if (isActive) {
                b.style.background = '#444';
                b.style.color = '#fff';
                b.style.borderColor = '#888';
              } else {
                b.style.background = '#fff';
                b.style.color = '#333';
                b.style.borderColor = '#ccc';
              }
            });
          }

          function run() {
            var query = input.value.trim().toLowerCase();
            var visible = 0;

            dtIndex.forEach(function (entry) {
              var textMatch = !query || entry.text.indexOf(query) !== -1;
              var lectureMatch = !activeLecture || entry.tags.has(activeLecture);
              var match = textMatch && lectureMatch;

              entry.dt.style.display = match ? '' : 'none';
              entry.dds.forEach(function (dd) { dd.style.display = match ? '' : 'none'; });
              if (match) visible++;
            });

            /* Hide letter-section headings + dl when every term inside is hidden. */
            document.querySelectorAll('dl.glossary').forEach(function (dl) {
              var anyVisible = Array.prototype.some.call(
                dl.querySelectorAll('dt'),
                function (dt) { return dt.style.display !== 'none'; }
              );
              dl.style.display = anyVisible ? '' : 'none';

              var section = getLetterSection(dl);
              if (section) {
                section.style.display = anyVisible ? '' : 'none';
              } else {
                var prev = dl.previousElementSibling;
                while (prev) {
                  if (prev.tagName === 'H2' || prev.tagName === 'H1') {
                    prev.style.display = anyVisible ? '' : 'none';
                    break;
                  }
                  prev = prev.previousElementSibling;
                }
              }
            });

            /* Result count: show whenever a filter is active. */
            if (query || activeLecture) {
              count.textContent = visible === 1
                ? '1 term found'
                : visible + ' terms found';
            } else {
              count.textContent = '';
            }
          }

          /* Wire up the lecture-chip clicks (event delegation). */
          filterBar.addEventListener('click', function (e) {
            var btn = e.target.closest('button[data-lecture]');
            if (!btn) return;
            var lec = btn.dataset.lecture;
            activeLecture = (lec === 'all') ? null : lec;
            paintButtons();
            run();
          });

          input.addEventListener('input', run);
          input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
          });

          paintButtons();
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initGlossarySearch);
        } else {
          initGlossarySearch();
        }
      })();
      </script>

----


.. _glossary-num:

0 to 9
======

.. glossary::

   4D/RCS
      NIST's reference model architecture for unmanned vehicle systems (NISTIR
      6910). Each level plans over its own time span and keeps its own world
      model. The course takes two ideas from it: a world model at each layer,
      and errors handled where they are seen while status moves up. :doc:`L3
      </lectures/lecture3/l3_index>`


.. _glossary-a:

A
=

.. glossary::

   Action (planning)
      A planning step with preconditions (facts that must hold before it) and
      effects (facts it makes true, and delete effects, written (not ...),
      that it makes false). :doc:`L6 </lectures/lecture6/l6_index>`

   Action (ROS 2)
      A long request with feedback while it runs and a result at the end; the
      client may ask to cancel it. Teams move AGVs with ARIAC's /agvN/move
      action, which rejects cancel requests. :doc:`L1
      </lectures/lecture1/l1_index>`

   Action client leaf
      A py_trees_ros leaf that sends an action goal and returns SUCCESS only
      if the result status is SUCCEEDED. :doc:`L4
      </lectures/lecture4/l4_index>`

   Action expert
      The part of a VLA, such as SmolVLA, that turns the vision-language
      model's features into robot actions. :doc:`L13
      </lectures/lecture13/l13_index>`

   Action failure
      A skill or service call does not do what it was asked, such as a failed
      grasp. Recovery starts in the behavior tree. :doc:`L11
      </lectures/lecture11/l11_index>`

   Agent
      A program that loops around an LLM: it observes the world, asks the
      model, calls a tool, checks the result and repeats. In this course the
      tools are robot skills. :doc:`L1 </lectures/lecture1/l1_index>` ·
      :doc:`L8 </lectures/lecture8/l8_index>`

   Agent loop
      The loop the orchestrator runs: read the state, ask the LLM, check and
      run the tool call it returns, record the result, and stop when a stop
      condition fires. The agent's behavior comes from the loop, not from the
      model alone. :doc:`L8 </lectures/lecture8/l8_index>`

   Agentic closed loop
      Act, observe again, compare what you see with the expected effect, then
      decide: retry, wait or replan. :doc:`L9 </lectures/lecture9/l9_index>`

   AGV
      Automated Guided Vehicle. ARIAC 2025 has three (agv1 to agv3). Each
      carries a tray with four slots between the inspection, assembly,
      shipping and recycling stations. :doc:`L1 </lectures/lecture1/l1_index>`

   Angular step and point spacing
      The angle between neighboring lidar rays, (max angle - min angle) / (N -
      1); on a surface, neighboring points are about the angular step (in
      radians) times the distance apart. :doc:`L5
      </lectures/lecture5/l5_index>`

   API key
      A secret string that identifies your account with a model provider.
      Anyone who holds it can make calls billed to you, so it lives in an
      environment variable, never in the code or the repository.
      :doc:`Pre-read </preread/index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   Architecture
      How a robot's software is split into parts, and how the parts pass
      decisions and data to each other. :doc:`L2
      </lectures/lecture2/l2_index>`

   ARIAC
      Agile Robotics for Industrial Automation Competition, a NIST simulation
      testbed and competition. ENPM663 uses ARIAC 2025, a simulated EV battery
      factory with cell inspection, kit building and module construction.
      :doc:`L1 </lectures/lecture1/l1_index>`


.. _glossary-b:

B
=

.. glossary::

   Backoff
      A wait before a retry, so a tool or device has time to recover.
      :doc:`L11 </lectures/lecture11/l11_index>`

   Base score
      ARIAC's score for completed work: W1 kc/kd + W2 mc/md, the weighted
      share of the wanted kits (kd) and modules (md) that were completed (kc,
      mc). :doc:`L12 </lectures/lecture12/l12_index>`

   Behavior tree
      A tree of nodes that a robot ticks to decide which action runs.
      Composites (sequence, selector, parallel) choose which children to tick,
      decorators change a child's result, and leaves do the work. The
      executive layer in this course. :doc:`L4 </lectures/lecture4/l4_index>`
      · :doc:`L7 </lectures/lecture7/l7_index>`

   BehaviorTree.CPP
      The C++ behavior tree library used in industry (Nav2 uses it). Trees are
      written in XML and nodes are C++ classes. :doc:`L7
      </lectures/lecture7/l7_index>`

   Blackboard
      The key-value store that behavior tree nodes read and write, so nodes
      can share state without being wired to each other. In py_trees each
      behavior registers the keys it may read or write. :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`L4 </lectures/lecture4/l4_index>`

   Bonus gate
      The ARIAC rule that pays bonuses only if every wanted kit and module was
      submitted and accepted. :doc:`L12 </lectures/lecture12/l12_index>`

   Bounded retry
      Sending the exact error back to the model and asking again, up to a
      fixed number of times, then falling back to a safe action. :doc:`L8
      </lectures/lecture8/l8_index>`

   Break beam
      A sensor that fires when something crosses its beam, such as a cell
      passing a point on the conveyor. :doc:`L10
      </lectures/lecture10/l10_index>`

   Builder
      A function that takes one plan action's arguments and returns the
      behavior tree subtree for that step. :doc:`L7
      </lectures/lecture7/l7_index>`


.. _glossary-c:

C
=

.. glossary::

   Callback
      A function you hand to ROS 2 that it runs when an event arrives, such as
      a message or a timer tick. :doc:`Pre-read </preread/index>` · :doc:`L1
      </lectures/lecture1/l1_index>`

   Callback group
      Sets which of a node's callbacks may run at the same time: mutually
      exclusive (one at a time) or reentrant (several at once). :doc:`L1
      </lectures/lecture1/l1_index>`

   Challenge
      An event ARIAC injects during a trial to test whether the system adapts:
      a conveyor malfunction, a voltage tester malfunction, a vacuum tool
      malfunction or a high-priority order. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Challenge test matrix
      A table of test runs: each challenge alone and combined, on several
      trial configurations, each run more than once. :doc:`L11
      </lectures/lecture11/l11_index>`

   Clean stop
      Stopping on purpose, with a reason, instead of going on with bad data.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Closed-world assumption
      A fact not listed in a planning state is false. :doc:`L6
      </lectures/lecture6/l6_index>`

   Code freeze
      The tagged commit the instructor builds the team's Docker image from for
      the final demo. No change is allowed after it. :doc:`L11
      </lectures/lecture11/l11_index>` · :doc:`Final demo
      </assignments/final_demo>`

   colcon
      The tool that builds every package in a ROS 2 workspace. :doc:`Pre-read
      </preread/index>`

   Competition states
      The states an ARIAC trial moves through: PREPARING, READY, STARTED,
      ORDERS_COMPLETE, ENDED. :doc:`L1 </lectures/lecture1/l1_index>`

   Composite
      A behavior tree node with several children that decides which of them to
      tick: a sequence, a selector or a parallel. :doc:`L4
      </lectures/lecture4/l4_index>`

   Confusion matrix
      The 2 by 2 table of a detector's TP, FP, FN and TN counts. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Constrained output
      A provider holds the model's output to a schema while it is generated.
      It removes parse and schema errors, not semantic ones, so the semantic
      checks stay. :doc:`L8 </lectures/lecture8/l8_index>`

   Context
      The messages sent in one LLM call. It is all the model knows for that
      call. :doc:`L8 </lectures/lecture8/l8_index>`

   Context window
      The most tokens a model reads in one call. :doc:`Pre-read
      </preread/index>` · :doc:`L8 </lectures/lecture8/l8_index>`

   Controlled comparison
      A test of two systems that differ in one variable only, with everything
      else held fixed and the runs alternated. :doc:`L12
      </lectures/lecture12/l12_index>`

   CORA
      The core ontology for robotics and automation, IEEE 1872-2015. :doc:`L3
      </lectures/lecture3/l3_index>`

   Course skills package
      The Python ROS 2 package the course gives teams with GP1. Its skills are
      ROS 2 actions for the arms (pick, place) built on MoveIt 2. A skill
      reports success or a failure reason, accepts cancel, and never retries a
      task itself. AGVs are moved with ARIAC's own action, not a skill.
      :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L10
      </lectures/lecture10/l10_index>`


.. _glossary-d:

D
=

.. glossary::

   Deadlock
      Each robot waits for the other, forever. :doc:`L2
      </lectures/lecture2/l2_index>`

   Decorator
      A behavior tree node with one child that changes the child's result or
      how it runs, such as Inverter, Retry, Timeout or EternalGuard. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L7 </lectures/lecture7/l7_index>`
      · :doc:`L11 </lectures/lecture11/l11_index>`

   Default
      A starting filler for a frame's slot that new information can replace.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Defect (dent, scratch, bulge)
      The three ARIAC cell defects: a round dip, a long narrow dip and a round
      bump. The ARIAC docs say each is at least 2 mm off the surface; ARIAC's
      training cell meshes measure 0.84 to 2.49 mm. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`GP2 </assignments/gp2>`

   Degraded operation
      The system keeps working, more slowly or with fewer devices, while one
      device is down. :doc:`L11 </lectures/lecture11/l11_index>`

   Deliberative layer
      The top layer of the three-layer architecture. It decides over a long
      horizon, such as which kit to build and which cells to use: the PDDL
      planner in GP3, the LLM agent in GP4. :doc:`L2
      </lectures/lecture2/l2_index>`

   Detection threshold
      The value above which a detector flags an item. Lowering it trades
      precision for recall. :doc:`L5 </lectures/lecture5/l5_index>` ·
      :doc:`L12 </lectures/lecture12/l12_index>`


.. _glossary-e:

E
=

.. glossary::

   Embodied-reasoning model
      A vision-language model trained to answer spatial questions about a
      scene, such as where an object is or how to grasp it. Google DeepMind's
      Gemini Robotics ER is one. In the final demo it judges cell defects from
      camera images. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L9 </lectures/lecture9/l9_index>`
      · :doc:`L13 </lectures/lecture13/l13_index>`

   Enum
      A schema field that lists the only values it may take. :doc:`L9
      </lectures/lecture9/l9_index>`

   Environment variable
      A name and value the shell hands to every program it starts; the place
      to keep an API key out of the code. :doc:`Pre-read </preread/index>`

   EternalGuard
      A py_trees decorator that checks a condition before every tick of its
      child and stops the child when the condition fails. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Executive layer
      The middle layer of the three-layer architecture. It runs the plan step
      by step: it calls skills, watches results, and retries or reports
      failure. The behavior tree in this course. :doc:`L2
      </lectures/lecture2/l2_index>`

   Executor (plan)
      The code that runs a plan: it builds a behavior tree from the plan and
      ticks it. :doc:`L7 </lectures/lecture7/l7_index>`

   Executor (ROS 2)
      Runs a node's callbacks, on one thread or several. Not the same thing as
      a plan executor. :doc:`L1 </lectures/lecture1/l1_index>`

   Expected effect
      The change an action should make, which the orchestrator checks against
      fresh observations. :doc:`L9 </lectures/lecture9/l9_index>`


.. _glossary-f:

F
=

.. glossary::

   Fast Downward
      The classical planner used in L6 and GP3. Its translator grounds the
      PDDL, keeping only the ground actions that can ever apply, then its
      search finds a plan. :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3
      </assignments/gp3>`

   Few-shot example
      A short worked decision in the prompt that shows the model the expected
      output format. :doc:`L8 </lectures/lecture8/l8_index>`

   Filler
      What a frame's slot holds: a value or a link to another frame. :doc:`L3
      </lectures/lecture3/l3_index>`

   Fine-tuning
      More training of a trained model, on a smaller set of data for a new
      robot or task. :doc:`L13 </lectures/lecture13/l13_index>`

   Finite state machine
      A robot program that is in one state at a time and moves between states
      by transitions written by hand. :doc:`L4 </lectures/lecture4/l4_index>`

   Frame (knowledge representation)
      A description of a kind of object as a set of named slots, with fillers,
      defaults and inheritance. Used to model ARIAC cells, kits and modules.
      :doc:`L3 </lectures/lecture3/l3_index>`


.. _glossary-g:

G
=

.. glossary::

   Global recovery
      Recovery by the planner or the LLM agent, which makes a new plan or
      takes a new goal. :doc:`L11 </lectures/lecture11/l11_index>`

   Groot2
      The editor and monitor for BehaviorTree.CPP trees. :doc:`L7
      </lectures/lecture7/l7_index>`

   Ground action
      An action name with its arguments filled in by real objects, such as
      (pick-from-tester inspection_robot_2 c3 tester1). :doc:`L7
      </lectures/lecture7/l7_index>`

   Ground truth
      The true values a metric compares against. For cell defects, ARIAC
      prints them when launched with log_cell_info:=true, a cheat tool for
      practice runs only. :doc:`L12 </lectures/lecture12/l12_index>` ·
      :doc:`L13 </lectures/lecture13/l13_index>`

   Grounding
      Basing the agent's decisions on what a camera sees, through a VLM's
      checked record. :doc:`L9 </lectures/lecture9/l9_index>`

   Guard, act, verify, update
      The four leaves of one plan step: check the preconditions on the
      blackboard, send the goal, check the effect in the factory, then write
      the effects. :doc:`L7 </lectures/lecture7/l7_index>`


.. _glossary-h:

H
=

.. glossary::

   Hang
      A skill that stays RUNNING and never returns SUCCESS or FAILURE. A
      Timeout decorator turns it into a failure. :doc:`L11
      </lectures/lecture11/l11_index>`

   Heuristic
      An estimate of how many actions a state is from the goal, used to order
      a planner's search. An admissible heuristic never overestimates.
      :doc:`L6 </lectures/lecture6/l6_index>`

   Hybrid design
      The LLM picks goals and PDDL plans the steps, or PDDL runs the normal
      flow and the LLM handles replanning triggers. :doc:`L9
      </lectures/lecture9/l9_index>`


.. _glossary-i:

I
=

.. glossary::

   Inheritance
      A more specific frame takes the slots of a more general one. :doc:`L3
      </lectures/lecture3/l3_index>`

   Inspection bonuses
      ARIAC's speed bonus, 500 x (1 - g / 4 s) with g the average time from a
      cell's spawn to its report, and its classification bonus, 500 x the
      share of defective cells whose report matches every defect in type, z
      (within 5 mm) and theta (within 0.26 rad). :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Inspection door
      The ARIAC gate that lets a cell pass only after a passing inspection
      report for it was submitted. Otherwise it pushes the cell into the
      inspection bin. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`GP1
      </assignments/gp1>`

   Inspection report
      The report your system submits for each cell in ARIAC 2025 Task 1:
      whether the cell passed, with an optional defect type and location.
      :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L5
      </lectures/lecture5/l5_index>`

   Intrinsic matrix
      The 3 by 3 matrix K of a camera's focal lengths (fx, fy, in pixels) and
      principal point (cx, cy, the pixel where the optical axis meets the
      image), sent in CameraInfo.k. :doc:`L10 </lectures/lecture10/l10_index>`

   Invented object
      A name in an LLM reply (a cell, slot, AGV or order ID) that does not
      exist in the factory. :doc:`L12 </lectures/lecture12/l12_index>`


.. _glossary-j:

J
=

.. glossary::

   JSON Schema
      A JSON document that describes the fields and values another JSON
      document may have. A validator checks a record against it and lists
      every rule the record breaks. :doc:`L3 </lectures/lecture3/l3_index>` ·
      :doc:`L8 </lectures/lecture8/l8_index>` · :doc:`GP4 </assignments/gp4>`

   JSON-RPC 2.0
      The request and response message format MCP uses. :doc:`L8
      </lectures/lecture8/l8_index>`


.. _glossary-k:

K
=

.. glossary::

   Kit
      In ARIAC 2025, four battery cells on an AGV tray. Each cell must be in
      range and free of defects, and the kit's total voltage must be inside
      the kit voltage window. :doc:`L1 </lectures/lecture1/l1_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>`

   Kit voltage window
      The range a kit's total voltage must fall in: 4 x nominal voltage plus
      or minus 0.15 V. For Li-Ion cells, 14.25 V to 14.55 V. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L9 </lectures/lecture9/l9_index>`

   Knowledge representation
      How a system writes down what it knows about the world, the task and
      itself, in a form programs can read and check. :doc:`L3
      </lectures/lecture3/l3_index>`


.. _glossary-l:

L
=

.. glossary::

   Latency
      The time from sending a request to getting its answer. Latency per
      decision is the time from an observation to a validated decision.
      :doc:`L8 </lectures/lecture8/l8_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Launch file
      A file that starts several ROS 2 nodes at once, each with its own
      parameters. :doc:`Pre-read </preread/index>`

   Leaf
      A behavior tree node that does the work. An action leaf runs a skill or
      calls a service; a condition leaf checks a fact and answers at once.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Lidar
      A sensor that measures the distance along each ray of a grid of angles,
      giving one 3D point per ray that hits something in range. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`GP2 </assignments/gp2>`

   Lifecycle node
      A ROS 2 managed node with explicit states (unconfigured, inactive,
      active, finalized) and transitions between them, for predictable
      start-up and shutdown. :doc:`Pre-read </preread/index>`

   LLM
      Large language model. It takes a list of messages and returns text,
      keeps nothing between calls, and can answer the same messages
      differently. In this course, the decision part of the GP4 agent.
      :doc:`L8 </lectures/lecture8/l8_index>`

   Local recovery
      Recovery in the skill and the behavior tree (retry, timeout, another
      branch) that leaves the plan unchanged. :doc:`L11
      </lectures/lecture11/l11_index>`

   LoRA
      Low-rank adaptation, a lighter way to fine-tune a large model. :doc:`L13
      </lectures/lecture13/l13_index>`


.. _glossary-m:

M
=

.. glossary::

   MCP
      Model Context Protocol, an open protocol between agent applications and
      servers that provide tools, resources and prompts. A host (the AI
      application) runs one client per server; messages use JSON-RPC 2.0 over
      stdio or Streamable HTTP. :doc:`L8 </lectures/lecture8/l8_index>`

   Measurement science
      The work of making a number trustworthy: a defined metric, a source of
      truth, and a known run-to-run variation. :doc:`L12
      </lectures/lecture12/l12_index>`

   Memory (behavior tree)
      With memory, a composite's next tick resumes at the child that was
      running; without it, every tick starts at the first child. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Mock skill
      A small Python stand-in for a course skill or an ARIAC interface, used
      to run demos without ROS or the simulator. :doc:`L7
      </lectures/lecture7/l7_index>`

   Module
      In ARIAC 2025, four cells in a bottom and a top shell, joined by six
      welds. :doc:`L1 </lectures/lecture1/l1_index>`

   MoveIt 2
      The ROS 2 motion planning framework. The course skills package uses it
      to plan the arms' motions, below the behavior tree. :doc:`L10
      </lectures/lecture10/l10_index>`

   MoveItPy and MoveItCpp
      MoveIt 2's Python interface, and the C++ interface it calls inside the
      same process, with no ROS actions or services in between. move_group is
      the separate node that offers the same parts over ROS. :doc:`L10
      </lectures/lecture10/l10_index>`


.. _glossary-n:

N
=

.. glossary::

   Node (ROS 2)
      One program that takes part in the ROS 2 graph. :doc:`Pre-read
      </preread/index>` · :doc:`L1 </lectures/lecture1/l1_index>`

   Nominal voltage
      The voltage a cell type is meant to have: Li-Ion 3.6 V, Ni-MH 1.2 V.
      :doc:`L1 </lectures/lecture1/l1_index>`

   Numeric fluent
      A PDDL 2.1 function with a number value, such as a kit's total voltage,
      that actions can change. Fast Downward does not support them. :doc:`L6
      </lectures/lecture6/l6_index>`


.. _glossary-o:

O
=

.. glossary::

   Observed, inferred and unknown facts
      Facts read from an ARIAC interface; facts the team works out; facts no
      ARIAC interface gives. :doc:`L3 </lectures/lecture3/l3_index>`

   OMPL
      The Open Motion Planning Library, which holds MoveIt's sampling-based
      planners such as RRT-Connect, PRM and RRTstar. :doc:`L10
      </lectures/lecture10/l10_index>`

   Ontology
      The classes, relations and instances of a domain, written so software
      can check that a statement makes sense. :doc:`L3
      </lectures/lecture3/l3_index>`

   Optical frame
      A camera's second frame, named with the _optical suffix: z forward, x
      right, y down (REP 103). :doc:`L10 </lectures/lecture10/l10_index>`

   Optimal and satisficing search
      Optimal search returns a shortest plan (A* with an admissible
      heuristic), possibly slowly; satisficing search returns a plan quickly,
      not always the shortest. :doc:`L6 </lectures/lecture6/l6_index>`

   Orchestrator
      Your team's code that runs the agent loop and owns the tools, checks and
      logs. The LLM never sends a ROS goal itself. :doc:`L8
      </lectures/lecture8/l8_index>`

   OWL
      The W3C Web Ontology Language, for writing ontologies. :doc:`L3
      </lectures/lecture3/l3_index>`


.. _glossary-p:

P
=

.. glossary::

   Package (ROS 2)
      The unit ROS 2 builds and installs: a folder with a package.xml that
      names it and its dependencies. :doc:`Pre-read </preread/index>`

   Parallel
      A behavior tree composite that ticks all its children every tick, fails
      if any fails, and succeeds as its policy says (SuccessOnAll,
      SuccessOnOne, SuccessOnSelected). With synchronise True, the default, it
      skips children that already succeeded. :doc:`L4
      </lectures/lecture4/l4_index>`

   Parameter (ROS 2)
      A named setting of one node, declared with a default value, that can be
      set at start-up without changing the code. :doc:`Pre-read
      </preread/index>`

   Parameterized grasp
      A gripper target computed as the part's frame plus a fixed offset for
      that part type. :doc:`L10 </lectures/lecture10/l10_index>`

   PDDL
      Planning Domain Definition Language. A planning problem is written as a
      domain (types, predicates and actions with preconditions and effects)
      and a problem (objects, initial state and goal). :doc:`L6
      </lectures/lecture6/l6_index>`

   Perception
      Turning sensor data into facts the system can use, such as a dent's
      location on a cell. :doc:`L5 </lectures/lecture5/l5_index>`

   Physical AI
      AI systems that perceive, reason and act in the physical world, such as
      robots and self-driving cars. It covers both learned models that produce
      actions (VLAs) and agents that run robot skills, which is what this
      course builds. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

   Pilz industrial motion planner
      A MoveIt planner for the standard industrial motions PTP (point to point
      in joint space), LIN (a straight line) and CIRC (an arc), with no random
      sampling: the same request gives the same motion. :doc:`L10
      </lectures/lecture10/l10_index>`

   Pinhole camera model
      A camera treated as one point that every ray passes through, so a point
      at (X, Y, Z) in the optical frame lands at pixel u = fx X/Z + cx, v = fy
      Y/Z + cy. :doc:`L10 </lectures/lecture10/l10_index>`

   Plan
      A sequence of actions that turns the initial state into a state where
      the goal holds. :doc:`L6 </lectures/lecture6/l6_index>`

   Plan failure
      The plan is invalid, such as an LLM plan that puts a fifth cell on a
      four-slot tray. A check before execution catches it. :doc:`L11
      </lectures/lecture11/l11_index>`

   Plan length and plan cost
      The number of actions in a plan, and the sum of action costs if the
      domain defines them (or the time the plan takes to run). :doc:`L12
      </lectures/lecture12/l12_index>`

   Plan validity
      Every action's preconditions hold in the state where it runs, and the
      plan reaches the goal. A plan validator replays the plan and names the
      first action whose precondition fails. :doc:`L6
      </lectures/lecture6/l6_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Plan-and-execute
      The LLM writes a full plan once, and the executor asks for a new one
      only when a replanning trigger fires. Contrasted with ReAct. :doc:`L8
      </lectures/lecture8/l8_index>`

   Plan-to-BT factory
      Code that looks up each plan action's name in a registry and calls its
      builder, in plan order, to make one subtree per action. :doc:`L7
      </lectures/lecture7/l7_index>` · :doc:`GP3 </assignments/gp3>`

   Planning pipeline
      In MoveIt, request adapters, then a planner plugin, then response
      adapters. :doc:`L10 </lectures/lecture10/l10_index>`

   Planning scene
      MoveIt's picture of the robot's current joint state and the collision
      objects around it. :doc:`L10 </lectures/lecture10/l10_index>`

   Point cloud
      A set of 3D points a lidar measures on the surfaces it sees. In ROS 2 it
      arrives as a sensor_msgs/PointCloud2 message. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`GP2 </assignments/gp2>`

   PointCloud2
      The ROS 2 message for a point cloud: packed bytes plus their layout
      (fields, point_step, row_step). :doc:`L5 </lectures/lecture5/l5_index>`

   Port
      A BehaviorTree.CPP node's typed input or output. {key} in the XML
      connects it to a blackboard entry. :doc:`L7
      </lectures/lecture7/l7_index>`

   Precision
      TP / (TP + FP): the share of the detector's calls that were right.
      :doc:`L5 </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>` · :doc:`L13
      </lectures/lecture13/l13_index>` · :doc:`GP2 </assignments/gp2>`

   Predicate
      A fact that is true or false in a PDDL state, such as (hand-free
      inspection_robot_1). :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3
      </assignments/gp3>`

   PRM
      Probabilistic roadmap: builds a roadmap of free configurations once and
      reuses it for many queries. :doc:`L10 </lectures/lecture10/l10_index>`

   Problem generator
      Code that writes a new PDDL problem file from the current factory state.
      :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3 </assignments/gp3>`

   py_trees and py_trees_ros
      The Python behavior tree library, and its ROS 2 integration, which runs
      the tree as a node ticked by a timer. Used for the executive layer from
      GP1 on. :doc:`L4 </lectures/lecture4/l4_index>`


.. _glossary-q:

Q
=

.. glossary::

   QoS profile
      Quality of Service settings that decide how messages are delivered on a
      ROS 2 topic: reliability, durability, history and depth. :doc:`L1
      </lectures/lecture1/l1_index>`


.. _glossary-r:

R
=

.. glossary::

   Re-prompt
      Asking the model again, once, with the exact error message of the check
      that failed. :doc:`L11 </lectures/lecture11/l11_index>`

   ReAct
      An agent pattern where each iteration is one reasoning step and one tool
      call, and the model sees each result before choosing the next step.
      :doc:`L8 </lectures/lecture8/l8_index>`

   Reactive architecture
      Sensor readings map straight to actions, with no world model. :doc:`L2
      </lectures/lecture2/l2_index>`

   Reactive layer
      The bottom layer of the three-layer architecture: fast control close to
      the hardware, such as controllers, grippers and sensors. :doc:`L2
      </lectures/lecture2/l2_index>`

   Recall
      TP / (TP + FN): the share of real defects the detector found. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>` · :doc:`L13
      </lectures/lecture13/l13_index>` · :doc:`GP2 </assignments/gp2>`

   Recovery rate
      Failures recovered without operator help, divided by failures detected.
      :doc:`L12 </lectures/lecture12/l12_index>`

   Registry
      A dictionary from each plan action name to the builder function for that
      action. :doc:`L7 </lectures/lecture7/l7_index>`

   Replanning trigger
      An event that stops the plan and asks for a new one, such as an
      out-of-range voltage, a tester malfunction or a skill that still fails
      after the tree's retries. :doc:`L7 </lectures/lecture7/l7_index>` ·
      :doc:`GP3 </assignments/gp3>`

   Residual
      For a lidar point on a cell, its distance from the fitted cell axis
      minus the cell radius (10.5 mm). Negative is set in (a dent or scratch);
      positive sticks out (a bulge). :doc:`L5 </lectures/lecture5/l5_index>`

   Retry decorator
      Runs its child again after a failure, up to num_failures failures, then
      returns FAILURE. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L7
      </lectures/lecture7/l7_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Robot foundation model
      A model trained once on data from many tasks and robots, then adapted to
      a new robot or task with less data. :doc:`L13
      </lectures/lecture13/l13_index>`

   ROS_DOMAIN_ID
      The number that separates ROS 2 groups on one network: only nodes with
      the same ID see each other. The default is 0. :doc:`Pre-read
      </preread/index>`

   RRT-Connect
      A sampling-based planner that grows two random trees, from the start and
      from the goal, until they meet. :doc:`L10
      </lectures/lecture10/l10_index>`

   RRTstar
      A sampling-based planner that grows one tree and keeps shortening its
      path while planning time remains. :doc:`L10
      </lectures/lecture10/l10_index>`

   Run score
      ARIAC's score for one run: the base score plus bonuses minus penalties.
      :doc:`L12 </lectures/lecture12/l12_index>`


.. _glossary-s:

S
=

.. glossary::

   Safe point
      A place to stop a plan without leaving the robots in an unknown state:
      between subtrees, or after a cancelled skill retreats. :doc:`L7
      </lectures/lecture7/l7_index>`

   Sampling-based planner
      A planner that picks random collision-free configurations and links them
      into a path. Two runs can give different paths. :doc:`L10
      </lectures/lecture10/l10_index>`

   Schema-valid rate
      The share of LLM replies that pass the JSON schema on the first try, and
      after one re-prompt. :doc:`L12 </lectures/lecture12/l12_index>`

   Scripted stand-in model
      A fake model that returns replies written in advance, so a demo repeats
      exactly. A real model's answers vary. :doc:`L8
      </lectures/lecture8/l8_index>` · :doc:`L9 </lectures/lecture9/l9_index>`
      · :doc:`L13 </lectures/lecture13/l13_index>`

   Second source
      Another way to learn the same fact, used to cross-check a VLM's output,
      such as /agvN/tray_status or a recorded tester voltage. :doc:`L9
      </lectures/lecture9/l9_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Seed
      The number that starts a random number generator. The same seed repeats
      a run exactly. :doc:`L2 </lectures/lecture2/l2_index>`

   Selection step
      Python code that picks which cells go in which slots so the kit total
      lands inside the kit voltage window. Its result goes to PDDL as facts.
      :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3 </assignments/gp3>`

   Selector
      A behavior tree composite that ticks its children in order and succeeds
      at the first success; it fails only if all fail. Also called a fallback.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Semantic check
      A check that needs the factory's current state, which a schema cannot
      express, such as whether a slot is free. :doc:`L8
      </lectures/lecture8/l8_index>`

   Sense-plan-act
      An architecture where the robot senses, builds a world model, plans,
      then acts, in that order. :doc:`L2 </lectures/lecture2/l2_index>`

   Sensor budget
      In ARIAC 2025, $9600 for the sensors a team places. Spending less earns
      a bonus; spending more costs points. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   Sensor failure
      A device gives no data or wrong data, such as a voltage tester
      malfunction. :doc:`L11 </lectures/lecture11/l11_index>`

   Sequence
      A behavior tree composite that ticks its children in order: it fails at
      the first failure, keeps running while a child runs, and succeeds when
      all succeed. :doc:`L4 </lectures/lecture4/l4_index>`

   Service (ROS 2)
      One request and one reply between a client and a server, defined by a
      .srv type. :doc:`Pre-read </preread/index>` · :doc:`L1
      </lectures/lecture1/l1_index>`

   Service client leaf
      A py_trees_ros leaf that returns SUCCESS when the reply arrives,
      whatever the reply says. Check the reply in a condition after it.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Skill
      One robot capability, offered as a ROS 2 action. It reports success or a
      failure reason and never retries a task on its own. :doc:`L2
      </lectures/lecture2/l2_index>`

   Slot (knowledge representation)
      A named part of a frame (Minsky's terminals). :doc:`L3
      </lectures/lecture3/l3_index>`

   Snapshot
      The tree's structure and every node's status at one moment, published by
      py_trees_ros as a ROS message. :doc:`L7 </lectures/lecture7/l7_index>`

   Spin
      To wait for events and run the matching callbacks until the node shuts
      down. :doc:`Pre-read </preread/index>` · :doc:`L1
      </lectures/lecture1/l1_index>`

   Standard error
      About how far chance moves a measured success rate between sets of n
      runs: sqrt(p(1 - p) / n). :doc:`L12 </lectures/lecture12/l12_index>`

   State (planning)
      The set of facts that are true at one moment. :doc:`L6
      </lectures/lecture6/l6_index>`

   Stateless API
      Each call stands alone, so the program must send the full conversation
      history on every call. :doc:`Pre-read </preread/index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   Status (behavior tree)
      What a node returns when ticked: SUCCESS, FAILURE, RUNNING (needs more
      ticks) or INVALID (not run yet, or stopped). :doc:`L4
      </lectures/lecture4/l4_index>`

   Stop condition
      A check in code that ends the agent loop: the goal is reached, a step
      limit, too many invalid outputs in a row, a time limit, or an operator
      stop. :doc:`L8 </lectures/lecture8/l8_index>`

   STRIPS
      The planning model of Fikes and Nilsson (1971): states are sets of
      facts, and actions have preconditions and effects. PDDL writes it down.
      :doc:`L6 </lectures/lecture6/l6_index>`

   Structured output
      An LLM answer in a fixed format, usually JSON that follows a schema, so
      a program can check it and use it. :doc:`L8
      </lectures/lecture8/l8_index>`

   Subsumption architecture
      Brooks, 1986: layers of behaviors run in parallel; a higher layer
      suppresses a lower layer's inputs and inhibits its outputs while the
      lower layer keeps running. :doc:`L2 </lectures/lecture2/l2_index>`

   Success rate
      k / n, the share of n runs on which the system completes the trial.
      :doc:`L12 </lectures/lecture12/l12_index>`

   System message
      The part of every LLM call that stays fixed during a run: the role, the
      factory facts, the rules and the output format. The user message carries
      the current state and goal. :doc:`L8 </lectures/lecture8/l8_index>`


.. _glossary-t:

T
=

.. glossary::

   Team charter
      A one-page agreement each team writes before L3: owners and backups,
      meetings and Git, what happens when someone goes quiet, and AI use.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Team configuration file
      The YAML file where a team declares its sensors (name, type, pose,
      rate). ARIAC checks it at startup. :doc:`L5
      </lectures/lecture5/l5_index>`

   Temperature
      An API setting that changes how much a model's answers vary. No setting
      makes the output safe without checks. :doc:`L8
      </lectures/lecture8/l8_index>`

   TF2
      The ROS 2 library that keeps a tree of coordinate frames, with a
      transform between each parent and child, and answers where a frame is
      relative to another at a given time. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L10
      </lectures/lecture10/l10_index>`

   Three-layer architecture
      A deliberative layer plans, a reactive layer controls, and an executive
      layer between them chooses the next skill and reacts to failures (Gat:
      deliberator, sequencer, controller). The frame for the course's group
      projects. :doc:`L2 </lectures/lecture2/l2_index>`

   Tick
      One pass through a behavior tree from the root down. Each node visited
      returns a status. :doc:`L4 </lectures/lecture4/l4_index>`

   Tick trace
      A log line for every status change of a plan step, with the tick number.
      :doc:`L7 </lectures/lecture7/l7_index>`

   Timeout decorator
      Fails its child and stops it if the child is still running after a set
      duration, so a hang becomes a failure. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L7 </lectures/lecture7/l7_index>`
      · :doc:`L11 </lectures/lecture11/l11_index>`

   Token
      A piece of text the model reads or writes. Calls are paid for in tokens.
      :doc:`L8 </lectures/lecture8/l8_index>`

   Tool
      A function the agent may call, given to the model as a name, a
      description and an input schema. In this course, robot skills and
      factory queries. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   Tool calling
      The model's way of asking to run a tool with JSON arguments, instead of
      only writing text. The orchestrator checks and runs the call and sends
      the result back. Also called function calling. :doc:`L8
      </lectures/lecture8/l8_index>`

   Topic
      A named channel where publishers send messages of one type and
      subscribers receive them, with no reply. :doc:`Pre-read
      </preread/index>` · :doc:`L1 </lectures/lecture1/l1_index>`

   Transform
      Where one frame sits in another, as a translation and a rotation. A
      static transform never changes (a tray slot on its AGV); a moving one is
      sent again as it changes (an AGV in the world). :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L10
      </lectures/lecture10/l10_index>`

   Transport (MCP)
      How MCP messages travel between client and server: stdio (the client
      starts the server as a child process) or Streamable HTTP (the client
      posts each message to the server's endpoint). :doc:`Pre-read
      </preread/index>` · :doc:`L8 </lectures/lecture8/l8_index>`

   True and false positives and negatives
      The four outcomes of a detector for one class: TP (flagged and
      defective), FP (flagged but good), FN (missed), TN (correctly passed).
      :doc:`L5 </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

   Two-system design
      A slow reasoning model above a fast control policy. :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`


.. _glossary-u:

U
=

.. glossary::

   Unified Planning Framework
      UPF, a Python library that reads or builds planning problems and calls
      planners and validators through one interface. :doc:`L6
      </lectures/lecture6/l6_index>`

   Unseen trial
      A trial file no team has seen, with its own ID, seed and challenge
      times, used in the final demo. :doc:`Final demo
      </assignments/final_demo>`


.. _glossary-v:

V
=

.. glossary::

   Validator
      Code that checks a record against a schema and lists every rule it
      breaks. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   VLA
      Vision-language-action model: a learned model that maps camera images
      and language straight to robot actions. Surveyed in this course, not
      built. :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

   VLM
      Vision-language model: a model that takes images and text in one prompt
      and returns text, for example a description of a tray. Used in GP4 to
      ground the agent's decisions in what the cameras see. :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L9 </lectures/lecture9/l9_index>`


.. _glossary-w:

W
=

.. glossary::

   Watcher
      Code that reads a device's messages and decides at any moment whether
      the device is up (giving valid readings) or down. :doc:`L11
      </lectures/lecture11/l11_index>`

   Workspace (ROS 2)
      A folder that holds ROS 2 packages in src, and the build, install and
      log folders that colcon creates. :doc:`Pre-read </preread/index>`

   World drift
      The factory no longer matches what the plan assumed, and no single
      action failed, such as a high-priority order arriving in the middle of a
      kit. :doc:`L9 </lectures/lecture9/l9_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   World model
      Two meanings. In robot architecture, the robot's own record of what the
      world looks like (L2, L3). In learned AI, a model that predicts how a
      scene will change, used to make training data and test policies in
      simulation (L13). :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`


.. _glossary-z:

Z
=

.. glossary::

   Zone lock
      A rule that lets one robot at a time into a shared area, such as the
      voltage testers. :doc:`L10 </lectures/lecture10/l10_index>`
