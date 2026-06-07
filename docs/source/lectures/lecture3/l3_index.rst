.. _l3-index:

====================================
L3: Pointers and Memory Management
====================================

Overview
--------

This lecture covers memory allocation types, raw pointers, references, and dynamic memory management. Students learn to declare, initialize, and use pointers safely, understand const-correctness, and recognize common pitfalls. Valgrind is introduced for memory debugging.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, students will be able to:

   1. Identify and explain the three types of memory allocation: static, automatic, and dynamic.
   2. Declare, initialize, and use raw pointers, including the address-of (``&``) and dereference (``*``) operators.
   3. Apply const-correctness to pointers (pointer-to-const, const-pointer, and const-pointer-to-const).
   4. Allocate and deallocate memory dynamically using ``new`` and ``delete``.
   5. Recognize common pointer pitfalls: dangling pointers, memory leaks, double delete, and null dereferencing.
   6. Distinguish between references and pointers, understanding when to use each.
   7. Use Valgrind to detect memory leaks and memory errors in C++ programs.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 3 Contents

   l3_lecture
   l3_shell
   l3_exercises
   l3_quiz
   l3_references

Next Steps
----------

In **L4: STL Containers**, we will explore the Standard Template Library, covering strings, arrays, vectors, and iterators. These containers leverage dynamic memory management internally, building directly on the concepts introduced in this lecture.
