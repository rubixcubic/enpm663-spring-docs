====================================================
Lecture
====================================================


Flow Control
====================================================

Sometimes we need to branch out from the straight-line path to execute
statements based on some conditions or execute statements multiple times
efficiently. C++ provides different **flow control** statements, which
allow the programmer to change the normal path of execution through the
program. Controlling the flow of a program can be performed with
**selection statements** and **iteration statements**.

.. figure:: /_static/images/rm/figure1.pdf
   :align: center
   :width: 60%

   Flow control overview.


Statements
====================================================

Many of the flow control statements explained in this reading material
require a generic (sub)statement as part of its syntax.

This statement may either be:

- A **simple statement**, terminated with a semicolon, e.g.,
  ``int a{10};``
- A **compound statement** -- a group of statements (each terminated by
  its own semicolon), but all grouped together in a block enclosed in
  braces.

.. code-block:: cpp

   int main() {
       {  // start of compound statement 1
           int a{10};          // simple statement
           if (a <= 100) {     // start of compound statement 2
               a = 100;        // simple statement
               std::cout << "a is: " << a << '\n'; // simple statement
           }  // end of compound statement 2
       }      // end of compound statement 1
   }


Selection Statements
====================================================

A **selection statement** is a statement that specifies whether some
associated statement(s) should be executed or not.


``if`` Statements
----------------------------------------------------

An ``if`` statement allows the execution of one (or more) lines of code
only if some condition is true.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      if (condition)
          statement

- ``condition`` is an expression which evaluates to a boolean.

  - If ``condition`` is ``true`` then ``statement`` is executed.
  - If ``condition`` is ``false`` then ``statement`` is **not** executed
    (it is just ignored).

.. figure:: /_static/images/rm/if.jpg
   :align: center
   :width: 40%

   Flowchart for the ``if`` statement.

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      std::cout << "Enter your age: ";
      unsigned short age{};
      std::cin >> age;

      if (age >= 18)
          std::cout << "You can vote!\n";

   - ``if (age >= 18)`` checks whether the value of ``age`` is 18 or
     greater.
   - If the condition is true (the user is 18 or older), the program
     prints ``You can vote!``
   - If the condition is false (the user is younger than 18), the
     program does nothing and simply ends.


Implicit Block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the programmer does not declare a block in the statement portion of
an ``if`` statement, the compiler will implicitly declare one.

.. code-block:: cpp

   if (condition)
       statement_true

is equivalent to:

.. code-block:: cpp

   if (condition){
       statement_true
   }

.. warning::

   Implicit blocks work only for one single statement. Be careful when
   you need multiple statements to be executed.

.. code-block:: cpp

   int a{2};
   if (a > 0)
       std::cout << "a is positive\n";
       a = -a; // this is always executed

is equivalent to:

.. code-block:: cpp

   int a{2};
   if (a > 0){
       std::cout << "a is positive\n";
   }
   a = -a; // this is always executed

Did you want the following instead?

.. code-block:: cpp

   int a{2};
   if (a > 0){
       std::cout << "a is positive\n";
       a = -a; // executed only if a is positive
   }


``if``-``else`` Statements
----------------------------------------------------

Selection statements with ``if`` can also specify what happens when the
condition is not fulfilled with the ``else`` keyword.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      if (condition)
          statement_true
      else
          statement_false

- ``condition`` is an expression which evaluates to a boolean.

  - If ``condition`` is ``true`` then ``statement_true`` is executed.
  - If ``condition`` is ``false`` then ``statement_false`` is executed.

.. figure:: /_static/images/rm/if-else.jpg
   :align: center
   :width: 60%

   Flowchart for the ``if``-``else`` statement.

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      int a{1};

      if (a >= 0)
          std::cout << "a is positive\n";  // executed only if a>=0 is true
      else
          std::cout << "a is negative\n";  // executed only if a<0 is true

Implicit Block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the programmer does not declare a block in the statement portion of
an ``if`` statement or ``else`` statement, the compiler will implicitly
declare one.

.. code-block:: cpp

   if (condition)
       statement_true
   else
       statement_false

is equivalent to:

.. code-block:: cpp

   if (condition){
       statement_true
   }
   else{
       statement_false
   }


Conditional (Ternary) Operator
----------------------------------------------------

The **conditional operator** ``?:`` (also called the ternary operator)
takes 3 operands. It provides a less verbose method for doing a
particular type of ``if``-``else`` statement.

.. code-block:: cpp

   if (condition)
       statement_true
   else
       statement_false

...can be written as follows with the conditional operator:

.. code-block:: cpp

   (condition) ? statement_true : statement_false;

.. admonition:: Example
   :class: hint

   Consider the following code using an ``if``-``else`` statement:

   .. code-block:: cpp

      int x{1};

      if (x % 2)
          std::cout << x << " is even\n";
      else
          std::cout << x << " is odd\n";

   Here is the same code using the conditional operator:

   .. code-block:: cpp

      int x{1};
      std::cout << ((x % 2) ? "x is even\n" : "x is odd\n");

   .. note::

      You have to parenthesize the whole conditional operator as seen
      above.

.. admonition:: Example -- Initializing with the Ternary Operator
   :class: hint

   The conditional operator can be used in some situations where an
   ``if``-``else`` statement cannot be used. In the example below, the
   constant variable ``larger_value`` is initialized based on the result
   of the expression ``x > y ? x : y``.

   If ``x > y`` is ``true``, ``larger_value`` is initialized to ``x``,
   otherwise it is initialized to ``y``.

   .. code-block:: cpp

      constexpr int x{3};
      constexpr int y{2};

      constexpr int larger_value{x > y ? x : y}; // initialize larger_value
      std::cout << "The larger value is: " << larger_value << '\n'; // 3

