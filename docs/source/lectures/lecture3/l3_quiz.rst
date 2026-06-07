.. _l3-quiz:

=====
Quiz
=====

Multiple Choice
================

.. admonition:: Question 1
   :class: hint

   Which type of memory allocation is used for local variables declared inside a function?

   A. Static allocation
   B. Automatic allocation (stack)
   C. Dynamic allocation (heap)
   D. Register allocation

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Automatic allocation (stack)**

      Local variables are allocated on the stack and automatically deallocated when the function returns (i.e., when the variable goes out of scope).

.. admonition:: Question 2
   :class: hint

   What does the following declaration create?

   .. code-block:: cpp

      int* c, d;

   A. Two pointers to ``int``
   B. A pointer to ``int`` (``c``) and a regular ``int`` (``d``)
   C. Two regular ``int`` variables
   D. A compilation error

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. A pointer to** ``int`` **(** ``c`` **) and a regular** ``int`` **(** ``d`` **)**

      The ``*`` binds to the variable name, not the type. Only ``c`` is a pointer. To make both pointers: ``int *c, *d;``

.. admonition:: Question 3
   :class: hint

   Which of the following correctly initializes a null pointer in modern C++?

   A. ``int *p = NULL;``
   B. ``int *p{0};``
   C. ``int *p{nullptr};``
   D. All of the above work, but C is preferred

   .. dropdown:: Answer
      :class-container: sd-border-success

      **D. All of the above work, but C is preferred**

      All three produce a null pointer, but ``nullptr`` (C++11) is type-safe and preferred in modern C++. ``NULL`` is a C-style macro and ``0`` is ambiguous.

.. admonition:: Question 4
   :class: hint

   What does the dereference operator ``*`` do when applied to a pointer ``p``?

   A. Returns the address stored in ``p``
   B. Returns the value at the address stored in ``p``
   C. Returns the size of the data ``p`` points to
   D. Returns the address of ``p`` itself

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Returns the value at the address stored in** ``p``

      The dereference operator follows the pointer to the memory address it holds and retrieves the value stored there.

.. admonition:: Question 5
   :class: hint

   Given the following code, which statement is true?

   .. code-block:: cpp

      const int *p{&x};

   A. The pointer ``p`` cannot be reassigned
   B. The data pointed to by ``p`` cannot be modified through ``p``
   C. Neither the pointer nor the data can be modified
   D. Both the pointer and the data can be modified

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. The data pointed to by** ``p`` **cannot be modified through** ``p``

      ``const int *p`` means "pointer to const int." The data is const (through this pointer), but the pointer itself can be reassigned to point elsewhere.

.. admonition:: Question 6
   :class: hint

   What happens when you call ``delete`` on a pointer that was not allocated with ``new``?

   A. Nothing -- ``delete`` is a no-op on stack pointers
   B. The stack variable is deallocated immediately
   C. Undefined behavior
   D. A compiler error

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Undefined behavior**

      You must only ``delete`` what you ``new``. Calling ``delete`` on a pointer to a stack variable is undefined behavior and may corrupt the program's memory.

.. admonition:: Question 7
   :class: hint

   Which of the following is a **dangling pointer**?

   A. A pointer set to ``nullptr``
   B. A pointer that has never been initialized
   C. A pointer that points to memory that has been freed
   D. A pointer that points to a local variable in the current scope

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. A pointer that points to memory that has been freed**

      A dangling pointer is one that still holds an address to memory that has been deallocated. Dereferencing it is undefined behavior.

.. admonition:: Question 8
   :class: hint

   What is the result of the following code?

   .. code-block:: cpp

      int *p{new int{42}};
      int *q{p};
      delete p;
      p = nullptr;
      delete q;

   A. Both deletions succeed
   B. Memory leak
   C. Undefined behavior (double delete)
   D. Compilation error

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Undefined behavior (double delete)**

      Both ``p`` and ``q`` point to the same dynamically allocated memory. After ``delete p``, the memory is freed. ``delete q`` attempts to free the same memory again, which is undefined behavior.

.. admonition:: Question 9
   :class: hint

   Which of the following is true about C++ references?

   A. A reference can be reseated to refer to a different variable
   B. A reference can be null
   C. A reference must be initialized when declared
   D. A reference has its own memory address separate from the original variable

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. A reference must be initialized when declared**

      References must be bound to an existing variable at the time of declaration. They cannot be null, cannot be reseated, and share the same address as the original variable.

.. admonition:: Question 10
   :class: hint

   What tool can be used to detect memory leaks in a C++ program on Linux?

   A. ``gdb``
   B. ``valgrind``
   C. ``make``
   D. ``cmake``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.** ``valgrind``

      Valgrind (specifically its Memcheck tool) detects memory leaks, invalid memory accesses, and other memory-related errors. ``gdb`` is a debugger, not a memory checker.

True or False
==============

.. admonition:: Question 11
   :class: hint

   **True or False:** All pointers have the same size regardless of the type they point to.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      On a given system, all pointers are the same size (e.g., 8 bytes on a 64-bit system). The type of the pointer determines how the data at the address is interpreted, not the size of the pointer itself.

.. admonition:: Question 12
   :class: hint

   **True or False:** Calling ``delete`` on a ``nullptr`` causes undefined behavior.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Calling ``delete`` on ``nullptr`` is explicitly defined as a safe no-op in C++. It does nothing.

.. admonition:: Question 13
   :class: hint

   **True or False:** A memory leak occurs when dynamically allocated memory is freed but the pointer is not set to ``nullptr``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      A memory leak occurs when dynamically allocated memory is **never freed** (i.e., ``delete`` is never called). Not setting the pointer to ``nullptr`` after ``delete`` can lead to a dangling pointer, but the memory itself has been freed -- there is no leak.

.. admonition:: Question 14
   :class: hint

   **True or False:** When you write ``ref = other;`` where ``ref`` is a reference bound to variable ``a``, the reference is reseated to refer to ``other``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      References cannot be reseated. The statement ``ref = other;`` assigns the **value** of ``other`` to the variable ``a`` (the variable ``ref`` is bound to). The reference remains bound to ``a``.

.. admonition:: Question 15
   :class: hint

   **True or False:** The stack has a limited size, which can be checked on Linux using the command ``ulimit -s``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      The stack has a limited size (typically 8 MB on Linux). You can check the stack size limit by running ``ulimit -s`` in the terminal, which reports the size in kilobytes.
