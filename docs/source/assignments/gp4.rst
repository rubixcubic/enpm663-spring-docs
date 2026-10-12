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


.. admonition:: Specification draft
   :class: note

   This page is the specification draft for GP4. The provided code (the
   course skills package, as in GP1 to GP3), the GP4 trial configurations
   and the cost guidance for the models are released with the project, on
   the day GP4 is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.

   In GP4, AI tools are also **required**: the system you build calls an
   LLM and a VLM. Your team must understand, design and debug the code that
   calls them.


Overview
--------

GP4 replaces the PDDL planner with an LLM agent. An **agent** is a program
that runs a loop around a large language model (LLM): it observes the
factory, asks the model what to do next, runs the tool the model chose,
checks the result, and repeats. The program that runs this loop is the
**orchestrator**.

The agent's tools are the robot skills and the ARIAC services that the GP3
executor already runs. Your team may expose them through the **Model
Context Protocol (MCP)**, a standard way to describe tools to an LLM. The
agent returns structured output that your code checks against a **JSON
schema** (a description of the fields and values an answer may have)
before anything moves. The same GP3 executor carries out each decision.

A **vision-language model (VLM)** reads camera images and describes the
cells for the agent. Your team places the cameras within the sensor budget:
$800 for a 1080p camera (grade A) and $500 for a 720p camera (grade B), from
the ARIAC Sensors page.

What GP4 tests
~~~~~~~~~~~~~~

GP4 tests the agent on the situations the GP3 domain does not model:

- a conveyor malfunction,
- a voltage tester malfunction,
- high-priority orders.

The vacuum tool malfunction affects only Task 2, so the final demo tests it,
not GP4. Your team then compares the agent with GP3 on the same trials.
Lectures L8 and L9 cover what GP4 needs.

.. note::

   GP4 asks for an agent, but a hybrid is a legitimate design: for example,
   the LLM chooses the goal and PDDL plans the steps, or PDDL runs the normal
   flow and the LLM is called only when a replanning trigger fires. A team
   may defend a hybrid in its reflection.


Learning Objectives
-------------------

After completing GP4, you will be able to:

- Write an agent loop with tool calling, stop conditions and a step limit.
- Specify a JSON schema for the agent's output and validate every response
  against it, with a bounded retry.
- Expose robot skills and ARIAC services to an LLM as tools, through MCP if
  your team chooses.
- Use a VLM to describe cells from camera images and feed the description
  to the agent as an observation.
- Compare the LLM agent with the GP3 planner on identical trials: plan
  validity, plan length, cost and latency.
- Evaluate the agent's failure modes and how the system caught them.


Provided Resources
------------------

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - Resource
     - What it gives you
   * - Your team's GP3 package
     - The executor, the selection step and the planner, for the
       comparison.
   * - An LLM and a VLM
     - A hosted API or local open-weight models. See
       :doc:`/ariac/ai_setup`. Cost guidance is given with the project.
   * - GP4 trial configurations
     - Trials with each challenge GP4 tests.

.. warning::

   **Never commit an API key.** Read it from an environment variable or a
   local ``.env`` file listed in ``.gitignore``.


Tasks
-----

.. dropdown:: Task 1: Write the orchestrator loop
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** an agent loop that always ends.

   **Requirements:**

   - Observe (topics, inspection results, the VLM description), ask the
     LLM, validate its output, run it through the executor, observe the
     result.
   - Stop when the goal is met, when a stop condition fires, or at the step
     limit.
   - Log each iteration: the observation, the model's choice, the tool
     result, the time and the token count.

.. dropdown:: Task 2: Write the tools and the output schema
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** no unchecked model output reaches the robots.

   **Requirements:**

   - Write a description for each tool, and a JSON schema for the agent's
     output.
   - On output that breaks the schema, re-prompt with the validation error.
     Stop after a fixed number of retries.
   - Write a test that feeds a malformed response, and keep its log.

.. dropdown:: Task 3: Place cameras and add the VLM step
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** the agent sees what the cameras see, in text.

   **Requirements:**

   - Place the cameras within the sensor budget, and add their cost to the
     GP2 total.
   - Write a VLM prompt that asks, for each cell, its type, its position
     and any visible defects, not only labels.
   - Turn the description into an observation for the agent.

   .. note::

      ARIAC requires lidar for defect detection, and its training defects
      reach only 0.84 to 2.49 mm off the surface (measured in L5). Whether
      they show in camera images has not been measured. Your GP2 lidar result decides the inspection report; treat a
      VLM defect call as a second opinion.

.. dropdown:: Task 4: Handle a conveyor malfunction
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** inspection pauses and resumes with the conveyor.

   **Requirements:**

   - Detect the malfunction on the conveyor status topic.
   - Pause inspection, and resume when the conveyor reports that it works
     again.

   .. note::

      The ARIAC documentation says the cell feed also pauses during a
      conveyor malfunction. The ARIAC code stops only the belt. Check what
      your trial does, and handle both.

.. dropdown:: Task 5: Handle a voltage tester malfunction
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** keep testing cells with the tester that still works.

   **Requirements:**

   - Detect that a tester is malfunctioning, use the other tester, and
     return to both when it reports ``OPERATIONAL`` again.
   - Check for two behaviors. The ARIAC Challenges page says the tester
     stops providing data. The ARIAC code (``voltage_tester_plugin.cpp``)
     keeps publishing, with ``operation_status`` set to ``MALFUNCTIONING``
     (value 2) and a voltage of -1.

