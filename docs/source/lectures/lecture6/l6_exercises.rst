====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises on the L6 slides and scripts. Exercises 1 and 3
change the domain or the generator and ask what the planner then does;
Exercise 2 has you write a problem by hand; Exercise 4 breaks plans for the
validator; Exercises 5 and 6 start on paper (the kit voltage window and the
ground action counts) and end with a run. In every exercise, predict the
result first, write the prediction down, then run the script.

.. note::

   The scripts are on the :doc:`code page <l6_code>`. Work on a copy of the
   ``code/`` and ``outputs/`` folders, so the originals still give the
   outputs in the notes: several scripts overwrite files in ``../outputs/``.
   Every run below was measured on 2026-10-12 with Python 3.12.3,
   ``unified-planning`` 1.3.0 and ``up-fast-downward`` 1.0.0 (Fast Downward
   26.6), with the venv of the code page active. Plans and counts were the
   same on every run; times in seconds differ from run to run.


.. dropdown:: Exercise 1. Break the Domain, Read the Plan
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Remove one delete effect and one precondition from ``domain.pddl``,
   predict what the planner does with each, and see that a mistake can hide
   in one problem and show in another.

   The notes show only the output of ``mistakes.py``. This exercise edits
   the script's ``MISTAKES`` dictionary (lines 15 to 22): read the full
   script on the :doc:`code page <l6_code>` (Demo 5) first. Each entry is
   the text to find, its replacement, and the step numbers to print.

   .. raw:: html

      <hr>

   **Part A. A missing delete effect**

   ``move-agv`` has the effect ``(and (agv-at ?a ?to) (not (agv-at ?a
   ?from)))``.

   1. Before you run anything: if the delete effect ``(not (agv-at ?a
      ?from))`` is removed, where is the AGV after a move? How could the
      planner use that to make a plan without a step it needs now?
   2. In your copy of ``mistakes.py``, add a third entry to ``MISTAKES``,
      after the second one:

      .. code-block:: python

         "move-agv without (not (agv-at ?a ?from))": (
             "(and (agv-at ?a ?to) (not (agv-at ?a ?from)))",
             "(agv-at ?a ?to)", (1, 18, 19)),

      The third item is the steps to print; a tuple works as well as a
      ``range``. Run ``python mistakes.py``.

   .. raw:: html

      <hr>

   **Part B. A missing precondition**

   ``place-in-slot`` needs ``(agv-at ?a inspection)``.

   3. Replace the three entries of ``MISTAKES`` with this one, which removes
      that precondition (the text ``(agv-at ?a inspection))`` appears once in
      the domain, at the end of the ``place-in-slot`` precondition):

      .. code-block:: python

         "place-in-slot without (agv-at ?a inspection)": (
             "(agv-at ?a inspection))", ")", range(1, 20)),

      Predict: does the plan for ``problem.pddl`` show the mistake? Run it.
   4. Copy ``problem.pddl`` to ``problem_shipping.pddl`` and change one fact:
      ``(agv-at agv1 inspection)`` becomes ``(agv-at agv1 shipping)``. In
      ``mistakes.py``, read ``problem_shipping.pddl`` instead of
      ``problem.pddl`` and print ``range(1, 21)``. Predict, then run.
   5. Plan ``problem_shipping.pddl`` with the correct domain (change the
      problem file name in your copy of ``plan_kit.py``). Where does the
      first ``move-agv`` come now?
   6. A validator replays the plan on the domain you give it. Would it
      accept the plans of questions 2 and 4 if you gave it the changed
      domain? What does that tell you about where these mistakes must be
      caught?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Without the delete effect, ``move-agv`` adds the new
      station and keeps the old one: the AGV is at both stations at once.
      The planner can then move agv1 to shipping at the start, load it "at
      inspection" (still true), and submit it "at shipping" without the
      second move.

      **Question 2.** Measured (the first two entries print as in the
      notes):

      .. code-block:: text

         move-agv without (not (agv-at ?a ?from)): 19 steps
          1. move-agv(agv1, inspection, shipping)
         18. check-kit(agv1, c1, c2, c3, c4)
         19. submit-kit(agv1)

      The plan still has 19 steps, but the move is now step 1. Steps 2 to
      17 load the kit and step 18 checks it, at an AGV that the model says
      is at both stations. Step 19 submits with no move after the check. In the
      factory, ``/agv1/move`` takes the AGV away before any cell is placed,
      so every ``place-in-slot`` fails.

      **Question 3.** No. The plan has 19 steps, and its only move is step
      18, after the check:

      .. code-block:: text

         place-in-slot without (agv-at ?a inspection): 19 steps
         ...
         17. check-kit(agv1, c1, c2, c3, c4)
         18. move-agv(agv1, inspection, shipping)
         19. submit-kit(agv1)

      In ``problem.pddl`` the AGV starts at inspection, and ``check-kit``
      also needs it there. So the planner never has a reason to place a
      cell while the AGV is somewhere else, and the missing precondition
      never shows.

      **Question 4.** Measured:

      .. code-block:: text

         place-in-slot without (agv-at ?a inspection): 20 steps
          1. pick-from-conveyor(inspection_robot_1, c1)
          2. place-on-tester(inspection_robot_1, c1, tester1)
          3. pick-from-conveyor(inspection_robot_1, c2)
          4. place-on-tester(inspection_robot_1, c2, tester2)
          5. pick-from-tester(inspection_robot_2, c1, tester1)
          6. pick-from-conveyor(inspection_robot_1, c3)
          7. place-on-tester(inspection_robot_1, c3, tester1)
          8. pick-from-conveyor(inspection_robot_1, c4)
          9. place-in-slot(inspection_robot_2, c1, agv1, s1)
         10. pick-from-tester(inspection_robot_2, c3, tester1)
         11. place-on-tester(inspection_robot_1, c4, tester1)
         12. place-in-slot(inspection_robot_2, c3, agv1, s3)
         13. pick-from-tester(inspection_robot_2, c4, tester1)
         14. place-in-slot(inspection_robot_2, c4, agv1, s4)
         15. pick-from-tester(inspection_robot_2, c2, tester2)
         16. place-in-slot(inspection_robot_2, c2, agv1, s2)
         17. move-agv(agv1, shipping, inspection)
         18. check-kit(agv1, c1, c2, c3, c4)
         19. move-agv(agv1, inspection, shipping)
         20. submit-kit(agv1)

      All four ``place-in-slot`` steps (9, 12, 14, 16) happen while agv1 is
      at shipping. The AGV comes to inspection only in step 17, because
      ``check-kit`` still needs it there.

      **Question 5.** With the correct domain the plan also has 20 steps,
      and the first step is ``move-agv(agv1, shipping, inspection)``: the
      AGV comes to inspection before any cell is placed (step 8 is the first
      ``place-in-slot``).

      **Question 6.** Yes. Each plan is valid for the domain it was made
      from: the validator checks the plan against the model, not the model
      against the factory. A model mistake must be caught by reading plans
      against the Task 1 steps, and by planning problems that start in
      different states (Part B needed the AGV at shipping to show the
      mistake).