.. admonition:: Example -- Why ``if``-``else`` Cannot Always Replace the Ternary
   :class: hint

   Trying to write the code from the previous example using an
   ``if``-``else`` statement results in the following code:

   .. code-block:: cpp
      :linenos:

      constexpr int x{3};
      constexpr int y{2};

      if (x > y)
          constexpr int larger_value{x};
      else
          constexpr int larger_value{y};

      std::cout << "The larger value is: " << larger_value << '\n';

   .. warning::

      The program above will not compile: ``larger_value`` is local to
      the ``if`` statement (line 5) and to the ``else`` statement
      (line 7). During the execution of line 9, ``larger_value`` will
      be out of scope and trying to use an out-of-scope variable raises
      an error.


``else``-``if`` Statements
----------------------------------------------------

Sometimes we want to check if several things are ``true`` or ``false``
in sequence. We can do so by chaining an ``if`` statement to a prior
``if``-``else``.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      if (condition1)
          statement1
      else if (condition2)
          statement2
      else
          statement3

.. figure:: /_static/images/rm/if_else_if.jpg
   :align: center
   :width: 60%

   Flowchart for the ``else``-``if`` statement.

Implicit Block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   if (condition1)
       statement1
   else if (condition2)
       statement2
   else
       statement3

is equivalent to:

.. code-block:: cpp

   if (condition1){
       statement1
   }
   else if (condition2){
       statement2
   }
   else{
       statement3
   }

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      int a{1};

      if (a > 0)
          std::cout << "Value is positive\n"; // if a > 0 is true
      else if (a < 0)
          std::cout << "Value is negative\n"; // if a < 0 is true
      else
          std::cout << "Value is zero\n";     // if a > 0 AND a < 0 are false


Implicit Conversion
----------------------------------------------------

In the previous examples, ``condition`` is evaluated to ``true`` or
``false``. If ``condition`` is an expression that does not evaluate to
``true`` or ``false``, ``condition`` is **implicitly converted** to
``true`` or ``false``.

.. admonition:: Example
   :class: hint

   ``2`` is converted to ``true``, ``0.01`` is converted to ``true``,
   ``0`` is converted to ``false``, and ``0.0`` is converted to
   ``false``.

   .. code-block:: cpp

      if (2)                                   // converted to true
          std::cout << "Condition1 is true\n";  // executed
      if (0.01)                                // converted to true
          std::cout << "Condition2 is true\n";  // executed
      if (0)                                   // converted to false
          std::cout << "Condition3 is true\n";  // not executed
      if (0.0)                                 // converted to false
          std::cout << "Condition4 is true\n";  // not executed


Dangling ``else``
----------------------------------------------------

In C++ (as well as in many other programming languages that have a
similar syntax), a **dangling** ``else`` refers to an ambiguity in
certain ``if``-``else`` statements when nested ``if`` statements are
used without braces.

.. admonition:: Question

   Does the ``else`` statement in the program match up with the outer
   ``if`` (line 4) or inner ``if`` (line 5)? The indentation on line 7
   is deceptive.

.. code-block:: cpp
   :linenos:

   int x{5};
   int y{10};

   if (x > 0)
       if (y > 0)
           std::cout << "x and y are positive\n";
   else
       std::cout << "x is non-positive\n";

.. note::

   An ``else`` statement is paired up with the last unmatched ``if``
   statement in the same block. Thus, in the previous program, the
   ``else`` is matched up with the inner ``if``, as if the program had
   been written as follows:

.. code-block:: cpp

   int x{5};
   int y{10};

   if (x > 0){
       if (y > 0){
           std::cout << "x and y are positive\n";
       }
       else{
           std::cout << "x is non-positive\n";
       }
   }


``switch`` Statements
----------------------------------------------------

The ``switch`` statement in C++ is used for multiple-way decision
making. It tests the value of a variable and compares it with multiple
cases. Once the case match is found, the block of statements associated
with that case is executed. Each case in a ``switch`` statement is a
distinct value, but the variable being tested for can only have one of
these values.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      switch (condition) statement

- We start with the ``switch`` keyword followed by the ``condition`` we
  would like to evaluate. Typically, this ``condition`` is just a single
  variable but it can be something more complex.

  - The one restriction on this ``condition`` is that it must evaluate
    to an integral type.

- Following the ``switch`` expression, we declare a ``statement``
  (typically a compound ``statement``). Inside the ``statement`` we use
  labels to define all of the values we want to test for equality. There
  are two kinds of labels: ``case`` and ``default``.

.. figure:: /_static/images/rm/switch.jpg
   :align: center
   :width: 80%

   Flowchart for the ``switch`` statement.

.. admonition:: Example -- Side-by-side comparison
   :class: hint

   Below is a side-by-side comparison of an ``if``-``else`` statement
   and a ``switch`` statement.

   .. grid:: 2

      .. grid-item-card:: ``if``-``else``

         .. code-block:: cpp

            int a{1};
            if (a == 1)
                std::cout << "one\n";
            else if (a == 2)
                std::cout << "two\n";
            else if (a == 3)
                std::cout << "three\n";
            else
                std::cout << "unknown\n";

      .. grid-item-card:: ``switch``

         .. code-block:: cpp

            int a{1};

            switch (a){
            case 1:
                std::cout << "one\n";
                break;
            case 2:
                std::cout << "two\n";
                break;
            case 3:
                std::cout << "three\n";
                break;
            default:
                std::cout << "unknown\n";
                break;
            }


``case`` Label
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first kind of label that can be used with ``switch`` is the
``case`` label, which is declared using the ``case`` keyword and
followed by a constant expression (e.g., ``case 1:``, ``case 2:``,
etc.).

The constant expression following the ``case`` label is tested for
equality against the expression following the ``switch`` keyword. If
they match, the code under the ``case`` label is executed.

