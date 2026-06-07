====================================================
Lecture
====================================================



Valgrind
========

Valgrind is a powerful memory debugging and profiling tool for Linux. It helps detect memory-related bugs that are otherwise difficult to find.

Installation
------------

.. code-block:: bash

   sudo apt install valgrind

Capabilities
-------------

Valgrind provides several tools for different types of analysis:

- **Memcheck** -- Memory leak detection and memory error detection (the default tool).
- **Callgrind** -- Function call profiling; generates call graphs.
- **Cachegrind** -- Cache and branch prediction profiling.
- **Helgrind** -- Detects synchronization errors in multithreaded programs.
- **DRD** -- Another thread error detector.
- **Massif** -- Heap and stack usage analysis.

Basic Usage
-----------

To run Valgrind on a compiled C++ program:

.. code-block:: bash

   valgrind --leak-check=full ./my_program

CMake Integration
-----------------

You can add a custom CMake target to run Valgrind automatically:

.. code-block:: cmake

   add_custom_target(valgrind
       COMMAND valgrind --leak-check=full --show-leak-kinds=all
               --track-origins=yes $<TARGET_FILE:my_program>
       DEPENDS my_program
       WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
       COMMENT "Running Valgrind on my_program"
   )

Then run it with:

.. code-block:: bash

   cmake --build build --target valgrind

Memory Allocation
=================

C++ programs use three types of memory allocation, each with distinct characteristics and lifetimes.

Static Allocation
-----------------

- Stored in the **data segment** (initialized) or **BSS segment** (uninitialized).
- Used for global variables and variables declared with the ``static`` keyword.
- Memory is allocated at program start and deallocated at program end.

.. code-block:: cpp

   int global_count{0};  // static allocation (data segment)

   void foo() {
       static int call_count{0};  // static allocation, persists across calls
       call_count++;
   }

Automatic Allocation
--------------------

- Stored on the **stack**.
- Used for local variables declared inside functions and blocks.
- Memory is automatically allocated when the variable comes into scope and deallocated when it goes out of scope.

.. code-block:: cpp

   void bar() {
       int x{10};       // automatic allocation on the stack
       double y{3.14};  // automatic allocation on the stack
   }  // x and y are automatically deallocated here

Dynamic Allocation
------------------

- Stored on the **heap** (also called the free store).
- Memory is manually allocated (using ``new``) and manually deallocated (using ``delete``).
- STL containers such as ``std::vector`` and ``std::string`` use heap allocation internally.

.. code-block:: cpp

   void baz() {
       int *p{new int{42}};  // dynamic allocation on the heap
       delete p;              // manual deallocation
       p = nullptr;
   }

Stack vs. Heap
--------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - Stack
     - Heap
   * - Size determined
     - Compile time
     - Runtime
   * - Deallocation
     - Automatic (scope-based)
     - Manual (``delete``)
   * - Speed
     - Fast (pointer adjustment)
     - Slower (allocation bookkeeping)
   * - Size limit
     - Limited (check with ``ulimit -s``)
     - Flexible (limited by system memory)
   * - Data lifetime
     - Destroyed at end of scope
     - Persists until explicitly freed

.. tip::

   You can check the default stack size on your system by running ``ulimit -s`` in the terminal. The value is in kilobytes.

.. figure:: /_static/images/l3/pointer0.pdf
   :align: center

   Stack vs. heap memory layout.

Pointers
========

A **pointer** is a variable that holds a memory address. The address can belong to a variable, a literal, or a function.

Why Learn Pointers?
-------------------

Even though modern C++ favors smart pointers and references, understanding raw pointers is essential because:

- **Memory savings** -- Passing pointers avoids copying large objects.
- **Modify external data** -- Functions can modify variables outside their scope via pointers.
- **Polymorphism** -- Base class pointers enable runtime polymorphism.
- **Dynamic allocation** -- Pointers are required to manage heap memory.
- **ROS 2** -- Uses smart pointers extensively (which are built on raw pointers).
- **Third-party libraries** -- Many libraries use raw pointers in their APIs.

.. figure:: /_static/images/l3/pointer1.pdf
   :align: center

   A pointer stores the address of another variable.

Normal Pointers
---------------

Raw pointers can reference data on the stack or the heap. The pointer variable itself is typically on the stack, but the data it points to can be anywhere.

.. figure:: /_static/images/l3/pointer2.pdf
   :align: center

   A pointer on the stack pointing to data.

Declaration
~~~~~~~~~~~

