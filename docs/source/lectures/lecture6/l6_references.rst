.. _l6_references:

===================
Lecture 6 References
===================

.. dropdown:: Lecture 6 Summary
   :class-container: sd-border-success

   This lecture covered advanced function topics in C++:

   - **struct**: We reviewed ``struct`` as a lightweight data container with public-by-default members, aggregate initialization for direct member initialization without constructors, and structured bindings (C++17) for decomposing struct members into local variables.

   - **Templates**: We explored function templates for writing generic, type-independent code. Key topics included template syntax, instantiation, definition placement (always in headers), documentation with Doxygen, multiple template parameters, explicit template arguments, type deduction rules (with references, const, and deduction failures), and full template specialization for type-specific behavior.

   - **Function Operators, Specifiers, and Attributes**: We covered ``decltype`` for compile-time type inspection (preserving references and const qualifiers), trailing return types for template functions, ``constexpr`` for compile-time evaluation, ``inline`` for ODR compliance, ``noexcept`` for exception guarantees, and attributes ``[[nodiscard]]``, ``[[maybe_unused]]``, and ``[[deprecated]]`` for safer API design.

   - **Callables**: We studied the full spectrum of callable objects -- function pointers (syntax, declaring, calling, callbacks, limitations), functors (stateful function objects with ``operator()``), lambdas (anonymous functions with capture clauses, parameter lists, mutable keyword, and return type deduction), and ``std::function`` (type-erased wrapper for storing any callable with a compatible signature).


.. dropdown:: cppreference Links
   :class-container: sd-border-success

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Function Templates
         :link: https://en.cppreference.com/w/cpp/language/function_template
         :class-card: sd-border-secondary

         **cppreference -- Function Templates**

         Complete reference for function template syntax, instantiation, argument deduction, specialization, and overload resolution.

         +++

         - Template parameter lists
         - Template argument deduction
         - Explicit specialization
         - Overload resolution with templates

      .. grid-item-card:: Lambda Expressions
         :link: https://en.cppreference.com/w/cpp/language/lambda
         :class-card: sd-border-secondary

         **cppreference -- Lambda Expressions**

         Full reference for lambda syntax, capture clauses, parameter lists, mutable lambdas, return type deduction, and generic lambdas.

         +++

         - Capture modes (value, reference, mixed)
         - Mutable keyword
         - Trailing return types
         - Generic lambdas (C++14)

      .. grid-item-card:: std::function
         :link: https://en.cppreference.com/w/cpp/utility/functional/function
         :class-card: sd-border-secondary

         **cppreference -- std::function**

         Reference for the polymorphic function wrapper, including construction, assignment, invocation, and the empty state.

         +++

         - Type erasure mechanism
         - Storing lambdas, functors, function pointers
         - ``std::bad_function_call``
         - Small object optimization

      .. grid-item-card:: decltype Specifier
         :link: https://en.cppreference.com/w/cpp/language/decltype
         :class-card: sd-border-secondary

         **cppreference -- decltype**

         Reference for the ``decltype`` type specifier, including rules for identifiers, lvalue expressions, and prvalue expressions.

         +++

         - Value category rules
         - Parenthesized expressions
         - ``decltype(auto)``

      .. grid-item-card:: Function Attributes
         :link: https://en.cppreference.com/w/cpp/language/attributes
         :class-card: sd-border-secondary

         **cppreference -- Attributes**

         Reference for C++ standard attributes including ``[[nodiscard]]``, ``[[maybe_unused]]``, ``[[deprecated]]``, and others.

         +++

         - ``[[nodiscard]]`` with custom messages
         - ``[[maybe_unused]]`` for parameters and variables
         - ``[[deprecated]]`` with migration guidance

      .. grid-item-card:: constexpr Specifier
         :link: https://en.cppreference.com/w/cpp/language/constexpr
         :class-card: sd-border-secondary

         **cppreference -- constexpr**

         Reference for ``constexpr`` variables, functions, and constructors, including requirements and relaxations across C++ standards.

         +++

         - Compile-time vs runtime evaluation
         - C++14/C++17 relaxations
         - ``constexpr`` vs ``const``


.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   - *A Tour of C++* by Bjarne Stroustrup -- Chapter 7 (Templates) and Chapter 15 (Function Objects)
   - *C++ Primer* by Lippman, Lajoie, and Moo -- Chapter 16 (Templates and Generic Programming) and Chapter 10 (Generic Algorithms / Lambdas)
   - *Effective Modern C++* by Scott Meyers -- Items 1--4 (deduction), Item 31 (lambdas), Item 34 (``std::function``)
   - `LearnCpp.com: Function Templates <https://www.learncpp.com/cpp-tutorial/function-templates/>`_
   - `LearnCpp.com: Lambda Expressions <https://www.learncpp.com/cpp-tutorial/introduction-to-lambdas-anonymous-functions/>`_
   - `LearnCpp.com: std::function <https://www.learncpp.com/cpp-tutorial/introduction-to-stdfunction/>`_
