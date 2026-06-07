.. _l8_references:

===================
Lecture 8 References
===================

.. dropdown:: Lecture 8 Summary
   :class-container: sd-border-success

   This lecture covered the fundamentals of Object-Oriented Programming in C++:

   - **Core Principles of OOP**: Encapsulation, abstraction, inheritance, and polymorphism. We discussed the advantages (modularity, reusability, flexibility, maintainability) and disadvantages (learning curve, design overhead, code size, performance overhead) of OOP.

   - **Classes and Objects**: A class is a blueprint that bundles attributes (data) and methods (behavior). An object is a concrete instance of a class with its own state. Each object has its own copy of attributes, but all objects share the same method code.

   - **Design Phase**: Requirement analysis (functional, non-functional, technical constraints, success criteria) and the modeling phase (static structure with UML class diagrams, dynamic behavior with sequence diagrams). We surveyed UML modeling tools.

   - **Implementation Phase**: Project structure best practices (separate ``include/`` and ``src/`` directories). Modern C++ features: ``std::string_view`` for lightweight, non-owning string references, and ``std::optional`` for type-safe representation of values that may not exist.

   - **Encapsulation**: Access specifiers (``public``, ``private``, ``protected``). All attributes must be ``private`` or ``protected``.

   - **Accessors/Mutators**: Getters with ``const``, ``[[nodiscard]]``, and ``noexcept``. Setters with validation and without ``const``.

   - **Constructors**: Default constructors, parameterized constructors, and member initializer lists. Construction order: base class, member attributes (in declaration order), constructor body. Member initializer lists are required for ``const`` and reference members.

   - **const Objects**: Can only call ``const`` methods. Non-``const`` objects can call both ``const`` and non-``const`` methods.

   - **The this Pointer**: Implicit pointer to the current object in non-``static`` methods. Used for disambiguation, method chaining (``return *this``), and returning the current object.

   - **static Members**: ``static`` attributes belong to the class (one shared copy). ``static`` methods have no ``this`` pointer and cannot access non-``static`` members. Useful for counters, shared resources, and utility functions.

.. dropdown:: cppreference Links
   :class-container: sd-border-success

   - `Classes -- cppreference.com <https://en.cppreference.com/w/cpp/language/classes>`_
   - `Constructors and member initializer lists -- cppreference.com <https://en.cppreference.com/w/cpp/language/constructor>`_
   - `Access specifiers -- cppreference.com <https://en.cppreference.com/w/cpp/language/access>`_
   - `static members -- cppreference.com <https://en.cppreference.com/w/cpp/language/static>`_
   - `this pointer -- cppreference.com <https://en.cppreference.com/w/cpp/language/this>`_
   - `const member functions -- cppreference.com <https://en.cppreference.com/w/cpp/language/member_functions>`_
   - `std::string_view -- cppreference.com <https://en.cppreference.com/w/cpp/string/basic_string_view>`_
   - `std::optional -- cppreference.com <https://en.cppreference.com/w/cpp/utility/optional>`_
   - `[[nodiscard]] attribute -- cppreference.com <https://en.cppreference.com/w/cpp/language/attributes/nodiscard>`_

.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   - *A Tour of C++* by Bjarne Stroustrup -- Chapters 5--6 (Classes and Essential Operations)
   - *C++ Primer* by Lippman, Lajoie, and Moo -- Chapter 7 (Classes)
   - *Effective Modern C++* by Scott Meyers -- Items 3, 7, 10 (uniform initialization, member init lists, ``noexcept``)
   - `LearnCpp.com: Introduction to classes <https://www.learncpp.com/cpp-tutorial/introduction-to-object-oriented-programming/>`_
   - `LearnCpp.com: Constructors <https://www.learncpp.com/cpp-tutorial/constructors/>`_
   - `LearnCpp.com: Access specifiers <https://www.learncpp.com/cpp-tutorial/access-specifiers-and-access-functions/>`_
