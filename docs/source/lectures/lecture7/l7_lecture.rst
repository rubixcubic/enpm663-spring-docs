====================================================
Lecture
====================================================



Move Semantics
==============

Introduced in C++11, **move semantics** revolutionized resource management by
distinguishing between **objects that must retain ownership** and **temporary
objects whose resources can be safely transferred**. This capability enables
highly efficient handling of dynamically allocated memory and other system
resources while preserving the safety and predictability of automatic resource
management.

Why Move Semantics?
-------------------

Consider the following code that copies a large vector:

.. code-block:: cpp

   int main() {
       std::vector<std::vector<int>> matrix;

       // Create a large vector representing a row of sensor data
       std::vector<int> row(1'000'000);
       for (int i{0}; i < 1'000'000; i++) {
           row[i] = i;
       }

       // Copy this row to our matrix
       matrix.push_back(row);  // This COPIES all 1 million integers!
   }

**Problem:** When we call ``push_back(row)``, it copies all 1 million integers.
But what if we are done with ``row`` and won't use it again? Why waste time and
memory copying when we could just *move* the data?

Here is what we really want:

.. code-block:: cpp
   :emphasize-lines: 10

   int main() {
       std::vector<std::vector<int>> matrix;

       // Create a large vector representing a row of sensor data
       std::vector<int> row(1'000'000);
       for (int i{0}; i < 1'000'000; i++) {
           row[i] = i;
       }

       // Move this row to our matrix
       matrix.push_back(std::move(row));  // Move row into matrix
   }

**Result:** No copying! The internal buffer is transferred from ``row`` to
``matrix[0]`` (``row`` becomes empty). *This is what move semantics enables.*


Understanding Value Categories
------------------------------

To understand move semantics, we first need to understand how C++ categorizes
expressions. C++ classifies every expression along two independent axes:

1. **Has identity?** (Does it occupy a specific memory location?)
2. **Can we move from it?** (Is it safe to steal its resources?)

This gives us three primary categories:

.. list-table::
   :widths: 20 15 15 50
   :header-rows: 1

   * - Category
     - Has Identity?
     - Can Move From?
     - Common Name
   * - **lvalue**
     - Yes
     - No
     - Named objects
   * - **prvalue**
     - No
     - Yes
     - Temporaries
   * - **xvalue**
     - Yes
     - Yes
     - Expiring values


lvalues: Named Objects with Identity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An **lvalue** refers to an object that has a persistent identity. It occupies a
specific location in memory and persists beyond a single expression.

.. code-block:: cpp

   int main() {
       int x{5};                    // x is an lvalue
       int* ptr{&x};                // Can take address -- proof it has identity
       std::vector<int> vec{1,2,3}; // vec is an lvalue

       int arr[10];
       arr[3] = 42;                 // arr[3] is an lvalue -- names a location
   }

**Key Properties:**

- Has a name (usually)
- Persists across multiple statements
- You can take its address with ``&``
- Cannot move from it without explicit permission


prvalues: Pure Temporary Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **prvalue** is a temporary value without identity.

.. code-block:: cpp

   int main() {
       int x{10 + 20};  // "10 + 20" is a prvalue
       int y{x + 5};    // "x + 5" is a prvalue

       42;       // Literal -- prvalue
       3.14159;  // Literal -- prvalue
       true;     // Literal -- prvalue

       std::vector<int>{1, 2, 3};  // Temporary object -- prvalue
       x + y;
   }

**Key Properties:**

