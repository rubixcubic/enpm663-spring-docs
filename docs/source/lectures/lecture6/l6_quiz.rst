.. _l6_quiz:

================
Lecture 6 Quiz
================

This quiz covers the key concepts from Lecture 6: Functions -- Advanced. Topics include structs, templates, template type deduction, ``decltype``, ``constexpr`` functions, ``inline``/ODR, function pointers, functors, lambdas, capture clauses, and ``std::function``.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1--10)
===================================

.. admonition:: Question 1
   :class: hint

   What is the **only** difference between a ``struct`` and a ``class`` in C++?

   A. ``struct`` cannot have methods; ``class`` can.
   B. ``struct`` members are ``public`` by default; ``class`` members are ``private`` by default.
   C. ``struct`` is allocated on the stack; ``class`` is allocated on the heap.
   D. ``struct`` does not support inheritance; ``class`` does.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. struct members are public by default; class members are private by default.**

      In C++, ``struct`` and ``class`` are nearly identical. Both support methods, inheritance, templates, and all other class features. The sole difference is the default access level.

.. admonition:: Question 2
   :class: hint

   What does the compiler do when it encounters a call to a function template with specific types?

   A. It interprets the template at runtime.
   B. It instantiates a concrete function for those types at compile time.
   C. It converts the template to a virtual function.
   D. It stores the template for lazy evaluation.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It instantiates a concrete function for those types at compile time.**

      Templates are blueprints. When you call ``add(3, 4)``, the compiler generates ``int add(int, int)`` at compile time. This is called template instantiation.

.. admonition:: Question 3
   :class: hint

   Why must template definitions be placed in header files (``.hpp``)?

   A. Because templates are always ``inline``.
   B. Because the compiler needs the full definition to instantiate the template for each type used.
   C. Because the linker cannot resolve template symbols.
   D. Because ``.cpp`` files cannot contain template code.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Because the compiler needs the full definition to instantiate the template for each type used.**

      Templates are not compiled until they are instantiated. If the definition is in a ``.cpp`` file, other translation units cannot see it and cannot instantiate the template, resulting in a linker error.

.. admonition:: Question 4
   :class: hint

   Given ``template<typename T> T add(T a, T b);``, what happens when you call ``add(3, 4.5)``?

   A. The compiler deduces ``T = double`` and converts ``3`` to ``double``.
   B. The compiler deduces ``T = int`` and truncates ``4.5``.
   C. The call fails because the compiler cannot deduce a single consistent ``T``.
   D. The compiler creates two instantiations and picks the best one.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The call fails because the compiler cannot deduce a single consistent T.**

      Both parameters share the same ``T``. Argument ``3`` suggests ``T = int`` while ``4.5`` suggests ``T = double``. The compiler cannot reconcile these, so deduction fails. You must either use explicit template arguments (``add<double>(3, 4.5)``) or use two template parameters.

.. admonition:: Question 5
   :class: hint

   What does ``decltype(x)`` produce when ``x`` is declared as ``int x{10};``?

   A. ``int&``
   B. ``const int``
   C. ``int``
   D. ``int&&``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. int**

      ``decltype(x)`` (without extra parentheses) yields the **declared type** of ``x``, which is ``int``. Note: ``decltype((x))`` would yield ``int&`` because ``(x)`` is an lvalue expression.

.. admonition:: Question 6
   :class: hint

   Which statement about ``constexpr`` functions is correct?

   A. A ``constexpr`` function is always evaluated at compile time.
   B. A ``constexpr`` function can be evaluated at compile time if all arguments are constant expressions.
   C. A ``constexpr`` function cannot contain local variables (even in C++14).
   D. A ``constexpr`` function can perform I/O operations.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. A constexpr function can be evaluated at compile time if all arguments are constant expressions.**

      ``constexpr`` marks a function as *potentially* evaluable at compile time. If called with runtime values, it executes at runtime like a normal function. From C++14 onward, ``constexpr`` functions may contain variables, loops, and conditionals.

