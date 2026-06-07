.. _l3-references:

===========
References
===========

.. dropdown:: Lecture 3 Summary
   :class-container: sd-border-success

   This lecture covered the fundamentals of pointers and memory management in C++:

   - **Memory Allocation Types**: Static (global/static variables in data/BSS segments), automatic (local variables on the stack), and dynamic (heap memory managed with ``new``/``delete``).
   - **Stack vs. Heap**: Stack allocation is fast and automatic but limited in size. Heap allocation is flexible and persists beyond function scope but requires manual management.
   - **Pointer Basics**: Pointers store memory addresses. They are declared with ``*``, initialized with ``nullptr``, ``&variable``, or the result of ``new``.
   - **Dereference Operator**: ``*p`` accesses the value at the address stored in the pointer. It can also be used to modify the value.
   - **Const-Correctness**: Three modes -- pointer-to-const (``const int *p``), const-pointer (``int *const p``), and const-pointer-to-const (``const int *const p``).
   - **Dynamic Memory**: ``new`` allocates on the heap, ``delete`` frees it. Always ``delete`` what you ``new``.
   - **Common Pitfalls**: Dangling pointers (pointing to freed memory), memory leaks (never freeing memory), double delete (freeing twice), and null dereferencing.
   - **References**: Aliases for existing variables. Must be initialized, cannot be null, cannot be reseated.
   - **Valgrind**: A tool for detecting memory leaks and memory errors. Run with ``valgrind --leak-check=full ./program``.

.. dropdown:: Pointer References
   :class-container: sd-border-success

   - `Pointer declaration (cppreference) <https://en.cppreference.com/w/cpp/language/pointer>`_
   - `new expression (cppreference) <https://en.cppreference.com/w/cpp/language/new>`_
   - `delete expression (cppreference) <https://en.cppreference.com/w/cpp/language/delete>`_
   - `Reference declaration (cppreference) <https://en.cppreference.com/w/cpp/language/reference>`_
   - `nullptr (cppreference) <https://en.cppreference.com/w/cpp/language/nullptr>`_
   - `const qualifier (cppreference) <https://en.cppreference.com/w/cpp/language/cv>`_

.. dropdown:: Valgrind Documentation
   :class-container: sd-border-success

   - `Valgrind Official Documentation <https://valgrind.org/docs/manual/manual.html>`_
   - `Memcheck: a memory error detector <https://valgrind.org/docs/manual/mc-manual.html>`_
   - `Valgrind Quick Start Guide <https://valgrind.org/docs/manual/quick-start.html>`_
   - `Using Valgrind with CMake <https://cmake.org/cmake/help/latest/module/FindValgrind.html>`_

.. dropdown:: C++ Core Guidelines
   :class-container: sd-border-success

   - `R.3: A raw pointer (T*) is non-owning <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r3-a-raw-pointer-t-is-non-owning>`_ -- Raw pointers should not own resources. Use them only to reference data owned by someone else.
   - `R.11: Avoid calling new and delete explicitly <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r11-avoid-calling-new-and-delete-explicitly>`_ -- Prefer smart pointers (``std::unique_ptr``, ``std::shared_ptr``) or containers that manage memory automatically.
   - `R.12: Immediately give the result of an explicit resource allocation to a manager object <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r12-immediately-give-the-result-of-an-explicit-resource-allocation-to-a-manager-object>`_
   - `R.13: Perform at most one explicit resource allocation in a single expression statement <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r13-perform-at-most-one-explicit-resource-allocation-in-a-single-expression-statement>`_
