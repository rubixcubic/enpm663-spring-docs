====================================================
Glossary
====================================================

This glossary covers the key terms of ENPM663, grouped by the lecture or
project page that introduces them and sorted A to Z within each. Click a
lecture in the right panel to jump to its terms. A term that a later lecture
or project uses again is listed at the end of that section.

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
      <div id="glossary-letters" aria-label="Show the terms that start with a letter"
           style="display: flex; flex-wrap: wrap; gap: 0.3em; margin: 0 0 1.4em 0;"></div>

      <style>
        #glossary-letters button {
          min-width: 2em;
          padding: 0.15em 0.45em;
          font: inherit;
          font-size: 0.95em;
          color: var(--pst-color-primary, #2f6fb5);
          background: transparent;
          border: 1px solid var(--pst-color-border, #ccc);
          border-radius: 4px;
          cursor: pointer;
        }
        #glossary-letters button.active {
          color: var(--pst-color-background, #fff);
          background: var(--pst-color-primary, #2f6fb5);
          border-color: var(--pst-color-primary, #2f6fb5);
        }
      </style>

      <script>
      (function () {
        /* The search box filters by text; a letter button shows the terms
           that start with that letter, across all lectures. Both apply
           together. A lecture section with no matching term is hidden. */
        function initGlossarySearch() {
          var input   = document.getElementById('glossary-search');
          var count   = document.getElementById('glossary-search-count');
          var letters = document.getElementById('glossary-letters');
          if (!input) return;
          var letter = '';

          function firstLetter(dt) {
            var m = dt.textContent.trim().match(/[a-z]/i);
            return m ? m[0].toUpperCase() : '';
          }

          /* One button per letter that starts a term, plus "All". */
          var present = {};
          document.querySelectorAll('dl.glossary dt').forEach(function (dt) {
            var c = firstLetter(dt);
            if (c) present[c] = true;
          });
          function addButton(label, value) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.textContent = label;
            btn.dataset.letter = value;
            if (value === '') btn.classList.add('active');
            btn.addEventListener('click', function () {
              letter = value;
              letters.querySelectorAll('button').forEach(function (b) {
                b.classList.toggle('active', b.dataset.letter === letter);
              });
              run();
            });
            letters.appendChild(btn);
          }
          addButton('All', '');
          Object.keys(present).sort().forEach(function (c) { addButton(c, c); });

          function run() {
            var query = input.value.trim().toLowerCase();
            var filtering = query !== '' || letter !== '';
            var visible = 0;

            document.querySelectorAll('dl.glossary dt').forEach(function (dt) {
              var match = (!query || dt.textContent.toLowerCase().indexOf(query) !== -1)
                       && (!letter || firstLetter(dt) === letter);
              dt.style.display = match ? '' : 'none';
              var node = dt.nextElementSibling;
              while (node && node.tagName === 'DD') {
                node.style.display = match ? '' : 'none';
                node = node.nextElementSibling;
              }
              if (match) visible++;
            });

            /* Each lecture section: hide it when nothing in it matches, and
               hide its "Also used here" line while a filter is on. */
            document.querySelectorAll('section > h2').forEach(function (h2) {
              var section = h2.parentElement;
              var dts = section.querySelectorAll('dl.glossary dt');
              var any = Array.prototype.some.call(dts, function (dt) {
                return dt.style.display !== 'none';
              });
              section.style.display = (!filtering || any) ? '' : 'none';
              section.querySelectorAll('dl.glossary').forEach(function (dl) {
                dl.style.display = (!filtering || any) ? '' : 'none';
              });
              section.querySelectorAll('p.glossary-also').forEach(function (p) {
                p.style.display = filtering ? 'none' : '';
              });
            });

            count.textContent = filtering
              ? (visible === 1 ? '1 term found' : visible + ' terms found')
              : '';
          }

          input.addEventListener('input', run);
          input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
          });
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initGlossarySearch);
        } else {
          initGlossarySearch();
        }
      })();
      </script>

----


.. _g-pre-read:

Pre-Read Material
=================