.. admonition:: Question 7
   :class: hint

   What is the primary modern purpose of the ``inline`` keyword in C++?

   A. To force the compiler to inline the function body at every call site.
   B. To relax the One Definition Rule (ODR), allowing the function to be defined in a header included by multiple translation units.
   C. To make the function run faster.
   D. To prevent the function from being called recursively.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. To relax the One Definition Rule (ODR), allowing the function to be defined in a header included by multiple translation units.**

      Modern compilers decide on their own whether to inline a function. The ``inline`` keyword's primary purpose today is to tell the linker that identical definitions across translation units are intentional and should be merged rather than causing a linker error.

.. admonition:: Question 8
   :class: hint

   Given the following code, what is the type of ``func_ptr``?

   .. code-block:: cpp

      int multiply(int a, int b) { return a * b; }
      auto func_ptr = &multiply;

   A. ``int*``
   B. ``int(*)(int, int)``
   C. ``int&(int, int)``
   D. ``std::function<int(int, int)>``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. int(\*)(int, int)**

      ``&multiply`` produces a function pointer. The type is "pointer to a function taking two ``int``\s and returning ``int``", written as ``int(*)(int, int)``.

.. admonition:: Question 9
   :class: hint

   What does the ``mutable`` keyword do when used with a lambda?

   A. It allows the lambda to modify global variables.
   B. It allows the lambda to modify its copies of variables captured by value.
   C. It makes the lambda thread-safe.
   D. It allows the lambda to be called multiple times.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It allows the lambda to modify its copies of variables captured by value.**

      By default, variables captured by value are ``const`` inside the lambda. The ``mutable`` keyword removes this restriction, allowing the lambda to modify its internal copies. The original variables in the enclosing scope are not affected.

.. admonition:: Question 10
   :class: hint

   What is **type erasure** in the context of ``std::function``?

   A. Deleting the type information of a variable at runtime.
   B. Hiding the specific callable type (lambda, functor, function pointer) behind a common interface.
   C. Converting all callables to function pointers.
   D. Removing template parameters after instantiation.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Hiding the specific callable type (lambda, functor, function pointer) behind a common interface.**

      ``std::function`` "erases" the concrete type of the stored callable and presents a uniform interface based solely on the function signature. This allows different callable types to be stored in the same variable or passed to the same function parameter.


True/False (Questions 11--15)
===============================

.. admonition:: Question 11
   :class: hint

   **True or False**: Structured bindings can only decompose ``struct`` types, not ``std::pair`` or ``std::tuple``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Structured bindings (``auto [a, b] = ...``) work with ``struct`` types, ``std::pair``, ``std::tuple``, and arrays. They bind to the members/elements in declaration order.

.. admonition:: Question 12
   :class: hint

   **True or False**: A lambda with capture clause ``[=]`` captures all variables from the surrounding scope by value, and the copies are ``const`` by default.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      The ``[=]`` capture clause makes copies of all used variables. These copies are ``const`` inside the lambda's ``operator()`` by default. To modify them, you must add the ``mutable`` keyword.

.. admonition:: Question 13
   :class: hint

   **True or False**: If a ``noexcept`` function throws an exception, the program invokes undefined behavior.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      If an exception escapes a ``noexcept`` function, ``std::terminate()`` is called. This is well-defined behavior (the program is terminated), not undefined behavior.

.. admonition:: Question 14
   :class: hint

   **True or False**: Calling a default-constructed (empty) ``std::function`` object results in a ``std::bad_function_call`` exception.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      A default-constructed ``std::function`` holds no callable. Invoking it throws ``std::bad_function_call``. You should check with ``if (func) { ... }`` before calling it if the function might be empty.

.. admonition:: Question 15
   :class: hint

   **True or False**: A functor can hold state between calls, whereas a regular function (without ``static`` variables) cannot.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      A functor is an object with member variables that persist across calls to ``operator()``. A regular function is stateless (unless it uses ``static`` local variables, which is a different mechanism with its own implications).
