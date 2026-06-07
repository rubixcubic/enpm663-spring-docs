.. _l4_quiz:

================
Lecture 4 Quiz
================

Multiple Choice
----------------

.. admonition:: Question 1
   :class: hint

   Which of the following is **not** a category of STL containers?

   A. Sequence containers
   B. Associative containers
   C. Pointer containers
   D. Unordered associative containers

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Pointer containers**

      The four categories of STL containers are: sequence containers, associative containers, unordered associative containers, and container adapters. There is no category called "pointer containers."

.. admonition:: Question 2
   :class: hint

   What character terminates a C-style string?

   A. ``'\n'``
   B. ``'\t'``
   C. ``'\0'``
   D. ``' '``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. '\\0'**

      C-style strings are null-terminated. The null character ``'\0'`` marks the end of the string. Functions that operate on C-strings rely on finding this terminator.

.. admonition:: Question 3
   :class: hint

   What is Small String Optimization (SSO)?

   A. Compressing strings to use less memory on the heap
   B. Storing short strings inline within the string object instead of allocating heap memory
   C. Using shorter variable names to reduce binary size
   D. Automatically truncating strings that are too long

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Storing short strings inline within the string object instead of allocating heap memory**

      SSO avoids the overhead of heap allocation for short strings (typically fewer than 15--22 characters) by storing the character data directly inside the ``std::string`` object on the stack.

.. admonition:: Question 4
   :class: hint

   What is the difference between ``std::string::operator[]`` and ``std::string::at()``?

   A. ``[]`` is slower because it checks bounds
   B. ``at()`` throws ``std::out_of_range`` on invalid access; ``[]`` causes undefined behavior
   C. They are identical in behavior
   D. ``[]`` works with iterators; ``at()`` does not

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. at() throws std::out_of_range on invalid access; [] causes undefined behavior**

      The subscript operator ``[]`` does not perform bounds checking, so accessing an out-of-bounds index is undefined behavior. The ``.at()`` method performs bounds checking and throws a ``std::out_of_range`` exception if the index is invalid.

.. admonition:: Question 5
   :class: hint

   What must be true about the size of a ``std::array``?

   A. It can be determined at runtime
   B. It must be a compile-time constant
   C. It must be less than 256
   D. It must be a signed integer

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It must be a compile-time constant**

      The size of a ``std::array`` is a template parameter and must be known at compile time. You can use ``constexpr`` variables or literal values, but not runtime variables.

.. admonition:: Question 6
   :class: hint

   What is the primary advantage of ``emplace_back()`` over ``push_back()``?

   A. ``emplace_back()`` is always faster
   B. ``emplace_back()`` can add multiple elements at once
   C. ``emplace_back()`` constructs the element in place, avoiding a temporary object
   D. ``emplace_back()`` does not cause reallocation

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. emplace_back() constructs the element in place, avoiding a temporary object**

      ``emplace_back()`` forwards its arguments to the element's constructor and constructs the object directly in the vector's memory. This avoids creating a temporary object and then copying or moving it, which is what ``push_back()`` does.

.. admonition:: Question 7
   :class: hint

   After calling ``vec.clear()`` on a ``std::vector``, what happens to its capacity?

   A. Capacity is set to 0
   B. Capacity is reduced to half
   C. Capacity remains unchanged
   D. Capacity is undefined

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Capacity remains unchanged**

      ``clear()`` removes all elements and sets the size to 0, but the allocated memory is not released. The capacity remains the same as it was before the call.

.. admonition:: Question 8
   :class: hint

   What does ``std::vector::reserve(n)`` do?

   A. Sets the size of the vector to ``n``
   B. Adds ``n`` default-constructed elements
   C. Pre-allocates memory for at least ``n`` elements without changing the size
   D. Removes elements until the size is ``n``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Pre-allocates memory for at least n elements without changing the size**

      ``reserve(n)`` ensures the vector has capacity for at least ``n`` elements. It does **not** change the size or add any elements. This is useful for avoiding repeated reallocations when you know approximately how many elements you will add.

.. admonition:: Question 9
   :class: hint

   What does ``sizeof(vec)`` return for a ``std::vector<int>`` containing 1000 elements?

   A. 4000 (1000 * sizeof(int))
   B. 4008
   C. The size of the vector object on the stack (typically 24 bytes)
   D. It depends on the capacity

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The size of the vector object on the stack (typically 24 bytes)**

      ``sizeof()`` measures the size of the vector object itself, which is on the stack. This consists of three pointers (start, finish, end_of_storage), so it is typically 24 bytes on a 64-bit system, regardless of how many elements are stored on the heap.

.. admonition:: Question 10
   :class: hint

   Which of the following correctly reads a full line of input including spaces into a ``std::string``?

   A. ``std::cin >> name;``
   B. ``std::getline(std::cin >> std::ws, name);``
   C. ``std::cin.read(name);``
   D. ``std::scanf("%s", name);``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. std::getline(std::cin >> std::ws, name);**

      ``std::cin >>`` stops at the first whitespace character. ``std::getline()`` reads the entire line. Using ``std::cin >> std::ws`` first discards any leading whitespace, including leftover newline characters from previous input operations.

True or False
--------------

.. admonition:: Question 11
   :class: hint

   True or False: A ``std::array`` can change its size after it is created.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      ``std::array`` has a fixed size determined at compile time. It cannot grow or shrink. If you need a dynamic-size container, use ``std::vector``.

.. admonition:: Question 12
   :class: hint

   True or False: The ``end()`` iterator of a container points to the last element.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      The ``end()`` iterator points to **one past** the last element. It is a sentinel that marks the boundary of the container. Dereferencing ``end()`` is undefined behavior.

.. admonition:: Question 13
   :class: hint

   True or False: ``std::vector::pop_back()`` returns the removed element.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      ``pop_back()`` removes the last element but does **not** return it. To retrieve the last element before removing it, use ``.back()`` first, then call ``pop_back()``.

.. admonition:: Question 14
   :class: hint

   True or False: ``std::string::length()`` and ``std::string::size()`` return different values.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      ``length()`` and ``size()`` are identical. Both return the number of characters in the string. ``size()`` exists for consistency with other STL containers, while ``length()`` is more intuitive for strings.

.. admonition:: Question 15
   :class: hint

   True or False: ``std::vector::shrink_to_fit()`` is guaranteed to reduce the capacity to match the size.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      ``shrink_to_fit()`` is a **non-binding request**. The implementation is allowed to ignore it. In practice, most implementations do honor the request, but it is not guaranteed by the standard.