.. dropdown:: Exercise 2. Write a Problem by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write the PDDL problem for a kit that is half done, predict the plan
   length, and see what the closed-world assumption does to a problem with
   a missing fact.

   .. raw:: html

      <hr>

   **Part A. A half-filled tray**

   The factory state, chosen for this exercise:

   - agv1 is at the inspection station. c1 is in slot s1 and c2 in slot s2
     (cells lock to the tray, so they stay). Slots s3 and s4 are free.
   - c3 is on tester1. Its averaged reading is in range.
   - c4 has passed the inspection door and waits on the conveyor.
   - tester2 is free, and both robots' hands are free.
   - The kit is c1 to c4 in s1 to s4, and it must be submitted.

   1. Write ``problem_half.pddl`` for ``domain.pddl``: the objects, the
      initial state (with the fixed facts of ``problem.pddl``) and the goal.
      Which ``voltage-ok`` facts do you need, and why does c4 get one before
      it is tested?
   2. Before you run anything: how many steps does the plan need? Count the
      actions for c3, for c4, and for the AGV.
   3. Plan it: in your copy of ``plan_kit.py``, read ``problem_half.pddl``
      instead of ``problem.pddl``.

   .. raw:: html

      <hr>

   **Part B. A missing fact**

   4. Delete the line with ``(in-slot c1 agv1 s1) (in-slot c2 agv1 s2)``
      from your problem, as if the generator had forgotten the tray. Predict
      what the planner reports, and why. Then run it.

   .. dropdown:: Solution
      :color: success

      **Question 1.** One answer:

      .. code-block:: lisp

         ; Exercise 2: agv1 already holds c1 and c2; c3 is on tester1 and
         ; tested in range; c4 has passed the door. State chosen for this example.
         (define (problem kit-half)
           (:domain task1)
           (:objects
             c1 c2 c3 c4 - cell
             inspection_robot_1 inspection_robot_2 - robot
             tester1 tester2 - tester
             agv1 - agv)
           (:init
             (picks-conveyor inspection_robot_1)
             (loads-agv inspection_robot_2)
             (serves inspection_robot_1 tester1)
             (serves inspection_robot_1 tester2)
             (serves inspection_robot_2 tester1)
             (serves inspection_robot_2 tester2)
             (hand-free inspection_robot_1)
             (hand-free inspection_robot_2)
             (on-tester c3 tester1) (tester-free tester2)
             (agv-at agv1 inspection)
             (in-slot c1 agv1 s1) (in-slot c2 agv1 s2)
             (slot-free agv1 s3) (slot-free agv1 s4)
             (at-door c4)
             (voltage-ok c3) (voltage-ok c4))
           (:goal (and
             (in-slot c3 agv1 s3) (in-slot c4 agv1 s4)
             (submitted agv1))))

      - c1 and c2 must be in the objects (``check-kit`` needs a cell in every
        slot), but they need no ``voltage-ok``: no action will move them.
      - c3 gets ``voltage-ok`` from its reading. c4 is untested, so it gets
        ``voltage-ok`` as an assumption, as ``gen_problem.py`` does for a
        cell with no reading.
      - ``(tester-free tester1)`` is not listed: c3 is on it.
      - The goal does not repeat ``(in-slot c1 agv1 s1)`` and
        ``(in-slot c2 agv1 s2)``: they are true already and no action can
        make them false. Adding them would not change the plan.

      **Question 2.** Count the actions:

      1. c3 is on a tester: ``pick-from-tester``, ``place-in-slot``. 2
         actions.
      2. c4 is at the door: ``pick-from-conveyor``, ``place-on-tester``,
         ``pick-from-tester``, ``place-in-slot``. 4 actions.
      3. The AGV: ``check-kit``, ``move-agv``, ``submit-kit``. 3 actions.

      2 + 4 + 3 = **9 steps**.

      **Question 3.** Measured:

      .. code-block:: text

         8 actions, 15 objects, 3 goal facts
         status: SOLVED_SATISFICING
          1. pick-from-conveyor(inspection_robot_1, c4)
          2. place-on-tester(inspection_robot_1, c4, tester2)
          3. pick-from-tester(inspection_robot_2, c3, tester1)
          4. place-in-slot(inspection_robot_2, c3, agv1, s3)
          5. pick-from-tester(inspection_robot_2, c4, tester2)
          6. place-in-slot(inspection_robot_2, c4, agv1, s4)
          7. check-kit(agv1, c1, c2, c3, c4)
          8. move-agv(agv1, inspection, shipping)
          9. submit-kit(agv1)

      9 steps, as counted. c4 goes to tester2, the free one. Still 15
      objects: 4 cells, 2 robots, 2 testers, 1 AGV, 2 stations and 4 slots.

      **Question 4.** Measured:

      .. code-block:: text

         8 actions, 15 objects, 3 goal facts
         status: UNSOLVABLE_PROVEN

      after which ``plan_kit.py`` stops with ``AttributeError: 'NoneType'
      object has no attribute 'actions'``: there is no plan to print.

      The reason is the closed-world assumption. With the line gone, nothing
      says c1 is in s1, and nothing says s1 is free either (it was never
      listed), so both are false. ``check-kit`` needs some cell in s1, and
      the only action that puts a cell in s1, ``place-in-slot``, needs
      ``(slot-free agv1 s1)``. No action makes that true, so ``check-kit``,
      and then ``submit-kit``, can never run. The planner proves that no
      plan exists. A generator that drops a fact does not get a warning; it
      gets no plan, or a wrong one.


