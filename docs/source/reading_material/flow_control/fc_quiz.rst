====================================================
Flow Control and Operations -- Quiz
====================================================


.. admonition:: Question 1
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      int x{5};
      if (x > 3)
          std::cout << "A\n";
      else
          std::cout << "B\n";

   a) ``A``
   b) ``B``
   c) ``AB``
   d) No output

   .. dropdown:: Answer
      :class-container: sd-border-success

      **a) A**

      Since ``x`` is 5 and ``5 > 3`` is ``true``, the ``if`` branch
      executes and prints ``A``.


.. admonition:: Question 2
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      int a{2};
      if (a > 0)
          std::cout << "positive\n";
          std::cout << "done\n";

   a) ``positive`` only
   b) ``done`` only
   c) Both ``positive`` and ``done``
   d) No output

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) Both positive and done**

      Without braces, only the first statement after ``if`` is
      conditional. ``std::cout << "done\n";`` is always executed
      regardless of the condition because it is not part of the ``if``
      block (implicit block covers only one statement).


.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      int val{2};
      switch (val) {
          case 1:
              std::cout << "one\n";
              break;
          case 2:
              std::cout << "two\n";
          case 3:
              std::cout << "three\n";
              break;
          default:
              std::cout << "other\n";
      }

   a) ``two``
   b) ``two`` followed by ``three``
   c) ``two`` followed by ``three`` followed by ``other``
   d) ``three``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) two followed by three**

      ``case 2`` matches and prints ``two``. There is no ``break``
      after ``case 2``, so execution falls through to ``case 3``,
      printing ``three``. The ``break`` in ``case 3`` then exits the
      ``switch``.


.. admonition:: Question 4
   :class: hint

   What value does ``result`` hold after the following code executes?

   .. code-block:: cpp

      int a{7};
      int b{3};
      int result{(a > b) ? a : b};

   a) 3
   b) 7
   c) 0
   d) Compilation error

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) 7**

      Since ``a > b`` (7 > 3) is ``true``, the ternary operator
      returns ``a`` which is 7.


.. admonition:: Question 5
   :class: hint

   How many times does the following loop execute?

   .. code-block:: cpp

      for (int i{0}; i <= 5; ++i) {
          std::cout << i << ' ';
      }

   a) 5
   b) 6
   c) 4
   d) Infinite

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) 6**

      The loop starts at ``i = 0`` and runs while ``i <= 5``, so it
      executes for ``i`` values 0, 1, 2, 3, 4, 5 -- that is 6
      iterations.


.. admonition:: Question 6
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      int i{0};
      while (i < 5) {
          if (i == 3)
              break;
          std::cout << i << ' ';
          ++i;
      }

   a) ``0 1 2 3 4``
   b) ``0 1 2``
   c) ``0 1 2 3``
   d) ``1 2 3``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) 0 1 2**

      When ``i`` reaches 3, the ``break`` statement exits the loop
      before printing 3. So the output is ``0 1 2``.


.. admonition:: Question 7
   :class: hint

   What is the value of ``x`` after the following code?

   .. code-block:: cpp

      int x{10};
      int y{3};
      x %= y;

   a) 3
   b) 1
   c) 0
   d) 10

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) 1**

      ``x %= y`` is equivalent to ``x = x % y``, which is
      ``x = 10 % 3 = 1``.


.. admonition:: Question 8
   :class: hint

   What does the following expression evaluate to?

   .. code-block:: cpp

      int a{5};
      int b{0};
      bool result{a > 3 && b != 0};

   a) ``true``
   b) ``false``
   c) Compilation error
   d) Undefined behavior

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) false**

      ``a > 3`` is ``true``, but ``b != 0`` is ``false``. Since
      logical AND requires both operands to be ``true``, the result is
      ``false``.


.. admonition:: Question 9
   :class: hint

   What is the value of ``result`` after this code?

   .. code-block:: cpp

      int a{2};
      int b{++a};
      int result{a + b};

   a) 4
   b) 5
   c) 6
   d) 3

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) 6**

      ``++a`` increments ``a`` to 3, then assigns 3 to ``b``.
      ``result = a + b = 3 + 3 = 6``.


.. admonition:: Question 10
   :class: hint

   Which of the following is the correct evaluation order for
   ``2 + 3 * 4``?

   a) ``(2 + 3) * 4 = 20``
   b) ``2 + (3 * 4) = 14``
   c) Left to right: ``2 + 3 = 5``, then ``5 * 4 = 20``
   d) The order is undefined

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) 2 + (3 * 4) = 14**

      Multiplication has a higher precedence level (level 5) than
      addition (level 6), so ``3 * 4`` is evaluated first.


.. admonition:: Question 11
   :class: hint

   True or False: A ``do``-``while`` loop always executes its body at
   least once.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      The ``do``-``while`` loop executes the statement first and then
      checks the condition, so the body always runs at least once.


.. admonition:: Question 12
   :class: hint

   True or False: In a ``switch`` statement, the ``default`` case is
   required.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      The ``default`` label is optional. If no ``default`` is provided
      and none of the ``case`` labels match, the ``switch`` statement
      simply does nothing.


.. admonition:: Question 13
   :class: hint

   True or False: The expression ``if (0)`` will execute the body of
   the ``if`` statement.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      The integer ``0`` is implicitly converted to ``false``, so the
      body of the ``if`` statement is not executed.


.. admonition:: Question 14
   :class: hint

   True or False: The logical OR operator (``||``) uses short-circuit
   evaluation, meaning if the first operand is ``true``, the second
   operand is not evaluated.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      Logical OR returns ``true`` as soon as one operand is ``true``.
      If the first operand is already ``true``, there is no need to
      evaluate the second operand.


.. admonition:: Question 15
   :class: hint

   True or False: Variables declared in the ``init_statement`` of a
   ``for`` loop (since C++11) can be accessed after the loop ends.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Since C++11, the scope of the variable declared in the
      ``init_statement`` is limited to the body of the loop. Accessing
      it outside the loop results in a compilation error.
