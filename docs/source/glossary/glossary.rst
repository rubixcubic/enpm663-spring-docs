====================================================
Glossary
====================================================

Key terms used across ENPM663. Terms are cross-referenced from the lectures.
This glossary grows as the Spring 2027 lectures are authored.

.. glossary::
   :sorted:

   Agent loop
      The control loop an orchestrator runs around an LLM: observe the world,
      ask the model what to do next, execute the chosen tool, feed the result
      back, and repeat until a goal or stop condition is reached. The agent
      behavior comes from the loop, not from the model alone.

   AGV
      Automated Guided Vehicle. In ARIAC, the mobile platform that carries a
      kit tray between stations.

   ARIAC
      Agile Robotics for Industrial Automation Competition, a NIST-run
      simulation testbed. ENPM663 uses ARIAC 2025 as its unifying testbed.

   Behavior tree
      A tree-structured task-execution model built from composites (sequence,
      selector, parallel) and decorators, ticked at a fixed rate. The
      industry-standard executive layer for robot task execution.

   Blackboard
      A shared key-value store that behavior-tree nodes read from and write to,
      used to pass state between nodes without hard-wiring connections.

   Closed-loop replanning
      Detecting that execution has drifted from the expected world state and
      re-invoking the planner (classical or LLM) with updated observations,
      rather than blindly executing a stale plan.

   Decorator
      A behavior-tree node with a single child that modifies its result or
      execution, such as inverter, retry, or timeout.

   Executor (ROS 2)
      The ROS 2 component that manages callback execution for nodes
      (single-threaded or multi-threaded). Not to be confused with a plan
      executor.

   Frame (knowledge representation)
      A structured representation with named slots and fillers, optionally with
      defaults and inheritance, used to model entities such as ARIAC orders,
      parts, and kits.

   Kitting
      Assembling a specified set of parts into a kit tray according to an order.
      The primary ARIAC task used throughout the course.

   Knowledge representation
      The formalisms (frames, ontologies, hierarchical world models) used to
      represent the world, the task, and robot state so that classical planners,
      LLMs, and VLMs can all consume them.

   Lifecycle node
      A ROS 2 managed node with explicit states (unconfigured, inactive,
      active, finalized) and transitions, used for deterministic bring-up and
      shutdown.

   LLM
      Large Language Model. In this course, used as the reasoning core of an
      agent for task planning.

   MCP
      Model Context Protocol, the 2024-onward standard for exposing tools and
      context to LLMs across agent frameworks.

   MoveIt2
      The ROS 2 motion-planning framework used for pick-and-place and
      parameterized-grasp execution. The reactive layer beneath the executor.

   Ontology
      A formal specification of classes, relations, and instances used to
      connect perception output to planning vocabulary.

   PDDL
      Planning Domain Definition Language, the classical formalism for
      describing planning problems as a domain (predicates and actions) and a
      problem (initial state and goal).

   Plan-and-execute
      An agent pattern that produces a full plan up front, then executes it. The
      LLM analog of a classical PDDL planner, contrasted with ReAct.

   py_trees_ros
      The Python behavior-tree library, integrated with ROS 2, used as the
      primary teaching tool for task execution.

   QoS
      Quality of Service. ROS 2 policies (reliability, durability, history) that
      govern how messages are delivered on a topic.

   ReAct
      An agent pattern that interleaves reasoning and acting: the model
      produces a thought, calls a tool, reads the observation, and adjusts,
      step by step.

   Structured output
      Constraining an LLM's response to a schema (typically JSON), so the output
      can be validated and consumed programmatically.

   TF2
      The ROS 2 transform library that tracks coordinate frames over time and
      answers transform queries between them.

   Tool calling
      The mechanism by which an LLM invokes explicitly defined functions (tools)
      described by a schema, rather than emitting free text. Also called
      function calling.

   Three-layer architecture
      The dominant robot architecture pattern: a deliberative planner, an
      executive (behavior tree), and a reactive control layer. AI plugs into
      specific layers rather than replacing the architecture.

   VLA
      Vision-Language-Action model. An end-to-end learned policy mapping pixels
      and language directly to actions. Surveyed in this course but not built;
      the course teaches the modular stack instead.

   VLM
      Vision-Language Model. A multimodal model that produces a scene
      description or spatial relations from an image, used for grounding.