.. dropdown:: Exercise 3. Change the Factory State in the Generator
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict the facts and goals that ``make_problem()`` writes for a new
   factory state, and the plan that follows.

   .. raw:: html

      <hr>

   **Part A. A second bad cell**

   In your copy of ``gen_problem.py``, change two lines of ``STATE``:

   .. code-block:: python

      "on_tester": {"tester1": "c6", "tester2": "c5"},
      "voltage": {"c5": 3.86, "c6": 3.31},

   1. Before you run anything: which ``voltage-ok`` and ``voltage-bad``
      facts does the generator write? Which goal facts?
   2. How many steps should the plan have? Start from the 21 steps of the
      notes.
   3. Run ``python gen_problem.py``, and read the goal in
      ``../outputs/problem_generated.pddl``.

   .. raw:: html

      <hr>

   **Part B. A good cell that is not in the kit**

   Start again from the original ``STATE``, and change only c5's reading:

   .. code-block:: python

      "voltage": {"c5": 3.80},

   4. Before you run anything: is 3.80 V in range for the generator? What
      goal does c5 get, and what does the planner do with c5?
   5. Run it. What happens to tester2 in the plan, and what would happen to
      it in the factory? Which step of the GP3 pipeline should have decided
      c5's place?

   .. dropdown:: Solution
      :color: success

      **Question 1.** The generator tests ``LOW <= v <= HIGH`` with
      ``LOW`` = 3.4 and ``HIGH`` = 3.8.

      - c1 to c4 have no reading: ``voltage-ok`` (assumed).
      - c5: 3.86 > 3.8, so ``voltage-bad`` and the goal ``(recycled c5)``.
      - c6: 3.31 < 3.4, so ``voltage-bad`` and the goal ``(recycled c6)``.

      Both testers are occupied, so neither ``tester-free`` fact is written.
      The goal, as written:

      .. code-block:: lisp

         (:goal (and
           (recycled c6)
           (recycled c5)
           (in-slot c1 agv1 s1)
           (in-slot c2 agv1 s2)
           (in-slot c3 agv1 s3)
           (in-slot c4 agv1 s4)
           (submitted agv1)
         )))

      c6 comes first because ``make_problem()`` walks the testers in the
      order tester1, tester2.

      **Question 2.** The notes' plan has 21 steps: the 19 of the four-cell
      plan plus 2 for c5 (``pick-from-tester``, ``recycle``). c6 needs the
      same 2. 21 + 2 = **23 steps**.

      **Question 3.** Measured:

      .. code-block:: text

         status: SOLVED_SATISFICING
          1. pick-from-tester(inspection_robot_2, c6, tester1)
          2. pick-from-conveyor(inspection_robot_1, c1)
          3. recycle(inspection_robot_2, c6)
          4. place-on-tester(inspection_robot_1, c1, tester1)
          5. pick-from-tester(inspection_robot_2, c1, tester1)
          6. place-in-slot(inspection_robot_2, c1, agv1, s1)
          7. pick-from-conveyor(inspection_robot_1, c2)
          8. place-on-tester(inspection_robot_1, c2, tester1)
          9. pick-from-tester(inspection_robot_2, c2, tester1)
         10. place-in-slot(inspection_robot_2, c2, agv1, s2)
         11. pick-from-conveyor(inspection_robot_1, c3)
         12. place-on-tester(inspection_robot_1, c3, tester1)
         13. pick-from-conveyor(inspection_robot_1, c4)
         14. pick-from-tester(inspection_robot_2, c3, tester1)
         15. place-in-slot(inspection_robot_2, c3, agv1, s3)
         16. place-on-tester(inspection_robot_1, c4, tester1)
         17. pick-from-tester(inspection_robot_2, c5, tester2)
         18. recycle(inspection_robot_2, c5)
         19. pick-from-tester(inspection_robot_2, c4, tester1)
         20. place-in-slot(inspection_robot_2, c4, agv1, s4)
         21. check-kit(agv1, c1, c2, c3, c4)
         22. move-agv(agv1, inspection, shipping)
         23. submit-kit(agv1)

      23 steps. The planner clears c6 first (steps 1 and 3), so tester1 is
      free for c1. c5 stays on tester2 until steps 17 and 18, and every
      cell of the kit goes through tester1: the plan has no time, so it sees
      no cost in waiting.

      **Question 4.** Yes: 3.80 is equal to ``HIGH``, and the test uses
      ``<=``, so c5 gets ``voltage-ok``. It is not in ``STATE["kit"]``, so
      it gets **no goal** at all. The planner has no reason to move it, and
      it stays on tester2.

      **Question 5.** Measured: 19 steps, the same length as the four-cell
      plan, and no step uses tester2 or c5. All four cells go through
      tester1 (steps 2, 6, 10 and 14 are ``place-on-tester`` on tester1).
      In the factory, a good cell would sit on tester2 for the whole kit,
      and only one tester would work. The selection step (tag 1 in
      :ref:`the GP3 pipeline <l6-gp3>`) should give every measured,
      in-range cell a place: a slot of agv1, or the next kit, as
      ``select_cells.py`` sends c3 to agv2. Then the generator writes a goal
      for it.