A pointer is declared using the ``*`` symbol:

.. code-block:: cpp

   type* identifier;

To read a pointer declaration, read **inside-out** (right to left):

- ``int *a;`` -- "``a`` is a pointer to ``int``"
- ``const int *b;`` -- "``b`` is a pointer to ``const int``"

.. warning::

   Be careful when declaring multiple variables on one line:

   .. code-block:: cpp

      int* c, d;  // c is a pointer to int, but d is just a regular int!
      int *e, *f; // both e and f are pointers to int

Initialization
~~~~~~~~~~~~~~

A pointer is initialized using uniform initialization:

.. code-block:: cpp

   type* identifier{value};

Common initial values:

- ``nullptr`` -- Null pointer (points to nothing).
- ``&variable`` -- Address of an existing variable.
- Result of ``new`` -- Address of dynamically allocated memory.

.. warning::

   Always initialize pointers. An uninitialized pointer contains a garbage address and dereferencing it is undefined behavior.

Null Pointer
~~~~~~~~~~~~

A null pointer explicitly points to nothing:

.. code-block:: cpp

   int *p{nullptr};  // preferred (C++11 and later)
   int *q{NULL};     // C-style, avoid in modern C++
   int *r{0};        // works but not recommended
   int *s{};         // zero-initialized, equivalent to nullptr

.. important::

   Always use ``nullptr`` in modern C++. It is type-safe, unlike ``NULL`` or ``0``.

A null pointer is **not** the same as an uninitialized pointer. A null pointer has a well-defined value (``nullptr``), while an uninitialized pointer has an indeterminate value.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int *p{nullptr};

       if (p == nullptr) {
           std::cout << "p is null\n";
       }

       if (!p) {
           std::cout << "p is null (boolean check)\n";
       }

       return 0;
   }

Indirection (Dereference) Operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dereference operator ``*`` retrieves the value stored at the address a pointer holds:

.. code-block:: cpp

   #include <iostream>

   int main() {
       int x{10};
       int *p{&x};  // p holds the address of x

       std::cout << "Address of x: " << &x << '\n';
       std::cout << "Value of p (address): " << p << '\n';
       std::cout << "Dereferenced value: " << *p << '\n';  // prints 10

       *p = 20;  // modify x through the pointer
       std::cout << "x is now: " << x << '\n';  // prints 20

       return 0;
   }

You can also use the dereference operator to modify the value at the address:

.. code-block:: cpp

   #include <iostream>

   int main() {
       int a{5};
       int *ptr{&a};

       std::cout << "Before: a = " << a << '\n';  // 5
       *ptr = 100;
       std::cout << "After:  a = " << a << '\n';  // 100

       return 0;
   }

.. warning::

   The ``*`` symbol has multiple meanings in C++:

   - **Multiplication**: ``int result{a * b};``
   - **Pointer declaration**: ``int *p;``
   - **Dereference**: ``int value{*p};``

   Context determines which meaning applies.

Size of Pointers
~~~~~~~~~~~~~~~~

All pointers have the same size regardless of the type they point to. The size depends on the system architecture (typically 8 bytes on a 64-bit system).

.. code-block:: cpp

   #include <iostream>

   int main() {
       std::cout << "sizeof(int*):    " << sizeof(int*) << '\n';
       std::cout << "sizeof(double*): " << sizeof(double*) << '\n';
       std::cout << "sizeof(float*):  " << sizeof(float*) << '\n';
       std::cout << "sizeof(char*):   " << sizeof(char*) << '\n';

       // All print the same value (e.g., 8 on a 64-bit system)

       return 0;
   }

Typed Pointers
~~~~~~~~~~~~~~

Although all pointers are the same size, the type of a pointer tells the compiler **how to interpret** the data at the address when dereferencing.

The compiler enforces type matching:

.. code-block:: cpp

   double pi{3.14159};
   int *p{&pi};  // ERROR: cannot convert 'double*' to 'int*'

.. figure:: /_static/images/l3/pointer6.pdf
   :align: center

   Pointer type determines how memory at the address is interpreted.

Const-Correctness with Pointers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three modes of const-correctness with pointers:

**1. Pointer to const data** (``const int *p``)

The data pointed to cannot be modified through the pointer, but the pointer itself can be reassigned.

.. code-block:: cpp

   int a{10};
   int b{20};
   const int *p{&a};

   // *p = 50;  // ERROR: cannot modify data through pointer-to-const
   p = &b;      // OK: pointer itself can be reassigned

**2. Const pointer** (``int *const p``)