.. dropdown:: Task 6: Handle a high-priority order
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** ship the urgent kit, then go back to the normal work.

   **Requirements:**

   - Detect the order on ``/high_priority_orders``.
   - Switch the cell feed to NiMH, and build a NiMH kit: 4 × 1.2 V = 4.8 V,
     ± 0.15 V, so the total must land from 4.65 V to 4.95 V.
   - Ship the kit, submit it with the order id, and switch the feed back to
     Li-Ion.

.. dropdown:: Task 7: Compare the agent with GP3
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a fair, measured comparison.

   **Requirements:**

   - Run GP3 and GP4 on the same trials: the same configurations and the
     same seeds.
   - Record plan validity, plan length, cost (tokens or dollars) and
     latency for each.
   - State the number of runs per trial. An LLM can answer differently on
     the same input, so one run per trial is not enough to compare.


Deliverables
------------

1. The agent module, the VLM module and the executor changes in your team's
   repository. Submit the link on Canvas.
2. A README that names the models used, their versions and settings, and
   how to supply API keys without committing them.
3. A run log for each challenge.
4. The side-by-side comparison with GP3 on identical trials (validity, plan
   length, cost, latency).
5. A reflection (1 to 2 pages) on the agent's failure modes and how they
   were caught.
6. The honor pledge, signed by every team member.


Submission Checklist
--------------------

.. admonition:: Before submitting, check every item
   :class: tip

   - [ ] No API key is anywhere in the repository history.
   - [ ] The README names each model, its version and its settings.
   - [ ] One run log shows each iteration and the stop condition that ended
         the loop.
   - [ ] The malformed-response test shows the re-prompt and the retry
         limit.
   - [ ] One log entry shows an image, the VLM description and the
         observation built from it.
   - [ ] There is a run log for each of the three challenges.
   - [ ] The comparison table states the trials, the seeds and the number
         of runs per trial.
   - [ ] Every failure named in the reflection comes with the log line or
         check that caught it.
   - [ ] Every team member signed the honor pledge.
   - [ ] Each member fills in the peer-review form after the deadline (see
         :ref:`peer-evaluation`).


Grading Rubric (Draft)
----------------------

.. admonition:: Draft rubric
   :class: note

   This rubric is a draft. It may change before GP4 is posted. The total is
   100 points, scaled to 10% of the course grade.

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Criterion
     - Points
     - How the grader checks it
   * - Agent loop
     - 15
     - The grader reads the orchestrator and one run log: each iteration
       shows the observation, the model's choice, the tool result, and a
       stop condition or step limit that ends the loop.
   * - Tools, schema and validation
     - 15
     - The grader reads the tool descriptions and the JSON schema, and runs
       the team's test that feeds a malformed response: the log shows the
       re-prompt with the error and the retry limit.
   * - VLM grounding
     - 10
     - The grader reads the VLM prompt and a log entry that shows an image,
       the VLM description and the agent observation built from it.
   * - Normal Task 1 trial
     - 10
     - The grader runs a trial with no challenges: the kits are submitted
       and accepted (ARIAC run results).
   * - Challenges handled
     - 20
     - The 20 points are split equally among the three challenges GP4 tests
       (conveyor malfunction, voltage tester malfunction, high-priority
       order): 20 / 3, about 6.7 points each. The grader reads the run log
       for each: the detection, the recovery action and the run continuing
       to the next kit. The high-priority order also needs the submission
       with the correct id in the ARIAC run results.
   * - Comparison with GP3
     - 15
     - The grader reads the table: both systems on the same trial
       configurations and seeds, with validity, plan length, cost and
       latency, and the number of runs per trial stated.
   * - Reflection on failure modes
     - 10
     - The grader reads the reflection: each failure named comes with the
       log line or check that caught it.
   * - Reproducibility
     - 5
     - The README names the models and settings, and the grader runs the
       system from it; no API key is in the repository.

The points add up to 15 + 15 + 10 + 10 + 20 + 15 + 10 + 5 = 100.


Common Mistakes
---------------

.. danger::

   - **Adding logging at the end.** The comparison needs the time and the
     token count of every call. Log every decision with its inputs,
     outputs, time and token count from the first day.
   - **Retrying a bad answer forever.** Re-prompt with the error, then stop
     after the fixed number of retries and fall back to a safe action.
   - **Checking only for silence from a tester.** In the ARIAC code a
     malfunctioning tester keeps publishing, with a voltage of -1. Check its
     status.
   - **Letting the LLM do arithmetic.** Keep the voltage sums in code, as
     in GP3, and give the agent the result.
   - **A comparison on different trials.** Run both systems on the same
     configurations and seeds.


Tips for Success
----------------

.. tip::

   **Ask first which challenges GP3 already handles.** For each challenge,
   decide whether your GP3 domain would handle it with no change. The ones
   it would not are where the agent has to earn its place.

.. tip::

   **Start with one challenge per trial.** Set the challenges in the trial
   configuration file (the ARIAC Configuration Files page has an example),
   and add them one at a time.