.. dropdown:: Exercise 4. Break a Plan for the Validator
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict the validator's verdict, reason and failed step for three edited
   plans.

   .. raw:: html

      <hr>

   **Parts**

   ``validate_plan.py`` edits ``plan.txt`` in line 15. Each edit below
   replaces that line; run ``python plan_kit.py`` first if
   ``../outputs/plan.txt`` is missing. The last three lines of
   ``plan.txt`` are steps 17 to 19: ``check-kit``, ``move-agv``,
   ``submit-kit``.

   1. Delete step 17 (``check-kit``): ``del lines[16]``.
   2. Delete step 19 (``submit-kit``): ``del lines[18]``.
   3. Swap steps 18 and 19: ``lines[17], lines[18] = lines[18], lines[17]``.

   For each one, before you run it: is the plan valid? If not, what is the
   reason, which step fails first, and which fact is missing? Then run
   ``python validate_plan.py``.

   4. Edit 2 fails in a different way from edits 1 and 3. Why does the
      validator name no failed step?

   .. dropdown:: Solution
      :color: success

      **Edit 1.** Without ``check-kit``, ``(kit-checked agv1)`` is never
      true. ``move-agv`` (now step 17) has no such precondition and runs;
      ``submit-kit`` (now step 18) fails:

      .. code-block:: text

         validator: sequential_plan_validator
         plan.txt: VALID
         plan_swapped.txt: INVALID
           reason: INAPPLICABLE_ACTION
           failed step: submit-kit(agv1)
           log: Preconditions [kit-checked(agv1)] of 18-th action instance submit-kit(agv1) are not satisfied.

      The log says "18-th" because the deletion moved every later step up
      by one. The step numbers in a validator's message refer to the plan
      it was given.

      **Edit 2.** Every action still applies, but ``(submitted agv1)`` is
      never made true:

      .. code-block:: text

         validator: sequential_plan_validator
         plan.txt: VALID
         plan_swapped.txt: INVALID
           reason: UNSATISFIED_GOALS
           failed step: None
           log: Goals [(in-slot(c1, agv1, s1) and in-slot(c2, agv1, s2) and in-slot(c3, agv1, s3) and in-slot(c4, agv1, s4) and submitted(agv1))] are not satisfied by the plan.

      **Edit 3.** ``submit-kit`` now comes before ``move-agv``, and agv1 is
      still at inspection:

      .. code-block:: text

         validator: sequential_plan_validator
         plan.txt: VALID
         plan_swapped.txt: INVALID
           reason: INAPPLICABLE_ACTION
           failed step: submit-kit(agv1)
           log: Preconditions [agv-at(agv1, shipping)] of 18-th action instance submit-kit(agv1) are not satisfied.

      **Question 4.** A plan is valid if every precondition holds on the way
      **and** the goal holds at the end. Edit 2 passes the first test, so no
      step fails; it fails the second. The log prints the whole goal as one
      ``and``, not only the missing fact, so you find ``submitted(agv1)`` by
      reading it against the final state.