- No identity (doesn't occupy addressable memory yet)
- Temporary (about to disappear)
- Cannot take its address
- Can move from it -- it's going away anyway!


xvalues: Expiring Values
^^^^^^^^^^^^^^^^^^^^^^^^^^

An **xvalue** (expiring value) represents an object that has identity but whose
resources can be moved because we have explicitly marked it as "expiring".

.. code-block:: cpp

   int main() {
       std::vector<int> vec{1, 2, 3};  // vec is an lvalue
       std::move(vec);                 // std::move(vec) is an xvalue
   }

**Key Properties:**

- Has identity
- Can move from it (unlike lvalues)
- Represents objects whose lifetime is ending ("expiring")
- Created primarily by ``std::move``

**Why do we need xvalues?** xvalues let us move from named objects when we
explicitly say it's okay.


Value Category Hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^

The complete value category hierarchy:

.. code-block:: text

                  expression
                 /          \
           glvalue          rvalue
          (has identity)    (can move from)
          /       \         /       \
       lvalue    xvalue   xvalue   prvalue

- expression = glvalue |  rvalue
- glvalue = lvalue | xvalue
- rvalue = prvalue | xvalue
- xvalue = glvalue & rvalue
- expression = lvalue | xvalue | prvalue


rvalue References
-----------------

An **rvalue reference** is a reference that can bind to rvalues (prvalues or xvalues).

**Binding to an rvalue:** When an rvalue reference binds to a prvalue, the
temporary is *materialized* (given storage), and its lifetime is extended:

.. code-block:: cpp

   // not realistic example: demonstration purpose only
   int&& rref{10 + 20};    // The result of 10+20 is stored in memory
                            // and lives as long as rref exists
   rref = 100;             // We can even modify it!
   std::cout << rref << '\n';  // Output: 100

Think of it as "giving a name" to a temporary object.

.. admonition:: Question
   :class: hint

   Is ``rref`` an lvalue, prvalue, or xvalue?

.. dropdown:: Answer
   :class-container: sd-border-success

   ``rref`` is an **lvalue**. Even though its type is ``int&&`` (rvalue reference),
   the expression ``rref`` itself is an lvalue because it has a name and
   you can take its address.

**rvalue reference variables are lvalues!**

.. code-block:: cpp

   int main() {
       int&& rref{10 + 20};
       // rref is an lvalue even though its type is int&&
       static_assert(std::is_lvalue_reference_v<decltype((rref))>);
       std::cout << "rref is an lvalue reference: "
                 << std::boolalpha
                 << std::is_lvalue_reference_v<decltype((rref))> << '\n';
   }

.. admonition:: Key Distinction
   :class: note

   - ``rref``'s **type** --> ``int&&`` (rvalue reference)
   - ``rref``'s **value category** --> lvalue (has a name and can take its address)
   - The expression ``10 + 20`` --> prvalue (temporary)

   The binding is legal because rvalue references can bind to rvalues.


std::move and xvalues
---------------------

``std::move`` does not move anything by itself. It simply performs a
``static_cast<T&&>`` to turn an lvalue into an xvalue (type is ``T&&``).

**Purpose:** It tells the compiler that the object is *safe to treat as expiring*
and can therefore be *moved from* rather than copied.

.. code-block:: cpp

   std::string s1{"hello"};
   std::string s2 = std::move(s1);  // Cast lvalue -> xvalue
                                    // Move constructor for s2 is called

**After the move:**

- ``s2`` takes ownership of ``s1``'s resources.
- ``s1`` remains valid but empty (its state is unspecified).
- No new object is created -- only a different way of treating ``s1``.


std::move in Detail
^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :emphasize-lines: 4

   template <typename T>
   constexpr typename std::remove_reference<T>::type&&
   move(T&& arg) noexcept {
       return static_cast<typename std::remove_reference<T>::type&&>(arg);
   }

**Key Points:**

- Performs a ``static_cast<T&&>`` -- no data is moved.
- Converts an lvalue into an xvalue.
- Used to enable **move constructors** or **move assignment operators**.
- The result has **type** ``T&&`` and **value category** xvalue.

.. admonition:: Note
   :class: note

   All standard STL containers (such as ``std::vector``, ``std::string``,
   ``std::map``, and others) implement efficient move constructors that
   transfer ownership of their internal resources -- like dynamically
   allocated memory -- rather than copying them.

The following example shows a simplified move constructor for a vector class:

.. code-block:: cpp
   :emphasize-lines: 10-19

   template<typename T>
   class vector {
   private:
       T* data_;           // Pointer to the heap-allocated array
       size_t size_;       // Number of elements
       size_t capacity_;   // Allocated capacity

   public:
       // Move constructor
       vector(vector&& other) noexcept
           : data_{other.data_},
             size_{other.size_},
             capacity_{other.capacity_}
       {
           // Leave 'other' in a valid empty state
           other.data_ = nullptr;
           other.size_ = 0;
           other.capacity_ = 0;
       }

       // For comparison, here's the copy constructor
       vector(const vector& other)
           : data_{new T[other.capacity_]},
             size_{other.size_},
             capacity_{other.capacity_}
       {
           // Deep copy: copy all elements
           for (size_t i{0}; i < size_; ++i) {
               data_[i] = other.data_[i];
           }
       }
   };

When the move constructor is used:

.. code-block:: cpp

   int main(){
       std::vector<int> v1{1,2,3};
       std::vector<int> v2{std::move(v1)};
   }

The move constructor is called, which transfers ``v1``'s internal pointers to
``v2`` and leaves ``v1`` in a valid empty state -- no element-by-element copy
occurs.


Move Semantics Summary
-----------------------

The purpose of ``std::move`` is not to create a new object, but to change
**how the compiler treats the existing one.**

- Normally, a named object (lvalue) can only be copied.
- Using ``std::move`` changes its value category to xvalue (type ``T&&``),
  allowing *move constructors* or *move assignment operators* to be called.
- This avoids unnecessary deep copies of resources such as memory buffers,
  file handles, and sockets.

.. code-block:: cpp

   std::vector<int> v1{1, 2, 3};
   std::vector<int> v2{v1};            // Copy (expensive)
   std::vector<int> v3{std::move(v1)}; // Move (cheap!)

*"We don't move data with std::move; we give permission to move"*


Lifetime and Expiration Summary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 18 18 39
   :header-rows: 1

   * - Expression
     - Value Category
     - Type
     - Lifetime Behavior
   * - ``10 + 20``
     - prvalue
     - ``int``
     - Temporary (no identity)
   * - ``int&& r = 10 + 20;``
     - binds prvalue to rvalue ref
     - ``int&&``
     - Materialized, lifetime extended
   * - ``s1``
     - lvalue
     - ``std::string``
     - Persistent, has identity
   * - ``std::move(s1)``
     - xvalue
     - ``std::string&&``
     - Same object, now expiring

Binding a prvalue **extends lifetime**; using ``std::move`` **marks it as
expiring**.


Smart Pointers
==============

A smart pointer (from ``<memory>``) is a class that wraps a raw pointer (also
called **stored pointer**) to manage the lifetime of the resource being pointed
to.

Smart pointers are designed to manage dynamic memory allocation on the heap,
ensuring that resources are properly released when they are no longer needed.
They store a normal pointer to the allocated memory and automatically call the
appropriate cleanup function (typically ``delete``) when the object is destroyed
or goes out of scope.

Types of Smart Pointers
-----------------------

C++ provides three distinct smart pointer types, each designed to abstract raw
pointer management while clearly expressing ownership semantics and programmer
intent.

- ``std::unique_ptr`` -- **Exclusive ownership**: single object controls the resource lifetime.
- ``std::shared_ptr`` -- **Shared ownership**: multiple objects collectively manage the resource.
- ``std::weak_ptr`` -- **Non-owning observer**: monitors resource state without affecting lifetime, prevents circular dependencies.


Unique Pointers
===============

A ``std::unique_ptr`` (from ``<memory>``) implements **exclusive ownership**
semantics for dynamically allocated resources. This exclusivity guarantees that
exactly one ``std::unique_ptr`` instance controls any given memory location at
any time.

- **Automatic Resource Management** -- The ``std::unique_ptr`` owns its resource
  and automatically invokes ``delete`` when the pointer is destroyed, reassigned,
  or goes out of scope, ensuring deterministic cleanup.
- **Move-Only Semantics** -- ``std::unique_ptr`` is *non-copyable* but *movable*,
  enforcing single ownership through the type system and preventing accidental
  resource sharing.


Initialization
--------------

.. code-block:: cpp

   std::unique_ptr<T> identifier = std::make_unique<T>(args...);
   auto identifier = std::make_unique<T>(args...);

- ``T`` -- Type of the managed object allocated on the heap.
- ``identifier`` -- Variable name for the unique pointer instance.
- ``args...`` -- Constructor arguments passed to the managed object.

.. admonition:: C++ Core Guideline
   :class: tip

   `R.23: Use make_unique() to make unique_ptrs <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-make_unique>`_


Discouraged Approaches
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<T> identifier(new T(args...));
   std::unique_ptr<T> identifier = std::unique_ptr<T>(new T(args...));
   auto identifier = std::unique_ptr<T>(new T(args...));
   std::unique_ptr<T> identifier(raw_ptr);

**Why discouraged?**

- Using ``new`` directly inside larger expressions can leak if another
  subexpression throws after ``new`` succeeds but before the ``unique_ptr`` is
  constructed.
- ``std::unique_ptr<T>(raw_ptr)`` "adopts" a raw pointer. If that raw pointer
  is also owned/freed elsewhere, you risk double ``delete`` or use-after-free.
- Repeating ``T`` and spelling ``new`` adds noise and invites mistakes.


Example
^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<int> u = std::make_unique<int>(10);

.. figure:: /_static/images/l7/unique_ptr_structure.png
   :alt: Structure of a std::unique_ptr
   :align: center
   :width: 60%

   Internal structure of a ``std::unique_ptr``.

- ``_M_ptr``: Raw pointer to the managed object.
- ``_M_deleter``: Callable used to destroy the object.


Exclusive Ownership
-------------------

A ``std::unique_ptr`` *exclusively* manages the lifetime of a resource.

.. code-block:: cpp

   std::unique_ptr<int> u = std::make_unique<int>(10);
   std::unique_ptr<int> v{u}; // Error: copy constructor is deleted

.. code-block:: cpp
   :linenos:

   int main(){
       {
           // Create managed resource on heap
           auto u = std::make_unique<int>(10);
           std::cout << *u << '\n';  // Output: 10 (dereference to access value)
           *u = 20;                  // modify the managed resource
           std::cout << *u << '\n';  // Output: 20
           //std::cout << u << '\n';   // Error: no operator<< for unique_ptr
       } // u destructor automatically calls delete on managed resource
   }

Line 8 will fail to compile because ``std::unique_ptr`` does not provide an
``operator<<`` overload. The smart pointer wrapper cannot be directly streamed.
A solution for accessing the raw pointer is demonstrated in the ``get()``
section below.


Methods
-------

``std::unique_ptr`` provides a comprehensive set of
`member functions <https://en.cppreference.com/w/cpp/memory/unique_ptr>`_ for
resource management and inspection. Many of these methods share consistent
interfaces with ``std::shared_ptr`` and ``std::weak_ptr``, facilitating code
maintainability across different smart pointer types.


get()
^^^^^^

The ``get()`` method returns a raw pointer to the managed resource without
transferring ownership or modifying the ``std::unique_ptr`` state.

- The raw pointer returned by ``get()`` is a **copy** of the managed pointer
  and must be used only for **non-owning observation**.

  - **Null checking**: verify whether the ``std::unique_ptr`` currently manages a valid resource.
  - **Address inspection**: retrieve the address of the managed object for diagnostic or logging purposes.
  - **Read-only access**: dereference the pointer to inspect the object without assuming ownership or modifying lifetime.

.. warning::

   Never call ``delete`` on the returned raw pointer. The ``std::unique_ptr``
   retains ownership and will automatically ``delete`` the resource upon
   destruction, resulting in **double-delete undefined behavior**.

.. code-block:: cpp

   // Create managed resource on heap
   auto u = std::make_unique<int>(10);
   if (u) { // check if u!=nullptr
       std::cout << "Value at " << u.get() << " is " << *u << '\n';
   }

or

.. code-block:: cpp

   // Create managed resource on heap
   auto u = std::make_unique<int>(10);
   int* raw_ptr{u.get()}; // get a copy of the raw pointer for observation
   if (raw_ptr) { // check if raw_ptr!=nullptr
       std::cout << "Value at " << raw_ptr << " is " << *raw_ptr << '\n';
   }


release()
^^^^^^^^^^

The ``release()`` method transfers ownership of the managed resource from the
``std::unique_ptr`` to the caller without destroying the resource.

- The ``std::unique_ptr`` relinquishes ownership of the managed resource.
- Returns a raw pointer to the previously managed resource.
- The ``std::unique_ptr`` is reset to ``nullptr`` and no longer manages any resource.

.. warning::

   After calling ``release()``, *manual memory management becomes your
   responsibility*. The returned raw pointer must be explicitly deleted using
   ``delete`` when no longer needed, or **memory leaks** will occur.

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 1, 2, 8

   auto u = std::make_unique<int>(10);
   auto ptr = u.release(); // transfer ownership to ptr

   std::cout << *ptr << '\n'; // Output: 10
   assert(u.get() == nullptr); // u no longer owns the resource
   assert(u == nullptr); // implicit bool conversion check

   delete ptr; // Mandatory: prevent memory leak

.. figure:: /_static/images/l7/unique_ptr_release.png
   :alt: unique_ptr release operation
   :align: center
   :width: 80%

   Result of calling ``release()`` on a ``std::unique_ptr``.

**Memory Leak Example:**

The following code introduces a *memory leak*:

.. code-block:: cpp

   auto u = std::make_unique<int>(10);
   u.release();  // Raw pointer returned but never stored or deleted!

**When to Use release()?**

Use ``release()`` when transferring ownership from a ``std::unique_ptr`` to
legacy code, C-style APIs, or systems that require raw pointer management.

.. code-block:: cpp

   void legacy_function(int* ptr) {
       if (ptr) {
           std::cout << "Processing: " << *ptr << '\n';
           delete ptr; // Legacy code handles cleanup
       }
   }

   int main() {
       auto u = std::make_unique<int>(42);
       // Transfer ownership to raw pointer for legacy interface
       int* ptr{u.release()};
       // Verify ownership transfer
       assert(u == nullptr); // u no longer owns resource
       // Pass to legacy system that expects raw pointer ownership
       legacy_function(ptr); // ptr now responsible for deletion
   }

Transferring ownership to another ``std::unique_ptr`` (move semantics is
preferred):

.. code-block:: cpp

   auto u1 = std::make_unique<int>(10);
   int* ptr{u1.release()};
   std::unique_ptr<int> u2(ptr); // u2 assumes ownership
   assert(u1 == nullptr);

- ``u2`` takes ownership of the resource pointed to by ``ptr``.
- ``ptr`` continues pointing to the resource but no longer manages its lifetime.
- If ``u2`` is destroyed or reset, the resource is deleted and ``ptr`` becomes
  a dangling pointer.

.. admonition:: Best Practice
   :class: tip

   Use *move semantics* instead of ``release()`` for ownership transfer between
   smart pointers.


reset()
^^^^^^^^

The ``reset()`` method provides controlled resource replacement with automatic
cleanup of the previously managed resource.

- Cleans up the currently managed resource (if any) by calling ``delete``.
- Optionally assumes ownership of a new dynamically allocated resource.
- Sets the ``std::unique_ptr`` to ``nullptr`` if no new resource is provided.

Calling ``reset()`` without arguments cleans up (calls ``delete``) the currently
managed resource and resets the ``std::unique_ptr`` to ``nullptr``.

.. code-block:: cpp
   :linenos:

   auto u = std::make_unique<int>(10);
   u.reset(); // cleans up managed resource, set to nullptr
   assert(u.get() == nullptr); // verification: u is now null

.. figure:: /_static/images/l7/fig_uniqueptr_reset.png
   :alt: unique_ptr reset without argument
   :align: center
   :width: 60%

   Result of calling ``reset()`` without arguments.

When ``reset()`` receives a pointer argument, it first cleans up the currently
managed resource (calls ``delete``), then assumes ownership of the new resource
in a single atomic operation.

.. code-block:: cpp
   :linenos:

   auto u = std::make_unique<int>(10);
   u.reset(new int(20)); // clean up old resource, manage new one

.. figure:: /_static/images/l7/fig_uniqueptr_reset2.png
   :alt: unique_ptr reset with argument
   :align: center
   :width: 60%

   Result of calling ``reset()`` with a new pointer.


swap()
^^^^^^^

The ``swap()`` method exchanges ownership of managed resources between two
``std::unique_ptr`` instances. Each pointer assumes control of the resource
previously managed by the other.

Swapping ``std::unique_ptr`` instances is an **O(1)** constant-time operation
that only exchanges *internal pointer values* (no resource copying, moving, or
reallocation occurs).

.. code-block:: cpp
   :linenos:

   auto u = std::make_unique<int>(10);
   auto v = std::make_unique<int>(20);
   u.swap(v);

.. figure:: /_static/images/l7/fig_uniqueptr_swap.png
   :alt: unique_ptr swap operation
   :align: center
   :width: 80%

   Result of swapping two ``std::unique_ptr`` instances.


Move Semantics with unique_ptr
-------------------------------

The compiler automatically applies move semantics in many contexts. For explicit
control, use ``std::move()`` to force move operations when the compiler cannot
deduce the intent.

.. admonition:: C++ Standard
   :class: note

   **S 23.11.1** -- After move-transferring ownership from ``source_ptr`` to
   ``dest_ptr``, the source pointer is guaranteed to be in a valid but
   unspecified state (typically ``nullptr``).

**Passing by value without std::move (Error):**

.. code-block:: cpp
   :linenos:

   void display(std::unique_ptr<int> v){
       // Implicit: std::unique_ptr<int> v{u};
       std::cout << *v << '\n';
   }

   int main(){
       auto u = std::make_unique<int>(10);
       display(u);  // Error: cannot copy unique_ptr
   }

**Transferring Ownership: The Correct Way:**

.. code-block:: cpp
   :linenos:

   void display(std::unique_ptr<int> v){
       // Implicit: std::unique_ptr<int> v{std::move(u)};
       std::cout << *v << '\n'; // 10
   } // v is destroyed here, resource is deleted

   int main(){
       auto u = std::make_unique<int>(10);
       display(std::move(u)); // Transfer ownership to function
       // u is now nullptr -- ownership transferred
   }

.. figure:: /_static/images/l7/fig_uniqueptr_move.png
   :alt: unique_ptr move to function
   :align: center
   :width: 80%

   Ownership transfer via ``std::move`` to a function parameter.

**Move constructor example:**

.. code-block:: cpp
   :linenos:

   // Create managed resource on heap
   auto u = std::make_unique<int>(10);
   std::cout << "u: " << u.get() << '\n';  // @1

   // Transfer ownership using move constructor
   auto v{std::move(u)}; // u transfers ownership to v
   std::cout << "v: " << v.get() << '\n'; // @1 (same address)
   assert(u == nullptr);  // u is now empty

   // u can be reused for new resource management
   u.reset(new int{20});
   std::cout << u.get() << '\n';  // @2 (different address)

.. figure:: /_static/images/l7/fig_uniqueptr_move2.png
   :alt: unique_ptr move between variables
   :align: center
   :width: 80%

   Ownership transfer between ``std::unique_ptr`` instances.


Pass to Functions: Sink
------------------------

A **sink function** accepts ownership of a resource, typically through move
semantics. The function becomes responsible for the resource's lifetime and
cleanup.

.. code-block:: cpp

   void process_widget(std::unique_ptr<Widget> widget_ptr);
   // Caller transfers ownership: process_widget(std::move(my_widget));

.. admonition:: C++ Core Guideline
   :class: tip

   `R.32: Take a unique_ptr<widget> parameter to express that a function assumes ownership of a widget <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r32-take-a-unique_ptrwidget-parameter-to-express-that-a-function-assumes-ownership-of-a-widget>`_


Pass to Functions: Reseat
--------------------------

A **reseat function** modifies a smart pointer to manage a different resource.
The function may destroy the current resource and assign a new one, or simply
replace the managed object.

.. code-block:: cpp

   void configure_widget(std::unique_ptr<Widget>& widget_ptr);
   // Function may call: widget_ptr.reset(new EnhancedWidget());

.. admonition:: C++ Core Guideline
   :class: tip

   `R.33: Take a unique_ptr<widget>& parameter to express that a function reseats the widget <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r33-take-a-unique_ptrwidget-parameter-to-express-that-a-function-reseats-the-widget>`_

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 1, 2, 3, 6, 9

   void reseat_unique(std::unique_ptr<int>& v) { // Pass by reference to modify original
       v.reset(new int(20)); // Destroy current resource, create new one
   }

   int main(){
       auto u = std::make_unique<int>(10); // Create managed resource
       std::cout << "*u: " << *u << '\n';        // 10
       std::cout << "u: " << u.get() << '\n';    // @1
       reseat_unique(u); // u will be modified to point to new resource
       std::cout << "*u: " << *u << '\n';        // 20
       std::cout << "u: " << u.get() << '\n';    // @2
   }

.. figure:: /_static/images/l7/fig_uniqueptr_reseat.png
   :alt: unique_ptr reseat operation
   :align: center
   :width: 80%

   Reseat operation: modifying a ``std::unique_ptr`` through a reference parameter.


Return from Functions
----------------------

.. admonition:: C++ Core Guideline
   :class: tip

   `F.26: Use a unique_ptr<T> to transfer ownership where a pointer is needed <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f26-use-a-unique_ptrt-to-transfer-ownership-where-a-pointer-is-needed>`_

.. code-block:: cpp

   std::unique_ptr<int> create_resource() {
       auto v = std::make_unique<int>(10);
       std::cout << *v << '\n';     // 10
       std::cout << &v << '\n';     // @1 (address of local variable)
       return v; // Ownership transferred to caller
   }
   int main(){
       auto u{create_resource()};
       std::cout << *u << '\n';       // 10
       std::cout << &u << '\n';       // @1 (same address due to optimization)
   }

.. admonition:: Question
   :class: hint

   Which compiler optimization technique is being used here?

.. dropdown:: Answer
   :class-container: sd-border-success

   **Return Value Optimization (RVO)** -- The compiler constructs the return
   value directly in the caller's memory, eliminating the need for a move
   or copy.


Shared Pointers
===============

A ``std::shared_ptr`` (from ``<memory>``) implements shared ownership semantics,
allowing multiple smart pointers to collectively manage a single resource through
a **reference-counted control block**.

- Resource acquisition occurs during ``std::shared_ptr`` construction.
- Multiple ``std::shared_ptr`` instances can share ownership by copying from an
  existing instance.
- The resource remains valid while *at least one ``std::shared_ptr`` maintains
  ownership*.
- Automatic resource deallocation occurs when the reference count reaches zero:

  - The last ``std::shared_ptr`` is reassigned to manage a different resource.
  - The last ``std::shared_ptr`` is destroyed (scope exit).
  - The last ``std::shared_ptr`` is explicitly reset via ``reset()``.

.. figure:: /_static/images/l7/fig_uniqueptr_demo.png
   :alt: Shared pointer lifecycle demo
   :align: center
   :width: 70%

   Shared pointer lifecycle: multiple pointers managing the same resource.


Initialization
--------------

.. code-block:: cpp

   // Preferred: Exception-safe, efficient single allocation
   std::shared_ptr<T> identifier = std::make_shared<T>(args...);
   auto identifier = std::make_shared<T>(args...);

.. code-block:: cpp

   // Discouraged: Two allocations, potential exception issues
   std::shared_ptr<T> identifier(new T(args...));
   std::shared_ptr<T> identifier = std::shared_ptr<T>(new T(args...));
   auto identifier = std::shared_ptr<T>(new T(args...));

- ``T`` -- Type of the managed object allocated on the heap.
- ``identifier`` -- Variable name for the shared pointer instance.
- ``args...`` -- Constructor arguments passed to the managed object.

.. admonition:: C++ Core Guideline
   :class: tip

   `R.22: Use make_shared() to make shared_ptrs <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r22-use-make_shared-to-make-shared_ptrs>`_

**Multiple shared_ptr managing the same resource:**

.. code-block:: cpp
   :linenos:

   auto s1 = std::make_shared<int>(10);
   auto s2{s1};
   auto s3 = s2;

.. figure:: /_static/images/l7/fig_uniqueptr_demo2.png
   :alt: Multiple shared_ptr instances
   :align: center
   :width: 80%

   Three ``std::shared_ptr`` instances sharing ownership of the same resource.


Structure
---------

A ``std::shared_ptr`` maintains two essential pointers to implement shared
ownership semantics.

- **Resource Pointer** (``_M_ptr``) -- Points directly to the managed object
  on the heap.
- **Control Block Pointer** (``_M_refcount``) -- Points to the control block
  containing reference counts (strong and weak) and metadata. *The control block
  is also created on the heap.*

.. code-block:: cpp

   auto s = std::make_shared<int>(10);
   //   +-- _M_ptr           -> pointer to managed object (10)
   //   +-- _M_refcount      -> shared reference count (to control block)
   //   +-- [Control block]  -> allocated separately on the heap
   //          +-- strong count (shared ownership)
   //          +-- weak count (weak_ptr references)
   //          +-- deleter (function to destroy the object)
   //          +-- allocator info
   //          +-- possibly type-erased holder for custom deleters

.. figure:: /_static/images/l7/shared_ptr_structure.png
   :alt: Structure of a std::shared_ptr
   :align: center
   :width: 50%

   Internal structure of a ``std::shared_ptr`` showing the resource pointer and
   control block pointer.


Control Block
^^^^^^^^^^^^^^

A control block is a heap-allocated data structure that manages shared ownership
metadata for ``std::shared_ptr`` and ``std::weak_ptr``, enabling reference
counting and coordinated resource cleanup.

- Created when the first ``std::shared_ptr`` is constructed; *subsequent copies
  share the same control block instance*.
- Contains reference counts (strong and weak), custom deleters, and allocator
  information to ensure thread-safe resource management.
- Introduces memory overhead compared to ``std::unique_ptr`` or raw pointers,
  but enables safe shared ownership semantics.


Strong Count (``s_count``)
"""""""""""""""""""""""""""

.. figure:: /_static/images/l7/control_block_s_count.png
   :alt: Strong count in control block
   :align: center
   :width: 30%

   Strong count component of the control block.

Tracks the number of ``std::shared_ptr`` instances sharing ownership of the
resource.

- Incremented when a ``std::shared_ptr`` is **copied**.
- Unchanged when a ``std::shared_ptr`` is **moved**, since ownership is
  transferred, not duplicated.
- Decremented when a ``std::shared_ptr`` is destroyed, reset, or reassigned.
- *The managed resource is automatically destroyed when the strong count reaches
  zero.*


Weak Count (``w_count``)
""""""""""""""""""""""""""

.. figure:: /_static/images/l7/control_block_w_count.png
   :alt: Weak count in control block
   :align: center
   :width: 30%

   Weak count component of the control block.

Tracks the number of ``std::weak_ptr`` instances observing the resource without
owning it.

- Incremented/decremented as ``std::weak_ptr`` instances are created or
  destroyed.
- Does not influence resource lifetime: only the lifetime of the control block.
- *The control block is destroyed only when both the strong and weak counts
  reach zero.*


Managed Pointer
""""""""""""""""

.. figure:: /_static/images/l7/control_block_ptr.png
   :alt: Managed pointer in control block
   :align: center
   :width: 30%

   Managed pointer component of the control block.

A managed pointer to the managed resource. This managed pointer is mainly used
by the ``lock()`` method of ``std::weak_ptr``.


Deleter and Allocator
""""""""""""""""""""""

.. figure:: /_static/images/l7/control_block_deleter_allocator.png
   :alt: Deleter and allocator in control block
   :align: center
   :width: 30%

   Deleter and allocator components of the control block.

**Deleter**: A callable object (function, functor, or lambda) stored inside the
control block. It defines how the managed object is destroyed when the last
``std::shared_ptr`` owner goes away.

**Allocator**: Controls how memory is obtained and released for the object and
sometimes for the control block itself.


.. warning::

   Every control block starts with **one weak reference**: this is the control
   block's *self-reference*.

   - It ensures the control block remains valid even after the managed object is
     destroyed, allowing existing ``std::weak_ptr`` instances to safely call
     ``expired()`` or ``lock()``.
   - This self-reference is released automatically when the **last**
     ``std::shared_ptr`` is destroyed and no ``std::weak_ptr`` instances remain,
     causing both the strong and weak counts to reach zero: at which point the
     control block itself is deallocated.


Control Block Demo
"""""""""""""""""""

Let's analyze how the control block evolves with the following code:

.. code-block:: cpp
   :linenos:

   int main(){
       auto s1 = std::make_shared<int>(10);
       auto s2{s1};
       s1.reset();
       s2.reset();
   }

**Step 1: Line 2** -- ``auto s1 = std::make_shared<int>(10);``

.. figure:: /_static/images/l7/demo1_shared_ptr_1.png
   :alt: Shared pointer demo step 1
   :align: center
   :width: 50%

- Managed object: ``int(10)``
- Control block: allocated by ``make_shared``
- ``s_count``: 1 -- ``s1`` owns the object.
- ``w_count``: 1 -- the *implicit* reference keeping the control block alive.

**Step 2: Line 3** -- ``auto s2{s1};``

.. figure:: /_static/images/l7/demo1_shared_ptr_2.png
   :alt: Shared pointer demo step 2
   :align: center
   :width: 50%

- Copies ``s1`` --> another ``std::shared_ptr`` pointing to the same control block.
- ``s_count``: 2 -- ``s1`` and ``s2`` share ownership.
- ``w_count``: 1 -- unchanged (still only the control block's self-reference).

**Step 3: Line 4** -- ``s1.reset();``

.. figure:: /_static/images/l7/demo1_shared_ptr_3.png
   :alt: Shared pointer demo step 3
   :align: center
   :width: 50%

- Releases one shared owner.
- ``s_count``: 1 -- only ``s2`` remains.
- ``w_count``: 1 -- unchanged.

**Step 4: Line 5** -- ``s2.reset();`` (part a)

.. figure:: /_static/images/l7/demo1_shared_ptr_4a.png
   :alt: Shared pointer demo step 4a
   :align: center
   :width: 50%

- Releases the last shared owner.
- ``s_count``: 0 -- no more shared owners.
- ``w_count``: 1 -- still held by the control block's own internal ref.
- At this moment: the managed ``int(10)`` is cleaned up, because ``s_count`` == 0.

**Step 4: Line 5** -- ``s2.reset();`` (part b)

.. figure:: /_static/images/l7/demo1_shared_ptr_4b.png
   :alt: Shared pointer demo step 4b
   :align: center
   :width: 50%

- At the end of the same line (``s2.reset()``), the control block detects that
  the **last** ``std::shared_ptr`` is destroyed (``s_count`` = 0):

  - The control block releases its internal weak reference, making ``w_count``
    = 0 and **destroys itself immediately**.


Shared Pointer Methods
-----------------------

**Accessors:**

- ``get()`` -- raw pointer (non-owning).
- ``operator*()``, ``operator->()`` -- dereference access.
- ``explicit operator bool()`` -- ``true`` if not empty.

**Observers:**

- ``use_count()`` -- returns the current number of ``std::shared_ptr`` instances
  sharing ownership of the same resource. Intended primarily for debugging or
  instrumentation. Avoid using it in program logic -- the count can change at
  any time in multithreaded contexts.
- ``unique()`` -- convenience function that checks whether the calling
  ``std::shared_ptr`` is the only owner of the managed object.
  ``s.unique()`` is equivalent to ``s.use_count() == 1``.

**Modifiers:**

- ``reset()`` / ``reset(ptr)`` -- release current; optionally take new pointer
  (decrements previous control block).
- ``swap(other)`` -- exchange managed object and control block.


Pass to Functions: Sink (shared_ptr)
-------------------------------------

.. admonition:: C++ Core Guideline
   :class: tip

   `R.34: Take a shared_ptr<widget> parameter to express shared ownership <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r34-take-a-shared_ptrwidget-parameter-to-express-shared-ownership>`_

.. code-block:: cpp

   void process_widget(std::shared_ptr<Widget> widget_ptr);
   // Call: process_widget(my_shared_widget); // Copy shares ownership

.. code-block:: cpp

   void sink_shared(std::shared_ptr<int> ptr) { // Copy constructor increments ref count
       std::cout << ptr.use_count() << '\n';     // 2 (original + copy)
   }

   int main() {
       auto original = std::make_shared<int>(10);
       std::cout << original.use_count() << '\n';   // 1
       sink_shared(original); // Pass by value creates copy
       std::cout << original.use_count() << '\n';   // 1 (copy destroyed after function)
   }


Pass to Functions: Reseat (shared_ptr)
---------------------------------------

.. admonition:: C++ Core Guideline
   :class: tip

   `R.35: Take a shared_ptr<widget>& parameter to express that a function might reseat the shared pointer <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r35-take-a-shared_ptrwidget-parameter-to-express-that-a-function-might-reseat-the-shared-pointer>`_

.. code-block:: cpp

   void configure_widget(std::shared_ptr<Widget>& widget_ptr);
   // Function may call: widget_ptr.reset(std::make_shared<EnhancedWidget>());

.. code-block:: cpp

   void reseat_shared(std::shared_ptr<int>& ptr) { // Pass by reference -- no copy
       std::cout << ptr.use_count() << '\n';     // 1 (same instance, no increment)
       // Could modify ptr here: ptr.reset(std::make_shared<int>(20));
   }

   int main() {
       auto original = std::make_shared<int>(10);
       std::cout << original.use_count() << '\n';   // 1
       reseat_shared(original); // Pass by reference
       std::cout << original.use_count() << '\n';   // 1 (no copy made)
   }


Return from Functions (shared_ptr)
------------------------------------

Return Value Optimization (RVO) eliminates unnecessary copies when returning
``std::shared_ptr`` by value, resulting in efficient ownership transfer.

.. code-block:: cpp

   std::shared_ptr<int> create_shared_resource() {
       auto local_ptr = std::make_shared<int>(10);
       std::cout << &local_ptr << '\n';   // @1 (local variable address)
       return local_ptr; // RVO: no copy, direct construction in caller's context
   }

   int main() {
       auto result{create_shared_resource()};
       std::cout << &result << '\n'; // @1 (same address due to RVO)
   }


Weak Pointers
=============

A ``std::weak_ptr`` (from ``<memory>``) provides non-owning observation of
resources managed by ``std::shared_ptr``, enabling safe access without affecting
resource lifetime.

.. admonition:: Primary Purpose
   :class: note

   The primary purpose of ``std::weak_ptr`` is to break circular dependencies
   and provide safe resource monitoring without extending object lifetimes.

Key use cases for ``std::weak_ptr``:

- Breaking circular references that would cause memory leaks with
  ``std::shared_ptr`` (essential for parent-child relationships and observer
  patterns).
- Safe checking of resource validity using ``expired()`` before access.
- Temporary promotion to ``std::shared_ptr`` via ``lock()`` when needed.

Like ``std::shared_ptr``, a ``std::weak_ptr`` contains both a resource pointer
and a control block pointer.


Initialization
--------------

A ``std::weak_ptr`` is initialized from an existing ``std::shared_ptr`` or
copied from another ``std::weak_ptr``. This operation increases the *weak count*
in the control block but does not affect the *strong (ownership) count*.

.. code-block:: cpp

   auto s = std::make_shared<int>(10);

   // Create a weak_ptr from a shared_ptr
   std::weak_ptr<int> w1{s};

   // Create another weak_ptr from an existing weak_ptr
   std::weak_ptr<int> w2{w1};


Structure
---------

.. code-block:: cpp

   auto s = std::make_shared<int>(10);
   std::weak_ptr<int> w{s};
   //   +-- _M_refcount       -> points to the same control block as s
   //   +-- [Control block]   -> shared with all related shared_ptr / weak_ptr
   //          +-- strong count (number of shared_ptr owners)
   //          +-- weak count   (number of weak_ptr observers + 1 internal self-ref)
   //          +-- managed object pointer (to int(10))
   //          +-- deleter and allocator info
   //          +-- destroyed when both counts reach zero

.. figure:: /_static/images/l7/weak_ptr_structure.png
   :alt: Structure of a std::weak_ptr
   :align: center
   :width: 80%

   Structure of a ``std::weak_ptr`` showing the shared control block.

``std::weak_ptr`` cannot be directly dereferenced or provide raw pointer access.
It is purely an observer that requires promotion to ``std::shared_ptr`` for
resource access.

.. code-block:: cpp

   auto s = std::make_shared<int>(10);
   // Create weak_ptr from shared_ptr
   std::weak_ptr<int> w{s};

   std::cout << *w << '\n';        // Error: No operator*
   std::cout << w.get() << '\n';   // Error: No get() method


Methods
-------

- ``use_count()`` -- returns the number of ``std::shared_ptr`` instances currently
  owning the resource.
- ``reset()`` -- releases the weak reference, leaving the ``std::weak_ptr`` in
  an empty (non-observing) state.
- ``swap()`` -- exchanges control block references with another ``std::weak_ptr``
  (no ownership or object lifetime change).
- ``lock()`` -- safely tries to promote the weak reference to a
  ``std::shared_ptr``. Returns a valid ``std::shared_ptr`` if the object is
  still alive, or a **null** ``std::shared_ptr`` if it has expired.
- ``expired()`` -- returns ``true`` if the managed object has been destroyed;
  ``false`` otherwise.

**Reference count tracing example:**

.. code-block:: cpp
   :linenos:

   auto sp = std::make_shared<int>(42); // s_count=1, w_count=1 (implicit)
   std::weak_ptr<int> w1{sp};          // s_count=1, w_count=2
   std::weak_ptr<int> w2{sp};          // s_count=1, w_count=3

   sp.reset();     // s_count -> 0, object destroyed
                   // implicit w_count dropped -> w_count becomes 2 (w1, w2)

   std::cout << "expired? w1=" << w1.expired()
             << ", w2=" << w2.expired() << '\n'; // both true

   w1.reset();     // w_count -> 1
   w2.reset();     // w_count -> 0, control block destroyed here

.. list-table::
   :widths: 8 20 12 12 48
   :header-rows: 1

   * - Line
     - Statement
     - ``s_count``
     - ``w_count``
     - Notes
   * - 1
     - ``make_shared``
     - 1
     - 1
     - implicit ``w_count`` = 1
   * - 2
     - ``w1{sp}``
     - 1
     - 2
     - +1 user weak
   * - 3
     - ``w2{sp}``
     - 1
     - 3
     - +1 user weak
   * - 5
     - ``sp.reset()``
     - 0
     - 2
     - resource (``42``) destroyed; implicit weak dropped
   * - 11
     - ``w1.reset()``
     - 0
     - 1
     - one user weak dropped, one user weak remains
   * - 12
     - ``w2.reset()``
     - 0
     - 0
     - control block destroyed here


lock()
^^^^^^^

The ``lock()`` method safely promotes a weak reference to a ``std::shared_ptr``.

**Pseudocode:**

1. If the control block exists and the strong count > 0:

   - Atomically increment the strong count.
   - Retrieve the managed pointer from the control block.
   - Construct a new ``std::shared_ptr`` with that pointer and the same control block.

2. Otherwise:

   - Return an empty ``std::shared_ptr``.

.. code-block:: cpp
   :linenos:

   int main() {
       std::weak_ptr<int> weak;

       {
           auto shared = std::make_shared<int>(42);
           weak = shared;  // weak observes shared
       }  // shared destroyed here -> object deleted

       if (auto sp = weak.lock()) {
           std::cout << "Value: " << *sp << '\n';
       } else {
           std::cout << "Object no longer exists.\n";
       }
   }


expired()
^^^^^^^^^^

The ``expired()`` method checks whether the managed object has been destroyed.

**Pseudocode:**

1. If the control block is null, return ``true``.
2. If the strong count in the control block == 0, return ``true``.
3. Otherwise, return ``false``.

.. code-block:: cpp
   :linenos:

   // Declare empty weak pointer
   std::weak_ptr<int> weak_observer;
   {
       auto shared_resource = std::make_shared<int>(10);
       weak_observer = shared_resource;  // weak_observer now observes the resource
       if (weak_observer.expired())
           std::cout << "Resource has been destroyed\n";
       else
           std::cout << "Resource is still valid\n";
   }  // shared_resource destroyed, resource deallocated

   if (weak_observer.expired())
       std::cout << "Resource has been destroyed\n";
   else
       std::cout << "Resource is still valid\n";


Summary
=======

.. admonition:: Best Practice
   :class: tip

   Prefer smart pointers over raw pointers for all dynamic memory management to
   ensure automatic resource cleanup and exception safety.

   - Use ``std::unique_ptr`` as the default choice for single ownership. Only
     use ``std::shared_ptr`` when multiple owners are genuinely required.
   - Use ``std::weak_ptr`` to break circular dependencies and provide safe
     observation of shared resources without affecting their lifetime.
