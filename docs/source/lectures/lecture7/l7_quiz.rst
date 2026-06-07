.. _l7_quiz:

====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 7: Smart Pointers and Move
Semantics. Topics include value categories (lvalues, prvalues, xvalues),
rvalue references, ``std::move``, ``std::unique_ptr`` (exclusive ownership,
methods, move semantics), ``std::shared_ptr`` (reference counting, control
blocks), ``std::weak_ptr`` (non-owning observation, ``lock()``, ``expired()``),
``std::make_unique``, ``std::make_shared``, and RAII.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1--10)
==================================

.. admonition:: Question 1
   :class: hint

   Which value category does the expression ``std::move(x)`` produce, where
   ``x`` is a named variable?

   A. lvalue

   B. prvalue

   C. xvalue

   D. glvalue (but not lvalue or xvalue)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- xvalue

   ``std::move(x)`` performs a ``static_cast<T&&>`` on ``x``, converting the
   lvalue into an xvalue. An xvalue has identity (it still refers to ``x``)
   but can be moved from.


.. admonition:: Question 2
   :class: hint

   What does ``std::move`` actually do at runtime?

   A. It transfers ownership of the object's resources to a new location.

   B. It calls the move constructor of the object.

   C. It performs a ``static_cast`` to an rvalue reference -- no data is moved.

   D. It swaps the contents of two objects.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It performs a ``static_cast`` to an rvalue reference -- no data is moved.

   ``std::move`` does not move anything. It simply casts an lvalue to an
   xvalue (type ``T&&``), which allows the compiler to select move
   constructors or move assignment operators. The actual transfer of
   resources happens in those constructors/operators.


.. admonition:: Question 3
   :class: hint

   Given the following code, what happens at the line marked ``// ???``?

   .. code-block:: cpp

      auto u = std::make_unique<int>(42);
      auto v{u};  // ???

   A. ``v`` is initialized with a copy of ``u``, and both manage the same resource.

   B. Compilation error: ``std::unique_ptr`` is non-copyable.

   C. ``u`` is moved into ``v``, and ``u`` becomes ``nullptr``.

   D. Undefined behavior.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Compilation error: ``std::unique_ptr`` is non-copyable.

   ``std::unique_ptr`` enforces exclusive ownership by deleting its copy
   constructor. To transfer ownership, you must use ``std::move``:
   ``auto v{std::move(u)};``.


.. admonition:: Question 4
   :class: hint

   What is the correct way to initialize a ``std::unique_ptr``?

   A. ``std::unique_ptr<int> u = new int(10);``

   B. ``auto u = std::make_unique<int>(10);``

   C. ``std::unique_ptr<int> u{10};``

   D. ``auto u = std::unique_ptr<int>::create(10);``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``auto u = std::make_unique<int>(10);``

   ``std::make_unique`` is the preferred way to create a ``std::unique_ptr``.
   It is exception-safe and avoids the need to use ``new`` directly
   (C++ Core Guideline R.23).


.. admonition:: Question 5
   :class: hint

   What happens when you call ``release()`` on a ``std::unique_ptr``?

   A. The managed resource is deleted and the pointer is set to ``nullptr``.

   B. The ``unique_ptr`` gives up ownership and returns a raw pointer; the
      caller is responsible for calling ``delete``.

   C. The ``unique_ptr`` is reset to manage a new resource.

   D. The ``unique_ptr`` shares ownership with another smart pointer.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The ``unique_ptr`` gives up ownership and returns a raw pointer;
   the caller is responsible for calling ``delete``.

   After ``release()``, the ``unique_ptr`` is set to ``nullptr`` and no
   longer manages any resource. The returned raw pointer must be explicitly
   deleted to avoid a memory leak.


.. admonition:: Question 6
   :class: hint

   What is a control block in the context of ``std::shared_ptr``?

   A. A compiler-generated structure that tracks all smart pointers in a program.

   B. A heap-allocated data structure that holds reference counts (strong and
      weak), a managed pointer, a deleter, and allocator information.

   C. A stack-allocated structure that stores the managed object.

   D. A thread-local structure that prevents data races on smart pointers.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A heap-allocated data structure that holds reference counts
   (strong and weak), a managed pointer, a deleter, and allocator information.

   The control block is created when the first ``std::shared_ptr`` is
   constructed. All copies of that ``shared_ptr`` share the same control
   block. The managed resource is destroyed when the strong count reaches
   zero, and the control block itself is destroyed when both strong and weak
   counts reach zero.