The pointer cannot be reassigned, but the data it points to can be modified.

.. code-block:: cpp

   int a{10};
   int b{20};
   int *const p{&a};  // must be initialized

   *p = 50;       // OK: can modify data through const pointer
   // p = &b;     // ERROR: cannot reassign a const pointer

**3. Const pointer to const data** (``const int *const p``)

Neither the pointer nor the data it points to can be modified.

.. code-block:: cpp

   int a{10};
   int b{20};
   const int *const p{&a};  // must be initialized

   // *p = 50;   // ERROR: cannot modify data
   // p = &b;    // ERROR: cannot reassign pointer

.. tip::

   Read pointer declarations **right to left** to determine const-correctness:

   - ``const int *p`` -- "``p`` is a pointer to a ``const int``"
   - ``int *const p`` -- "``p`` is a ``const`` pointer to an ``int``"
   - ``const int *const p`` -- "``p`` is a ``const`` pointer to a ``const int``"

Wild Pointers
~~~~~~~~~~~~~

A **wild pointer** is an uninitialized pointer. It contains a garbage address, and dereferencing it is **undefined behavior**.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int *p;           // wild pointer -- contains garbage address
       // std::cout << *p;  // UNDEFINED BEHAVIOR: dereferencing a wild pointer

       return 0;
   }

.. danger::

   Never dereference an uninitialized pointer. Always initialize pointers to ``nullptr`` or a valid address.

Dynamic Memory Allocation
==========================

Dynamic memory allocation allows you to reserve and free memory at runtime. This is essential when the amount of memory needed is not known at compile time.

.. warning::

   In modern C++, prefer **smart pointers** (``std::unique_ptr``, ``std::shared_ptr``) over raw ``new``/``delete``. Raw dynamic allocation is shown here for educational purposes and because understanding it is necessary for working with legacy code.

The ``new`` Operator
--------------------

The ``new`` operator allocates memory on the heap and returns a pointer to it:

.. code-block:: cpp

   int *p{new int{15}};  // allocates an int on the heap, initializes to 15

Key points about dynamically allocated objects:

- They have **no identifier** (no variable name) -- they are accessed only through pointers.
- They **never go out of scope** automatically -- they persist until explicitly deleted.

.. figure:: /_static/images/l3/pointer7.pdf
   :align: center

   The ``new`` operator allocates memory on the heap and returns a pointer.

The ``delete`` Operator
-----------------------

The ``delete`` operator deallocates heap memory that was allocated with ``new``:

.. code-block:: cpp

   int *p{new int{15}};
   // ... use p ...
   delete p;       // deallocates the heap memory
   p = nullptr;    // good practice: avoid dangling pointer

.. figure:: /_static/images/l3/pointer8.pdf
   :align: center

   The ``delete`` operator frees heap memory.

Important details about ``delete``:

- ``delete`` does **not** destroy the pointer variable itself. The pointer variable is destroyed when it goes out of scope (it lives on the stack).
- After ``delete``, the pointer becomes a **dangling pointer** -- it still holds the old address, but the memory at that address has been freed.
- After deleting, either point the pointer elsewhere or set it to ``nullptr``.
- **Deleting a stack resource is undefined behavior**. Only ``delete`` what you ``new``!
- **Deleting** ``nullptr`` **is safe** -- it does nothing (a no-op).

.. code-block:: cpp

   int stack_var{10};
   int *p{&stack_var};
   // delete p;  // UNDEFINED BEHAVIOR: stack_var is on the stack!

   int *q{nullptr};
   delete q;  // safe: does nothing

Common Issues with Dynamic Memory
-----------------------------------

Dangling Pointer
~~~~~~~~~~~~~~~~

A **dangling pointer** points to memory that has already been deallocated. Dereferencing a dangling pointer is **undefined behavior**.

Causes:

- Deleting memory without setting the pointer to ``nullptr``.
- A local variable going out of scope while a pointer still references it.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int *p{new int{42}};
       delete p;
       // p is now dangling -- it still holds the old address

       // std::cout << *p;  // UNDEFINED BEHAVIOR

       p = nullptr;  // fix: set to nullptr after delete

       return 0;
   }

Solutions:

- Set pointers to ``nullptr`` immediately after ``delete``.
- Use **smart pointers** which follow the RAII (Resource Acquisition Is Initialization) pattern.

Memory Leak
~~~~~~~~~~~~

A **memory leak** occurs when dynamically allocated memory is never freed. The memory remains allocated for the lifetime of the program, reducing available memory.

