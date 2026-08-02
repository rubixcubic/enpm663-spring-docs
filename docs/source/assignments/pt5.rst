====================================================
PT5: Integrated Capstone on an Unseen ARIAC Scenario
====================================================

.. list-table::
   :widths: 25 25 25 25
   :class: compact-table

   * - **Hand out:** Week 12
     - **Due:** Week 15
     - **Weight:** 20%
     - **Graded:** live, unseen

Goal
----

PT5 combines selected ARIAC challenges with scenarios drawn from PT1 through
PT4. Teams integrate their existing components (behavior tree, perception
pipeline, PDDL planner, LLM agent with VLM grounding) and apply the recovery
and robustness patterns from Week 12 to handle a scenario that includes
ARIAC-specific challenges not present in any single earlier PT. Manipulation
uses classical MoveIt2 with parameterized grasps; the AI complexity lives in
task planning, scene grounding, and replanning.

ARIAC Tie-in
------------

The challenge set (for example, faulty parts, faulty grippers, sensor
blackouts, kit rearrangement, high-priority orders) is published at hand-out
(Week 12). The exact ARIAC scenario used for grading is unseen by teams until
the live demo in Week 15, which preserves the unseen-scenario pedagogy of the
former final project.

Deliverable
-----------

- An integrated codebase.
- A live demo in class, graded on performance against the unseen scenario.
- A short presentation (5 to 7 minutes) covering architecture, design
  decisions, failure modes encountered, and how they were handled.

Relevant Lectures
-----------------

- Week 12: Recovery, Robustness, and Failure Handling for AI-Driven Systems.
- Week 13: Evaluation and Measurement Science for AI-Augmented Systems.
- Weeks 14 to 15: PT5 Lab and PT5 Demo.