.. admonition:: Question 7
   :class: hint

   Given the following code, what is the value of ``s2.use_count()`` on the
   last line?

   .. code-block:: cpp

      auto s1 = std::make_shared<int>(10);
      auto s2{s1};
      auto s3 = s2;
      s1.reset();

   A. 1

   B. 2

   C. 3

   D. 0

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 2

   After creation, ``s1``, ``s2``, and ``s3`` all share ownership (strong
   count = 3). When ``s1.reset()`` is called, ``s1`` releases its ownership,
   decrementing the strong count to 2. Both ``s2`` and ``s3`` still share
   ownership of the resource.


.. admonition:: Question 8
   :class: hint

   Which smart pointer should you use to break circular references?

   A. ``std::unique_ptr``

   B. ``std::shared_ptr``

   C. ``std::weak_ptr``

   D. ``std::auto_ptr``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``std::weak_ptr``

   ``std::weak_ptr`` provides non-owning observation of a resource managed
   by ``std::shared_ptr``. It does not increment the strong reference count,
   which breaks circular dependency chains that would otherwise prevent
   resources from being deallocated.


.. admonition:: Question 9
   :class: hint

   What does the ``lock()`` method of ``std::weak_ptr`` return?

   A. A raw pointer to the managed resource.

   B. A ``bool`` indicating whether the resource is still valid.

   C. A ``std::shared_ptr`` that shares ownership if the resource is still
      alive, or an empty ``std::shared_ptr`` if it has expired.

   D. A reference to the managed object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A ``std::shared_ptr`` that shares ownership if the resource is
   still alive, or an empty ``std::shared_ptr`` if it has expired.

   ``lock()`` atomically checks whether the strong count is greater than
   zero. If so, it increments the strong count and returns a new
   ``std::shared_ptr``. If the object has already been destroyed, it returns
   an empty ``std::shared_ptr``.


.. admonition:: Question 10
   :class: hint

   Which expression is an lvalue?

   A. ``42``

   B. ``x + y``

   C. ``std::move(v)``

   D. ``arr[3]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``arr[3]``

   ``arr[3]`` names a specific memory location and has identity -- you can
   take its address with ``&arr[3]``. The literal ``42`` and the expression
   ``x + y`` are prvalues (temporaries). ``std::move(v)`` is an xvalue.


----


True/False (Questions 11--15)
==============================

.. admonition:: Question 11
   :class: hint

   **True or False:** An rvalue reference variable (e.g., ``int&& rref{10 + 20};``)
   is itself an lvalue.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Although ``rref``'s type is ``int&&`` (rvalue reference), the expression
   ``rref`` itself is an lvalue because it has a name, persists across
   statements, and you can take its address.


.. admonition:: Question 12
   :class: hint

   **True or False:** After calling ``std::move(v)`` on a ``std::vector``,
   the vector ``v`` is immediately destroyed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``std::move`` does not destroy the object. It casts ``v`` to an xvalue,
   giving permission to move from it. After a move, ``v`` remains a valid
   object in an unspecified (but typically empty) state. It is not destroyed
   until it goes out of scope.


.. admonition:: Question 13
   :class: hint

   **True or False:** ``std::make_shared`` is preferred over using ``new``
   with ``std::shared_ptr`` because it performs a single allocation for both
   the managed object and the control block.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``std::make_shared`` typically allocates the control block and the managed
   object in a single memory allocation, which is more efficient and
   exception-safe compared to ``std::shared_ptr<T>(new T(...))`` which
   requires two separate allocations (C++ Core Guideline R.22).


.. admonition:: Question 14
   :class: hint

   **True or False:** You can directly dereference a ``std::weak_ptr`` using
   the ``*`` operator to access the managed resource.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``std::weak_ptr`` does not provide ``operator*`` or ``get()``. It is a
   non-owning observer that requires promotion to ``std::shared_ptr`` via
   ``lock()`` before the managed resource can be accessed.


.. admonition:: Question 15
   :class: hint

   **True or False:** When all ``std::shared_ptr`` instances managing a
   resource are destroyed, the control block is also immediately destroyed,
   even if ``std::weak_ptr`` instances still reference it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   When the strong count reaches zero, the managed resource (object) is
   destroyed. However, the control block persists as long as any
   ``std::weak_ptr`` instances reference it (weak count > 0). The control
   block is only destroyed when both the strong count and weak count reach
   zero.
