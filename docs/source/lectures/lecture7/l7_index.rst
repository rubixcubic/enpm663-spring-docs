.. _l7_index:

==========================================
L7: Smart Pointers and Move Semantics
==========================================

Overview
--------

This lecture introduces **move semantics** and **smart pointers** -- two foundational
C++11 features that together eliminate the most common categories of memory
management bugs. We begin with value categories (lvalues, prvalues, xvalues),
rvalue references, and ``std::move``, showing how the compiler distinguishes
objects that must retain ownership from temporaries whose resources can be
safely transferred. With that foundation, we explore the three smart pointer
types provided by ``<memory>``: ``std::unique_ptr`` (exclusive ownership),
``std::shared_ptr`` (shared ownership via reference counting), and
``std::weak_ptr`` (non-owning observation). For each smart pointer, we cover
initialization, internal structure, key methods, ownership transfer, and
idiomatic patterns for passing to and returning from functions.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Understand** move semantics and the differences between *lvalue*, *rvalue*, and *xvalue*.
   2. **Understand** the different types of smart pointers and their use cases.
   3. **Use** ``std::unique_ptr`` to express exclusive ownership with move-only semantics.
   4. **Use** ``std::shared_ptr`` and its reference-counted control block for shared ownership.
   5. **Use** ``std::weak_ptr`` to observe shared resources without affecting their lifetime.
   6. **Apply** idiomatic patterns for passing smart pointers to and returning them from functions.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 7 Contents

   l7_lecture
   l7_shell
   l7_exercises
   l7_quiz
   l7_references

Next Steps
----------

In **Lecture 8: OOP Basics**, we will cover:

- Classes and objects: defining custom types with data members and member functions.
- Access specifiers: ``public``, ``private``, and ``protected``.
- Constructors and destructors: controlling object initialization and cleanup.
- The ``this`` pointer, ``const`` member functions, and ``static`` members.

Before next class, complete the C++ exercises on this page (especially the smart
pointer resource manager challenge) and review the quiz on smart pointers.
