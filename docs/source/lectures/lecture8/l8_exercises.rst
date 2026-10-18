====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes, the four group projects and
   the final demo listed in the :doc:`syllabus </syllabus/index>`.

Five take-home exercises on the L8 slides and scripts. Exercises 1 and 5 are
paper and arithmetic: token growth for other run lengths, and model latency
against the factory's clocks. Exercises 2 to 4 change one script each: the
scripted model's replies in the orchestrator, the validator and an MCP
server. Predict the result first, write the prediction down, then run the
script.

.. note::

   The scripts are on the :doc:`code page <l8_code>`. Work on a copy of each
   script, so the original still gives the outputs in the notes. Exercises 1
   to 3 run offline with the system Python 3.12.3 and ``jsonschema`` 4.10.3,
   with no ARIAC and no API key. Exercise 4 runs with ``mcp`` 2.3.0 from the
   lecture's virtual environment, and needs no ARIAC either. Every output
   below was made on 2026-10-17. They all use scripted replies or plain code,
   so your outputs should match these exactly.


.. dropdown:: Exercise 1. Token Growth for Other Run Lengths
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the lecture's formula for the input tokens of a ReAct run on run
   lengths the slides did not show, then check your numbers with
   ``token_growth.py``.

   Use the lecture's values: :math:`F` = 1264 tokens sent on every call and
   :math:`h` = 261 tokens added by each earlier step (both measured in Run
   1), 16 output tokens per ReAct call (Run 1's mean, rounded), and the
   Gemini prices of ``gemini_prices.py``, $0.30 per million input tokens and
   $2.50 per million output tokens.

   .. raw:: html

      <hr>

   **Part A. Paper**

   1. For :math:`n` = 8 and :math:`n` = 30 steps, compute the tokens sent by
      the last call and the total input tokens over the run.
   2. Compute the cost of each run, input and output.
   3. Find the smallest number of steps for which the total input is above
      100,000 tokens.
   4. The slides say that twice the steps gives about four times the history.
      Check it: compute the history term :math:`h\,n(n - 1)/2` for
      :math:`n` = 20 and :math:`n` = 40, and their ratio.

   .. raw:: html

      <hr>

   **Part B. Keep the history short**

   The slides suggest summarizing old steps. Suppose the orchestrator sends
   only the last 5 steps in full, and drops the older ones (ignore the tokens
   of any summary).

   5. For :math:`n` = 20, compute the total input tokens, and compare with the
      74,870 of the full history.
   6. Compute the cost of that run.

   .. raw:: html

      <hr>

   **Part C. Check with the script**

   7. In a copy of ``token_growth.py``, change both loops to
      ``for n in (8, 23, 24, 30):`` and run it. Compare with Part A.

   .. dropdown:: Solution
      :color: success

      **Question 1.** Call :math:`k` sends :math:`F + (k - 1)\,h`; the run
      sends :math:`nF + h\,n(n - 1)/2`.

      - :math:`n` = 8: last call 1264 + 7 × 261 = 1264 + 1827 = 3091 tokens.
        Total 8 × 1264 + 261 × 8 × 7 / 2 = 10,112 + 7308 = 17,420 tokens.
      - :math:`n` = 30: last call 1264 + 29 × 261 = 1264 + 7569 = 8833
        tokens. Total 30 × 1264 + 261 × 30 × 29 / 2 = 37,920 + 113,535 =
        151,455 tokens.

      **Question 2.**

      - :math:`n` = 8: input 17,420 × 0.30 / 1,000,000 = $0.005226. Output
        8 × 16 = 128 tokens, 128 × 2.50 / 1,000,000 = $0.00032. Total
        $0.005546.
      - :math:`n` = 30: input 151,455 × 0.30 / 1,000,000 = $0.0454365.
        Output 30 × 16 = 480 tokens, 480 × 2.50 / 1,000,000 = $0.0012. Total
        $0.0466365.

      **Question 3.** **24 steps.**

      1. :math:`n` = 23: 23 × 1264 + 261 × 23 × 22 / 2 = 29,072 + 66,033 =
         95,105 tokens, below 100,000.
      2. :math:`n` = 24: 24 × 1264 + 261 × 24 × 23 / 2 = 30,336 + 72,036 =
         102,372 tokens, above 100,000.

      **Question 4.** For :math:`n` = 20: 261 × 20 × 19 / 2 = 49,590. For
      :math:`n` = 40: 261 × 40 × 39 / 2 = 203,580. The ratio is
      203,580 / 49,590 = 4.1, so "about four times" holds. It is not exactly
      4 because :math:`n(n - 1)` is not exactly :math:`n^2`.

      **Question 5.**

      1. Calls 1 to 6 still send all earlier steps (at most 5):
         6 × 1264 + 261 × (0 + 1 + 2 + 3 + 4 + 5) = 7584 + 3915 = 11,499
         tokens.
      2. Calls 7 to 20, 14 calls, each send :math:`F + 5h`
         = 1264 + 5 × 261 = 2569 tokens: 14 × 2569 = 35,966 tokens.
      3. Total 11,499 + 35,966 = **47,465 tokens**, which is
         74,870 − 47,465 = 27,405 fewer, or 27,405 / 74,870 = 37% less.

      With a fixed window the input of each call stops growing after step 6,
      so the total grows in a straight line with :math:`n`, not with its
      square.

      **Question 6.** Input 47,465 × 0.30 / 1,000,000 = $0.0142395, plus the
      same $0.0008 of output (320 tokens): **$0.0150395**, against $0.023261
      with the full history.

      **Question 7.** The output of the edited script:

      .. code-block:: text

         ReAct, one call per step
         steps last call   input output  cost $
             8      3091   17420    128  0.0055
            23      7006   95105    368  0.0295
            24      7267  102372    384  0.0317
            30      8833  151455    480  0.0466
         Plan-and-execute, one plan and one replan
         steps     calls   input output  cost $
             8         2    2528    640  0.0024
            23         2    2528   1840  0.0054
            24         2    2528   1920  0.0056
            30         2    2528   2400  0.0068

      The ReAct rows match Part A; the script rounds the cost to four
      decimals. Plan-and-execute still sends 2528 input tokens at every
      length; only its output (2 calls × :math:`n` steps × 40 tokens, the
      chosen ``PLAN_OUT``) grows.


.. dropdown:: Exercise 2. Make the Loop Hit Each Stop Condition
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Change the scripted model's replies in ``orchestrator.py`` so that the
   loop ends for each reason it checks, and find a case where the stop
   reason is not the one you expect.

   The loop runs offline on the stand-in factory, ``FakeTools``: each skill
   call adds 20 s of simulation time, and the first cell reads 3.61 V
   (chosen for this example). In a copy, ``my_loop.py``, replace the line
   ``RUN2_REPLIES = ...`` with your own list, and run it as Run 2:

   .. code-block:: bash

      python3 my_loop.py --fake --runs 2

   Use the helper ``act(name, **args)`` for a tool call, ``{"text":
   "done"}`` for a reply with no tool call, and keep ``MAX_STEPS`` = 15 and
   ``MAX_INVALID`` = 2. ``DRY_REPLIES`` holds the five replies that do the
   whole task. Give each list at least as many replies as the loop will ask
   for: ``ScriptedModel`` raises ``IndexError`` when it runs out.

   .. raw:: html

      <hr>

   **Part A. Each stop reason**

   1. Write a list that ends with ``stop: step limit``. How many calls does
      the loop make?
   2. Write a list that ends with ``2 invalid outputs in a row`` because of
      a tool name that does not exist, for example ``submit_kit``.
   3. Write a list whose first reply is ``{"text": "done"}``, followed by
      ``DRY_REPLIES``. ``RUN2_REPLIES`` is defined above ``DRY_REPLIES``, so
      delete the old ``RUN2_REPLIES`` line and put yours right after the
      ``DRY_REPLIES`` definition; otherwise Python raises ``NameError``. What
      does the orchestrator send back? Does that reply
      count as an invalid output?

   .. raw:: html

      <hr>

   **Part B. Invalid, valid, invalid**

   4. Run this list: robot 2 picks from tester 1, robot 1 picks from the
      conveyor, robot 2 picks from tester 1, robot 1 places on tester 1,
      robot 2 places in agv1 slot 1, robot 2 picks from tester 1, robot 2
      places in agv1 slot 1, ``done``. Three calls are refused. Why does the
      run not stop on ``MAX_INVALID``?
   5. Run ``DRY_REPLIES[:4] + [act("robot1_move_home")] * 11`` (again on a
      line after the ``DRY_REPLIES`` definition): the task, then no "done". After call 4, agv1 slot 1 holds the tested cell. What
      is the stop reason, and why?

   .. raw:: html

      <hr>

   **Part C. Check the goal after every result**

   6. Change ``run()`` so it checks ``goal_check(snap, rec)`` right after it
      prints each ``obs`` line. Rerun question 5's list. What changes?

   .. raw:: html

      <hr>

   **Part D. A time limit**

   7. The lecture lists a stop condition that the demo does not check: the
      trial's time limit. Add one in simulation time, as ARIAC counts it: at
      the top of each step, return ``"time limit"`` once
      ``snap["sim_time_s"]`` is above ``TIME_LIMIT_S`` = 50 s (chosen for
      this exercise). Run the whole task with ``--runs dry``. How many calls
      run?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Fifteen valid calls that never place a cell, and no
      "done":

      .. code-block:: python

         RUN2_REPLIES = [act("robot1_move_home")] * 15

      The loop makes **15 calls**, all ``SUCCESS``, then stops. The last
      lines of the output:

      .. code-block:: text

         call 15: 29 messages; scripted
           model:  robot1_move_home({})
           result: {"code": "SUCCESS", "holding": "NOTHING", "message": "parked", "attempts": 1, "wall_s": 0.0}
         obs 15:  t=300.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots ---- | robot 1 NOTHING, robot 2 NOTHING
         stop: step limit

      **Question 2.** ``RUN2_REPLIES = [act("submit_kit")] * 2``. The first
      step of ``check_call()`` refuses a tool that is not declared:

      .. code-block:: text

         === Run 2 (scripted model: fixed replies) ===
         goal:   Put one Li-Ion cell from the conveyor into agv1 slot 1. Test its voltage on tester 1 first.
         obs 0:  t=0.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots ---- | robot 1 NOTHING, robot 2 NOTHING
         call 1: 1 messages; scripted
           model:  submit_kit({})
           orch:   {"error": "refused: unknown tool 'submit_kit'"}
         obs 1:  t=0.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots ---- | robot 1 NOTHING, robot 2 NOTHING
         call 2: 3 messages; scripted
           model:  submit_kit({})
           orch:   {"error": "refused: unknown tool 'submit_kit'"}
         stop: 2 invalid outputs in a row

      No robot moved, so the simulation time stays at 0.0 s.

      **Question 3.** With ``RUN2_REPLIES = [{"text": "done"}] +
      DRY_REPLIES`` after the ``DRY_REPLIES`` definition, the first lines of
      the output:

      .. code-block:: text

         call 1: 1 messages; scripted
           model:  text 'done'
           orch:   goal not reached (checked in code)
         call 2: 3 messages; scripted
           model:  robot1_pick_from_conveyor({})

      and the run ends ``call 6: ... model: text 'done'``, then
      ``stop: goal reached``. The orchestrator checks the goal in code, finds
      slot 1 empty, and sends back ``"error": "goal not reached"`` with the
      observation and the record. It is **not** counted as invalid:
      ``invalid`` goes up only when ``check_call()`` refuses a tool call.
      This is the warning from the slides in action: the model said "done",
      and the code decided it was not.

      **Question 4.** The list:

      .. code-block:: python

         RUN2_REPLIES = [act("robot2_pick_from_tester", tester=1), act("robot1_pick_from_conveyor"),
                         act("robot2_pick_from_tester", tester=1), act("robot1_place_on_tester", tester=1),
                         act("robot2_place_in_slot", agv=1, slot=1), act("robot2_pick_from_tester", tester=1),
                         act("robot2_place_in_slot", agv=1, slot=1), {"text": "done"}]

      The model and orchestrator lines of the output:

      .. code-block:: text

         call 1: 1 messages; scripted
           model:  robot2_pick_from_tester({"tester": 1})
           orch:   {"error": "refused: tester 1 is empty (0.00 V)"}
         call 2: 3 messages; scripted
           model:  robot1_pick_from_conveyor({})
           result: {"code": "SUCCESS", "holding": "CELL", "message": "", "attempts": 1, "wall_s": 0.0}
         call 3: 5 messages; scripted
           model:  robot2_pick_from_tester({"tester": 1})
           orch:   {"error": "refused: tester 1 is empty (0.00 V)"}
         call 4: 7 messages; scripted
           model:  robot1_place_on_tester({"tester": 1})
           result: {"code": "SUCCESS", "holding": "NOTHING", "message": "", "attempts": 1, "wall_s": 0.0}
         call 5: 9 messages; scripted
           model:  robot2_place_in_slot({"agv": 1, "slot": 1})
           orch:   {"error": "refused: robot 2 holds NOTHING, needs CELL"}
         call 6: 11 messages; scripted
           model:  robot2_pick_from_tester({"tester": 1})
           result: {"code": "SUCCESS", "holding": "CELL", "message": "", "attempts": 1, "wall_s": 0.0}
         call 7: 13 messages; scripted
           model:  robot2_place_in_slot({"agv": 1, "slot": 1})
           result: {"code": "SUCCESS", "holding": "NOTHING", "message": "", "attempts": 1, "wall_s": 0.0}
         call 8: 15 messages; scripted
           model:  text 'done'
         stop: goal reached

      ``MAX_INVALID`` counts invalid outputs **in a row**. Each valid call
      sets ``invalid = 0``, so the count never gets past 1. Three of this
      run's eight calls were refused, and the limit never fired. A team that
      wants to catch this pattern needs a second limit on the total number
      of invalid outputs.

      **Question 5.** ``stop: step limit``, after 15 calls, even though
      ``obs 4`` already shows ``slots 1---``. The demo checks the goal only
      when the model replies with no tool call, and this model never said
      "done". Its last eleven calls parked robot 1 again and again:

      .. code-block:: text

         obs 4:  t=80.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots 1--- | robot 1 NOTHING, robot 2 NOTHING
         call 5: 9 messages; scripted
           model:  robot1_move_home({})
         ...
         call 15: 29 messages; scripted
           model:  robot1_move_home({})
           result: {"code": "SUCCESS", "holding": "NOTHING", "message": "parked", "attempts": 1, "wall_s": 0.0}
         obs 15:  t=300.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots 1--- | robot 1 NOTHING, robot 2 NOTHING
         stop: step limit

      **Question 6.** The change, right after the line that prints ``obs``:

      .. code-block:: python

         if goal_check(snap, rec):
             return "goal reached"

      Question 5's list now ends after call 4:

      .. code-block:: text

         call 4: 7 messages; scripted
           model:  robot2_place_in_slot({"agv": 1, "slot": 1})
           result: {"code": "SUCCESS", "holding": "NOTHING", "message": "", "attempts": 1, "wall_s": 0.0}
         obs 4:  t=80.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots 1--- | robot 1 NOTHING, robot 2 NOTHING
         stop: goal reached

      The run saves eleven calls, and with a real model the cost and the
      wait of each. Either design is valid; what matters is that the goal
      check is code, not the model's word.

      **Question 7.** **3 calls**, then ``stop: time limit``. The change:

      .. code-block:: python

         TIME_LIMIT_S = 50    # simulation s, chosen for this exercise

      and, as the first lines inside ``for step in range(...)``:

      .. code-block:: python

         if snap["sim_time_s"] > TIME_LIMIT_S:
             return "time limit"

      Each skill call adds 20 s. After call 2 the time is 40 s, under 50 s,
      so call 3 runs; after call 3 it is 60 s, so the loop stops before call
      4. The output ends with:

      .. code-block:: text

         call 3: 5 messages; scripted
           model:  robot2_pick_from_tester({"tester": 1})
           result: {"code": "SUCCESS", "holding": "CELL", "message": "", "attempts": 1, "wall_s": 0.0}
         obs 3:  t=60.0 s | tester 1 0.00 V OPERATIONAL | tester 2 0.00 V OPERATIONAL | conveyor OPERATIONAL | agv1 INSPECTION slots ---- | robot 1 NOTHING, robot 2 CELL
         stop: time limit

      Robot 2 still holds the cell when the loop stops. In GP4 the time to
      compare against is ARIAC's simulation time (``TIME_LIMIT``).


.. dropdown:: Exercise 3. Extend the Validator with a New Semantic Rule
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write the check for a second kind of agent decision, placing a tested
   cell in a tray slot, with the semantic checks the slides list: the cell ID
   exists, the AGV is where the action needs it, the kit total stays inside
   its window.

   The decision has three fields: ``cell`` (a cell ID such as ``"c7"``),
   ``agv`` (1 to 3) and ``slot`` (1 to 4). The team's records, chosen for
   this exercise:

   - ``agv1`` is at ``INSPECTION`` with the L3 kit's three cells in slots 1
     to 3 (3.55 V, 3.62 V, 3.70 V) and slot 4 empty.
   - ``agv3`` is at ``RECYCLING`` with an empty tray.
   - Tested cells not yet placed: ``c7`` at 3.66 V, ``c8`` at 3.71 V, ``c9``
     at 3.30 V.

   .. raw:: html

      <hr>

   **Part A. Schema and rules**

   1. Write a JSON schema for the decision in the style of ``SCHEMA`` in
      ``validator.py``.
   2. List the semantic checks, in the order you will run them. Use the
      Li-Ion rules from the lecture: each cell 3.4 V to 3.8 V, a full kit
      14.25 V to 14.55 V.

   .. raw:: html

      <hr>

   **Part B. Predict, then run**

   3. Write ``check_place(text)``, in the shape of ``check`` in
      ``validator.py``, and predict its result for these seven outputs:

      .. code-block:: text

         {"cell": "c7", "agv": 1, "slot": 4}
         {"cell": "c8", "agv": 1, "slot": 4}
         {"cell": "c9", "agv": 1, "slot": 4}
         {"cell": "c12", "agv": 1, "slot": 4}
         {"cell": "c7", "agv": 1, "slot": 2}
         {"cell": "c7", "agv": 3, "slot": 1}
         {"cell": "c7", "agv": 1, "slot": 5}

   4. Which of the seven would a schema alone catch?

   .. dropdown:: Solution
      :color: success

      **Question 1 and 2.** The solution file:

      .. code-block:: python

         """Exercise 3 solution: check a place-in-slot decision."""

         import json

         from jsonschema import Draft202012Validator

         PLACE_SCHEMA = {
             "type": "object",
             "required": ["cell", "agv", "slot"],
             "additionalProperties": False,
             "properties": {
                 "cell": {"type": "string"},
                 "agv": {"type": "integer", "minimum": 1, "maximum": 3},
                 "slot": {"type": "integer", "minimum": 1, "maximum": 4},
             },
         }

         # The team's records (chosen for this exercise): measured voltages of
         # the cells not yet placed, and what each AGV holds.
         CELLS = {"c7": 3.66, "c8": 3.71, "c9": 3.30}
         AGVS = {
             1: {"station": "INSPECTION", "slots": {1: 3.55, 2: 3.62, 3: 3.70, 4: None}},
             3: {"station": "RECYCLING", "slots": {1: None, 2: None, 3: None, 4: None}},
         }


         def check_place(text):
             """Return None if the placement can run, else the error text."""
             try:
                 place = json.loads(text)
             except json.JSONDecodeError as err:
                 return f"not JSON: {err.msg}"
             errors = list(Draft202012Validator(PLACE_SCHEMA).iter_errors(place))
             if errors:
                 return "schema: " + errors[0].message
             cell, agv, slot = place["cell"], place["agv"], place["slot"]
             if cell not in CELLS:
                 return f"semantic: no cell {cell} in the records"
             if agv not in AGVS or AGVS[agv]["station"] != "INSPECTION":
                 return f"semantic: agv{agv} is not at INSPECTION"
             slots = AGVS[agv]["slots"]
             if slots[slot] is not None:
                 return f"semantic: slot {slot} of agv{agv} is full"
             volts = CELLS[cell]
             if not 3.4 <= volts <= 3.8:
                 return f"semantic: {cell} reads {volts} V, outside 3.4 to 3.8 V"
             others = [v for v in slots.values() if v is not None]
             if len(others) == 3:
                 total = round(sum(others) + volts, 2)
                 if not 14.25 <= total <= 14.55:
                     return f"semantic: kit total {total} V, outside 14.25 to 14.55 V"
             return None

      The semantic checks, in order: the cell exists in the records; the AGV
      is at ``INSPECTION``; the slot is empty; the cell is inside the cell
      range; and, when the cell fills the fourth slot, the kit total is inside
      the kit window. The cheap lookups come first, so the error text names
      the most basic problem.

      ``round(..., 2)`` matters: in Python, 3.55 + 3.62 + 3.70 is
      10.870000000000001, not 10.87. For a kit of 3.43 V, 3.70 V, 3.70 V and
      3.72 V, Python's sum is 14.550000000000002, so without the rounding the
      check would refuse a kit that sits exactly on the 14.55 V limit.

      **Question 3.** Run with a loop like the one in ``validator.py``'s
      ``__main__`` block:

      .. code-block:: text

         {"cell": "c7", "agv": 1, "slot": 4}
           -> valid
         {"cell": "c8", "agv": 1, "slot": 4}
           -> semantic: kit total 14.58 V, outside 14.25 to 14.55 V
         {"cell": "c9", "agv": 1, "slot": 4}
           -> semantic: c9 reads 3.3 V, outside 3.4 to 3.8 V
         {"cell": "c12", "agv": 1, "slot": 4}
           -> semantic: no cell c12 in the records
         {"cell": "c7", "agv": 1, "slot": 2}
           -> semantic: slot 2 of agv1 is full
         {"cell": "c7", "agv": 3, "slot": 1}
           -> semantic: agv3 is not at INSPECTION
         {"cell": "c7", "agv": 1, "slot": 5}
           -> schema: 5 is greater than the maximum of 4

      The arithmetic behind the first three, with the three placed cells at
      3.55 + 3.62 + 3.70 = 10.87 V:

      1. ``c7``: 10.87 + 3.66 = 14.53 V, inside 14.25 V to 14.55 V. It also
         sits inside the lecture's window for the fourth cell, 3.40 V to
         3.68 V.
      2. ``c8``: 3.71 V passes on its own (inside 3.4 V to 3.8 V), but
         10.87 + 3.71 = 14.58 V is 14.58 − 14.55 = 0.03 V above the kit
         window. It is a good cell for another kit.
      3. ``c9``: 3.30 V is 3.4 − 3.30 = 0.10 V below the cell range, so the
         cell check refuses it before the kit check runs.

      **Question 4.** Only the last one, slot 5, which breaks ``maximum``.
      The other five failures are well formed: the schema cannot know which
      cells exist, where each AGV is, which slots are full or what the kit
      already holds. The same lesson as the seven outputs in class.


.. dropdown:: Exercise 4. Serve a Kit Tool Through MCP
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   The lecture says the orchestrator should do the voltage sums, and that "a
   tool that computes the window is the other option". Write that tool, serve
   it through MCP the way ``skills_mcp_server.py`` serves the skill tools,
   then list it and call it from a client.

   The skill tools need ARIAC, so this server holds only the new tool. Run it
   with the ``mcp`` package 2.3.0, for example from the lecture's virtual
   environment, ``/opt/enpm663_lecture_venv``, in the course container.

   .. raw:: html

      <hr>

   **Part A. The tool**

   1. Write ``kit_mcp_server.py``. Define ``kit_window(voltages)``: it takes a
      list of exactly three floats, and returns the kit total and the range
      the fourth Li-Ion cell must read (the kit window, clipped to the cell
      range). Use ``Annotated`` and pydantic's ``Field`` to require exactly
      three values. Register it as ``skills_mcp_server.py`` registers each
      skill tool: ``server.tool(name=..., description=...)(function)``.
   2. Name the tool ``kit_window``, not ``kit-window``. Why?
   3. Before you run anything, predict the input schema MCP will write for
      ``voltages``.

   .. raw:: html

      <hr>

   **Part B. The calls**

   4. Write ``kit_mcp_client.py`` from ``skills_mcp_client.py``: start
      ``kit_mcp_server.py`` in place of the skills server, drop the
      ``sim_session`` lines (no ARIAC here), and call ``kit_window`` with
      ``[3.55, 3.62, 3.70]`` and with ``[3.55, 3.62]``. Predict ``is_error``
      and the result of each call.
   5. Why is a tool for this sum better than writing the three voltages into
      the prompt?

   .. dropdown:: Solution
      :color: success

      **Question 1.** The server:

      .. code-block:: python

         """Exercise 4: one tool, kit_window, served through MCP over stdio. No ARIAC."""
         from typing import Annotated

         from mcp.server.mcpserver import MCPServer
         from pydantic import Field

         KIT_MIN, KIT_MAX = 14.25, 14.55    # 4 x 3.6 V +/- 0.15 V (CellTypes.msg)
         CELL_MIN, CELL_MAX = 3.4, 3.8      # 3.6 V +/- 0.2 V (CellTypes.msg)


         def kit_window(voltages: Annotated[list[float], Field(min_length=3, max_length=3)]) -> dict:
             total = sum(voltages)
             low = max(KIT_MIN - total, CELL_MIN)     # kit minimum, raised to the cell minimum
             high = min(KIT_MAX - total, CELL_MAX)    # kit maximum, capped at the cell maximum
             return {"total": round(total, 2), "low": round(low, 2), "high": round(high, 2)}


         server = MCPServer("kit-tools")
         server.tool(name="kit_window",
                     description="The range of voltages the fourth Li-Ion cell must read, "
                                 "given the three cells already in the kit.")(kit_window)

         if __name__ == "__main__":
             server.run("stdio")

      **Question 2.** The same tool may also go to Gemini as a function
      declaration, and the Gemini guide says to name functions "without
      spaces, periods, or dashes". That is why L6's ``move-agv`` is the tool
      ``move_agv`` in this lecture.

      **Question 3.** As for the skill tools, MCP wrote the schema from the
      type hints: ``list[float]`` became ``"type": "array"`` with
      ``"items": {"type": "number"}``, and ``Field(min_length=3,
      max_length=3)`` became ``minItems`` 3 and ``maxItems`` 3. The
      ``tool:`` line of the output under Question 4 shows it.

      **Question 4, the client.** The lines that differ from
      ``skills_mcp_client.py``:

      .. code-block:: python

         SERVER = StdioServerParameters(command=sys.executable, args=["kit_mcp_server.py"], env=dict(os.environ))
         CALLS = [("kit_window", {"voltages": [3.55, 3.62, 3.70]}),
                  ("kit_window", {"voltages": [3.55, 3.62]})]

      and the ``__main__`` block is only ``asyncio.run(main())``. Run it from
      the folder that holds both files:

      .. code-block:: bash

         /opt/enpm663_lecture_venv/bin/python kit_mcp_client.py

      The output (``mcp`` 2.3.0, run on 2026-10-17):

      .. code-block:: text

         tool: kit_window
             voltages: {"items": {"type": "number"}, "maxItems": 3, "minItems": 3, "title": "Voltages", "type": "array"}
         call: kit_window({"voltages": [3.55, 3.62, 3.7]})
           is_error: False
           result: {"total": 10.87, "low": 3.4, "high": 3.68}
         call: kit_window({"voltages": [3.55, 3.62]})
           is_error: True
           result: Error executing tool kit_window: 1 validation error for kit_windowArguments
           result: voltages
           result:   List should have at least 3 items after validation, not 2 [type=too_short, input_value=[3.55, 3.62], input_type=list]

      The server also wrote one line to standard error:
      ``Tool 'kit_window' rejected arguments: ['voltages']``.

      **Question 4, the two calls.**

      1. Three voltages: the tool runs, ``is_error`` is ``False``. The total
         is 3.55 + 3.62 + 3.70 = 10.87 V. Low: 14.25 − 10.87 = 3.38 V,
         raised to the cell minimum, 3.4 V. High: 14.55 − 10.87 = 3.68 V,
         below the cell maximum of 3.8 V, so it stays. These are the
         lecture's numbers.
      2. Two voltages: the server's argument check refuses the call before
         the function runs, so ``is_error`` is ``True``, as for AGV 4 in the
         lecture.

      ``json.dumps`` prints the input 3.70 as ``3.7``; it is the same number.

      **Question 5.** The model chooses; code does the sums. A tool returns a
      number the code computed, so a model's arithmetic slip cannot put a bad
      cell in the kit. The model only has to read "3.4 to 3.68" and pick a
      cell, and the orchestrator's semantic check (Exercise 3) still checks
      the final total before any robot moves.


.. dropdown:: Exercise 5. Model Latency Against the Factory's Clocks
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Put a number on what a model's latency costs in simulation time, with the
   factory clocks from the lecture.

   From the lecture: the conveyor moves at up to 0.1 m/s; ARIAC's target for
   an inspection report is 4 s; the nominal time for a high-priority order is
   150 s; Gazebo ran at about 0.37 times real time on the instructor's
   machine. Chosen for this exercise: every model call takes 3 s of wall
   clock.

   .. raw:: html

      <hr>

   **Part A. One call**

   1. On a machine where Gazebo runs at real time (1.0), how much simulation
      time passes during one call? How far does a cell at top speed move?
      What share of the 4 s inspection target is that?
   2. Answer the same three questions at 0.37 times real time.
   3. A team tests its agent only on a machine running at 0.37. What does it
      get wrong about a machine that runs at real time?

   .. raw:: html

      <hr>

   **Part B. A recovery**

   4. A ReAct recovery takes 20 calls. At real time, what share of the 150 s
      high-priority target goes to waiting for the model? At 0.37?
   5. Plan-and-execute with one replan makes 2 calls. Same question at real
      time. (Assume, for simplicity, that a plan call also takes 3 s; a long
      plan takes longer to write.)
   6. Should the inspection report go through the agent? Use Part A.

   .. dropdown:: Solution
      :color: success

      **Question 1.** At 1.0, 3 s of wall clock is 3 × 1.0 = 3 s of
      simulation time. The cell moves 0.1 × 3 = 0.3 m. That is 3 / 4 = 75% of
      the 4 s target, spent waiting for one answer.

      **Question 2.** At 0.37, 3 × 0.37 = 1.11 s of simulation time passes.
      The cell moves 0.1 × 1.11 = 0.111 m. That is 1.11 / 4 = 28% of the
      target (27.75%, rounded).

      **Question 3.** The same 3 s model costs 3 / 1.11 = 2.7 times more
      simulation time on the real-time machine. The slow simulator hides the
      model's latency. This is why the lecture says each team measures its
      own model's latency instead of assuming it: the same wall-clock wait
      costs a different amount of simulation time on each machine.

      **Question 4.**

      1. Wall clock: 20 × 3 = 60 s of waiting.
      2. At 1.0: 60 s of simulation time, 60 / 150 = 40% of the target.
      3. At 0.37: 60 × 0.37 = 22.2 s, 22.2 / 150 = 14.8% of the target.

      **Question 5.** 2 × 3 = 6 s, so 6 / 150 = 4% of the target at real
      time, ten times less than the ReAct recovery. Plan-and-execute keeps the
      number of calls, and so the wait, small.

      **Question 6.** No. One call already uses 75% of the 4 s target at real
      time (Question 1), and the report must reach ARIAC before the cell
      reaches the inspection door. Inspection is a loop tied to the moving
      conveyor, so it stays classical, as the lecture says. The agent decides
      at a slower level, such as which cells go in which kit.
