====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Five take-home exercises on the L8 slides and scripts. Exercises 1 and 5 are
paper and arithmetic: token growth for other run lengths, and model latency
against the factory's clocks. Exercises 2 to 4 change one script each: the
stand-in model's script, the validator and the MCP server. Predict the result
first, write the prediction down, then run the script.

.. note::

   The scripts are on the :doc:`code page <l8_code>`. Work on a copy of each
   script, so the original still gives the outputs in the notes. Every run
   below was made on 2026-10-12 with Python 3.12.3 (``jsonschema`` 4.10.3;
   ``mcp`` 2.3.0 for Exercise 4). The scripted stand-in model makes every
   output repeatable, so your outputs should match these exactly, except in
   Exercise 2, Part D, which depends on timing.


.. dropdown:: Exercise 1. Token Growth for Other Run Lengths
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the lecture's formula for the input tokens of a ReAct run on run
   lengths the slides did not show, then check your numbers with
   ``token_growth.py``.

   Use the lecture's values (all chosen for that example): :math:`F` = 2000
   tokens sent on every call, :math:`h` = 250 tokens added by each earlier
   step, 100 output tokens per ReAct call, $2 per million input tokens and
   $10 per million output tokens.

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
      87,500 of the full history.
   6. Compute the cost of that run.

   .. raw:: html

      <hr>

   **Part C. Check with the script**

   7. In a copy of ``token_growth.py``, change both loops to
      ``for n in (8, 21, 22, 30):`` and run it. Compare with Part A.

   .. dropdown:: Solution
      :color: success

      **Question 1.** Call :math:`k` sends :math:`F + (k - 1)\,h`; the run
      sends :math:`nF + h\,n(n - 1)/2`.

      - :math:`n` = 8: last call 2000 + 7 × 250 = 3750 tokens. Total
        8 × 2000 + 250 × 8 × 7 / 2 = 16,000 + 7000 = 23,000 tokens.
      - :math:`n` = 30: last call 2000 + 29 × 250 = 9250 tokens. Total
        30 × 2000 + 250 × 30 × 29 / 2 = 60,000 + 108,750 = 168,750 tokens.

      **Question 2.**

      - :math:`n` = 8: input 23,000 × 2 / 1,000,000 = $0.046. Output
        8 × 100 = 800 tokens, 800 × 10 / 1,000,000 = $0.008. Total $0.054.
      - :math:`n` = 30: input 168,750 × 2 / 1,000,000 = $0.3375. Output
        30 × 100 = 3000 tokens, 3000 × 10 / 1,000,000 = $0.030. Total
        $0.3675.

      **Question 3.** **22 steps.**

      1. :math:`n` = 21: 21 × 2000 + 250 × 21 × 20 / 2 = 42,000 + 52,500
         = 94,500 tokens, below 100,000.
      2. :math:`n` = 22: 22 × 2000 + 250 × 22 × 21 / 2 = 44,000 + 57,750
         = 101,750 tokens, above 100,000.

      **Question 4.** For :math:`n` = 20: 250 × 20 × 19 / 2 = 47,500. For
      :math:`n` = 40: 250 × 40 × 39 / 2 = 195,000. The ratio is
      195,000 / 47,500 = 4.1, so "about four times" holds. It is not exactly
      4 because :math:`n(n - 1)` is not exactly :math:`n^2`.

      **Question 5.**

      1. Calls 1 to 6 still send all earlier steps (at most 5):
         6 × 2000 + 250 × (0 + 1 + 2 + 3 + 4 + 5) = 12,000 + 3750
         = 15,750 tokens.
      2. Calls 7 to 20, 14 calls, each send :math:`F + 5h`
         = 2000 + 5 × 250 = 3250 tokens: 14 × 3250 = 45,500 tokens.
      3. Total 15,750 + 45,500 = **61,250 tokens**, which is
         87,500 − 61,250 = 26,250 fewer, or 26,250 / 87,500 = 30% less.

      With a fixed window the input of each call stops growing after step 6,
      so the total grows in a straight line with :math:`n`, not with its
      square.

      **Question 6.** Input 61,250 × 2 / 1,000,000 = $0.1225, plus the same
      $0.020 of output (2000 tokens): **$0.1425**, against $0.195 with the
      full history.

      **Question 7.** The output of the edited script:

      .. code-block:: text

         ReAct, one call per step
         steps last call   input output  cost $
             8      3750   23000    800  0.0540
            21      7000   94500   2100  0.2100
            22      7250  101750   2200  0.2255
            30      9250  168750   3000  0.3675
         Plan-and-execute, one plan and one replan
         steps     calls   input output  cost $
             8         2    4000    640  0.0144
            21         2    4000   1680  0.0248
            22         2    4000   1760  0.0256
            30         2    4000   2400  0.0320

      The ReAct rows match Part A. Plan-and-execute still sends 4000 input
      tokens at every length; only its output (2 calls × :math:`n` steps ×
      40 tokens) grows.