.. admonition:: Example
   :class: hint

   Lines 3 and 4 are executed if the value of ``a`` is ``1``.

   .. code-block:: cpp
      :linenos:

      switch (a){
      case 1: // equivalent to: if (a == 1)
          std::cout << "one\n";
          break;
      }

.. note::

   All ``case`` label expressions must evaluate to a unique value. The
   following code is not valid:

   .. code-block:: cpp

      switch (a){
      case 1:
          std::cout << "one\n";
          break;
      case 1: // error: duplicate case value
          std::cout << "one\n";
          break;
      }


``default`` Label
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The second kind of label is the ``default`` label (often called the
default case), which is declared using the ``default`` keyword.

The code under this label gets executed if none of the cases match the
``switch`` expression.

The ``default`` label is optional, and there can only be one
``default`` label per ``switch`` statement. It is also typically
declared as the last label in the ``switch`` block, though this is not
strictly necessary.

.. admonition:: Example
   :class: hint

   In the code below, the statements under the ``default`` label are
   executed because none of the ``case`` labels match the value of the
   variable ``a``.

   .. code-block:: cpp

      int a{3};

      switch (a){
      case 1:  // no match
          std::cout << "one\n";
          break;
      case 2:  // no match
          std::cout << "two\n";
          break;
      default: // executed since no cases matched
          std::cout << "unknown\n";
          break;
      }


