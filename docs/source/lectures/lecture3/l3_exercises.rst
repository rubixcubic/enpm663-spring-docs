====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 3: Pointers
and Memory Management. Work through them in order, as each exercise
builds on the skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp

   For memory checking, compile with debug symbols and use Valgrind:

   .. code-block:: bash

      g++ -g -std=c++17 -Wall -Wextra -o program program.cpp
      valgrind --leak-check=full ./program


----


.. dropdown:: Exercise 1 -- Pointer Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring pointers, using the address-of operator (``&``),
    and dereferencing pointers (``*``).

    **Specification**

    1. Declare an ``int`` variable ``x`` and initialize it to ``42``.
    2. Declare a pointer ``p`` and initialize it to the address of ``x``.
    3. Print the following:

       - The value of ``x``
       - The address of ``x`` (using ``&x``)
       - The value stored in ``p`` (the address it holds)
       - The dereferenced value of ``p`` (using ``*p``)

    4. Modify ``x`` through the pointer by setting ``*p = 100``.
    5. Print ``x`` again to confirm the change.
    6. Declare a second ``int`` variable ``y{200}`` and reassign ``p``
       to point to ``y``.
    7. Print the dereferenced value of ``p`` to confirm it now points
       to ``y``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               int x{42};
               int *p{&x};

               std::cout << "x = " << x << '\n';
               std::cout << "Address of x: " << &x << '\n';
               std::cout << "Value of p: " << p << '\n';
               std::cout << "*p = " << *p << '\n';

               *p = 100;
               std::cout << "After *p = 100: x = " << x << '\n';

               int y{200};
               p = &y;
               std::cout << "After reassigning p to &y: *p = " << *p << '\n';

               return 0;
           }


.. dropdown:: Exercise 2 -- Const-Correctness
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate all three modes of const-correctness with pointers.

    **Specification**

    1. Declare two ``int`` variables: ``a{10}`` and ``b{20}``.
    2. Create a **pointer to const data**: ``const int *p1{&a};``

       - Try to modify the data through ``p1`` (``*p1 = 50;``). Comment
         out the line and note the error.
       - Reassign ``p1`` to point to ``b``. This should work.

    3. Create a **const pointer**: ``int *const p2{&a};``

       - Modify the data through ``p2`` (``*p2 = 50;``). This should work.
       - Try to reassign ``p2`` to point to ``b``. Comment out the line
         and note the error.

    4. Create a **const pointer to const data**: ``const int *const p3{&a};``

       - Try to modify the data through ``p3``. Comment out and note the error.
       - Try to reassign ``p3``. Comment out and note the error.

    5. For each commented-out line, add a comment explaining **why** it fails.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               int a{10};
               int b{20};

               // Pointer to const data
               const int *p1{&a};
               // *p1 = 50;  // Error: cannot modify data through pointer to const
               p1 = &b;      // OK: can reassign the pointer itself

               // Const pointer
               int *const p2{&a};
               *p2 = 50;     // OK: can modify data
               // p2 = &b;   // Error: cannot reassign a const pointer

               // Const pointer to const data
               const int *const p3{&a};
               // *p3 = 50;  // Error: cannot modify data
               // p3 = &b;   // Error: cannot reassign pointer

               std::cout << "a = " << a << '\n';
               std::cout << "*p1 = " << *p1 << '\n';
               std::cout << "*p2 = " << *p2 << '\n';
               std::cout << "*p3 = " << *p3 << '\n';

               return 0;
           }