.. dropdown:: Exercise 2. Make the Loop Hit Each Stop Condition
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Change the stand-in model's script in ``orchestrator.py`` so that the loop
   ends for each reason it checks, and find a case where the stop reason is
   not the one you expect.

   In a copy of ``orchestrator.py``, replace the two runs in the
   ``__main__`` block with your own ``ScriptedModel([...])`` lists. Use the
   helper ``move(agv, station)`` for tool calls, ``{"text": "done"}`` for a
   reply with no tool call, and keep ``MAX_STEPS`` = 6 and ``MAX_INVALID``
   = 2. Give each script at least as many replies as the loop will ask for.

   .. raw:: html

      <hr>

   **Part A. Each stop reason**

   1. Write a script that ends with ``stop: step limit``. How many calls does
      the loop make?
   2. Write a script that ends with ``2 invalid outputs in a row`` because of
      a tool name that does not exist, for example ``submit-kit``.
   3. Write a script whose first reply is ``{"text": "done"}``, before any
      move. What does the orchestrator send back? Does that reply count as an
      invalid output?

   .. raw:: html

      <hr>

   **Part B. Invalid, valid, invalid**

   4. Run this script: ship ``agv2``, move ``agv1`` to ``ASSEMBLY``, ship
      ``agv2``, move ``agv1`` to ``INSPECTION``, ship ``agv2``, ship
      ``agv1``. Three calls are refused. Why does the run not stop on
      ``MAX_INVALID``?
   5. After call 6, ``agv1`` is at ``SHIPPING``. What is the stop reason, and
      why?

   .. raw:: html

      <hr>

   **Part C. Check the goal after every result**

   6. Change ``run()`` so it checks ``goal_check(factory)`` right after it
      prints each result. Rerun question 4's script and Run 1. What changes?

   .. raw:: html

      <hr>

   **Part D. A time limit**

   7. The lecture lists a fourth stop condition that the demo does not check:
      the time limit. Add one: record ``start = time.monotonic()`` before the
      loop, and at the top of each step return ``"time limit"`` once more than
      ``TIME_LIMIT`` = 0.5 s has passed (chosen for this exercise). Make the
      stand-in slow with ``time.sleep(0.2)`` in ``ScriptedModel.__call__``,
      and give it question 1's script. How many calls run?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Six valid moves that never ship ``agv1``, and no
      "done":

      .. code-block:: python

         ScriptedModel([move(1, "ASSEMBLY"), move(1, "INSPECTION")] * 3)

      The loop makes **6 calls**, all ``SUCCEEDED``, then stops. The last
      lines of the output:

      .. code-block:: text

         call 6: 11 messages, 1604 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "INSPECTION"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "INSPECTION"}
         stop: step limit

      **Question 2.** ``ScriptedModel([{"tool": "submit-kit", "args": {}}] * 2)``.
      The guard's first check refuses any tool that is not ``move-agv``:

      .. code-block:: text

           user:   {"goal": "ship the kit on agv1", "state": {"agv1": "INSPECTION, 4 cells", "agv2": "INSPECTION, 3 cells", "agv3": "RECYCLING, 0 cells"}}
         call 1: 1 messages, 666 chars
           model:  {"tool": "submit-kit", "args": {}}
           orch:   {"error": "guard: unknown tool 'submit-kit'"}
         call 2: 3 messages, 812 chars
           model:  {"tool": "submit-kit", "args": {}}
           orch:   {"error": "guard: unknown tool 'submit-kit'"}
         stop: 2 invalid outputs in a row

      **Question 3.** With
      ``ScriptedModel([{"text": "done"}, move(1, "SHIPPING"), {"text": "done"}])``:

      .. code-block:: text

           user:   {"goal": "ship the kit on agv1", "state": {"agv1": "INSPECTION, 4 cells", "agv2": "INSPECTION, 3 cells", "agv3": "RECYCLING, 0 cells"}}
         call 1: 1 messages, 666 chars
           model:  {"text": "done"}
           orch:   {"error": "goal not reached"}
         call 2: 3 messages, 778 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "SHIPPING"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "SHIPPING"}
         call 3: 5 messages, 964 chars
           model:  {"text": "done"}
         stop: goal reached

      The orchestrator checks the goal in code, finds ``agv1`` still at
      ``INSPECTION``, and sends back ``{"error": "goal not reached"}``. It is
      **not** counted as invalid: ``invalid`` goes up only when the guard
      refuses a tool call. This is the warning from the slides in action: the
      model said "done", and the code decided it was not.

      **Question 4.** The output:

      .. code-block:: text

           user:   {"goal": "ship the kit on agv1", "state": {"agv1": "INSPECTION, 4 cells", "agv2": "INSPECTION, 3 cells", "agv3": "RECYCLING, 0 cells"}}
         call 1: 1 messages, 666 chars
           model:  {"tool": "move-agv", "args": {"agv": 2, "station": "SHIPPING"}}
           orch:   {"error": "guard: agv2 holds 3 of 4 cells"}
         call 2: 3 messages, 839 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "ASSEMBLY"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "ASSEMBLY"}
         call 3: 5 messages, 1025 chars
           model:  {"tool": "move-agv", "args": {"agv": 2, "station": "SHIPPING"}}
           orch:   {"error": "guard: agv2 holds 3 of 4 cells"}
         call 4: 7 messages, 1198 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "INSPECTION"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "INSPECTION"}
         call 5: 9 messages, 1388 chars
           model:  {"tool": "move-agv", "args": {"agv": 2, "station": "SHIPPING"}}
           orch:   {"error": "guard: agv2 holds 3 of 4 cells"}
         call 6: 11 messages, 1561 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "SHIPPING"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "SHIPPING"}
         stop: step limit

      ``MAX_INVALID`` counts invalid outputs **in a row**. Each valid call
      runs ``invalid = 0``, so the count never gets past 1. Half of this
      run's calls were refused, and the limit never fired. A team that wants
      to catch this pattern needs a second limit on the total number of
      invalid outputs.

      **Question 5.** ``step limit``, even though ``agv1`` reached
      ``SHIPPING`` at call 6. The demo checks the goal only when the model
      replies with no tool call, and this model never said "done" before the
      sixth step ended the loop.

      **Question 6.** The change, after the line that prints ``orch``:

      .. code-block:: python

         if goal_check(factory):
             return "goal reached"

      Question 4's script now ends with ``stop: goal reached`` after call 6
      (the same six calls as above). Run 1 now ends after call 2:

      .. code-block:: text

           user:   {"goal": "ship the kit on agv1", "state": {"agv1": "INSPECTION, 4 cells", "agv2": "INSPECTION, 3 cells", "agv3": "RECYCLING, 0 cells"}}
         call 1: 1 messages, 666 chars
           model:  {"tool": "move-agv", "args": {"agv": 2, "station": "SHIPPING"}}
           orch:   {"error": "guard: agv2 holds 3 of 4 cells"}
         call 2: 3 messages, 839 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "SHIPPING"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "SHIPPING"}
         stop: goal reached

      The run saves the third call, and with a real model the cost and the
      wait of that call. Either design is valid; what matters is that the
      goal check is code, not the model's word.

      **Question 7.** **3 calls**, then ``stop: time limit``. Each call
      sleeps 0.2 s. At the top of step 4, about 3 × 0.2 = 0.6 s have passed,
      more than 0.5 s, so the loop stops before the fourth call. The output
      ends with:

      .. code-block:: text

         call 3: 5 messages, 1042 chars
           model:  {"tool": "move-agv", "args": {"agv": 1, "station": "ASSEMBLY"}}
           orch:   {"status": "SUCCEEDED", "agv": 1, "station": "ASSEMBLY"}
         stop: time limit

      Three runs on the course machine gave 3 calls each time. The count
      depends on timing, so a machine that is much slower could differ; the
      margin here is 0.1 s on each side. In GP4 the time to compare against
      is ARIAC's simulation time (``TIME_LIMIT``), not the wall clock.


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