.. glossary::

   API key
      A secret string that identifies your account with a model provider.
      Anyone who holds it can make calls billed to you, so it lives in an
      environment variable, never in the code or the repository.
      :doc:`Pre-read </preread/index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   Callback
      A function you hand to ROS 2 that it runs when an event arrives, such as
      a message or a timer tick. :doc:`Pre-read </preread/index>` · :doc:`L1
      </lectures/lecture1/l1_index>`

   colcon
      The tool that builds every package in a ROS 2 workspace. :doc:`Pre-read
      </preread/index>`

   Context window
      The most tokens a model reads in one call. :doc:`Pre-read
      </preread/index>` · :doc:`L8 </lectures/lecture8/l8_index>`

   Environment variable
      A name and value the shell hands to every program it starts; the place
      to keep an API key out of the code. :doc:`Pre-read </preread/index>`

   Launch file
      A file that starts several ROS 2 nodes at once, each with its own
      parameters. :doc:`Pre-read </preread/index>`

   Lifecycle node
      A ROS 2 managed node with explicit states (unconfigured, inactive,
      active, finalized) and transitions between them, for predictable
      start-up and shutdown. :doc:`Pre-read </preread/index>`

   Node (ROS 2)
      One program that takes part in the ROS 2 graph. :doc:`Pre-read
      </preread/index>` · :doc:`L1 </lectures/lecture1/l1_index>`

   Package (ROS 2)
      The unit ROS 2 builds and installs: a folder with a package.xml that
      names it and its dependencies. :doc:`Pre-read </preread/index>`

   Parameter (ROS 2)
      A named setting of one node, declared with a default value, that can be
      set at start-up without changing the code. :doc:`Pre-read
      </preread/index>`

   ROS_DOMAIN_ID
      The number that separates ROS 2 groups on one network: only nodes with
      the same ID see each other. The default is 0. :doc:`Pre-read
      </preread/index>`

   Service (ROS 2)
      One request and one reply between a client and a server, defined by a
      .srv type. :doc:`Pre-read </preread/index>` · :doc:`L1
      </lectures/lecture1/l1_index>`

   Spin
      To wait for events and run the matching callbacks until the node shuts
      down. :doc:`Pre-read </preread/index>` · :doc:`L1
      </lectures/lecture1/l1_index>`

   Stateless API
      Each call stands alone, so the program must send the full conversation
      history on every call. :doc:`Pre-read </preread/index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   Topic
      A named channel where publishers send messages of one type and
      subscribers receive them, with no reply. :doc:`Pre-read
      </preread/index>` · :doc:`L1 </lectures/lecture1/l1_index>`

   Transport (MCP)
      How MCP messages travel between client and server: stdio (the client
      starts the server as a child process) or Streamable HTTP (the client
      posts each message to the server's endpoint). :doc:`Pre-read
      </preread/index>` · :doc:`L8 </lectures/lecture8/l8_index>`

   Workspace (ROS 2)
      A folder that holds ROS 2 packages in src, and the build, install and
      log folders that colcon creates. :doc:`Pre-read </preread/index>`


.. _g-l1:

L1: Course Overview and ROS 2 Refresher
=======================================

.. glossary::

   Action (ROS 2)
      A long request with feedback while it runs and a result at the end; the
      client may ask to cancel it. Teams move AGVs with ARIAC's /agvN/move
      action, which rejects cancel requests. :doc:`L1
      </lectures/lecture1/l1_index>`

   Agent
      A program that loops around an LLM: it observes the world, asks the
      model, calls a tool, checks the result and repeats. In this course the
      tools are robot skills. :doc:`L1 </lectures/lecture1/l1_index>` ·
      :doc:`L8 </lectures/lecture8/l8_index>`

   Agentic physical AI
      In this course, a robot system in which an AI agent decides what the
      robots do next, and robot skills carry out each decision in the physical
      world. Here, that world is the ARIAC factory, simulated in Gazebo.
      :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

   AGV
      Automated Guided Vehicle. ARIAC 2025 has three (agv1 to agv3). Each
      carries a tray with four slots between the inspection, assembly,
      shipping and recycling stations. :doc:`L1 </lectures/lecture1/l1_index>`

   ARIAC
      Agile Robotics for Industrial Automation Competition, a NIST simulation
      testbed and competition. ENPM663 uses ARIAC 2025, a simulated EV battery
      factory with cell inspection, kit building and module construction.
      :doc:`L1 </lectures/lecture1/l1_index>`

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

   Competition states
      The states an ARIAC trial moves through: PREPARING, READY, STARTED,
      ORDERS_COMPLETE, ENDED. :doc:`L1 </lectures/lecture1/l1_index>`

   Course skills package
      The Python ROS 2 package the course gives teams with GP1. Its skills are
      ROS 2 actions for the arms (pick, place) built on MoveIt 2. A skill
      reports success or a failure reason, accepts cancel, and never retries a
      task itself. AGVs are moved with ARIAC's own action, not a skill.
      :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L10
      </lectures/lecture10/l10_index>`

   Embodied-reasoning model
      A vision-language model trained to answer spatial questions about a
      scene, such as where an object is or how to grasp it. Google DeepMind's
      Gemini Robotics ER is one. In the final demo it judges cell defects from
      camera images. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L9 </lectures/lecture9/l9_index>`
      · :doc:`L13 </lectures/lecture13/l13_index>`

   Executor (ROS 2)
      Runs a node's callbacks, on one thread or several. Not the same thing as
      a plan executor. :doc:`L1 </lectures/lecture1/l1_index>`

   Inspection door
      The ARIAC gate that lets a cell pass only after a passing inspection
      report for it was submitted. Otherwise the door stays closed and the
      cell drops into the inspection bin. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`GP1 </assignments/gp1>`

   Inspection report
      The report your system submits for each cell in ARIAC 2025 Task 1:
      whether the cell passed, with an optional defect type and location. Your
      team decides it from lidar (GP2) and submits it as an
      InspectionReport.msg with SubmitInspectionReport.srv; ARIAC never sends
      an inspection result. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   Kit
      In ARIAC 2025, four battery cells on an AGV tray. Each cell must be in
      range and free of defects, and the kit's total voltage must be inside
      the kit voltage window. :doc:`L1 </lectures/lecture1/l1_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>`

   Kit voltage window
      The range a kit's total voltage must fall in: 4 x nominal voltage plus
      or minus 0.15 V. For Li-Ion cells, 14.25 V to 14.55 V. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L9 </lectures/lecture9/l9_index>`

   Module
      In ARIAC 2025, four cells in a bottom and a top shell, joined by six
      welds. :doc:`L1 </lectures/lecture1/l1_index>`

   Nominal voltage
      The voltage a cell type is meant to have: Li-Ion 3.6 V, Ni-MH 1.2 V.
      :doc:`L1 </lectures/lecture1/l1_index>`

   Physical AI
      AI systems that perceive, reason and act in the physical world, such as
      robots and self-driving cars. It covers both learned models that produce
      actions (VLAs) and agents that run robot skills, which is what this
      course builds. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

   QoS profile
      Quality of Service settings that decide how messages are delivered on a
      ROS 2 topic: reliability, durability, history and depth. :doc:`L1
      </lectures/lecture1/l1_index>`

   Sensor budget
      In ARIAC 2025, $9600 for the sensors a team places. Spending less earns
      a bonus; spending more costs points. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   TF2
      The ROS 2 library that keeps a tree of coordinate frames, with a
      transform between each parent and child, and answers where a frame is
      relative to another at a given time. :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L10
      </lectures/lecture10/l10_index>`

   Tool
      A function the agent may call, given to the model as a name, a
      description and an input schema. In this course, robot skills and
      factory queries. :doc:`L1 </lectures/lecture1/l1_index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   Transform
      Where one frame sits in another, as a translation and a rotation. A
      static transform never changes (a tray slot on its AGV); a moving one is
      sent again as it changes (an AGV in the world). :doc:`L1
      </lectures/lecture1/l1_index>` · :doc:`L10
      </lectures/lecture10/l10_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Callback" target="_blank" rel="noopener">Callback</a> (Pre-read), <a href="#term-Node-ROS-2" target="_blank" rel="noopener">Node (ROS 2)</a> (Pre-read), <a href="#term-Service-ROS-2" target="_blank" rel="noopener">Service (ROS 2)</a> (Pre-read), <a href="#term-Spin" target="_blank" rel="noopener">Spin</a> (Pre-read), <a href="#term-Topic" target="_blank" rel="noopener">Topic</a> (Pre-read).</p>


.. _g-l2:

L2: System Architectures for Agentic Robotics
=============================================

.. glossary::

   Architecture
      How a robot's software is split into parts, and how the parts pass
      decisions and data to each other. :doc:`L2
      </lectures/lecture2/l2_index>`

   Clean stop
      Stopping on purpose, with a reason, instead of going on with bad data.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Deadlock
      Each robot waits for the other, forever. :doc:`L2
      </lectures/lecture2/l2_index>`

   Deliberative layer
      The top layer of the three-layer architecture. It decides over a long
      horizon, such as which kit to build and which cells to use: the PDDL
      planner in GP3, the LLM agent in GP4. :doc:`L2
      </lectures/lecture2/l2_index>`

   Executive layer
      The middle layer of the three-layer architecture. It runs the plan step
      by step: it calls skills, watches results, and retries or reports
      failure. The behavior tree in this course. :doc:`L2
      </lectures/lecture2/l2_index>`

   Reactive architecture
      Sensor readings map straight to actions, with no world model. :doc:`L2
      </lectures/lecture2/l2_index>`

   Reactive layer
      The bottom layer of the three-layer architecture: fast control close to
      the hardware, such as controllers, grippers and sensors. :doc:`L2
      </lectures/lecture2/l2_index>`

   Seed
      The number that starts a random number generator. The same seed repeats
      a run exactly. :doc:`L2 </lectures/lecture2/l2_index>`

   Sense-plan-act
      An architecture where the robot senses, builds a world model, plans,
      then acts, in that order. :doc:`L2 </lectures/lecture2/l2_index>`

   Skill
      One robot capability, offered as a ROS 2 action. It reports success or a
      failure reason and never retries a task on its own. :doc:`L2
      </lectures/lecture2/l2_index>`

   Subsumption architecture
      Brooks, 1986: layers of behaviors run in parallel; a higher layer
      suppresses a lower layer's inputs and inhibits its outputs while the
      lower layer keeps running. :doc:`L2 </lectures/lecture2/l2_index>`

   Team charter
      A one-page agreement each team writes before L3: owners and backups,
      meetings and Git, what happens when someone goes quiet, and AI use.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Three-layer architecture
      A deliberative layer plans, a reactive layer controls, and an executive
      layer between them chooses the next skill and reacts to failures (Gat:
      deliberator, sequencer, controller). The frame for the course's group
      projects. :doc:`L2 </lectures/lecture2/l2_index>`

   Two-system design
      A slow reasoning model above a fast control policy. :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

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

   World model
      Two meanings. In robot architecture, the robot's own record of what the
      world looks like (L2, L3). In learned AI, a model that predicts how a
      scene will change, used to make training data and test policies in
      simulation (L13). :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Embodied-reasoning-model" target="_blank" rel="noopener">Embodied-reasoning model</a> (L1).</p>


.. _g-l3:

L3: Knowledge Representation for Agentic Robotics
=================================================

.. glossary::

   4D/RCS
      NIST's reference model architecture for unmanned vehicle systems (NISTIR
      6910). It is a hybrid architecture, with deliberative and reactive
      capabilities (NISTIR 6910, p. 16). Each level plans over its own time
      span and keeps its own world model. The course takes two ideas from it:
      a world model at each layer, and errors handled where they are seen
      while status moves up. :doc:`L3 </lectures/lecture3/l3_index>`

   Blackboard
      The key-value store that behavior tree nodes read and write, so nodes
      can share state without being wired to each other. In py_trees each
      behavior registers the keys it may read or write. :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`L4 </lectures/lecture4/l4_index>`

   Class, relation and instance (ontology)
      The three parts of an ontology. A class is a kind of thing (Cell, AGV,
      Slot); a relation links classes, such as inSlot(Cell, AGV, Slot); an
      instance is one thing of a class that exists now, such as agv1. :doc:`L3
      </lectures/lecture3/l3_index>`

   CORA
      The core ontology for robotics and automation, IEEE 1872-2015. :doc:`L3
      </lectures/lecture3/l3_index>`

   Default
      A starting filler for a frame's slot that new information can replace.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Executor (plan)
      The code that runs a plan's actions. In L3 it is your behavior tree and
      the skills it calls (GP1 on); in L7 it builds a behavior tree from the
      plan and ticks it. Not a ROS 2 executor. :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`L7 </lectures/lecture7/l7_index>`

   Fact (PDDL)
      A predicate and its objects, such as (in-slot c1 agv1 s1). A fact that
      is not listed is false. :doc:`L3 </lectures/lecture3/l3_index>` ·
      :doc:`L6 </lectures/lecture6/l6_index>`

   Filler
      What a frame's slot holds: a value or a link to another frame. :doc:`L3
      </lectures/lecture3/l3_index>`

   Frame (knowledge representation)
      A description of a kind of object as a set of named slots, with fillers,
      defaults and inheritance. Used to model ARIAC cells, kits and modules.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Inheritance
      A more specific frame takes the slots of a more general one. :doc:`L3
      </lectures/lecture3/l3_index>`

   JSON
      JavaScript Object Notation, a text format for data: objects in braces
      with named fields, lists in brackets, numbers, strings, true, false and
      null. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

   JSON record
      One JSON object that holds a whole state, such as a kit. :doc:`L3
      </lectures/lecture3/l3_index>` · :doc:`GP4 </assignments/gp4>`

   JSON Schema
      A JSON document that describes the fields and values another JSON
      document may have. A validator checks a record against it and lists
      every rule the record breaks. :doc:`L3 </lectures/lecture3/l3_index>` ·
      :doc:`L8 </lectures/lecture8/l8_index>` · :doc:`GP4 </assignments/gp4>`

   Knowledge representation
      How a system writes down what it knows about the world, the task and
      itself, in a form programs can read and check. :doc:`L3
      </lectures/lecture3/l3_index>`

   Node (4D/RCS)
      One unit of the 4D/RCS hierarchy, at one level, with its own world
      model. In this course, read it as one layer. :doc:`L3
      </lectures/lecture3/l3_index>`

   Observed, inferred and unknown facts
      Facts read from an ARIAC interface; facts the team works out; facts no
      ARIAC interface gives. :doc:`L3 </lectures/lecture3/l3_index>`

   Ontology
      The classes, relations and instances of a domain, written so software
      can check that a statement makes sense. :doc:`L3
      </lectures/lecture3/l3_index>`

   OWL
      The W3C Web Ontology Language, for writing ontologies. :doc:`L3
      </lectures/lecture3/l3_index>`

   Slot (knowledge representation)
      A named part of a frame (Minsky's terminals). :doc:`L3
      </lectures/lecture3/l3_index>`

   Validator
      Code that checks a record against a schema and lists every rule it
      breaks. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L8
      </lectures/lecture8/l8_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Inspection-report" target="_blank" rel="noopener">Inspection report</a> (L1), <a href="#term-Kit" target="_blank" rel="noopener">Kit</a> (L1), <a href="#term-World-model" target="_blank" rel="noopener">World model</a> (L2).</p>


.. _g-l4:

L4: Behavior Trees for Task Execution
=====================================

.. glossary::

   Action client leaf
      A py_trees_ros leaf that sends an action goal and returns SUCCESS only
      if the result status is SUCCEEDED. :doc:`L4
      </lectures/lecture4/l4_index>`

   Behavior tree
      A tree of nodes that a robot ticks to decide which action runs.
      Composites (sequence, selector, parallel) choose which children to tick,
      decorators change a child's result, and leaves do the work. The
      executive layer in this course. :doc:`L4 </lectures/lecture4/l4_index>`
      · :doc:`L7 </lectures/lecture7/l7_index>`

   Composite
      A behavior tree node with several children that decides which of them to
      tick: a sequence, a selector or a parallel. :doc:`L4
      </lectures/lecture4/l4_index>`

   Decorator
      A behavior tree node with one child that changes the child's result or
      how it runs, such as Inverter, Retry, Timeout or EternalGuard. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L7 </lectures/lecture7/l7_index>`
      · :doc:`L11 </lectures/lecture11/l11_index>`

   EternalGuard
      A py_trees decorator that checks a condition before every tick of its
      child and stops the child when the condition fails. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Finite state machine
      A robot program that is in one state at a time and moves between states
      by transitions written by hand. :doc:`L4 </lectures/lecture4/l4_index>`

   Leaf
      A behavior tree node that does the work. An action leaf runs a skill or
      calls a service; a condition leaf checks a fact and answers at once.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Memory (behavior tree)
      With memory, a composite's next tick resumes at the child that was
      running; without it, every tick starts at the first child. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Parallel
      A behavior tree composite that ticks all its children every tick, fails
      if any fails, and succeeds as its policy says (SuccessOnAll,
      SuccessOnOne, SuccessOnSelected). With synchronise True, the default, it
      skips children that already succeeded. :doc:`L4
      </lectures/lecture4/l4_index>`

   py_trees and py_trees_ros
      The Python behavior tree library, and its ROS 2 integration, which runs
      the tree as a node ticked by a timer. Used for the executive layer from
      GP1 on. :doc:`L4 </lectures/lecture4/l4_index>`

   Retry decorator
      Runs its child again after a failure, up to num_failures failures, then
      returns FAILURE. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L7
      </lectures/lecture7/l7_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   Selector
      A behavior tree composite that ticks its children in order and succeeds
      at the first success; it fails only if all fail. Also called a fallback.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Sequence
      A behavior tree composite that ticks its children in order: it fails at
      the first failure, keeps running while a child runs, and succeeds when
      all succeed. :doc:`L4 </lectures/lecture4/l4_index>`

   Service client leaf
      A py_trees_ros leaf that returns SUCCESS when the reply arrives,
      whatever the reply says. Check the reply in a condition after it.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Status (behavior tree)
      What a node returns when ticked: SUCCESS, FAILURE, RUNNING (needs more
      ticks) or INVALID (not run yet, or stopped). :doc:`L4
      </lectures/lecture4/l4_index>`

   Tick
      One pass through a behavior tree from the root down. Each node visited
      returns a status. :doc:`L4 </lectures/lecture4/l4_index>`

   Timeout decorator
      Fails its child and stops it if the child is still running after a set
      duration, so a hang becomes a failure. :doc:`L4
      </lectures/lecture4/l4_index>` · :doc:`L7 </lectures/lecture7/l7_index>`
      · :doc:`L11 </lectures/lecture11/l11_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Blackboard" target="_blank" rel="noopener">Blackboard</a> (L3).</p>


.. _g-l5:

L5: Sensing and Perception for Robotic Systems
==============================================

.. glossary::

   Angular step and point spacing
      The angle between neighboring lidar rays, (max angle - min angle) / (N -
      1); on a surface, neighboring points are about the angular step (in
      radians) times the distance apart. :doc:`L5
      </lectures/lecture5/l5_index>`

   Confusion matrix
      The 2 by 2 table of a detector's TP, FP, FN and TN counts. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Defect (dent, scratch, bulge)
      The three ARIAC cell defects: a round dip, a long narrow dip and a round
      bump. The ARIAC docs say each is at least 2 mm off the surface; ARIAC's
      training cell meshes measure 0.84 to 2.49 mm. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`GP2 </assignments/gp2>`

   Detection threshold
      The value above which a detector flags an item. Lowering it trades
      precision for recall. :doc:`L5 </lectures/lecture5/l5_index>` ·
      :doc:`L12 </lectures/lecture12/l12_index>`

   Inspection bonuses
      ARIAC's speed bonus, 500 x (1 - g / 4 s) with g the average time from a
      cell's spawn to its report, and its classification bonus, 500 x the
      share of defective cells whose report matches every defect in type, z
      (within 5 mm) and theta (within 0.26 rad). :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Lidar
      A sensor that measures the distance along each ray of a grid of angles,
      giving one 3D point per ray that hits something in range. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`GP2 </assignments/gp2>`

   Perception
      Turning sensor data into facts the system can use, such as a dent's
      location on a cell. :doc:`L5 </lectures/lecture5/l5_index>`

   Point cloud
      A set of 3D points a lidar measures on the surfaces it sees. In ROS 2 it
      arrives as a sensor_msgs/PointCloud2 message. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`GP2 </assignments/gp2>`

   PointCloud2
      The ROS 2 message for a point cloud: packed bytes plus their layout
      (fields, point_step, row_step). :doc:`L5 </lectures/lecture5/l5_index>`

   Precision
      TP / (TP + FP): the share of the detector's calls that were right.
      :doc:`L5 </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>` · :doc:`L13
      </lectures/lecture13/l13_index>` · :doc:`GP2 </assignments/gp2>`

   Recall
      TP / (TP + FN): the share of real defects the detector found. :doc:`L5
      </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>` · :doc:`L13
      </lectures/lecture13/l13_index>` · :doc:`GP2 </assignments/gp2>`

   Residual
      For a lidar point on a cell, its distance from the fitted cell axis
      minus the cell radius (10.5 mm). Negative is set in (a dent or scratch);
      positive sticks out (a bulge). :doc:`L5 </lectures/lecture5/l5_index>`

   Team configuration file
      The YAML file where a team declares its sensors (name, type, pose,
      rate). ARIAC checks it at startup. :doc:`L5
      </lectures/lecture5/l5_index>`

   True and false positives and negatives
      The four outcomes of a detector for one class: TP (flagged and
      defective), FP (flagged but good), FN (missed), TN (correctly passed).
      :doc:`L5 </lectures/lecture5/l5_index>` · :doc:`L12
      </lectures/lecture12/l12_index>` · :doc:`L13
      </lectures/lecture13/l13_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Inspection-report" target="_blank" rel="noopener">Inspection report</a> (L1), <a href="#term-Sensor-budget" target="_blank" rel="noopener">Sensor budget</a> (L1).</p>


.. _g-l6:

L6: Task-Level Planning with PDDL
=================================

.. glossary::

   Action (planning)
      A planning step with preconditions (facts that must hold before it) and
      effects (facts it makes true, and delete effects, written (not ...),
      that it makes false). :doc:`L6 </lectures/lecture6/l6_index>`

   Closed-world assumption
      A fact not listed in a planning state is false. :doc:`L6
      </lectures/lecture6/l6_index>`

   Fast Downward
      The classical planner used in L6 and GP3. Its translator grounds the
      PDDL and drops the ground actions that a relaxed test (delete effects
      ignored) rules out, so some that can never apply stay. Then its search
      finds a plan. :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3
      </assignments/gp3>`

   Heuristic
      An estimate of how many actions a state is from the goal, used to order
      a planner's search. An admissible heuristic never overestimates.
      :doc:`L6 </lectures/lecture6/l6_index>`

   Numeric fluent
      A PDDL 2.1 function with a number value, such as a kit's total voltage,
      that actions can change. Fast Downward does not support them. :doc:`L6
      </lectures/lecture6/l6_index>`

   Optimal and satisficing search
      Optimal search returns a shortest plan (A* with an admissible
      heuristic), possibly slowly; satisficing search returns a plan quickly,
      not always the shortest. :doc:`L6 </lectures/lecture6/l6_index>`

   PDDL
      Planning Domain Definition Language. A planning problem is written as a
      domain (types, predicates and actions with preconditions and effects)
      and a problem (objects, initial state and goal). :doc:`L6
      </lectures/lecture6/l6_index>`

   Plan
      A sequence of actions that turns the initial state into a state where
      the goal holds. :doc:`L6 </lectures/lecture6/l6_index>`

   Plan validity
      Every action's preconditions hold in the state where it runs, and the
      plan reaches the goal. A plan validator replays the plan and names the
      first action whose precondition fails. :doc:`L6
      </lectures/lecture6/l6_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   Predicate
      A fact that is true or false in a PDDL state, such as (hand-free
      inspection_robot_1). :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3
      </assignments/gp3>`

   Problem generator
      Code that writes a new PDDL problem file from the current factory state.
      :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3 </assignments/gp3>`

   Selection step
      Python code that picks which cells go in which slots so the kit total
      lands inside the kit voltage window. Its result goes to PDDL as facts.
      :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`GP3 </assignments/gp3>`

   State (planning)
      The set of facts that are true at one moment. :doc:`L6
      </lectures/lecture6/l6_index>`

   STRIPS
      The planning model of Fikes and Nilsson (1971): states are sets of
      facts, and actions have preconditions and effects. PDDL writes it down.
      :doc:`L6 </lectures/lecture6/l6_index>`

   Unified Planning Framework
      UPF, a Python library that reads or builds planning problems and calls
      planners and validators through one interface. :doc:`L6
      </lectures/lecture6/l6_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Fact-PDDL" target="_blank" rel="noopener">Fact (PDDL)</a> (L3).</p>


.. _g-l7:

L7: Plan Execution Patterns with Behavior Trees
===============================================

.. glossary::

   BehaviorTree.CPP
      The C++ behavior tree library used in industry (Nav2 uses it). Trees are
      written in XML and nodes are C++ classes. :doc:`L7
      </lectures/lecture7/l7_index>`

   Builder
      A function that takes one plan action's arguments and returns the
      behavior tree subtree for that step. :doc:`L7
      </lectures/lecture7/l7_index>`

   Groot2
      The editor and monitor for BehaviorTree.CPP trees. :doc:`L7
      </lectures/lecture7/l7_index>`

   Ground action
      An action name with its arguments filled in by real objects, such as
      (pick-from-tester inspection_robot_2 c3 tester1). :doc:`L7
      </lectures/lecture7/l7_index>`

   Guard, act, verify, update
      The four leaves of one plan step: check the preconditions on the
      blackboard, send the goal, check the effect in the factory, then write
      the effects. :doc:`L7 </lectures/lecture7/l7_index>`

   Mock skill
      A small Python stand-in for a course skill or an ARIAC interface, used
      to run demos without ROS or the simulator. :doc:`L7
      </lectures/lecture7/l7_index>`

   Plan-to-BT factory
      Code that looks up each plan action's name in a registry and calls its
      builder, in plan order, to make one subtree per action. :doc:`L7
      </lectures/lecture7/l7_index>` · :doc:`GP3 </assignments/gp3>`

   Port
      A BehaviorTree.CPP node's typed input or output. {key} in the XML
      connects it to a blackboard entry. :doc:`L7
      </lectures/lecture7/l7_index>`

   Registry
      A dictionary from each plan action name to the builder function for that
      action. :doc:`L7 </lectures/lecture7/l7_index>`

   Replanning trigger
      An event that stops the plan and asks for a new one, such as an
      out-of-range voltage, a tester malfunction or a skill that still fails
      after the tree's retries. :doc:`L7 </lectures/lecture7/l7_index>` ·
      :doc:`GP3 </assignments/gp3>`

   Safe point
      A place to stop a plan without leaving the robots in an unknown state:
      between subtrees, or after a cancelled skill retreats. :doc:`L7
      </lectures/lecture7/l7_index>`

   Snapshot
      The tree's structure and every node's status at one moment, published by
      py_trees_ros as a ROS message. :doc:`L7 </lectures/lecture7/l7_index>`

   Tick trace
      A log line for every status change of a plan step, with the tick number.
      :doc:`L7 </lectures/lecture7/l7_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Behavior-tree" target="_blank" rel="noopener">Behavior tree</a> (L4), <a href="#term-Decorator" target="_blank" rel="noopener">Decorator</a> (L4), <a href="#term-Executor-plan" target="_blank" rel="noopener">Executor (plan)</a> (L3), <a href="#term-Retry-decorator" target="_blank" rel="noopener">Retry decorator</a> (L4), <a href="#term-Timeout-decorator" target="_blank" rel="noopener">Timeout decorator</a> (L4).</p>


.. _g-l8:

L8: LLM Agents I: Agent Loops, Tool Use, and Structured Output
==============================================================

.. glossary::

   Agent loop
      The loop the orchestrator runs: read the state, ask the LLM, check and
      run the tool call it returns, record the result, and stop when a stop
      condition fires. The agent's behavior comes from the loop, not from the
      model alone. :doc:`L8 </lectures/lecture8/l8_index>`

   Bounded retry
      Sending the exact error back to the model and asking again, up to a
      fixed number of times, then falling back to a safe action. :doc:`L8
      </lectures/lecture8/l8_index>`

   Constrained output
      A provider holds the model's output to a schema while it is generated.
      It removes parse and schema errors, not semantic ones, so the semantic
      checks stay. :doc:`L8 </lectures/lecture8/l8_index>`

   Context
      The messages sent in one LLM call. It is all the model knows for that
      call. :doc:`L8 </lectures/lecture8/l8_index>`

   Few-shot example
      A short worked decision in the prompt that shows the model the expected
      output format. :doc:`L8 </lectures/lecture8/l8_index>`

   JSON-RPC 2.0
      The request and response message format MCP uses. :doc:`L8
      </lectures/lecture8/l8_index>`

   Latency
      The time from sending a request to getting its answer. Latency per
      decision is the time from an observation to a validated decision.
      :doc:`L8 </lectures/lecture8/l8_index>` · :doc:`L12
      </lectures/lecture12/l12_index>`

   LLM
      Large language model. It takes a list of messages and returns text,
      keeps nothing between calls, and can answer the same messages
      differently. In this course, the decision part of the GP4 agent.
      :doc:`L8 </lectures/lecture8/l8_index>`

   MCP
      Model Context Protocol, an open protocol between agent applications and
      servers that provide tools, resources and prompts. A host (the AI
      application) runs one client per server; messages use JSON-RPC 2.0 over
      stdio or Streamable HTTP. :doc:`L8 </lectures/lecture8/l8_index>`

   Orchestrator
      Your team's code that runs the agent loop and owns the tools, checks and
      logs. The LLM never sends a ROS goal itself. :doc:`L8
      </lectures/lecture8/l8_index>`

   Plan-and-execute
      The LLM writes a full plan once, and the executor asks for a new one
      only when a replanning trigger fires. Contrasted with ReAct. :doc:`L8
      </lectures/lecture8/l8_index>`

   ReAct
      An agent pattern where each iteration is one reasoning step and one tool
      call, and the model sees each result before choosing the next step.
      :doc:`L8 </lectures/lecture8/l8_index>`

   Scripted stand-in model
      A fake model that returns replies written in advance, so a demo repeats
      exactly. A real model's answers vary. :doc:`L8
      </lectures/lecture8/l8_index>` · :doc:`L9 </lectures/lecture9/l9_index>`
      · :doc:`L13 </lectures/lecture13/l13_index>`

   Semantic check
      A check that needs the factory's current state, which a schema cannot
      express, such as whether a slot is free. :doc:`L8
      </lectures/lecture8/l8_index>`

   Stop condition
      A check in code that ends the agent loop: the goal is reached, a step
      limit, too many invalid outputs in a row, a time limit, or an operator
      stop. :doc:`L8 </lectures/lecture8/l8_index>`

   Structured output
      An LLM answer in a fixed format, usually JSON that follows a schema, so
      a program can check it and use it. :doc:`L8
      </lectures/lecture8/l8_index>`

   System message
      The part of every LLM call that stays fixed during a run: the role, the
      factory facts, the rules and the output format. The user message carries
      the current state and goal. :doc:`L8 </lectures/lecture8/l8_index>`

   Temperature
      An API setting that changes how much a model's answers vary. No setting
      makes the output safe without checks. :doc:`L8
      </lectures/lecture8/l8_index>`

   Token
      A piece of text the model reads or writes. Calls are paid for in tokens.
      :doc:`L8 </lectures/lecture8/l8_index>`

   Tool calling
      The model's way of asking to run a tool with JSON arguments, instead of
      only writing text. The orchestrator checks and runs the call and sends
      the result back. Also called function calling. :doc:`L8
      </lectures/lecture8/l8_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Agent" target="_blank" rel="noopener">Agent</a> (L1), <a href="#term-API-key" target="_blank" rel="noopener">API key</a> (Pre-read), <a href="#term-Context-window" target="_blank" rel="noopener">Context window</a> (Pre-read), <a href="#term-JSON" target="_blank" rel="noopener">JSON</a> (L3), <a href="#term-JSON-Schema" target="_blank" rel="noopener">JSON Schema</a> (L3), <a href="#term-Stateless-API" target="_blank" rel="noopener">Stateless API</a> (Pre-read), <a href="#term-Tool" target="_blank" rel="noopener">Tool</a> (L1), <a href="#term-Transport-MCP" target="_blank" rel="noopener">Transport (MCP)</a> (Pre-read), <a href="#term-Validator" target="_blank" rel="noopener">Validator</a> (L3).</p>


.. _g-l9:

L9: LLM Agents II: VLM Grounding and Agentic Replanning
=======================================================

.. glossary::

   Agentic closed loop
      Act, observe again, compare what you see with the expected effect, then
      decide: retry, wait or replan. :doc:`L9 </lectures/lecture9/l9_index>`

   Enum
      A schema field that lists the only values it may take. :doc:`L9
      </lectures/lecture9/l9_index>`

   Expected effect
      The change an action should make, which the orchestrator checks against
      fresh observations. :doc:`L9 </lectures/lecture9/l9_index>`

   Grounding
      Basing the agent's decisions on what a camera sees, through a VLM's
      checked record. :doc:`L9 </lectures/lecture9/l9_index>`

   Hybrid design
      The LLM picks goals and PDDL plans the steps, or PDDL runs the normal
      flow and the LLM handles replanning triggers. :doc:`L9
      </lectures/lecture9/l9_index>`

   Second source
      Another way to learn the same fact, used to cross-check a VLM's output,
      such as /agvN/tray_status or a recorded tester voltage. :doc:`L9
      </lectures/lecture9/l9_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

   World drift
      The factory no longer matches what the plan assumed, and no single
      action failed, such as a high-priority order arriving in the middle of a
      kit. :doc:`L9 </lectures/lecture9/l9_index>` · :doc:`L11
      </lectures/lecture11/l11_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Embodied-reasoning-model" target="_blank" rel="noopener">Embodied-reasoning model</a> (L1), <a href="#term-Kit-voltage-window" target="_blank" rel="noopener">Kit voltage window</a> (L1), <a href="#term-Scripted-stand-in-model" target="_blank" rel="noopener">Scripted stand-in model</a> (L8), <a href="#term-VLM" target="_blank" rel="noopener">VLM</a> (L2).</p>


.. _g-l10:

L10: Frames, Transforms, and Motion Planning
============================================

.. glossary::

   Break beam
      A sensor that fires when something crosses its beam, such as a cell
      passing a point on the conveyor. :doc:`L10
      </lectures/lecture10/l10_index>`

   Intrinsic matrix
      The 3 by 3 matrix K of a camera's focal lengths (fx, fy, in pixels) and
      principal point (cx, cy, the pixel where the optical axis meets the
      image), sent in CameraInfo.k. :doc:`L10 </lectures/lecture10/l10_index>`

   MoveIt 2
      The ROS 2 motion planning framework. The course skills package uses it
      to plan the arms' motions, below the behavior tree. :doc:`L10
      </lectures/lecture10/l10_index>`

   MoveItPy and MoveItCpp
      MoveIt 2's Python interface, and the C++ interface it calls inside the
      same process, with no ROS actions or services in between. move_group is
      the separate node that offers the same parts over ROS. :doc:`L10
      </lectures/lecture10/l10_index>`

   OMPL
      The Open Motion Planning Library, which holds MoveIt's sampling-based
      planners such as RRT-Connect, PRM and RRTstar. :doc:`L10
      </lectures/lecture10/l10_index>`

   Optical frame
      A camera's second frame, named with the _optical suffix: z forward, x
      right, y down (REP 103). :doc:`L10 </lectures/lecture10/l10_index>`

   Parameterized grasp
      A gripper target computed as the part's frame plus a fixed offset. The
      course skills package sets one offset per place in skills.yaml.
      :doc:`L10 </lectures/lecture10/l10_index>`

   Pilz industrial motion planner
      A MoveIt planner for the standard industrial motions PTP (point to point
      in joint space), LIN (a straight line) and CIRC (an arc), with no random
      sampling: the same request gives the same motion. :doc:`L10
      </lectures/lecture10/l10_index>`

   Pinhole camera model
      A camera treated as one point that every ray passes through, so a point
      at (X, Y, Z) in the optical frame lands at pixel u = fx X/Z + cx, v = fy
      Y/Z + cy. :doc:`L10 </lectures/lecture10/l10_index>`

   Planning pipeline
      In MoveIt, request adapters, then a planner plugin, then response
      adapters. :doc:`L10 </lectures/lecture10/l10_index>`

   Planning scene
      MoveIt's picture of the robot's current joint state and the collision
      objects around it. :doc:`L10 </lectures/lecture10/l10_index>`

   PRM
      Probabilistic roadmap: builds a roadmap of free configurations once and
      reuses it for many queries. :doc:`L10 </lectures/lecture10/l10_index>`

   RRT-Connect
      A sampling-based planner that grows two random trees, from the start and
      from the goal, until they meet. :doc:`L10
      </lectures/lecture10/l10_index>`

   RRTstar
      A sampling-based planner that grows one tree and keeps shortening its
      path while planning time remains. :doc:`L10
      </lectures/lecture10/l10_index>`

   Sampling-based planner
      A planner that picks random collision-free configurations and links them
      into a path. Two runs can give different paths. :doc:`L10
      </lectures/lecture10/l10_index>`

   Zone lock
      A rule that lets one robot at a time into a shared area, such as the
      voltage testers. :doc:`L10 </lectures/lecture10/l10_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Course-skills-package" target="_blank" rel="noopener">Course skills package</a> (L1), <a href="#term-TF2" target="_blank" rel="noopener">TF2</a> (L1), <a href="#term-Transform" target="_blank" rel="noopener">Transform</a> (L1).</p>


.. _g-l11:

L11: Recovery, Robustness, and Failure Handling for Agentic Systems
===================================================================

.. glossary::

   Action failure
      A skill or service call does not do what it was asked, such as a failed
      grasp. Recovery starts in the behavior tree. :doc:`L11
      </lectures/lecture11/l11_index>`

   Backoff
      A wait before a retry, so a tool or device has time to recover.
      :doc:`L11 </lectures/lecture11/l11_index>`

   Challenge test matrix
      A table of test runs: each challenge alone and combined, on several
      trial configurations, each run more than once. :doc:`L11
      </lectures/lecture11/l11_index>`

   Code freeze
      The tagged commit the instructor builds the team's Docker image from for
      the final demo. No change is allowed after it. :doc:`L11
      </lectures/lecture11/l11_index>` · :doc:`Final demo
      </assignments/final_demo>`

   Degraded operation
      The system keeps working, more slowly or with fewer devices, while one
      device is down. :doc:`L11 </lectures/lecture11/l11_index>`

   Global recovery
      Recovery that changes the plan: the planner or the LLM agent replans or
      takes a new goal. :doc:`L11 </lectures/lecture11/l11_index>`

   Hang
      A skill that stays RUNNING and never returns SUCCESS or FAILURE. A
      Timeout decorator turns it into a failure. :doc:`L11
      </lectures/lecture11/l11_index>`

   Local recovery
      Recovery that keeps the plan: the skill or the behavior tree retries a
      step or waits (retry, wait, timeout, another branch). :doc:`L11
      </lectures/lecture11/l11_index>`

   Plan failure
      The plan is invalid, such as an LLM plan that puts a fifth cell on a
      four-slot tray. A check before execution catches it. :doc:`L11
      </lectures/lecture11/l11_index>`

   Re-prompt
      Asking the model again, once, with the exact error message of the check
      that failed. :doc:`L11 </lectures/lecture11/l11_index>`

   Sensor failure
      A device gives no data or wrong data, such as a voltage tester
      malfunction. :doc:`L11 </lectures/lecture11/l11_index>`

   Watcher
      Code that reads a device's messages and decides at any moment whether
      the device is up (giving valid readings) or down. :doc:`L11
      </lectures/lecture11/l11_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Challenge" target="_blank" rel="noopener">Challenge</a> (L1), <a href="#term-Decorator" target="_blank" rel="noopener">Decorator</a> (L4), <a href="#term-EternalGuard" target="_blank" rel="noopener">EternalGuard</a> (L4), <a href="#term-Memory-behavior-tree" target="_blank" rel="noopener">Memory (behavior tree)</a> (L4), <a href="#term-Retry-decorator" target="_blank" rel="noopener">Retry decorator</a> (L4), <a href="#term-Second-source" target="_blank" rel="noopener">Second source</a> (L9), <a href="#term-Timeout-decorator" target="_blank" rel="noopener">Timeout decorator</a> (L4), <a href="#term-World-drift" target="_blank" rel="noopener">World drift</a> (L9).</p>


.. _g-l12:

L12: Evaluation and Measurement Science for Agentic Systems
===========================================================

.. glossary::

   Aborted run (ARIAC)
      A run in which not every wanted kit and module, high-priority kits
      included, was submitted and accepted. ARIAC marks the run aborted and
      sets all five bonuses to 0. :doc:`L12 </lectures/lecture12/l12_index>`

   Base score
      ARIAC's score for completed work: W1 kc/kd + W2 mc/md, the weighted
      share of the wanted kits (kd) and modules (md) that were completed (kc,
      mc). :doc:`L12 </lectures/lecture12/l12_index>`

   Controlled comparison
      A test of two systems that differ in one variable only, with everything
      else held fixed and the runs alternated. :doc:`L12
      </lectures/lecture12/l12_index>`

   Ground truth
      The true values a metric compares against. For cell defects, ARIAC
      prints them when launched with log_cell_info:=true, a cheat tool for
      practice runs only. :doc:`L12 </lectures/lecture12/l12_index>` ·
      :doc:`L13 </lectures/lecture13/l13_index>`

   Invented object
      A name in an LLM reply (a cell, slot, AGV or order ID) that does not
      exist in the factory. :doc:`L12 </lectures/lecture12/l12_index>`

   Measurement science
      The work of making a number trustworthy: a defined metric, a source of
      truth, and a known run-to-run variation. :doc:`L12
      </lectures/lecture12/l12_index>`

   Plan length and plan cost
      The number of actions in a plan, and the sum of action costs if the
      domain defines them (or the time the plan takes to run). :doc:`L12
      </lectures/lecture12/l12_index>`

   Recovery rate
      Failures recovered without operator help, divided by failures detected.
      :doc:`L12 </lectures/lecture12/l12_index>`

   Run score
      ARIAC's score for one run: the base score plus bonuses minus penalties.
      :doc:`L12 </lectures/lecture12/l12_index>`

   Schema-valid rate
      The share of LLM replies that pass the JSON schema on the first try, and
      after one re-prompt. :doc:`L12 </lectures/lecture12/l12_index>`

   Standard error
      The spread of one measured success rate: about how far p = k / n lands
      from the true rate, sqrt(p(1 - p) / n). Two independent sets of n runs
      differ by about sqrt(2) times this. :doc:`L12
      </lectures/lecture12/l12_index>`

   Success rate
      k / n, the share of n runs on which the system completes the trial.
      :doc:`L12 </lectures/lecture12/l12_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Confusion-matrix" target="_blank" rel="noopener">Confusion matrix</a> (L5), <a href="#term-Detection-threshold" target="_blank" rel="noopener">Detection threshold</a> (L5), <a href="#term-Inspection-bonuses" target="_blank" rel="noopener">Inspection bonuses</a> (L5), <a href="#term-Latency" target="_blank" rel="noopener">Latency</a> (L8), <a href="#term-Plan-validity" target="_blank" rel="noopener">Plan validity</a> (L6), <a href="#term-Precision" target="_blank" rel="noopener">Precision</a> (L5), <a href="#term-Recall" target="_blank" rel="noopener">Recall</a> (L5), <a href="#term-True-and-false-positives-and-negatives" target="_blank" rel="noopener">True and false positives and negatives</a> (L5).</p>


.. _g-l13:

L13: The Physical AI Frontier: VLAs, Robot Foundation Models, and World Models
==============================================================================

.. glossary::

   Action expert
      The part of a VLA, such as SmolVLA, that turns the vision-language
      model's features into robot actions. :doc:`L13
      </lectures/lecture13/l13_index>`

   Fine-tuning
      More training of a trained model, on a smaller set of data for a new
      robot or task. :doc:`L13 </lectures/lecture13/l13_index>`

   LoRA
      Low-rank adaptation, a lighter way to fine-tune a large model. :doc:`L13
      </lectures/lecture13/l13_index>`

   Robot foundation model
      A model trained once on data from many tasks and robots, then adapted to
      a new robot or task with less data. :doc:`L13
      </lectures/lecture13/l13_index>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Agentic-physical-AI" target="_blank" rel="noopener">Agentic physical AI</a> (L1), <a href="#term-Embodied-reasoning-model" target="_blank" rel="noopener">Embodied-reasoning model</a> (L1), <a href="#term-Ground-truth" target="_blank" rel="noopener">Ground truth</a> (L12), <a href="#term-Physical-AI" target="_blank" rel="noopener">Physical AI</a> (L1), <a href="#term-Precision" target="_blank" rel="noopener">Precision</a> (L5), <a href="#term-Recall" target="_blank" rel="noopener">Recall</a> (L5), <a href="#term-Scripted-stand-in-model" target="_blank" rel="noopener">Scripted stand-in model</a> (L8), <a href="#term-True-and-false-positives-and-negatives" target="_blank" rel="noopener">True and false positives and negatives</a> (L5), <a href="#term-Two-system-design" target="_blank" rel="noopener">Two-system design</a> (L2), <a href="#term-VLA" target="_blank" rel="noopener">VLA</a> (L2), <a href="#term-World-model" target="_blank" rel="noopener">World model</a> (L2).</p>


.. _g-gp1:

GP1: Behavior Tree for One Kit
==============================


.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Inspection-door" target="_blank" rel="noopener">Inspection door</a> (L1).</p>


.. _g-gp2:

GP2: Cell Inspection
====================


.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Defect-dent-scratch-bulge" target="_blank" rel="noopener">Defect (dent, scratch, bulge)</a> (L5), <a href="#term-Lidar" target="_blank" rel="noopener">Lidar</a> (L5), <a href="#term-Point-cloud" target="_blank" rel="noopener">Point cloud</a> (L5), <a href="#term-Precision" target="_blank" rel="noopener">Precision</a> (L5), <a href="#term-Recall" target="_blank" rel="noopener">Recall</a> (L5).</p>


.. _g-gp3:

GP3: PDDL Planner and BT Executor
=================================


.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Fast-Downward" target="_blank" rel="noopener">Fast Downward</a> (L6), <a href="#term-Plan-to-BT-factory" target="_blank" rel="noopener">Plan-to-BT factory</a> (L7), <a href="#term-Predicate" target="_blank" rel="noopener">Predicate</a> (L6), <a href="#term-Problem-generator" target="_blank" rel="noopener">Problem generator</a> (L6), <a href="#term-Replanning-trigger" target="_blank" rel="noopener">Replanning trigger</a> (L7), <a href="#term-Selection-step" target="_blank" rel="noopener">Selection step</a> (L6).</p>


.. _g-gp4:

GP4: LLM Agent with VLM Grounding
=================================


.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-JSON-record" target="_blank" rel="noopener">JSON record</a> (L3), <a href="#term-JSON-Schema" target="_blank" rel="noopener">JSON Schema</a> (L3).</p>


.. _g-final-demo:

Final Demo: Full ARIAC Trial, Unseen
====================================

.. glossary::

   Unseen trial
      A trial file no team has seen, with its own ID, seed and challenge
      times, used in the final demo. :doc:`Final demo
      </assignments/final_demo>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Code-freeze" target="_blank" rel="noopener">Code freeze</a> (L11).</p>
