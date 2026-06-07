.. _l6_index:

==============================
L6: Functions -- Advanced
==============================

Overview
--------

This lecture builds on the function fundamentals from Lecture 5 and introduces advanced features of C++ functions. We begin with ``struct`` as a lightweight data container and aggregate initialization, then move into templates for writing generic, reusable code. The lecture covers function operators (``decltype``), specifiers (``constexpr``, ``inline``, ``noexcept``), and attributes (``[[nodiscard]]``, ``[[maybe_unused]]``, ``[[deprecated]]``). Finally, we explore callables -- function pointers, functors, lambdas, and ``std::function`` -- which enable flexible, composable designs central to modern C++ programming.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Use struct**: aggregate initialization, structured bindings.
   2. **Write generic code**: function templates, type deduction, specialization.
   3. **Apply type inspection**: ``decltype`` operator.
   4. **Use modern function syntax**: trailing return types with templates.
   5. **Apply function specifiers**: ``constexpr``, ``inline``, ``noexcept``.
   6. **Apply function attributes**: ``[[nodiscard]]``, ``[[maybe_unused]]``, ``[[deprecated]]``.
   7. **Master callables**: function pointers, functors, lambdas, ``std::function``.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 6 Contents

   l6_lecture
   l6_shell
   l6_exercises
   l6_quiz
   l6_references

Next Steps
----------

In **Lecture 7: Smart Pointers**, we will explore modern C++ memory management with ``std::unique_ptr``, ``std::shared_ptr``, and ``std::weak_ptr``. Smart pointers automate resource cleanup through RAII, eliminating common bugs such as memory leaks, double frees, and dangling pointers that arise from manual ``new``/``delete`` usage.
