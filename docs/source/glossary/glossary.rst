====================================================
Glossary
====================================================

:ref:`A <glossary-a>` · :ref:`B <glossary-b>` · :ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`E <glossary-e>` · :ref:`F <glossary-f>` · :ref:`I <glossary-i>` · :ref:`K <glossary-k>` · :ref:`L <glossary-l>` · :ref:`M <glossary-m>` · :ref:`O <glossary-o>` · :ref:`P <glossary-p>` · :ref:`Q <glossary-q>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` · :ref:`T <glossary-t>` · :ref:`V <glossary-v>` · :ref:`W <glossary-w>`

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


.. _glossary-a:

A
=

.. glossary::

   Agent loop
      The loop an orchestrator runs around an LLM: observe the world, ask the
      model what to do next, run the tool it chose, feed the result back, and
      repeat until the goal or a stop condition is reached. The agent behavior
      comes from the loop, not from the model alone. See Orchestrator. L8

   AGV
      Automated Guided Vehicle. In ARIAC 2025, one of four mobile platforms
      that carry a kit tray between the inspection, assembly, shipping and
      recycling stations. L1

   ARIAC
      Agile Robotics for Industrial Automation Competition, a NIST simulation
      testbed and competition. ENPM663 uses ARIAC 2025, a simulated EV battery
      factory with inspection, kit building and module construction. L1


.. _glossary-b:

B
=

.. glossary::

   Behavior tree
      A tree of nodes, built from composites (sequence, selector, parallel)
      and decorators, that a robot ticks to decide which action runs. The
      standard executive layer for robot task execution in industry. L4 · L7

   Blackboard
      A shared key-value store that behavior tree nodes read from and write
      to, so nodes can pass state without being wired to each other. L4


.. _glossary-c:

C
=

.. glossary::

   Closed-loop replanning
      Detecting that execution has drifted from the expected world state and
      asking the planner (classical or LLM) for a new plan from the updated
      observations, instead of running a stale plan. L9

   Course skills package
      The Python ROS 2 package the course provides with GP1. It offers skills
      such as picking a cell, placing it and moving an AGV, built on MoveIt 2
      and the ARIAC robot actions. Behavior trees call the skills from GP1,
      and the LLM agent calls them as tools in GP4. L2 · L10


.. _glossary-d:

D
=

.. glossary::

   Decorator
      A behavior tree node with one child that changes the child's result or
      how it runs, such as inverter, retry or timeout. L4


.. _glossary-e:

E
=

.. glossary::

   Embodied-reasoning model
      A vision-language model trained to answer spatial questions about a
      scene (where an object is, how to grasp it) and to plan for a robot,
      often by calling tools. Google DeepMind's Gemini Robotics-ER is one. The
      final demo uses one for a perception step. L9 · L13

   Executor (ROS 2)
      The ROS 2 component that runs a node's callbacks, on one thread or
      several. Not the same thing as a plan executor. L1


.. _glossary-f:

F
=

.. glossary::

   Frame (knowledge representation)
      A structured representation with named slots and fillers, optionally
      with default values and inheritance, used to model things such as ARIAC
      cells, kits and modules. L3


.. _glossary-i:

I
=

.. glossary::

   Inspection report
      The result your system submits for each cell in ARIAC 2025 Task 1:
      whether the cell passed, and the list of its defects (dent, scratch,
      bulge). L5


.. _glossary-k:

K
=

.. glossary::

   Kit
      In ARIAC 2025, four battery cells placed on an AGV tray. Each cell must
      be free of defects and within the voltage range, and the kit's total
      voltage must be within a tolerance. L1 · L3

   Knowledge representation
      The formalisms (frames, ontologies, hierarchical world models) used to
      represent the world, the task and the robot's state so that classical
      planners, LLMs and VLMs can all use them. L3


.. _glossary-l:

L
=

.. glossary::

   Lifecycle node
      A ROS 2 managed node with explicit states (unconfigured, inactive,
      active, finalized) and transitions between them, used for predictable
      start-up and shutdown. L1

   LLM
      Large Language Model. In this course, the reasoning core of an agent
      that plans the factory's tasks. L8


.. _glossary-m:

M
=

.. glossary::

   MCP
      Model Context Protocol, the standard way, since 2024, to expose tools
      and context to an LLM across agent frameworks. L8

   MoveIt 2
      The ROS 2 motion planning framework. The course skills package uses it
      to plan pick and place motions, below the behavior tree. L10


.. _glossary-o:

O
=

.. glossary::

   Ontology
      A formal specification of classes, relations and instances, used to
      connect what perception reports to the vocabulary the planner uses. L3

   Orchestrator
      The program that runs the agent loop: it builds the prompt, calls the
      LLM, runs the tool the LLM chose, checks the result and decides whether
      to continue. The LLM itself keeps no state between calls. L8


.. _glossary-p:

P
=

.. glossary::

   PDDL
      Planning Domain Definition Language, the classical way to describe a
      planning problem as a domain (predicates and actions) and a problem
      (initial state and goal). L6

   Physical AI
      AI systems that perceive, reason and act in the physical world, such as
      robots and self-driving cars. The term covers both learned models that
      produce actions (VLAs) and agents that orchestrate robot skills, which
      is the part this course builds. L1 · L13

   Plan-and-execute
      An agent pattern that produces a full plan first and then runs it. The
      LLM counterpart of a classical PDDL planner, contrasted with ReAct. L8

   py_trees_ros
      The Python behavior tree library, integrated with ROS 2, used in this
      course for task execution. L4


.. _glossary-q:

Q
=

.. glossary::

   QoS
      Quality of Service. ROS 2 policies (reliability, durability, history)
      that set how messages are delivered on a topic. L1


.. _glossary-r:

R
=

.. glossary::

   ReAct
      An agent pattern that interleaves reasoning and acting: the model
      reasons, calls a tool, reads the result and adjusts, one step at a time.
      L8


.. _glossary-s:

S
=

.. glossary::

   Sensor budget
      In ARIAC 2025, the amount a team may spend on the sensors it places.
      Each sensor has a cost set by its type and grade; spending under the
      budget earns a bonus and spending over it costs a penalty. L5

   Structured output
      Constraining an LLM's response to a schema, usually JSON, so a program
      can check it and use it. L8


.. _glossary-t:

T
=

.. glossary::

   TF2
      The ROS 2 transform library that tracks coordinate frames over time and
      answers questions about the transform between two frames. L1 · L10

   Three-layer architecture
      The standard robot architecture: a deliberative planner, an executive (a
      behavior tree) and a reactive control layer. AI plugs into specific
      layers instead of replacing the architecture. L2

   Tool calling
      The way an LLM calls functions (tools) described by a schema, instead of
      only producing text. Also called function calling. L8


.. _glossary-v:

V
=

.. glossary::

   VLA
      Vision-Language-Action model. A learned model that maps camera images
      and language straight to robot actions. Surveyed in this course, not
      built. L2 · L13

   VLM
      Vision-Language Model. A model that takes an image and text and answers
      in text, for example by describing a scene. Used here to ground the
      agent's decisions in what the cameras see. L9


.. _glossary-w:

W
=

.. glossary::

   World model
      A learned model that predicts how a scene will change, used to generate
      training data and to test robot policies in simulation before they reach
      a robot. L13
