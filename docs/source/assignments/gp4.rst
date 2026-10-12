====================================================
GP4: LLM Agent with VLM Grounding
====================================================

.. card:: GP4: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 10 to Week 13), posted 03/31, due 04/21
      * - **Weight**
        - 10% of the course grade
      * - **Lectures**
        - L8 and L9
      * - **Team Size**
        - 3 students
      * - **Submission**
        - Canvas + GitHub repository link


.. admonition:: Specification in progress
   :class: note

   This page is the plan for GP4. The full specification (provided code,
   folder structure, submission checklist and grading rubric) is added
   before it is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP4 replaces the PDDL planner with an LLM agent. The agent calls the robot
skills as tools and returns structured output checked against a JSON schema;
a VLM describes the cells for it. The same executor from GP3 runs its
decisions. GP4 tests the agent on the situations GP3's domain does not model:
a conveyor malfunction, a voltage tester malfunction and high-priority orders.
The vacuum tool malfunction affects only Task 2, so the final demo tests it.


Learning Objectives
-------------------

- Build an agent loop with tool calling and validated structured output.
- Expose robot skills to an LLM as tools, through MCP if you choose.
- Ground the agent in VLM descriptions of the camera images.
- Compare an LLM agent with a PDDL planner on the same trials.


Provided Resources
------------------

- Your team's GP3 package.
- An LLM and a VLM: a hosted API or local models (see the ARIAC Testbed pages).


Tasks
-----

- Write the agent loop, its tools and its output schema.
- Add VLM grounding of the cell images.
- Handle each ARIAC 2025 challenge and show it on a trial.
- Compare the agent with GP3 on identical trials: validity, plan length, cost, latency.


Deliverables
------------

- The agent module, the VLM module and the executor changes.
- The side-by-side comparison with GP3.
- A reflection on the agent's failure modes and how they were caught.