.. dropdown:: Exercise 3 -- Dynamic Memory with Valgrind
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use ``new`` and ``delete`` for dynamic memory allocation, then
    verify with Valgrind that there are no leaks.

    **Specification**

    1. Dynamically allocate a single ``int`` with value ``99``:

       .. code-block:: cpp

          int *p{new int{99}};

    2. Print the value and the address.
    3. Deallocate the memory using ``delete`` and set ``p`` to ``nullptr``.
    4. Dynamically allocate an array of 5 ``double`` values:

       .. code-block:: cpp

          double *arr{new double[5]{1.1, 2.2, 3.3, 4.4, 5.5}};

    5. Print all values in the array.
    6. Deallocate the array using ``delete[]`` and set ``arr`` to ``nullptr``.
    7. Compile with debug symbols and run through Valgrind. Verify
       the output says: ``All heap blocks were freed -- no leaks are possible``
    8. **Intentional leak test:** Comment out the ``delete`` statements
       and re-run with Valgrind. Note how many bytes are "definitely lost"
       and which line numbers Valgrind identifies.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               // Single int
               int *p{new int{99}};
               std::cout << "Value: " << *p << '\n';
               std::cout << "Address: " << p << '\n';
               delete p;
               p = nullptr;

               // Array of doubles
               double *arr{new double[5]{1.1, 2.2, 3.3, 4.4, 5.5}};
               for (int i{0}; i < 5; ++i) {
                   std::cout << "arr[" << i << "] = " << arr[i] << '\n';
               }
               delete[] arr;
               arr = nullptr;

               return 0;
           }

        Compile and verify:

        .. code-block:: bash

           g++ -g -std=c++17 -o exercise3 exercise3.cpp
           valgrind --leak-check=full ./exercise3


.. dropdown:: Exercise 4 -- Reference vs. Pointer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Perform the same operations using both a pointer and a reference,
    then compare the behavior.

    **Specification**

    1. Declare an ``int`` variable ``value{50}``.
    2. Create a pointer ``ptr`` to ``value`` and a reference ``ref``
       to ``value``.
    3. Print the "value" they refer to (``*ptr`` and ``ref``) and the
       address they refer to (``ptr`` and ``&ref``).
    4. Modify ``value`` through the pointer (``*ptr = 75``) and print
       all three (``value``, ``*ptr``, ``ref``).
    5. Modify ``value`` through the reference (``ref = 100``) and print
       all three.
    6. Declare a second variable ``other{999}``.

       - Reassign ``ptr`` to point to ``other``.
       - Try to "reassign" ``ref`` to ``other`` (``ref = other``).
         Observe what happens.

    7. Print ``value``, ``*ptr``, ``ref``, and ``other`` to demonstrate
       the difference.

    **Key observation:** When you write ``ref = other``, the reference
    is **not** reseated. Instead, the value of ``other`` is copied into
    ``value`` (the variable ``ref`` is bound to).

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               int value{50};
               int *ptr{&value};
               int &ref{value};

               std::cout << "*ptr = " << *ptr << ", ref = " << ref << '\n';
               std::cout << "ptr = " << ptr << ", &ref = " << &ref << '\n';

               *ptr = 75;
               std::cout << "After *ptr = 75: value=" << value
                         << " *ptr=" << *ptr << " ref=" << ref << '\n';

               ref = 100;
               std::cout << "After ref = 100: value=" << value
                         << " *ptr=" << *ptr << " ref=" << ref << '\n';

               int other{999};
               ptr = &other;
               ref = other;  // copies value, does NOT rebind ref

               std::cout << "value=" << value << " *ptr=" << *ptr
                         << " ref=" << ref << " other=" << other << '\n';
               // value is now 999 (copied), ptr points to other, ref still aliases value

               return 0;
           }