.. dropdown:: Exercise 5. The Kit Voltage Window by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the selection step's arithmetic on paper for a new set of cells,
   check it with ``select_cells.py``, then see what a safety margin does to
   the window.

   .. raw:: html

      <hr>

   **Part A. On paper**

   Six Li-Ion cells arrive measured, in this order (voltages chosen for this
   exercise): c1 3.78 V, c2 3.76 V, c3 3.70 V, c4 3.58 V, c5 3.52 V,
   c6 3.41 V. The limits are those of the notes: each cell from 3.4 V to
   3.8 V, the kit of four from 14.25 V to 14.55 V.

   1. c1 and c2 go on agv1. What range must the last two cells add up to?
   2. What is the highest third cell that still lets the kit finish? Which
      of c3 and c4 can be the third cell?
   3. After the third cell, what range is left for the fourth? Which
      arriving cell completes the kit, and what is the total?
   4. Without look-ahead, every in-range cell goes on agv1. What happens?

   .. raw:: html

      <hr>

   **Part B. Check with the script**

   5. In your copy of ``select_cells.py``, replace ``ARRIVALS``:

      .. code-block:: python

         ARRIVALS = [("c1", 3.78), ("c2", 3.76), ("c3", 3.70),
                     ("c4", 3.58), ("c5", 3.52), ("c6", 3.41)]

      Run ``python select_cells.py`` and compare with Part A.

   .. raw:: html

      <hr>

   **Part C. A margin for noisy readings**

   Your team knows each voltage only as an average of 10 noisy readings,
   with a standard deviation of 0.016 V (the notes, from L5). ARIAC scores
   the true voltages.

   6. The kit total is a sum of four such averages. If their errors are
      independent, what is the standard deviation of the total?
   7. Shrink the kit window by a margin of 0.03 V on each side (chosen for
      this exercise, close to your answer to question 6): in your copy,
      replace the ``KIT_LOW`` and ``KIT_HIGH`` lines with

      .. code-block:: python

         MARGIN = 0.03
         KIT_LOW = round(4 * NOMINAL - KIT_TOL + MARGIN, 2)  # 14.28
         KIT_HIGH = round(4 * NOMINAL + KIT_TOL - MARGIN, 2) # 14.52

      Before you run it: which cells now go on agv1? Then run it, and
      explain the last line.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      1. The tray holds 3.78 + 3.76 = 7.54 V.
      2. The last two must add up to between 14.25 − 7.54 = 6.71 V and
         14.55 − 7.54 = 7.01 V.

      **Question 2.**

      1. The fourth cell is at least 3.4 V, so the third can be at most
         7.01 − 3.4 = 3.61 V.
      2. The fourth cell is at most 3.8 V, so the third must be at least
         6.71 − 3.8 = 2.91 V. Every cell in range is above that, so this
         limit does nothing.
      3. c3 (3.70 V) is above 3.61 V: it would block agv1, so it goes to
         agv2. c4 (3.58 V) is below 3.61 V: it is the third cell.

      **Question 3.**

      1. The tray holds 7.54 + 3.58 = 11.12 V.
      2. The fourth cell must be from 14.25 − 11.12 = 3.13 V to
         14.55 − 11.12 = 3.43 V. With the cell limit of 3.4 V, that leaves
         3.40 V to 3.43 V.
      3. c5 (3.52 V) is too high: agv2. c6 (3.41 V) fits.
      4. Total: 3.78 + 3.76 + 3.58 + 3.41 = 14.53 V, inside 14.25 V to
         14.55 V.

      **Question 4.** c1, c2 and c3 go on agv1: 3.78 + 3.76 + 3.70 =
      11.24 V. The fourth cell would have to be from 14.25 − 11.24 =
      3.01 V to 14.55 − 11.24 = 3.31 V, below every cell in range. The kit
      is lost, and agv1 goes to recycling.

      **Question 5.** Measured:

      .. code-block:: text

         3 cells at 3.75 V: rest must sum to 3.00 to 3.30 V; can finish: False
         2 cells at 3.75 V: rest must sum to 6.75 to 7.05 V; can finish: True
         look ahead: False
           c1 3.78 V: agv1 slot 1; rest must sum to 10.47 to 10.77 V
           c2 3.76 V: agv1 slot 2; rest must sum to 6.71 to 7.01 V
           c3 3.70 V: agv1 slot 3; rest must sum to 3.01 to 3.31 V
           kit total 11.24 V: lost, agv1 to recycling
         look ahead: True
           c1 3.78 V: agv1 slot 1; rest must sum to 10.47 to 10.77 V
           c2 3.76 V: agv1 slot 2; rest must sum to 6.71 to 7.01 V
           c3 3.70 V: agv2 (blocks agv1)
           c4 3.58 V: agv1 slot 3; rest must sum to 3.13 to 3.43 V
           c5 3.52 V: agv2 (blocks agv1)
           c6 3.41 V: agv1 slot 4; kit full
           kit total 14.53 V: complete
           goal: (in-slot c1 agv1 s1)
           goal: (in-slot c2 agv1 s2)
           goal: (in-slot c4 agv1 s3)
           goal: (in-slot c6 agv1 s4)

      The script agrees with Part A. Its "rest must sum to" line after c4
      gives 3.13 to 3.43 V before the cell limit is applied; ``can_finish``
      applies the limit.

      **Question 6.** For independent errors, variances add. The variance
      of the total is 4 × 0.016² V², so its standard deviation is
      √4 × 0.016 = 2 × 0.016 = 0.032 V.

      **Question 7.** The kit window is now 14.28 V to 14.52 V.

      1. After c1 and c2 (7.54 V), the last two must add up to
         14.28 − 7.54 = 6.74 V to 14.52 − 7.54 = 6.98 V.
      2. The third cell can be at most 6.98 − 3.4 = 3.58 V. c3 (3.70 V) is
         out; c4 (3.58 V) is exactly at the limit, so it goes on agv1.
      3. The fourth must be from 14.28 − 11.12 = 3.16 V to
         14.52 − 11.12 = 3.40 V, and at least 3.4 V: only a cell at exactly
         3.40 V fits. c5 (3.52 V) and c6 (3.41 V) are both too high.

      Measured, the look-ahead half of the output:

      .. code-block:: text

         look ahead: True
           c1 3.78 V: agv1 slot 1; rest must sum to 10.50 to 10.74 V
           c2 3.76 V: agv1 slot 2; rest must sum to 6.74 to 6.98 V
           c3 3.70 V: agv2 (blocks agv1)
           c4 3.58 V: agv1 slot 3; rest must sum to 3.16 to 3.40 V
           c5 3.52 V: agv2 (blocks agv1)
           c6 3.41 V: agv2 (blocks agv1)
           kit total 11.12 V: lost, agv1 to recycling

      The last line says "lost" because ``fill_kit`` ran out of arrivals
      with three cells on agv1, and the script prints "lost" for any kit
      that is not complete. agv1 is not lost yet: a later cell at exactly
      3.40 V would finish it. But such a cell is itself at the cell limit,
      where the same noise applies. The margin made c6 wait, where the
      plain window accepted a kit 0.02 V below its top edge (14.55 − 14.53
      = 0.02 V, less than one standard deviation of the total). c4, taken
      at the very edge of the third-cell limit, is what left so little room
      for the fourth.