.. code-block:: cpp

   #include <iostream>

   int main() {
       for (int i{0}; i < 1000; ++i) {
           int *p{new int{i}};
           // p goes out of scope without delete -- memory leak!
       }
       // 1000 int-sized blocks are now leaked

       return 0;
   }

.. important::

   Always fix memory leaks. Over time, leaked memory accumulates and can degrade system performance or cause the program to crash.

Double Delete
~~~~~~~~~~~~~

**Double delete** means freeing memory that has already been freed. This is **undefined behavior**.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int *p{new int{10}};
       int *q{p};  // q points to the same memory as p

       delete p;
       p = nullptr;

       // delete q;  // UNDEFINED BEHAVIOR: memory already freed via p

       return 0;
   }

Null Dereferencing
~~~~~~~~~~~~~~~~~~

**Null dereferencing** means dereferencing a pointer that is ``nullptr``. This is **undefined behavior** (typically causes a segmentation fault).

.. code-block:: cpp

   #include <iostream>

   int main() {
       int *p{nullptr};

       // Best practice: check before dereferencing
       if (p) {
           std::cout << *p << '\n';
       } else {
           std::cout << "Pointer is null, cannot dereference\n";
       }

       return 0;
   }

Minimizing Issues
~~~~~~~~~~~~~~~~~

Follow these best practices to minimize pointer-related bugs:

1. **Use Valgrind** to detect memory leaks and invalid memory access.
2. **Set pointers to** ``nullptr`` **after** ``delete``.
3. **Use smart pointers** (``std::unique_ptr``, ``std::shared_ptr``) instead of raw ``new``/``delete``.
4. **Always check** if a pointer is valid before dereferencing.

References
==========

A **reference** is an alias for an existing variable. It provides another name for the same memory location.

.. code-block:: cpp

   type& identifier{existing_variable};

References are commonly used to:

- Pass arguments to functions by reference (avoiding copies).
- Return values from functions by reference.
- Iterate over containers in range-based ``for`` loops.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int x{10};
       int& ref{x};  // ref is an alias for x

       std::cout << "x:   " << x << '\n';    // 10
       std::cout << "ref: " << ref << '\n';   // 10

       ref = 20;
       std::cout << "x after modifying ref: " << x << '\n';  // 20

       return 0;
   }

Characteristics of References
------------------------------

References have five key characteristics:

**1. Must be initialized to an existing variable**

.. code-block:: cpp

   int& ref{};    // ERROR: references must be initialized
   int& ref;      // ERROR: references must be initialized

   int x{5};
   int& ref{x};   // OK

**2. Is an alias -- modifying the reference modifies the original**

.. code-block:: cpp

   int x{10};
   int& ref{x};

   ref = 99;
   std::cout << x << '\n';  // 99

   x = 42;
   std::cout << ref << '\n';  // 42

**3. Has no own identity -- same address as the original**

.. code-block:: cpp

   int x{10};
   int& ref{x};

   std::cout << &x << '\n';    // e.g., 0x7ffd1234
   std::cout << &ref << '\n';  // same: 0x7ffd1234

**4. Cannot be reseated -- bound for life**

.. code-block:: cpp

   int a{10};
   int b{20};
   int& ref{a};  // ref is bound to a

   ref = b;  // this does NOT rebind ref to b
              // it assigns b's value (20) to a

   std::cout << a << '\n';  // 20 (a was modified, not ref rebound)

**5. Cannot be null**

.. code-block:: cpp

   int& ref{nullptr};  // ERROR: cannot bind reference to nullptr

Pointers vs. References
========================

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - Pointer
     - Reference
   * - What it is
     - Variable holding a memory address
     - Alias for an existing variable
   * - Declaration & Init
     - ``int *p{&x};``
     - ``int& ref{x};``
   * - Reassignment
     - Can be reassigned to point elsewhere
     - Cannot be reseated after initialization
   * - Nullability
     - Can be ``nullptr``
     - Cannot be null
   * - Usage
     - Dynamic memory, polymorphism, optional params
     - Function parameters, range-based loops, aliases
   * - Memory
     - Has its own address (occupies memory)
     - Shares address with original variable

.. note::

   Internally, compilers typically implement references using pointers. For example:

   .. code-block:: cpp

      int x{10};
      int& ref{x};        // conceptually equivalent to:
      int* const ptr{&x}; // a const pointer (cannot be reseated)

   The key difference is that references provide a cleaner, safer syntax with automatic dereferencing.
