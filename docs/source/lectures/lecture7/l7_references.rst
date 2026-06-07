.. _l7_references:

=====================
Lecture 7 References
=====================

.. dropdown:: Lecture 7 Summary
   :class-container: sd-border-success

   This lecture covered **move semantics** and the three **smart pointer** types in modern C++.

   - **Move Semantics**: We explored value categories (lvalues, prvalues, xvalues) and how C++ classifies every expression along two axes: identity and movability. We learned that ``std::move`` does not move anything -- it performs a ``static_cast<T&&>`` to convert an lvalue into an xvalue, giving the compiler permission to invoke move constructors or move assignment operators instead of copies. This enables efficient resource transfer for containers like ``std::vector`` and ``std::string``.

   - **Unique Pointers** (``std::unique_ptr``): We covered exclusive ownership semantics, initialization with ``std::make_unique``, and key methods (``get()``, ``release()``, ``reset()``, ``swap()``). We learned that ``std::unique_ptr`` is non-copyable but movable, and explored sink functions (pass by value to transfer ownership), reseat functions (pass by reference to replace the managed resource), and return-from-function patterns using RVO.

   - **Shared Pointers** (``std::shared_ptr``): We studied shared ownership through reference-counted control blocks containing strong counts, weak counts, a managed pointer, a deleter, and allocator info. We traced the lifecycle of shared pointers through creation, copying, resetting, and destruction. We also covered ``use_count()``, sink and reseat patterns, and returning shared pointers from functions.

   - **Weak Pointers** (``std::weak_ptr``): We learned that weak pointers provide non-owning observation of shared resources. They increment the weak count but not the strong count. Key methods include ``lock()`` (promotes to ``std::shared_ptr`` if the resource is still alive) and ``expired()`` (checks if the managed object has been destroyed). The primary use case is breaking circular references.

.. dropdown:: Smart Pointer References
   :class-container: sd-border-success

   - `std::unique_ptr -- cppreference.com <https://en.cppreference.com/w/cpp/memory/unique_ptr>`_
   - `std::shared_ptr -- cppreference.com <https://en.cppreference.com/w/cpp/memory/shared_ptr>`_
   - `std::weak_ptr -- cppreference.com <https://en.cppreference.com/w/cpp/memory/weak_ptr>`_
   - `std::make_unique -- cppreference.com <https://en.cppreference.com/w/cpp/memory/unique_ptr/make_unique>`_
   - `std::make_shared -- cppreference.com <https://en.cppreference.com/w/cpp/memory/shared_ptr/make_shared>`_
   - `std::move -- cppreference.com <https://en.cppreference.com/w/cpp/utility/move>`_

.. dropdown:: Move Semantics and Value Categories References
   :class-container: sd-border-success

   - `Value categories -- cppreference.com <https://en.cppreference.com/w/cpp/language/value_category>`_
   - `Move constructors -- cppreference.com <https://en.cppreference.com/w/cpp/language/move_constructor>`_
   - `Move assignment operator -- cppreference.com <https://en.cppreference.com/w/cpp/language/move_assignment>`_
   - `Rvalue references -- cppreference.com <https://en.cppreference.com/w/cpp/language/reference>`_

.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   - *A Tour of C++* by Bjarne Stroustrup -- Chapter 5 (Essential Operations), Chapter 13 (Resource Management)
   - *Effective Modern C++* by Scott Meyers -- Items 18--22 (Smart Pointers), Items 23--25 (Move Semantics)
   - `C++ Core Guidelines: Resource Management <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource>`_
   - `LearnCpp.com: Move semantics <https://www.learncpp.com/cpp-tutorial/introduction-to-smart-pointers-move-semantics/>`_
   - `LearnCpp.com: Smart pointers <https://www.learncpp.com/cpp-tutorial/introduction-to-smart-pointers-move-semantics/>`_