.. dropdown:: Exercise 5 -- Memory Tracing
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Analyze code on paper to trace memory allocation/deallocation and
    identify issues (dangling pointers, memory leaks).

    **Trace the following code:**

    .. code-block:: cpp
       :linenos:

       #include <iostream>

       int main() {
           int *a{new int{10}};
           int *b{new int{20}};
           int *c{a};

           std::cout << "*a = " << *a << '\n';
           std::cout << "*b = " << *b << '\n';
           std::cout << "*c = " << *c << '\n';

           delete a;
           a = nullptr;

           *b = 30;

           std::cout << "*b = " << *b << '\n';

           b = new int{40};

           std::cout << "*b = " << *b << '\n';

           delete b;
           b = nullptr;

           return 0;
       }

    **Tasks**

    1. For each line, state what happens in memory.
    2. After line 6, draw a diagram showing which pointers point where.
    3. After line 12, identify any dangling pointers. Is ``c`` dangling?
    4. After line 19, identify any memory leaks. Has the original ``*b``
       (value 20) been freed?
    5. Identify **all** issues in this code (dangling pointers, memory
       leaks, undefined behavior).
    6. Rewrite the code to fix all issues.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Issues identified:**

        1. **Dangling pointer:** After ``delete a;`` on line 12, ``c``
           still points to the freed memory. ``c`` is dangling.
        2. **Memory leak:** On line 19, ``b`` is reassigned to a new
           allocation without first deleting the old one (value 20).
           The original 20-byte block is leaked.

        **Fixed code:**

        .. code-block:: cpp

           #include <iostream>

           int main() {
               int *a{new int{10}};
               int *b{new int{20}};
               int *c{a};

               std::cout << "*a = " << *a << '\n';
               std::cout << "*b = " << *b << '\n';
               std::cout << "*c = " << *c << '\n';

               delete a;
               a = nullptr;
               c = nullptr;  // Fix: also nullify c (it pointed to same memory)

               *b = 30;
               std::cout << "*b = " << *b << '\n';

               delete b;     // Fix: delete old b before reassigning
               b = new int{40};
               std::cout << "*b = " << *b << '\n';

               delete b;
               b = nullptr;

               return 0;
           }


.. dropdown:: Exercise 6 -- Dynamic Integer Array Manager (Challenge)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a simple dynamic integer array manager using raw pointers.
    This simulates what ``std::vector<int>`` does internally.

    **Specification**

    Write a program that:

    1. **Allocates** a dynamic array of a user-specified size.
    2. **Fills** the array with sequential values (e.g., 10, 20, 30...).
    3. **Prints** all elements of the array.
    4. **Resizes** the array to a new user-specified size:

       - Allocate a new, larger array.
       - Copy existing elements to the new array.
       - Initialize new elements to 0.
       - Delete the old array.
       - Update the pointer to the new array.

    5. **Prints** all elements after resizing.
    6. **Frees** all dynamically allocated memory.
    7. Handle the case where the new size is smaller (truncate).
    8. Compile and run with Valgrind to verify **no memory leaks**.

    **Skeleton:**

    .. code-block:: cpp

       #include <iostream>

       int main() {
           int size{0};
           std::cout << "Enter initial array size: ";
           std::cin >> size;

           // Step 1: Allocate
           int *arr{new int[size]};

           // Step 2: Fill with sequential values
           for (int i{0}; i < size; ++i) {
               arr[i] = (i + 1) * 10;
           }

           // Step 3: Print
           std::cout << "Array contents: ";
           for (int i{0}; i < size; ++i) {
               std::cout << arr[i] << " ";
           }
           std::cout << '\n';

           // Step 4: Resize
           int new_size{0};
           std::cout << "Enter new array size: ";
           std::cin >> new_size;

           // TODO: Implement resize logic

           // Step 5: Print after resize

           // Step 6: Free memory

           return 0;
       }

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               int size{0};
               std::cout << "Enter initial array size: ";
               std::cin >> size;

               int *arr{new int[size]};
               for (int i{0}; i < size; ++i) {
                   arr[i] = (i + 1) * 10;
               }

               std::cout << "Array contents: ";
               for (int i{0}; i < size; ++i) {
                   std::cout << arr[i] << " ";
               }
               std::cout << '\n';

               int new_size{0};
               std::cout << "Enter new array size: ";
               std::cin >> new_size;

               // Resize
               int *new_arr{new int[new_size]{}};  // zero-initialized
               int copy_count{(size < new_size) ? size : new_size};
               for (int i{0}; i < copy_count; ++i) {
                   new_arr[i] = arr[i];
               }
               delete[] arr;
               arr = new_arr;
               size = new_size;

               std::cout << "Resized array: ";
               for (int i{0}; i < size; ++i) {
                   std::cout << arr[i] << " ";
               }
               std::cout << '\n';

               delete[] arr;
               arr = nullptr;

               return 0;
           }

        Verify with Valgrind:

        .. code-block:: bash

           g++ -g -std=c++17 -o array_manager array_manager.cpp
           valgrind --leak-check=full ./array_manager