.. dropdown:: Exercise 6. Count the Ground Actions, Then Shrink Them
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Derive the translator's ground action counts from the domain, then apply
   the notes' suggestion, a per-slot fact ``(filled ?a ?s)``, and measure
   what it changes.

   .. raw:: html

      <hr>

   **Part A. On paper**

   Use ``outputs/ground_actions.txt`` from the notes (small: 4 cells, 1 AGV;
   large: 8 cells, 2 AGVs). Remember that ``serves``, ``picks-conveyor`` and
   ``loads-agv`` are fixed facts: the translator drops a ground action whose
   fixed facts are false.

   1. Explain the 16 of ``pick-from-tester`` (small) and the 16 and 64 of
      ``place-in-slot`` (small and large).
   2. ``recycle`` is one of the eight actions, but it has no row. Why?

   .. raw:: html

      <hr>

   **Part B. A per-slot fact**

   3. In a copy of the domain, ``domain_filled.pddl``, make three changes:

      - add the predicate ``(filled ?a - agv ?s - slot)``;
      - add ``(filled ?a ?s)`` to the effect of ``place-in-slot``;
      - make ``check-kit`` take only the AGV:

        .. code-block:: lisp

           (:action check-kit
             :parameters (?a - agv)
             :precondition (and (agv-at ?a inspection)
                                (filled ?a s1) (filled ?a s2)
                                (filled ?a s3) (filled ?a s4))
             :effect (kit-checked ?a))

   4. Before you run anything: how many ground actions does each problem
      now have? Will the plans get longer or shorter?
   5. Run Fast Downward from the command line on both problems, with the
      venv active, from ``code/``:

      .. code-block:: bash

         FD="$(python -c 'import os, up_fast_downward as u; print(os.path.join(os.path.dirname(u.__file__), "downward", "fast-downward.py"))')"
         python "$FD" --plan-file filled_small.plan domain_filled.pddl problem.pddl --search "astar(lmcut())" | grep -e "Translator operators" -e "Plan length" -e "Expanded [0-9]"
         python "$FD" --plan-file filled_large.plan domain_filled.pddl ../outputs/problem_large.pddl --search "astar(lmcut())" | grep -e "Translator operators" -e "Plan length" -e "Expanded [0-9]"

      Compare with ``outputs/fd_summary.txt``. The notes quote only its
      expanded-state counts (124 and 2346); the full file is on the
      :doc:`code page <l6_code>`, under "Run everything".

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      - ``pick-from-tester`` has parameters robot, cell and tester. Both
        robots serve both testers, so all combinations stay:
        2 × 4 × 2 = 16.
      - ``place-in-slot`` has robot, cell, AGV and slot, but only
        inspection_robot_2 has ``loads-agv``. Small: 1 × 4 × 1 × 4 = 16.
        Large: 1 × 8 × 2 × 4 = 64.

      **Question 2.** ``recycle`` needs ``(voltage-bad ?c)``. Neither problem
      lists a ``voltage-bad`` fact, and no action makes one true, so no
      ground ``recycle`` can ever apply. The translator keeps only the
      ground actions that can ever apply, so it writes none.

      **Question 4.** Only ``check-kit`` changes: it now has one parameter,
      so it has one ground action per AGV, 1 (small) and 2 (large), instead
      of 256 and 8192.

      1. Small: 311 − 256 + 1 = **56**.
      2. Large: 8334 − 8192 + 2 = **144**.

      The plans keep the same length: each step does what it did before, and
      ``check-kit`` is still one step per kit. So 19 and 38 steps.

      **Question 5.** Measured (the time stamps at the start of the lines
      are left out):

      .. code-block:: text

         Translator operators: 56
         Plan length: 19 step(s).
         Expanded 22 state(s).
         Translator operators: 144
         Plan length: 38 step(s).
         Expanded 97 state(s).

      .. list-table::
         :header-rows: 1
         :widths: 40 15 15 15 15
         :class: compact-table

         * -
           - **Small, before**
           - **Small, after**
           - **Large, before**
           - **Large, after**
         * - Ground actions
           - 311
           - 56
           - 8334
           - 144
         * - Plan length
           - 19
           - 19
           - 38
           - 38
         * - Expanded states
           - 124
           - 22
           - 2346
           - 97

      The counts match the prediction, and the plans are as short as before.
      The search also expanded far fewer states: 2346 / 97 = 24.2 times
      fewer on the large problem. The search time of the large problem fell
      from 15.549870 s (``fd_summary.txt``) to 0.015796 s in one run with
      ``run_all.sh``'s settings. The plan now says ``check-kit agv1``: the
      executor must find the four cells from its own records, which it
      keeps anyway.
