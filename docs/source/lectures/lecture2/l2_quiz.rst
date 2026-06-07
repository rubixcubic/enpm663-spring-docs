====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 2: Introduction to C++.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What are the three stages of the C++ build process, in order?

   A. Compiler, preprocessor, linker
   B. Preprocessor, compiler, linker
   C. Linker, compiler, preprocessor
   D. Preprocessor, linker, compiler

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Preprocessor, compiler, linker

   *Explanation:* The preprocessor handles directives like ``#include`` and ``#define``, producing a translation unit. The compiler translates each translation unit into an object file. The linker combines object files and libraries into the final executable.


----

.. admonition:: Question 2
   :class: hint

   Which of the following is the correct way to use uniform (brace) initialization in C++?

   A. ``int speed = 10;``
   B. ``int speed(10);``
   C. ``int speed{10};``
   D. ``int speed[10];``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``int speed{10};``

   *Explanation:* Uniform initialization uses curly braces ``{}``. This is the preferred initialization style in modern C++ because it prevents narrowing conversions. Option A is copy initialization, B is direct initialization, and D declares an array.


----

.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      int value{5};
      {
          int value{10};
          std::cout << value;
      }
      std::cout << value;

   A. ``55``
   B. ``1010``
   C. ``105``
   D. ``510``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``105``

   *Explanation:* The inner block declares a new variable ``value`` that shadows the outer one. Inside the block, ``value`` is 10. Once the block ends, the inner ``value`` goes out of scope, and the outer ``value`` (which is 5) is printed.


----

.. admonition:: Question 4
   :class: hint

   What does the ``sizeof`` operator return?

   A. The value stored in a variable.
   B. The number of bits used by a type.
   C. The number of bytes used by a type or variable.
   D. The memory address of a variable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The number of bytes used by a type or variable.

   *Explanation:* The ``sizeof`` operator returns the size in bytes of a type or variable. For example, ``sizeof(int)`` typically returns 4 on most modern systems, meaning ``int`` uses 4 bytes (32 bits) of memory.


----

.. admonition:: Question 5
   :class: hint

   Which of the following demonstrates a narrowing conversion that uniform initialization would catch?

   A. ``int x{5};``
   B. ``double d{3.14};``
   C. ``int x{3.14};``
   D. ``float f{3.14f};``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``int x{3.14};``

   *Explanation:* Assigning a ``double`` literal (3.14) to an ``int`` using brace initialization is a narrowing conversion. The compiler will issue an error because data would be lost (the fractional part). This is one of the key benefits of uniform initialization -- it prevents accidental data loss.


----

.. admonition:: Question 6
   :class: hint

   What is the difference between ``const`` and ``constexpr``?

   A. ``const`` is evaluated at compile time; ``constexpr`` is evaluated at runtime.
   B. ``constexpr`` guarantees compile-time evaluation; ``const`` only means the value cannot be modified after initialization.
   C. They are identical in behavior.
   D. ``constexpr`` can only be used with integers.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``constexpr`` guarantees compile-time evaluation; ``const`` only means the value cannot be modified after initialization.

   *Explanation:* A ``const`` variable can be initialized with a runtime value (e.g., user input). A ``constexpr`` variable must be initialized with a value that can be computed at compile time. This allows the compiler to optimize by substituting the value directly.


----

.. admonition:: Question 7
   :class: hint

   What naming convention does the C++ Core Guidelines recommend for variables?

   A. camelCase (e.g., ``myVariable``)
   B. PascalCase (e.g., ``MyVariable``)
   C. snake_case (e.g., ``my_variable``)
   D. Hungarian notation (e.g., ``iMyVariable``)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- snake_case (e.g., ``my_variable``)

   *Explanation:* The C++ Core Guidelines recommend snake_case for variable and function names. This convention uses lowercase letters with underscores separating words, improving readability.


----

.. admonition:: Question 8
   :class: hint

   Given the following code, what is the type of ``result``?

   .. code-block:: cpp

      int a{5};
      double b{2.5};
      auto result = a + b;

   A. ``int``
   B. ``float``
   C. ``double``
   D. ``long``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``double``

   *Explanation:* When an ``int`` and a ``double`` are used in an arithmetic expression, the ``int`` is implicitly converted to ``double`` through arithmetic conversion (the type with the higher rank wins). The ``auto`` keyword deduces the type of the result, which is ``double``.


----

.. admonition:: Question 9
   :class: hint

   What happens when you access an uninitialized local variable in C++?

   A. It is automatically initialized to zero.
   B. The compiler always generates an error.
   C. It results in undefined behavior.
   D. It is initialized to ``nullptr``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It results in undefined behavior.

   *Explanation:* Reading an uninitialized local variable in C++ is undefined behavior. The variable holds whatever garbage value was previously at that memory location. The compiler may or may not warn about this. Always initialize your variables.


----

.. admonition:: Question 10
   :class: hint

   Which statement about namespaces is correct?

   A. ``using namespace std;`` is recommended in header files.
   B. Namespaces prevent naming collisions by grouping identifiers under a unique name.
   C. You cannot nest namespaces inside other namespaces.
   D. The ``::`` operator is called the dot operator.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Namespaces prevent naming collisions by grouping identifiers under a unique name.

   *Explanation:* Namespaces are used to organize code and prevent naming collisions. Using ``using namespace std;`` in header files is considered bad practice because it pollutes the global namespace for all files that include that header. Namespaces can be nested, and ``::`` is called the scope resolution operator.


----

True/False
==========

.. admonition:: Question 11
   :class: hint

   **True or False:** The ``#include`` directive is processed by the compiler during the compilation stage.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* The ``#include`` directive is processed by the **preprocessor**, not the compiler. The preprocessor runs before compilation and handles all directives that begin with ``#``, such as ``#include``, ``#define``, and ``#ifdef``.


----

.. admonition:: Question 12
   :class: hint

   **True or False:** A ``constexpr`` variable can be initialized with a value obtained from ``std::cin``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* A ``constexpr`` variable must be initialized with a value that can be computed at compile time. Since ``std::cin`` reads input at runtime, it cannot be used to initialize a ``constexpr`` variable. A ``const`` variable, however, can be initialized with runtime values.


----

.. admonition:: Question 13
   :class: hint

   **True or False:** In C++, ``bool`` values ``true`` and ``false`` are stored as integers ``1`` and ``0`` respectively.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* In C++, ``true`` is implicitly convertible to the integer ``1`` and ``false`` to ``0``. When a ``bool`` is used in an arithmetic context, this integral promotion occurs automatically. Similarly, any non-zero integer converts to ``true`` and zero converts to ``false``.


----

.. admonition:: Question 14
   :class: hint

   **True or False:** A variable declared inside a ``for`` loop body can be accessed after the loop ends.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Variables declared inside a ``for`` loop body (or any block enclosed in ``{}``) have local scope limited to that block. Once the block ends, the variable goes out of scope and is destroyed. Attempting to access it outside the block would result in a compilation error.


----

.. admonition:: Question 15
   :class: hint

   **True or False:** Using ``static_cast<int>(3.7)`` will result in the value ``4`` due to rounding.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* ``static_cast<int>(3.7)`` truncates the decimal part, resulting in ``3``, not ``4``. The cast does not round -- it simply discards the fractional portion. This is the same behavior as a C-style cast ``(int)3.7`` but is preferred because it is explicit and searchable.
