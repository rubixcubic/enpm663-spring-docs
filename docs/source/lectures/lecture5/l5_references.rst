.. _l5_references:

===================
Lecture 5 References
===================

.. dropdown:: Lecture 5 Summary
   :class-container: sd-border-success

   This lecture covered the fundamentals of functions in C++, organized into four parts:

   - **The Core Mechanics**: We introduced functions as named, reusable units of code, emphasizing the benefits of code reusability (DRY principle), modularity, easier debugging, and abstraction. We covered the function lifecycle -- declaration (the "promise"), definition (the implementation), and call (the execution). Header files (``.hpp``) and source files (``.cpp``) were introduced as the proper way to separate declarations from definitions, along with include guards (``#pragma once``). We also covered the ``return`` keyword, including returning from ``void`` functions, returning values, implicit return type conversion, returning multiple values (``std::pair``, ``std::tuple``, ``struct``), and return type deduction with ``auto``.

   - **The Function Interface**: We examined how data flows into functions through parameters (pass-by-value, pass-by-reference, pass-by-const-reference, pass-by-pointer) and out of functions through return values (return-by-value, return-by-reference, return-by-pointer). Copy elision (RVO and NRVO) was introduced as a key optimization that eliminates unnecessary copying. The dangers of dangling references and dangling pointers were highlighted.

   - **Enhancing Functions**: We covered static variables (persistent state across calls), function overloading (same name, different parameter lists), overload resolution, and default parameters. Best practices for default parameter placement (declaration only) were discussed.

   - **Under the Hood and Best Practices**: The call stack and stack frames were explained using the LIFO model. Recursive functions were introduced with the factorial example, along with guidelines for when to use (and avoid) recursion. Documentation with Doxygen (``@brief``, ``@param``, ``@return``) and the ``main()`` function with command-line arguments (``argc``, ``argv``) were covered.

.. dropdown:: C++ Reference Links
   :class-container: sd-border-success

   - `Functions -- cppreference.com <https://en.cppreference.com/w/cpp/language/functions>`_
   - `Function overloading -- cppreference.com <https://en.cppreference.com/w/cpp/language/overload_resolution>`_
   - `Default arguments -- cppreference.com <https://en.cppreference.com/w/cpp/language/default_arguments>`_
   - `Copy elision -- cppreference.com <https://en.cppreference.com/w/cpp/language/copy_elision>`_
   - `std::pair -- cppreference.com <https://en.cppreference.com/w/cpp/utility/pair>`_
   - `std::tuple -- cppreference.com <https://en.cppreference.com/w/cpp/utility/tuple>`_
   - `Structured bindings -- cppreference.com <https://en.cppreference.com/w/cpp/language/structured_binding>`_
   - `main function -- cppreference.com <https://en.cppreference.com/w/cpp/language/main_function>`_

.. dropdown:: C++ Core Guidelines
   :class-container: sd-border-success

   - `F: Functions <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-functions>`_
   - `F.1: "Package" meaningful operations as carefully named functions <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f1-package-meaningful-operations-as-carefully-named-functions>`_
   - `F.2: A function should perform a single logical operation <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f2-a-function-should-perform-a-single-logical-operation>`_
   - `F.3: Keep functions short and simple <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f3-keep-functions-short-and-simple>`_
   - `F.15: Prefer simple and conventional ways of passing information <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f15-prefer-simple-and-conventional-ways-of-passing-information>`_
   - `F.16: For "in" parameters, pass cheaply-copied types by value and others by reference to const <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f16-for-in-parameters-pass-cheaply-copied-types-by-value-and-others-by-reference-to-const>`_
   - `F.17: For "in-out" parameters, pass by reference to non-const <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f17-for-in-out-parameters-pass-by-reference-to-non-const>`_
   - `F.21: To return multiple "out" values, prefer returning a struct <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f21-to-return-multiple-out-values-prefer-returning-a-struct>`_
   - `F.43: Never return a pointer or reference to a local object <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f43-never-directly-or-indirectly-return-a-pointer-or-a-reference-to-a-local-object>`_
   - `F.46: int is the return type for main() <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f46-int-is-the-return-type-for-main>`_
   - `F.51: Where there is a choice, prefer default arguments over overloading <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#Rf-default-args>`_

.. dropdown:: Doxygen Documentation
   :class-container: sd-border-success

   - `Doxygen Manual <https://www.doxygen.nl/manual/index.html>`_
   - `Doxygen: Documenting the code <https://www.doxygen.nl/manual/docblocks.html>`_
   - `Doxygen: Special commands <https://www.doxygen.nl/manual/commands.html>`_ -- reference for ``@brief``, ``@param``, ``@return``, ``@note``, ``@warning``, and other commands.

.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   - *A Tour of C++* by Bjarne Stroustrup -- Chapter 1 (The Basics, functions and scope)
   - *C++ Primer* by Lippman, Lajoie, and Moo -- Chapter 6 (Functions)
   - `LearnCpp.com: Introduction to functions <https://www.learncpp.com/cpp-tutorial/introduction-to-functions/>`_
   - `LearnCpp.com: Function parameters and arguments <https://www.learncpp.com/cpp-tutorial/introduction-to-function-parameters-and-arguments/>`_
   - `LearnCpp.com: Header files <https://www.learncpp.com/cpp-tutorial/header-files/>`_
   - `Include Guards: #pragma once vs Header Guards <https://thamara.dev/posts/pragma-once-vs-header-guards/>`_