``break`` Statement (in ``switch``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``break`` statement (declared using the ``break`` keyword) tells the
compiler that we are done executing statements within the ``switch``.

The code below prints ``one`` in the terminal and exits the ``switch``
statement. The program then executes everything that is after the
``switch`` statement and prints ``switch has terminated`` in the
terminal.

.. code-block:: cpp

   int a{3};

   switch (a){
   case 1:
       std::cout << "one\n";
       break;
   case 2:
       std::cout << "two\n";
       break;
   default:
       std::cout << "unknown\n";
       break;
   }

   std::cout << "switch has terminated\n";


Fallthrough
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a ``switch`` expression matches a ``case`` label or optional
``default`` label, execution begins at the first statement following
the matching label. Execution will then continue sequentially until one
of the following termination conditions happens:

- The end of the ``switch`` block is reached.
- Another control flow statement (typically a ``break`` or ``return``)
  causes the ``switch`` block or function to exit.
- Something else interrupts the normal flow of the program (e.g., the
  OS shuts the program down).

If none of these termination conditions are met, cases will overflow
into subsequent cases. This is called a **fallthrough**.

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      int choice{1};

      switch (choice) {
          case 1: // we have a match here
              std::cout << "Choice is 1\n"; // this is executed
          case 2:
              std::cout << "Choice is 2\n"; // I want to execute this as well
              break;
          default:
              std::cout << "Unknown choice\n";
      }

The ``[[fallthrough]]`` Attribute
""""""""""""""""""""""""""""""""""""""""""""""""""""

When the code above is executed, the compiler will warn you about a
fallthrough. This is because an unintended fallthrough can introduce bugs
in your program.

A fallthrough can be done intentionally in some cases where you want the
current and following cases to execute. To include an intentional
fallthrough in your code, you can use the ``[[fallthrough]]`` attribute
(since C++17). This will tell your collaborators and the compiler that
the fallthrough is done intentionally.

.. code-block:: cpp

   int choice{1};

   switch (choice) {
       case 1: // we have a match here
           std::cout << "Choice is 1\n"; // this is executed
           [[fallthrough]]; // compiler will not raise a warning
       case 2:
           std::cout << "Choice is 2\n"; // I want to execute this as well
           break;
       default:
           std::cout << "Unknown choice\n";
   }


Sequential ``case`` Labels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can also stack ``case`` labels so that some statements are executed
for different cases. In the program below we ask the user if they want
to double a value (multiply a value by 2). The user can enter ``y`` for
yes and ``n`` for no. However, if the user enters ``Y`` instead of
``y`` and ``N`` instead of ``n`` we also accept the input.

.. code-block:: cpp

   int a{2};
   std::cout << "Do you want to double the value of variable a? (y/n) ";
   char input{};
   std::cin >> input;

   switch (input) {
       case 'y':
       case 'Y':
           a *= 2;// double the number
           break;
       case 'n':
       case 'N':
           break;// not doing anything
       default:
           std::cout << "unknown input\n";
           break;
   }
   std::cout << "Value of a: " << a << '\n';


Jump to ``case`` Labels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **jump to case label** error happens when you initialize and use a
variable within a ``case`` label without enclosing the ``case`` in
braces.

.. grid:: 2

   .. grid-item-card:: Error

      .. code-block:: cpp

         int x{1};

         switch (x) {
         case 1:
           int i{10};
           std::cout << i << '\n';
           break;
         case 2:  // Error: jump to case label
           int j{20};
           std::cout << j << '\n';
           break;
         }

   .. grid-item-card:: Fix -- use braces

      .. code-block:: cpp

         int x{1};

         switch (x) {
         case 1:{
           int i{10};
           std::cout << i << '\n';
           break;
         }
         case 2:{
           int j{20};
           std::cout << j << '\n';
           break;
         }
         }


``switch`` vs. ``if``-``else``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. grid:: 2

   .. grid-item-card:: ``switch``

      **Pros**

      - *Readability* -- In cases with many conditions, a ``switch`` can
        be more readable than an ``if``-``else`` statement.
      - *Performance* -- Some compilers can optimize switch statements
        better than equivalent ``if``-``else`` statements.
      - *Fallthrough* -- Allows for multiple cases to execute the same
        block of code (this can be a pitfall if not handled carefully).

      **Cons**

      - *Limited to constant expressions* -- You can only switch on
        integral types, enumerated types, and constant expressions
        (since C++14) that evaluate to one of these types.
      - *Fallthrough* -- It can be a pitfall if unintentional.
      - *Scope* -- Variables declared inside a switch case are visible to
        the subsequent cases unless they are enclosed in braces.

   .. grid-item-card:: ``if``-``else``

      **Pros**

      - *Flexibility* -- Can handle any boolean conditions, not just
        equality checks.
      - *Mixed conditions* -- Allows for different types of conditions to
        be mixed (e.g., equality, less than, greater than, logical
        operators, etc.).

      **Cons**

      - *Readability* -- Can become hard to read when there are many
        conditions.
      - *Performance* -- Depending on the compiler and the nature of the
        conditions, ``if``-``else`` statements might not be as optimized
        as ``switch`` statements.


Initialization Statements
----------------------------------------------------

Initialization in an ``if`` Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting from C++17, you can introduce an initialization statement
directly within an ``if`` condition. This allows you to declare and
initialize a variable right before checking the condition, which is
scoped to the ``if`` and ``else`` blocks.

.. code-block:: cpp

   if (int x{some_function()}; x > 0) {
           std::cout << "x is positive: " << x << '\n';
   } else {
       std::cout << "x is non-positive: " << x << '\n';
   }

- ``int x{some_function()};`` initializes ``x`` with the value returned
  by ``some_function()``.
- The condition ``x > 0`` is then evaluated.
- The variable ``x`` is only available within the scope of the ``if``
  and ``else`` blocks.


Initialization in a ``switch`` Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to ``if``, in C++17 and later, you can introduce an
initialization statement in a ``switch`` statement. This allows for
more concise and localized variable management.

.. code-block:: cpp

   switch (int y = some_function(); y) {
       case 1:
           std::cout << "y is 1\n";
           break;
       case 2:
           std::cout << "y is 2\n";
           break;
       default:
           std::cout << "y is something else: " << y << '\n';
           break;
   }

- ``int y = get_value();`` initializes ``y`` within the switch
  statement.
- The ``switch`` then operates on the value of ``y``.
- The variable ``y`` is only available within the scope of the
  ``switch`` statement.


Iteration Statements
====================================================

Iteration statements, also known as loop statements, are used in C++
(and in many other programming languages) to execute a block of code
multiple times. In C++, there are three primary iteration statements:

- ``for`` statement.
- ``while`` statement.
- ``do``-``while`` statement.


``while`` Statements
----------------------------------------------------

The ``while`` statement (also called a ``while`` loop) is the simplest
of the three loop types that C++ provides.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      while (condition){
          statement
          update condition
      }

1. Evaluate ``condition``:

   a. If ``condition`` is ``false``, exit the loop.
   b. If ``condition`` is ``true``, execute ``statement``, and update
      condition.

      i. Go to 1.

.. figure:: /_static/images/rm/while.jpg
   :align: center
   :width: 30%

   Flowchart for the ``while`` statement.

.. admonition:: Example
   :class: hint

   The ``while`` statement below executes as long as ``counter`` <= 10.

   .. code-block:: cpp
      :linenos:

      int counter{1};
      while (counter <= 10) {
          std::cout << counter << ' ';
          ++counter;
      }
      std::cout << '\n';

   .. warning::

      The tricky part of using an iteration is to make sure your loop
      can stop. You need a way to get out of a loop or your program
      will be stuck in an infinite loop. In the code provided, we
      increment the variable ``counter``. When ``counter`` is 11, the
      ``while`` statement will stop. If you comment out line 4 you get
      an infinite loop because ``counter`` will always be 1 and the
      condition ``(counter <= 10)`` will never evaluate to ``false``.


Infinite Loops
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create intentional infinite loops in some cases.

.. admonition:: Example
   :class: hint

   The program below will keep looping until the user inputs ``n``.

   .. code-block:: cpp

      while (true) {  // infinite loop
          std::cout << "Loop again (y/n)? ";
          char input{};
          std::cin >> input;

          if (input == 'n') {
              std::cout << "Stopping the loop\n";
              break;
          }
      }


Nested Loops
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **nested loop** is a loop inside another loop.

- Nested loops may be hard to understand for beginners.

  - You can use pen and paper to write down the execution of nested
    loops without running the program.
  - To understand the execution of nested loops while running your
    program, you can use the debugger to see the outputs.

.. admonition:: Example
   :class: hint

   The program below creates a times table for numbers ranging from 1
   to 5.

   .. code-block:: cpp
      :linenos:

      // outer loop loops 5 times
      int outer{1};
      while (outer <= 5) {
          int inner{1};
          // inner loop loops 10 times
          while (inner <= 10) {
              std::cout << outer * inner << ' ';
              ++inner;
          }
          // print a newline at the end of each row
          std::cout << '\n';
          ++outer;
      }

   - The outer loop starts at line 3 and will loop 5 times in total.
   - The inner loop starts at line 6 and will loop 50 times in total.

     - For each iteration of the outer loop, the inner loop will iterate
       10 times.


``do``-``while`` Statements
----------------------------------------------------

A ``do``-``while`` statement is a looping construct that works just like
a ``while`` loop statement, except the statement always executes at
least once.

After the statement has been executed, the ``do``-``while`` statement
checks the condition. If the condition evaluates to ``true``, the path
of execution jumps back to the top of the ``do``-``while`` loop and
executes it again.

``do``-``while`` statements are very useful when the program expects
correct user inputs to proceed further. The program keeps asking for
user inputs until the user enters correct inputs.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      do {
          statement
      } while (condition);

1. Execute ``statement``.
2. Evaluate ``condition``:

   a. If ``condition`` is ``false``, exit the loop.
   b. If ``condition`` is ``true``, go to 1.

.. figure:: /_static/images/rm/do-while.pdf
   :align: center
   :width: 30%

   Flowchart for the ``do``-``while`` statement.

.. admonition:: Example
   :class: hint

   The program below executes the same statements in a loop until the
   user inputs ``1`` or ``2`` on the command line.

   .. code-block:: cpp

      // selection must be declared outside of the do/while so we can use it later
      int selection{};

      do {
          std::cout << "Which approach do you want to use (1 or 2)?:\n";
          std::cout << "1) Breadth-first search\n";
          std::cout << "2) Depth-first search\n";
          std::cout << "Please select an approach: ";
          std::cin >> selection;
      } while (selection != 1 && selection != 2);

      switch (selection) {
          case 1:
            std::cout << "You selected: Breadth-first\n";
            break;
          case 2:
            std::cout << "You selected: Depth-first search\n";
            break;
      }


``for`` Statements
----------------------------------------------------

The ``for`` statement in many programming languages, including C++, is
used to repeatedly execute a block of code for a specified number of
times or until a certain condition is met. It provides a concise way to
iterate over a range of values or through elements in a container.

Since C++11, there are two different kinds of ``for`` statements:

- Classic ``for`` statements.
- Range-based ``for`` statements (covered in a future lecture).

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Syntax
   ^^^

   .. code-block:: cpp

      for (init_statement; condition; end_expression)
          statement

A ``for`` statement is evaluated in 3 parts:

1. ``init_statement`` consists of variable definitions and
   initialization. This is **only evaluated once**, when the loop is
   first executed.
2. ``condition`` is evaluated. If this evaluates to ``false``, the loop
   terminates immediately. If this evaluates to ``true``, ``statement``
   is executed.
3. After ``statement`` is executed, ``end_expression`` is evaluated.
   Typically, this expression is used to increment or decrement the
   variables declared in the ``init_statement``. After
   ``end_expression`` has been evaluated, the loop returns to step 2.

   .. note::

      ``end_expression`` is executed last.

.. figure:: /_static/images/rm/for.pdf
   :align: center
   :width: 40%

   Flowchart for the ``for`` statement.

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      for (int i{0}; i < 10; ++i)
          std::cout << i << " ";

   1. We initialize a loop variable ``i`` to 0. This step happens
      exactly once.
   2. ``i < 10`` is evaluated. Since ``i`` is 0, ``i < 10`` evaluates
      to ``true``.
   3. Since ``condition`` evaluates to ``true``, ``statement`` is
      executed, which prints ``0``.
   4. ``end_expression`` is executed, which increments ``i``.
   5. The flow goes back to step 2 (with ``i = 1``).

   The most difficult part to understand in a ``for`` statement is that
   ``end_expression`` (``++i`` in the example) is the very last thing
   that is implicitly executed after ``statement`` has executed.


Off-by-one Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An **off-by-one error** (often abbreviated as OBOE) refers to a common
programming mistake where an iteration or action occurs one time more or
one time less than intended.

This generally happens because the wrong relational operator is used in
the conditional-expression (e.g., ``>`` instead of ``>=``). In the
example below, the loop is executed 11 times. If you intended to execute
the loop 10 times instead of 11, you need to change ``i <= 10`` to
``i < 10``.

.. code-block:: cpp

   for (int i{0}; i <= 10; i++) {
     std::cout << i << '\n';
   }

.. admonition:: Best Practice
   :class: tip

   It is a good idea to test your loops using known values to make sure
   that they work as expected. A good way to do this is to test your
   loop with known inputs that cause it to iterate 1, 2, and 3 times.
   If it works for those, it will likely work for any number of
   iterations.


Omitted Expressions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are cases where not declaring a loop variable (because you already
have one) or not incrementing it in ``end_expression`` (because you are
incrementing it some other way) is desired.

.. code-block:: cpp
   :linenos:

   int count{0};
   for (; count < 10;) {  // no init_statement or end_expression
       std::cout << count << ' ';
       ++count;
   }
   std::cout << '\n';
   std::cout << "The final value of count is: " << count << '\n';

Rather than having the ``for`` statement do the initialization and
incrementing, we did it manually at line 1.


More Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // decrement is also possible. Also note the use of auto keyword.
   for (auto i{9}; i >= 0; --i)
       std::cout << i << " ";

   std::cout << "\n---------\n";

   // although not often used, multiple counters are also possible
   for (auto i{0}, j{0}; i < 3; ++i, --j)
       std::cout << i << ' ' << j << '\n';

   std::cout << "---------\n";

   // nested loops
   for (auto i{1}; i < 6; ++i) {
       for (auto j{1}; j < 11; ++j) {
           std::cout << i * j << ' ';
       }
       std::cout << '\n';
   }


Scope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since C++11, the scope of the variables declared in the
``init_statement`` is visible only in the ``statement`` of the loop.

.. code-block:: cpp

   for (auto i{0}; i < 10; ++i)
       std::cout << i << '\n';

   std::cout << i; // error: 'i' was not declared in this scope

.. note::

   Prior to C++11, this variable could be accessed outside the loop
   body. That is, the error we have in the code above was not an error
   in C++ versions earlier than C++11.


``break`` Statements
----------------------------------------------------

The ``break`` statement causes a ``while`` statement, ``do``-``while``
statement, ``for`` statement, or ``switch`` statement to end, with
execution continuing with the next statement after the loop or
``switch`` being broken out of.

.. admonition:: ``break`` with ``for``
   :class: hint

   The following program exits the loop as soon as the condition on
   line 4 is ``true``.

   .. code-block:: cpp
      :linenos:

      // iterate 10 times
      for (auto i{0}; i < 10; ++i) {
          // exit loop if i is 3
          if (i == 3)
              break;  // exit the loop now

          // otherwise print i
          std::cout << i << ' ';
      }

      // execution will continue here after the break
      std::cout << "\nResuming program execution\n";

.. admonition:: ``break`` with ``while``
   :class: hint

   This program keeps asking the user ``Loop again (y/n)?`` until the
   user decides to stop by entering ``n``.

   .. code-block:: cpp

      while (true){ // infinite loop
          std::cout << "Loop again (y/n)? ";
          char input{};
          std::cin >> input;

          if (input == 'n')
              break;
      }

      // execution will continue here after the break
      std::cout << "Resuming program execution\n";

.. admonition:: ``break`` with ``do``-``while``
   :class: hint

   The ``do``-``while`` loop here is set up as an infinite loop
   (``while (true)``), and the only way to exit the loop is by entering
   the value ``-1``, triggering the ``break`` statement.

   .. code-block:: cpp

      int num{};

      do {
          std::cout << "Enter a number (-1 to exit): ";
          std::cin >> num;

          if (num == -1) {
              break; // Exit the loop when -1 is entered
          }
          std::cout << "You entered: " << num << '\n';
      } while (true); // Infinite loop, but we have a break condition inside

      std::cout << "You chose to exit.\n";


Operations
====================================================

An **operation** is a mathematical calculation involving zero or more
input values (called **operands**) that produces a new value (called an
**output value**). The specific operation to be performed is denoted by
a construct (typically a symbol or pair of symbols) called an
**operator**.


Operator Precedence
----------------------------------------------------

**Operator precedence** (often referred to as the order of operations)
determines the order in which operators are evaluated in expressions. If
an expression contains multiple operators, operator precedence ensures
that the expression is evaluated correctly. An expression that has
multiple operators is called a **compound expression**, e.g.,
``int a{1 + 2 * 3};``

- In order to evaluate a compound expression, the compiler uses operator
  precedence (e.g., PEMDAS, BODMAS, BIDMAS, BEDMAS, etc.).
- In C++, operator precedence is defined as seen on the
  `cppreference page <https://en.cppreference.com/w/cpp/language/operator_precedence>`_.

  - It is hard to digest everything on this page at first. You only need
    to know that this page exists and you can refer to it when needed.

- Based on the operator precedence used in C++, addition has precedence
  level 6 and multiplication has precedence level 5. This means
  multiplication will be performed before addition.
- The compiler implicitly evaluates the previous compound expression as
  follows:

.. code-block:: cpp

   int a{1 + (2 * 3)};


Operator Associativity
----------------------------------------------------

What happens if two operators in the same expression have the same
precedence level? In the expression below, the multiplication and
division operators are both precedence level 5.

.. code-block:: cpp

   std::cout << 4 * 3 / 2 << '\n';

- If two operators with the same precedence level are adjacent to each
  other in an expression, the operator's associativity tells the
  compiler whether to evaluate the operators from left to right or from
  right to left.
- For multiplication and division the associativity is left-to-right.
- The previous compound expression will be evaluated by the compiler as
  follows:

.. code-block:: cpp

   std::cout << (4 * 3) / 2 << '\n';


Parentheses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In normal arithmetic you can use parentheses to change the order of
application of operations. This will also work in C++ because
parentheses have a precedence level 2, which is quite high.

.. code-block:: cpp

   std::cout << 2 + 10 / 2 << '\n';    // 2 + (10 / 2)
   std::cout << (2 + 10) / 2 << '\n';  // use parentheses to be safe

.. admonition:: Best Practice
   :class: tip

   Use parentheses to make it clear how a non-trivial expression should
   evaluate (even if they are technically unnecessary).

   Although the compiler knows how to evaluate
   ``2 + 10 * 2 - 3 * 5``, you can make it clear for other users by
   writing: ``2 + (10 * 2) - (3 * 5)`` instead.


Arithmetic Operators
----------------------------------------------------

In C++, **arithmetic operators** are used to perform mathematical
operations between variables and/or values. These operators can be used
to manipulate integer, floating-point, and even some user-defined types
(by overloading them). However, it is crucial to be aware of the data
types you are working with, especially concerning division, to ensure
you get the expected result.


Unary Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unary operators are operators that act on a single operand.

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1
   :class: compact-table

   * - **Name**
     - **Operator**
     - **Use**
     - **Operation**
   * - Unary plus
     - ``+``
     - ``+x``
     - Value of ``x``
   * - Unary minus
     - ``-``
     - ``-x``
     - Negation of ``x``

- The **unary minus** operator returns the operand multiplied by -1.
- The **unary plus** operator returns the value of the operand. This
  operator is not really used and it was added to C++ to provide
  symmetry with the unary minus operator.

.. code-block:: cpp

   int x{5};
   int y{-3};
   std::cout << +x << '\n'; // 5
   std::cout << -x << '\n'; // -5
   std::cout << +y << '\n'; // -3
   std::cout << -y << '\n'; // 3


Binary Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Binary operators are operators that take two operands.

.. list-table::
   :widths: 30 20 50
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Use**
     - **Operation**
   * - ``+``
     - ``x + y``
     - Addition
   * - ``-``
     - ``x - y``
     - Subtraction
   * - ``*``
     - ``x * y``
     - Multiplication
   * - ``/``
     - ``x / y``
     - Division
   * - ``%``
     - ``x % y``
     - Modulus


Division Operator
""""""""""""""""""""""""""""""""""""""""""""""""""""

If both operands are integers, the **division operator** performs integer
division. If at least one of the operands is a floating-point number,
the division performs floating-point division.

.. note::

   If you want to do floating-point division with 2 integer variables,
   you can do an explicit conversion with ``static_cast``.

.. code-block:: cpp

   std::cout << 4 / 3 << '\n';                       // 1
   std::cout << 4.0 / 3 << '\n';                     // 1.33333
   std::cout << 4 / 3.0 << '\n';                     // 1.33333
   std::cout << 4.0 / 3.0 << '\n';                   // 1.33333

   int x{3};
   int y{2};
   std::cout << x / y << '\n';  // 1
   std::cout << static_cast<double>(x) / y << '\n';  // 1.5


Modulus Operator
""""""""""""""""""""""""""""""""""""""""""""""""""""

The **modulus operator** returns the remainder of an integer division.
For instance, ``11 / 4 = 2`` remainder ``3``, therefore,
``11 % 4 = 3``.

- If ``y > x`` then the result of ``x % y`` is ``x``. For instance, the
  result of ``2 % 5`` is ``2`` since ``2 = 5 * 0 + 2``.
- The modulus operator works with negative operands too. ``x % y``
  always returns results with the sign of ``x``. For instance,
  ``-2 % 5 = -2``, ``2 % -5 = 2``, and ``-2 % -5 = -2``.


(Compound) Assignment Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **assignment operator** is represented by the ``=`` symbol. It is
used to assign the value on its right to the variable on its left.
**Compound assignment operators** combine an arithmetic operation with
an assignment in a single step.

.. list-table::
   :widths: 20 20 60
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Use**
     - **Operation**
   * - ``=``
     - ``x = y``
     - Assignment
   * - ``+=``
     - ``x += y``
     - Addition Assignment
   * - ``-=``
     - ``x -= y``
     - Subtraction Assignment
   * - ``*=``
     - ``x *= y``
     - Multiplication Assignment
   * - ``/=``
     - ``x /= y``
     - Division Assignment
   * - ``%=``
     - ``x %= y``
     - Modulus Assignment

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      int x{4};
      x = x + 3;              // add 3 to existing value of x. x = 4 + 3 = 7
      x = x % 3;              // put the remainder of x % 3 in x. x = 7 % 3 = 1
      std::cout << x << '\n'; // 1

   Although the code above is fine, it is a bit clunky. You can use the
   **addition assignment operator** and the **modulus assignment
   operator** to achieve the same result:

   .. code-block:: cpp

      int x{4};
      x += 3;                 // add 3 to existing value of x. x = 4 + 3 = 7
      x %= 3;                 // put the remainder of x % 3 in x. x = 7 % 3 = 1
      std::cout << x << '\n'; // 1


Increment/Decrement Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Incrementing (adding 1 to) and decrementing (subtracting 1 from) a
variable are very common in C++ and can be done with the **increment
operator** and the **decrement operator**, respectively.

.. list-table::
   :widths: 15 15 30 40
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Use**
     - **Operation**
     - **Description**
   * - ``++``
     - ``++x``
     - Prefix Increment
     - Increment ``x`` then return ``x``
   * - ``++``
     - ``x++``
     - Postfix Increment
     - Return ``x`` then increment ``x``
   * - ``--``
     - ``--x``
     - Prefix Decrement
     - Decrement ``x`` then return ``x``
   * - ``--``
     - ``x--``
     - Postfix Decrement
     - Return ``x`` then decrement ``x``

.. admonition:: Prefix and Postfix
   :class: hint

   **Prefix increment/decrement:**

   1. The variable is incremented/decremented first.
   2. The incremented/decremented value is then used in the expression.

   .. code-block:: cpp

      int a{2};
      int b{++a}; // increment a first then initialize b
      int c{--a}; // decrement a first then initialize c

      std::cout << a << ' ' << b << ' ' << c << '\n'; // 2 3 2

   **Postfix increment/decrement:**

   1. The current value of the variable is used in the expression.
   2. The variable is incremented/decremented afterward.

   .. code-block:: cpp

      int a{2};
      int b{a++}; // initialize b and then increment a
      int c{a--}; // initialize c and then decrement a

      std::cout << a << ' ' << b << ' ' << c << '\n'; // 2 2 3


Comma Symbol
----------------------------------------------------

In C++, the **comma symbol** is used as a separator or as an operator.
Most C++ users are more familiar with the use of the comma symbol as a
separator.

.. admonition:: Example -- Comma as Separator
   :class: hint

   .. code-block:: cpp

      void f(int x, int y){           // comma used to separate parameters
          g(x, y);                    // comma used to separate arguments
          for (int i{0}; i < x; ++i){
              std::cout << i << '\n';
          }
      }

The use of the comma symbol as an operator is less common. The comma
operator allows you to evaluate multiple expressions wherever a single
expression is allowed. The comma operator evaluates the left operand,
then the right operand, and then returns the result of the right
operand.

.. admonition:: Example -- Comma as Operator
   :class: hint

   .. code-block:: cpp
      :linenos:

      int x{1};
      int y{2};
      auto z{(++x, ++y)};// increment x, increment y, return y
      std::cout << x << ' ' << y << ' ' << z << '\n';  // 2 3 3

   In the code above, multiple things are happening on line 3:

   1. ``(++x, ++y)`` is evaluated:

      a. ``x`` is incremented (its value is now ``2``).
      b. ``y`` is incremented (its value is now ``3``).
      c. The value of ``y`` is returned.

   2. ``auto z{(++x, ++y)}`` is evaluated:

      - The value returned by ``(++x, ++y)`` (the new value of ``y``)
        is used to initialize ``z``. In other words, line 3 becomes
        ``auto z{3};``

   In almost every case, a statement written using the comma operator
   would be better written as separate statements:

   .. code-block:: cpp

      int x{1};
      int y{2};
      ++x;        // increment x
      auto z{++y};// increment y and use its incremented value to initialize z
      std::cout << x << ' ' << y << ' ' << z << '\n';  // 2 3 3


Relational Operators
----------------------------------------------------

**Relational operators** in C++ are used to compare two values. These
operators evaluate to a boolean value: ``true`` or ``false`` based on
the result of the comparison.

.. list-table::
   :widths: 30 15 15 40
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Symbol**
     - **Use**
     - **Description**
   * - greater than
     - ``>``
     - ``a > b``
     - ``true`` if ``a > b``, ``false`` otherwise
   * - less than
     - ``<``
     - ``a < b``
     - ``true`` if ``a < b``, ``false`` otherwise
   * - greater than or equals
     - ``>=``
     - ``a >= b``
     - ``true`` if ``a >= b``, ``false`` otherwise
   * - less than or equals
     - ``<=``
     - ``a <= b``
     - ``true`` if ``a <= b``, ``false`` otherwise
   * - equality
     - ``==``
     - ``a == b``
     - ``true`` if ``a == b``, ``false`` otherwise
   * - inequality
     - ``!=``
     - ``a != b``
     - ``true`` if ``a != b``, ``false`` otherwise

.. admonition:: Example
   :class: hint

   .. code-block:: cpp

      std::cout << "Enter two integers: ";
      int x{};
      int y{};
      std::cin >> x >> y;

      if (x == y)
          std::cout << x << " equals " << y << '\n';
      if (x != y)
          std::cout << x << " does not equal " << y << '\n';
      if (x > y)
          std::cout << x << " is greater than " << y << '\n';
      if (x < y)
          std::cout << x << " is less than " << y << '\n';
      if (x >= y)
          std::cout << x << " is greater than or equal to " << y << '\n';
      if (x <= y)
          std::cout << x << " is less than or equal to " << y << '\n';

.. admonition:: Best Practice
   :class: tip

   Do not explicitly compare a boolean variable to ``true`` or
   ``false``.

   .. code-block:: cpp

      bool b{true};
      if (b == true){                                  // redundant
          std::cout << std::boolalpha << b << '\n';
      }

   The same code is better written as:

   .. code-block:: cpp

      bool b{true};
      if (b){                                          // preferred
          std::cout << std::boolalpha << b << '\n';
      }


Logical Operators
----------------------------------------------------

**Logical operators** are used to form more complex conditions by
combining or negating boolean expressions. These operators evaluate to a
boolean value: ``true`` or ``false``.

With logical operators we can test multiple conditions. C++ has 3
logical operators:

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Symbol**
     - **Use**
     - **Description**
   * - logical NOT
     - ``!``
     - ``!a``
     - ``true`` if ``a`` is ``false``, or ``false`` if ``a`` is ``true``
   * - logical AND
     - ``&&``
     - ``a && b``
     - ``true`` if both ``a`` and ``b`` are ``true``, otherwise ``false``
   * - logical OR
     - ``||``
     - ``a || b``
     - ``true`` if at least ``a`` or ``b`` is ``true``, otherwise ``false``


Logical NOT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **logical NOT** operator changes a boolean value from ``true`` to
``false`` and vice-versa.

In the sample code below, if ``a`` is not greater than ``b`` then it
means that ``b`` is greater than ``a``.

.. code-block:: cpp

   int a{2};
   int b{4};
   if (!(a > b)) {
       std::cout << b << " is greater than " << a << '\n';
   }

.. warning::

   Writing the previous code as below means something completely
   different.

   .. code-block:: cpp

      int a{2};
      int b{4};
      if (!a > b) { // we removed the parentheses
          std::cout << b << " is greater than " << a << '\n';
      }

   - The **logical NOT** operator has a precedence level higher than
     the ``>`` operator.
   - In the example, ``if (!a > b)`` becomes ``if ((!a) > b)``
   - ``(!a)`` evaluates to 0 since ``(!2) = (!true) = false = 0``
   - The expression ``if (!a > b)`` becomes ``if (0 > 4)``, which
     evaluates to ``false``.
   - The program does not output anything.


Logical OR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **logical OR** can be chained to test multiple conditions.

.. code-block:: cpp

   int a{2};
   if (a == 1 || a == 2 || a == 4) {
       std::cout << "a is 1, 2, or 4\n";
   }


Logical AND
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **logical AND** can also be chained to test multiple conditions.

.. code-block:: cpp

   int a{2};
   if (a > 0 && a < 6 && a != 3) {
       std::cout << "a is between 1 and 5 and is not 3\n";
   }


Short Circuit Evaluation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Short circuit evaluation is a programming concept in which the compiler
skips the execution or evaluation of some sub-expressions in a logical
expression. The compiler stops evaluating the further sub-expressions as
soon as the value of the expression is determined.

In order for **logical AND** to return ``true``, both operands must
evaluate to ``true``. If the first operand evaluates to ``false``,
**logical AND** knows it must return ``false`` regardless of whether the
second operand evaluates to ``true`` or ``false``. In the example below,
the second operand ``b == 2`` is never evaluated since the first operand
``a == 1`` evaluates to ``false``.

.. code-block:: cpp

   int a{2};
   int b{2};
   if (a == 1 && b == 2)
       std::cout << "if statement evaluated to true\n";
   else
       std::cout << "if statement evaluated to false\n";


Miscellaneous
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Mixing ``&&`` and ``||`` is possible. You just need to be aware of
  operator precedence and operator associativity. ``&&`` and ``||`` are
  evaluated from left to right with ``&&`` having a higher precedence
  level than ``||``.

  - For instance: ``(a == 1 || a == 2 && b == 1)`` evaluates as
    ``(a == 1 || (a == 2 && b == 1))``
  - If you meant the evaluation to be
    ``((a == 1 || a == 2) && b == 1)`` then explicitly use parentheses
    in your code.

- ``!(a && b)`` is ``!a || !b``
- ``!(a || b)`` is ``!a && !b``
- C++ provides a list of
  `alternative representations <https://en.cppreference.com/w/cpp/language/operator_alternative>`_
  for many operators. For instance, you can write
  ``((a == 1 || a == 2) && !(b == 1))`` as
  ``((a == 1 or a == 2) and not(b == 1))``.