.. dropdown:: Exercise 4. Add a Tool to the MCP Server
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   The lecture says the orchestrator should do the voltage sums, and that "a
   tool that computes the window is the other option". Add that tool to
   ``agv_mcp_server.py``, then list it and call it from the client.

   .. raw:: html

      <hr>

   **Part A. The tool**

   1. In a copy of ``agv_mcp_server.py``, add a tool named ``kit-window``.
      It takes ``voltages``, a list of exactly three floats, and returns the
      kit total and the range the fourth Li-Ion cell must be in (the kit
      window, clipped to the cell range). Use ``Annotated`` and ``Field`` as
      ``move`` does to require exactly three values.
   2. Before you run anything, predict the input schema the server will
      generate for ``voltages``.

   .. raw:: html

      <hr>

   **Part B. The calls**

   3. In a copy of ``agv_mcp_client.py``, call ``kit-window`` with
      ``[3.55, 3.62, 3.70]`` and with ``[3.55, 3.62]``. Predict
      ``is_error`` and the result of each call.
   4. Why is a tool for this sum better than writing the three voltages into
      the prompt?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Add this after the ``move`` tool in the server:

      .. code-block:: python

         @server.tool(name="kit-window")
         def kit_window(voltages: Annotated[list[float],
                                            Field(min_length=3, max_length=3)]) -> dict:
             """Range the fourth Li-Ion cell must be in, given three cell voltages."""
             total = sum(voltages)
             low = max(14.25 - total, 3.4)     # kit minimum, raised to the cell minimum
             high = min(14.55 - total, 3.8)    # kit maximum, capped at the cell maximum
             return {"total": round(total, 2), "low": round(low, 2),
                     "high": round(high, 2)}

      **Question 3, client change.** Add a list next to ``CALLS``:

      .. code-block:: python

         KIT_CALLS = [[3.55, 3.62, 3.70], [3.55, 3.62]]

      and, after the ``move-agv`` loop, a second loop that does the same for
      ``kit-window``:

      .. code-block:: python

         for volts in KIT_CALLS:
             args = {"voltages": volts}
             result = await client.call_tool("kit-window", args)
             print("call:", json.dumps(args))
             text = result.content[0].text
             print("  is_error:", result.is_error)
             if result.is_error:
                 lines = text.splitlines()
                 print("  result:", lines[0])
                 print("   ", lines[2].split("[")[0].strip())
             else:
                 print("  result:", json.dumps(json.loads(text)))

      Run it with ``python3 agv_mcp_client.py`` in the virtual environment.
      The output (``mcp`` 2.3.0):

      .. code-block:: text

         tool: move-agv
           description: Move one AGV to a station (ARIAC /agvN/move).
           input_schema, type: object
             agv: {"maximum": 3, "minimum": 1, "title": "Agv", "type": "integer"}
             station: {"enum": ["INSPECTION", "ASSEMBLY", "SHIPPING", "RECYCLING"], "title": "Station", "type": "string"}
             required: ["agv", "station"]
         tool: kit-window
           description: Range the fourth Li-Ion cell must be in, given three cell voltages.
           input_schema, type: object
             voltages: {"items": {"type": "number"}, "maxItems": 3, "minItems": 3, "title": "Voltages", "type": "array"}
             required: ["voltages"]
         call: {"agv": 1, "station": "SHIPPING"}
           is_error: False
           result: {"status": "SUCCEEDED", "agv": 1, "station": "SHIPPING"}
         call: {"agv": 1, "station": "ASSEMBLY"}
           is_error: False
           result: {"status": "REJECTED", "reason": "no ARIAC path SHIPPING to ASSEMBLY"}
         call: {"agv": 4, "station": "SHIPPING"}
           is_error: True
           result: Error executing tool move-agv: 1 validation error for moveArguments
             Input should be less than or equal to 3
         call: {"voltages": [3.55, 3.62, 3.7]}
           is_error: False
           result: {"total": 10.87, "low": 3.4, "high": 3.68}
         call: {"voltages": [3.55, 3.62]}
           is_error: True
           result: Error executing tool kit-window: 1 validation error for kit_windowArguments
             List should have at least 3 items after validation, not 2

      **Question 2.** As with ``move``, the server wrote the schema from the
      type hints: ``list[float]`` became ``"type": "array"`` with
      ``"items": {"type": "number"}``, and ``Field(min_length=3,
      max_length=3)`` became ``minItems`` 3 and ``maxItems`` 3. The
      description is the docstring.

      **Question 3.**

      1. Three voltages: the tool runs, ``is_error`` is ``False``. The total
         is 3.55 + 3.62 + 3.70 = 10.87 V. Low: 14.25 − 10.87 = 3.38 V,
         raised to the cell minimum, 3.4 V. High: 14.55 − 10.87 = 3.68 V,
         below the cell maximum of 3.8 V, so it stays. These are the
         lecture's numbers.
      2. Two voltages: the server's argument check refuses the call before
         the function runs, so ``is_error`` is ``True``, as for AGV 4 in the
         lecture. The error names ``kit_windowArguments``: the server names
         the check after the Python function, not after the tool.

      ``json.dumps`` prints the input 3.70 as ``3.7``; it is the same number.

      **Question 4.** The model chooses; code does the sums. A tool returns a
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
