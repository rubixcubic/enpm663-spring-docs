.. _l4_references:

===================
Lecture 4 References
===================

.. dropdown:: Lecture 4 Summary
   :class-container: sd-border-success

   This lecture covered the Standard Template Library (STL) containers, focusing on three key container types:

   - **Strings**: We compared C-style strings (null-terminated character arrays) with ``std::string``, which provides safe, automatic memory management. Key topics included Small String Optimization (SSO), capacity growth, access and modification methods, iterators, input handling, concatenation, insertion, removal, and memory management with ``reserve()``, ``resize()``, and ``shrink_to_fit()``.

   - **Arrays**: We compared C-style arrays with ``std::array``, which provides bounds-checked access, size awareness, and compatibility with STL algorithms. We covered initialization, pointer decay, compile-time size requirements, access methods, and multidimensional arrays.

   - **Vectors**: We explored ``std::vector`` as a dynamic array with automatic memory management. Key topics included the three-pointer internal structure (start, finish, end_of_storage), initialization, access, insertion (``push_back``, ``emplace_back``, ``insert``, ``emplace``), deletion (``pop_back``, ``erase``, ``clear``), and memory management (``reserve``, ``resize``, ``shrink_to_fit``).

   The common themes across all containers are: safe access with ``.at()`` vs unsafe access with ``[]``, iterator-based traversal, and understanding the relationship between size and capacity.

.. dropdown:: STL References
   :class-container: sd-border-success

   - `std::string -- cppreference.com <https://en.cppreference.com/w/cpp/string/basic_string>`_
   - `std::array -- cppreference.com <https://en.cppreference.com/w/cpp/container/array>`_
   - `std::vector -- cppreference.com <https://en.cppreference.com/w/cpp/container/vector>`_
   - `Iterator library -- cppreference.com <https://en.cppreference.com/w/cpp/iterator>`_
   - `Containers library -- cppreference.com <https://en.cppreference.com/w/cpp/container>`_

.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   - *A Tour of C++* by Bjarne Stroustrup -- Chapter 11 (Containers) and Chapter 12 (Algorithms)
   - *C++ Primer* by Lippman, Lajoie, and Moo -- Chapter 3 (Strings, Vectors, and Arrays) and Chapter 9 (Sequential Containers)
   - *Effective STL* by Scott Meyers -- Items 1--5 on choosing and using containers effectively
   - `LearnCpp.com: std::string <https://www.learncpp.com/cpp-tutorial/introduction-to-stdstring/>`_
   - `LearnCpp.com: std::array <https://www.learncpp.com/cpp-tutorial/stdarray-length-and-indexing/>`_
   - `LearnCpp.com: std::vector <https://www.learncpp.com/cpp-tutorial/introduction-to-stdvector-and-list-constructors/>`_
