====================================================
Lecture
====================================================



Overhead
--------

In computing, **overhead** refers to the additional resources -- time, memory, bandwidth, or processing -- required beyond the minimum necessary to accomplish a task. For example, calling a function has overhead (saving registers, pushing the return address onto the stack), even though those steps are not part of the function's core logic. When we discuss containers, we will frequently consider the overhead of various operations such as insertion, deletion, and access.

The Standard Library
--------------------

The C++ Standard Library is a collection of classes and functions that are part of the C++ ISO Standard. It provides common utilities including:

- Input/output streams (``<iostream>``, ``<fstream>``)
- String manipulation (``<string>``)
- Containers (``<vector>``, ``<array>``, ``<map>``, etc.)
- Algorithms (``<algorithm>``)
- Utilities (``<memory>``, ``<functional>``, ``<chrono>``)

.. figure:: /_static/images/l4/standard_library.png
   :alt: C++ Standard Library
   :align: center
   :width: 80%

   Overview of the C++ Standard Library.

The **Standard Template Library (STL)** is a subset of the Standard Library that provides generic containers, iterators, and algorithms. It is built on the concept of templates, which allow code to work with any data type.

STL Containers
--------------

An STL container is a class template that manages a collection of elements. Containers handle memory allocation and deallocation automatically, provide standard interfaces for accessing and modifying elements, and are designed for efficiency and safety.

Categories of Containers
^^^^^^^^^^^^^^^^^^^^^^^^

STL containers are organized into four categories:

1. **Sequence Containers** -- Store elements in a linear order. The position of each element depends on when and where it was inserted, not on its value. Examples: ``std::vector``, ``std::array``, ``std::deque``, ``std::list``, ``std::forward_list``.

2. **Associative Containers** -- Store elements in a sorted order based on keys. They provide fast key-based retrieval, typically in O(log n) time. Examples: ``std::set``, ``std::map``, ``std::multiset``, ``std::multimap``.

3. **Unordered Associative Containers** -- Store elements using hash tables, providing O(1) average-case access time. Elements are not stored in any particular order. Examples: ``std::unordered_set``, ``std::unordered_map``, ``std::unordered_multiset``, ``std::unordered_multimap``.

4. **Container Adapters** -- Wrappers around other containers that provide a restricted interface. They limit which operations are available to enforce specific data structure semantics. Examples: ``std::stack``, ``std::queue``, ``std::priority_queue``.

Why Use STL Containers?
^^^^^^^^^^^^^^^^^^^^^^^

- **Fast and efficient**: Implementations are highly optimized.
- **Common interfaces**: All containers share similar method names (``size()``, ``empty()``, ``begin()``, ``end()``).
- **Well-documented**: Extensive documentation and community support.
- **Memory management**: Containers handle allocation and deallocation automatically.
- **Type safety**: Templates provide compile-time type checking.

Strings
-------

Strings are sequences of characters. In C++, there are two primary ways to work with strings: C-style strings (C-strings) and ``std::string``.

C-style Strings (C-Strings)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A C-string is a character array terminated by the null character ``'\0'``. The null terminator marks the end of the string and is essential for C-string functions to know where the string ends.

.. code-block:: cpp

   // Array form -- compiler adds '\0' automatically
   char my_string[] = "hello";
   // my_string contains: {'h', 'e', 'l', 'l', 'o', '\0'}
   // Size of array: 6 bytes (5 characters + 1 null terminator)

   // Pointer form -- points to a string literal in read-only memory
   const char* my_literal = "world";

.. figure:: /_static/images/l4/c-string-memory.pdf
   :alt: C-string memory layout
   :align: center
   :width: 70%

   Memory layout of a C-string showing the null terminator.

C-strings are **relatively unsafe** because:

- No bounds checking on access.
- Buffer overflows are easy to introduce.
- Manual memory management is required for dynamic C-strings.
- String length must be computed by scanning for ``'\0'``.

For these reasons, ``std::string`` is strongly recommended for modern C++ development.

std::string
^^^^^^^^^^^

``std::string`` is a modern, safe, and feature-rich string class defined in the ``<string>`` header. It manages its own memory and provides a rich set of operations.

.. code-block:: cpp

   #include <string>

Initialization
~~~~~~~~~~~~~~

``std::string`` supports multiple forms of initialization:

.. code-block:: cpp

   // 1. From a C-string literal
   std::string s1{"hello"};

   // 2. Copy construction
   std::string s2{s1};

   // 3. Substring (from position 1, length 3)
   std::string s3{s1, 1, 3};  // "ell"

   // 4. Repeated character (5 copies of 'x')
   std::string s4(5, 'x');  // "xxxxx"

   // 5. From a C-string pointer
   const char* cstr = "world";
   std::string s5{cstr};

   // 6. From iterators
   std::string s6{s1.begin(), s1.begin() + 3};  // "hel"

   // 7. Default (empty string)
   std::string s7{};  // ""

String Literals
~~~~~~~~~~~~~~~

By default, a string literal like ``"hello"`` is a ``const char*`` (C-string), not a ``std::string``. To create a ``std::string`` literal directly, use the ``s`` suffix:

.. code-block:: cpp

   using namespace std::string_literals;

   auto c_str = "hello";    // const char*
   auto cpp_str = "hello"s; // std::string

Length
~~~~~~

``std::string`` provides two equivalent methods for getting the number of characters:

.. code-block:: cpp

   std::string greeting{"hello"};
   std::cout << greeting.length() << '\n';  // 5
   std::cout << greeting.size() << '\n';    // 5 (identical to length())

Both return a value of type ``size_t`` (an alias for ``std::size_t``), which is an unsigned integer type. On a 64-bit system, ``size_t`` is typically ``unsigned long long`` (8 bytes). It is used throughout the STL to represent sizes and indices.

.. warning::

   Because ``size_t`` is unsigned, subtracting from it can cause wraparound if the result would be negative. Be careful when doing arithmetic with ``size_t`` values.

Components of std::string
~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``std::string`` object on the stack contains three components:

1. A **pointer** to the character data (which may be on the heap or inline).
2. The **size** -- the number of characters currently stored.
3. The **capacity** -- the total number of characters that can be stored before reallocation is needed.

.. figure:: /_static/images/l4/string1.pdf
   :alt: std::string components
   :align: center
   :width: 70%

   Internal components of a ``std::string`` object.

On a typical 64-bit system, ``sizeof(std::string)`` is **32 bytes**, regardless of the string's content. This is the size of the string object on the stack, not the size of the character data it manages.

.. code-block:: cpp

   std::string short_str{"hi"};
   std::string long_str{"this is a much longer string"};
   std::cout << sizeof(short_str) << '\n';  // 32
   std::cout << sizeof(long_str) << '\n';   // 32

.. figure:: /_static/images/l4/string2.pdf
   :alt: std::string memory layout
   :align: center
   :width: 70%

   Memory layout showing stack and heap components of ``std::string``.

union
~~~~~

Before discussing Small String Optimization, it is helpful to understand the ``union`` keyword. A ``union`` allows multiple members to occupy the **same memory location**. The size of a union is the size of its largest member. Only one member can hold a value at any given time.

.. code-block:: cpp

   union Data {
       int integer;
       float decimal;
       char character;
   };

   Data d;
   d.integer = 42;
   std::cout << d.integer << '\n';  // 42
   // Writing to another member overwrites the previous value
   d.decimal = 3.14f;
   // d.integer is now undefined -- reading it is undefined behavior

   std::cout << sizeof(Data) << '\n';  // 4 (size of float or int, the largest member)

Small String Optimization (SSO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many ``std::string`` implementations use **Small String Optimization (SSO)**. For short strings (typically fewer than 15-22 characters, depending on the implementation), the character data is stored **inline** within the string object itself, rather than allocating memory on the heap.

This is typically achieved using a ``union``: the space that would normally hold the pointer-to-heap-data and capacity is reused to store the characters directly when the string is short enough.

.. code-block:: cpp

   std::string short_str{"hi"};
   std::cout << "Size: " << short_str.size() << '\n';        // 2
   std::cout << "Capacity: " << short_str.capacity() << '\n'; // 15 (typical SSO buffer)

   std::string long_str{"this string is definitely longer than SSO"};
   std::cout << "Size: " << long_str.size() << '\n';        // 41
   std::cout << "Capacity: " << long_str.capacity() << '\n'; // >= 41 (heap allocated)

SSO avoids the overhead of heap allocation for short strings, which are extremely common in practice.

Capacity Growth
~~~~~~~~~~~~~~~

When a string's size exceeds its capacity, the string must allocate a new, larger block of memory, copy the existing characters, and deallocate the old block. Typically, the capacity **doubles** each time this happens.

.. code-block:: cpp

   std::string s{};
   std::cout << "Size: " << s.size() << ", Capacity: " << s.capacity() << '\n';

   for (int i{0}; i < 50; ++i) {
       s += 'x';
       std::cout << "Size: " << s.size()
                 << ", Capacity: " << s.capacity() << '\n';
   }
   // Output shows capacity growing: 15, 30, 60, 120, ...

Access and Modification
~~~~~~~~~~~~~~~~~~~~~~~

``std::string`` provides several ways to access individual characters:

.. code-block:: cpp

   std::string quote{"To be or not to be"};

   // .front() and .back()
   std::cout << quote.front() << '\n';  // 'T'
   std::cout << quote.back() << '\n';   // 'e'

   // Subscript operator [] -- NO bounds checking
   std::cout << quote[0] << '\n';   // 'T'
   std::cout << quote[3] << '\n';   // 'b'
   // quote[100] -- undefined behavior! No exception thrown.

   // .at() -- WITH bounds checking
   std::cout << quote.at(0) << '\n';  // 'T'
   // quote.at(100) -- throws std::out_of_range exception

.. warning::

   The subscript operator ``[]`` does **not** perform bounds checking. Accessing an out-of-bounds index results in **undefined behavior** (UB). Always use ``.at()`` when you need safety, or validate indices manually before using ``[]``.

Range-based for Loop
~~~~~~~~~~~~~~~~~~~~

The range-based for loop provides a convenient way to iterate over every character in a string:

.. code-block:: cpp

   std::string quote{"To be or not to be"};

   // By value -- copies each character
   for (char c : quote) {
       std::cout << c << ' ';
   }
   std::cout << '\n';

   // By const reference -- avoids copy (preferred for read-only)
   for (const char& c : quote) {
       std::cout << c << ' ';
   }
   std::cout << '\n';

   // By reference -- allows modification
   for (char& c : quote) {
       c = std::toupper(c);
   }
   std::cout << quote << '\n';  // "TO BE OR NOT TO BE"

When iterating **by value**, each element is **copied** into the loop variable. For ``char`` this is inexpensive, but for larger types you should use references.

Iterators
~~~~~~~~~

An **iterator** is an object that points to an element in a container. Iterators provide a uniform way to traverse containers, regardless of the container type.

.. code-block:: cpp

   std::string quote{"To be or not to be"};

   // begin() returns an iterator to the first element
   // end() returns an iterator to one past the last element
   for (auto it = quote.begin(); it != quote.end(); ++it) {
       std::cout << *it << ' ';
   }
   std::cout << '\n';

.. figure:: /_static/images/l4/iterator.pdf
   :alt: Iterator concept
   :align: center
   :width: 70%

   Iterators ``begin()`` and ``end()`` for a container.

Key points about iterators:

- ``begin()`` points to the first element.
- ``end()`` points to **one past** the last element (not the last element itself).
- ``*it`` dereferences the iterator to access the element.
- ``++it`` advances the iterator to the next element.
- ``auto`` is commonly used to let the compiler deduce the iterator type.

Inputs
~~~~~~

Reading strings from standard input has some nuances:

.. code-block:: cpp

   std::string name{};

   // std::cin >> stops at whitespace
   std::cout << "Enter your full name: ";
   std::cin >> name;
   // If the user types "John Doe", name will be "John"

   // std::getline reads the entire line
   std::cout << "Enter your full name: ";
   std::getline(std::cin >> std::ws, name);
   // If the user types "John Doe", name will be "John Doe"

``std::cin >> std::ws`` discards any leading whitespace (including leftover newline characters from previous input operations) before reading the line.

Concatenation
~~~~~~~~~~~~~

.. code-block:: cpp

   std::string first{"Hello"};
   std::string second{" World"};

   // += operator
   first += second;
   std::cout << first << '\n';  // "Hello World"

   // + operator (creates a new string)
   std::string result = first + "!";
   std::cout << result << '\n';  // "Hello World!"

   // .append()
   std::string greeting{"Hi"};
   greeting.append(" there");
   std::cout << greeting << '\n';  // "Hi there"

   // .push_back() -- single character only
   greeting.push_back('!');
   std::cout << greeting << '\n';  // "Hi there!"

Insert
~~~~~~

.. code-block:: cpp

   std::string str{"Hello World"};

   // Insert a string at a position
   str.insert(5, ",");
   std::cout << str << '\n';  // "Hello, World"

   // Insert a substring
   std::string source{"ABCDEF"};
   str.insert(7, source, 0, 3);  // Insert "ABC" at position 7
   std::cout << str << '\n';  // "Hello, ABCWorld"

   // Insert using iterators
   str.insert(str.begin(), '!');
   std::cout << str << '\n';  // "!Hello, ABCWorld"

Remove
~~~~~~

.. code-block:: cpp

   std::string str{"Hello, World!"};

   // erase(pos, count) -- remove characters starting at pos
   str.erase(5, 2);  // Remove ", "
   std::cout << str << '\n';  // "HelloWorld!"

   // erase with iterators -- remove a range
   str.erase(str.begin(), str.begin() + 5);
   std::cout << str << '\n';  // "World!"

   // clear() -- remove all characters
   str.clear();
   std::cout << "Empty: " << str.empty() << '\n';  // 1 (true)

   // pop_back() -- remove last character
   std::string text{"abc"};
   text.pop_back();
   std::cout << text << '\n';  // "ab"

Memory Management
~~~~~~~~~~~~~~~~~

Understanding how ``std::string`` manages memory is important for writing efficient code.

.. code-block:: cpp

   std::string s{"Hello"};
   std::cout << "Size: " << s.size() << '\n';          // 5
   std::cout << "Capacity: " << s.capacity() << '\n';  // 15 (SSO)

   // .reserve(n) -- request capacity for at least n characters
   // Does NOT change the size or content
   s.reserve(100);
   std::cout << "Size: " << s.size() << '\n';          // 5 (unchanged)
   std::cout << "Capacity: " << s.capacity() << '\n';  // >= 100

   // .resize(n) -- change the size to n
   // If n > size, new characters are value-initialized ('\0')
   // If n < size, characters are removed from the end
   s.resize(10);
   std::cout << "Size: " << s.size() << '\n';          // 10
   std::cout << "Content: '" << s << "'\n";             // "Hello\0\0\0\0\0"

   // .shrink_to_fit() -- request reduction of capacity to fit size
   // This is a non-binding request; the implementation may ignore it
   s.shrink_to_fit();
   std::cout << "Capacity: " << s.capacity() << '\n';  // likely 10

**Memory fragmentation** occurs when memory is allocated and deallocated in a pattern that leaves small, unusable gaps between allocated blocks. Frequent string resizing can contribute to fragmentation. Using ``reserve()`` to pre-allocate memory when you know the approximate final size can help reduce fragmentation.

.. figure:: /_static/images/l4/string-memory-0.jpg
   :alt: String memory step 0
   :align: center
   :width: 70%

   String memory: initial state.

.. figure:: /_static/images/l4/string-memory-1.jpg
   :alt: String memory step 1
   :align: center
   :width: 70%

   String memory: after appending characters.

.. figure:: /_static/images/l4/string-memory-2.jpg
   :alt: String memory step 2
   :align: center
   :width: 70%

   String memory: capacity exceeded, reallocation occurs.

.. figure:: /_static/images/l4/string-memory-3.jpg
   :alt: String memory step 3
   :align: center
   :width: 70%

   String memory: old block freed, data copied to new block.

.. figure:: /_static/images/l4/string-memory-4.jpg
   :alt: String memory step 4
   :align: center
   :width: 70%

   String memory: continued growth.

.. figure:: /_static/images/l4/string-memory-5.jpg
   :alt: String memory step 5
   :align: center
   :width: 70%

   String memory: after ``shrink_to_fit()``.

Arrays
------

Arrays store a fixed number of elements of the same type in contiguous memory. C++ provides both C-style arrays and the modern ``std::array`` wrapper.

Declaration
^^^^^^^^^^^

.. code-block:: cpp

   // C-style array
   int numbers[5];  // Uninitialized -- contains garbage values

   // std::array (from <array>)
   #include <array>
   std::array<int, 5> numbers;  // Uninitialized in some contexts

Initialization
^^^^^^^^^^^^^^

.. code-block:: cpp

   // C-style array initialization
   int a[5] = {1, 2, 3, 4, 5};     // Fully initialized
   int b[5] = {1, 2};               // Partial: {1, 2, 0, 0, 0}
   int c[5] = {};                    // Zero initialized: {0, 0, 0, 0, 0}
   int d[] = {1, 2, 3};             // Size deduced: 3

   // std::array initialization
   std::array<int, 5> e{1, 2, 3, 4, 5};   // Fully initialized
   std::array<int, 5> f{1, 2};             // Partial: {1, 2, 0, 0, 0}
   std::array<int, 5> g{};                  // Zero initialized

   // .fill() -- set all elements to the same value
   std::array<int, 5> h{};
   h.fill(42);  // {42, 42, 42, 42, 42}

.. figure:: /_static/images/l4/arrays.png
   :alt: Array memory layout
   :align: center
   :width: 70%

   Contiguous memory layout of an array.

C-style Arrays and Pointers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In most contexts, a C-style array name **decays** to a pointer to its first element. This means you can use pointer arithmetic to access elements.

.. code-block:: cpp

   int arr[5] = {10, 20, 30, 40, 50};

   // Array name decays to pointer
   int* ptr = arr;         // ptr points to arr[0]
   std::cout << *ptr << '\n';       // 10
   std::cout << *(ptr + 1) << '\n'; // 20
   std::cout << *(ptr + 2) << '\n'; // 30

   // ptr[i] is equivalent to *(ptr + i)
   std::cout << ptr[3] << '\n';     // 40

.. figure:: /_static/images/l4/array0.pdf
   :alt: Array and pointer relationship
   :align: center
   :width: 70%

   An array name decays to a pointer to its first element.

Array Length
^^^^^^^^^^^^

The size of both C-style arrays and ``std::array`` must be a **compile-time constant**. You cannot use a runtime variable as the array size.

.. code-block:: cpp

   constexpr size_t size{5};
   int arr[size];                  // OK -- constexpr
   std::array<int, size> arr2{};   // OK -- constexpr

   size_t runtime_size{5};
   // int bad_arr[runtime_size];   // Error with -pedantic-errors
   // Variable-length arrays (VLAs) are NOT standard C++

.. note::

   Compile with the ``-pedantic-errors`` flag to catch non-standard extensions like VLAs. This ensures your code is portable and standards-compliant.

Access and Modification
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::array<int, 5> arr{10, 20, 30, 40, 50};

   // Subscript operator [] -- no bounds checking
   std::cout << arr[0] << '\n';  // 10

   // .at() -- with bounds checking (throws std::out_of_range)
   std::cout << arr.at(2) << '\n';  // 30

   // .front() and .back()
   std::cout << arr.front() << '\n';  // 10
   std::cout << arr.back() << '\n';   // 50

   // .size()
   std::cout << arr.size() << '\n';   // 5

   // .empty()
   std::cout << arr.empty() << '\n';  // 0 (false)

   // .fill()
   arr.fill(0);  // {0, 0, 0, 0, 0}

   // Range-based for loop
   std::array<int, 4> scores{95, 87, 92, 78};
   for (const auto& score : scores) {
       std::cout << score << ' ';
   }
   std::cout << '\n';  // 95 87 92 78

.. figure:: /_static/images/l4/array1.pdf
   :alt: Array access operations
   :align: center
   :width: 70%

   Accessing array elements with ``[]`` and ``.at()``.

Multidimensional Arrays
^^^^^^^^^^^^^^^^^^^^^^^^

A 2D array is an array of arrays, often used to represent matrices. A 3D array is an array of 2D arrays.

.. code-block:: cpp

   // C-style 2D array (3 rows, 4 columns)
   int matrix[3][4] = {
       {1, 2, 3, 4},
       {5, 6, 7, 8},
       {9, 10, 11, 12}
   };

   // Access: matrix[row][col]
   std::cout << matrix[1][2] << '\n';  // 7

   // std::array 2D array
   std::array<std::array<int, 4>, 3> grid{{
       {1, 2, 3, 4},
       {5, 6, 7, 8},
       {9, 10, 11, 12}
   }};

   // Access: grid[row][col] or grid.at(row).at(col)
   std::cout << grid[1][2] << '\n';          // 7
   std::cout << grid.at(1).at(2) << '\n';    // 7

   // C-style 3D array
   int cube[2][3][4] = {
       {
           {1, 2, 3, 4},
           {5, 6, 7, 8},
           {9, 10, 11, 12}
       },
       {
           {13, 14, 15, 16},
           {17, 18, 19, 20},
           {21, 22, 23, 24}
       }
   };

   // std::array 3D array
   std::array<std::array<std::array<int, 4>, 3>, 2> cube3d{};

.. figure:: /_static/images/l4/array2.pdf
   :alt: 2D array layout
   :align: center
   :width: 70%

   Memory layout of a 2D array.

.. figure:: /_static/images/l4/array3.pdf
   :alt: 2D std::array layout
   :align: center
   :width: 70%

   Using ``std::array`` for multidimensional arrays.

.. figure:: /_static/images/l4/array4.pdf
   :alt: 3D array
   :align: center
   :width: 70%

   A 3D array represented as an array of 2D arrays.

Vectors
-------

``std::vector`` is a dynamic array that can grow and shrink at runtime. It is the most commonly used container in C++ and is defined in the ``<vector>`` header.

.. code-block:: cpp

   #include <vector>

Memory Management
^^^^^^^^^^^^^^^^^

A ``std::vector`` object resides on the **stack** and internally maintains a pointer to a dynamically allocated array on the **heap**. The vector manages three internal pointers:

1. **start** -- pointer to the first element of the allocated array.
2. **finish** -- pointer to one past the last element currently in use.
3. **end_of_storage** -- pointer to one past the last element of the allocated capacity.

.. figure:: /_static/images/l4/vector-memory1.pdf
   :alt: Vector memory layout
   :align: center
   :width: 70%

   Internal memory layout of a ``std::vector``.

- **Size**: the number of elements currently stored (``finish - start``).
- **Capacity**: the total number of elements the vector can hold before reallocation (``end_of_storage - start``).

.. figure:: /_static/images/l4/vector-memory2.pdf
   :alt: Vector size vs capacity
   :align: center
   :width: 70%

   Relationship between vector size and capacity.

The ``sizeof()`` a vector object is the same regardless of how many elements it contains, because ``sizeof()`` measures only the stack object (the three pointers), not the heap data.

.. code-block:: cpp

   std::vector<int> v1{};
   std::vector<int> v2{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

   std::cout << sizeof(v1) << '\n';  // 24 (typical: 3 pointers x 8 bytes)
   std::cout << sizeof(v2) << '\n';  // 24 (same!)

Initialization
^^^^^^^^^^^^^^

.. code-block:: cpp

   // Explicit values
   std::vector<int> v1{1, 2, 3, 4, 5};

   // N elements, all zero-initialized
   std::vector<int> v2(5);  // {0, 0, 0, 0, 0}

   // N elements, all with a specific value
   std::vector<int> v3(5, 42);  // {42, 42, 42, 42, 42}

   // Copy construction
   std::vector<int> v4{v1};

   // Using auto
   auto v5 = std::vector<int>{10, 20, 30};

Access and Modification
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> vec{10, 20, 30, 40, 50};

   // .front() and .back()
   std::cout << vec.front() << '\n';  // 10
   std::cout << vec.back() << '\n';   // 50

   // Subscript operator [] -- no bounds checking
   std::cout << vec[2] << '\n';  // 30

   // .at() -- with bounds checking
   std::cout << vec.at(2) << '\n';  // 30

   // Range-based for loop
   for (const auto& val : vec) {
       std::cout << val << ' ';
   }
   std::cout << '\n';

   // .assign() -- replace all contents
   vec.assign(3, 99);  // {99, 99, 99}

Insertion
^^^^^^^^^

push_back()
~~~~~~~~~~~

``push_back()`` adds an element to the end of the vector. If the vector's size equals its capacity, a reallocation occurs: a new, larger block of memory is allocated, existing elements are copied/moved, and the old block is deallocated.

.. code-block:: cpp

   std::vector<int> vec{1, 2, 3};
   vec.push_back(4);
   // vec is now {1, 2, 3, 4}

emplace_back()
~~~~~~~~~~~~~~

``emplace_back()`` constructs an element **in place** at the end of the vector, avoiding the creation of a temporary object. This can be more efficient than ``push_back()`` for complex types.

.. code-block:: cpp

   #include <utility>  // for std::pair

   std::vector<std::pair<int, std::string>> records{};

   // push_back: creates a temporary pair, then copies/moves it
   records.push_back({1, "Alice"});

   // emplace_back: constructs the pair directly in the vector's memory
   records.emplace_back(2, "Bob");

insert()
~~~~~~~~

``insert()`` adds elements at a specified position.

.. code-block:: cpp

   std::vector<int> vec{1, 2, 3, 4, 5};

   // Insert a single element at position
   auto it = vec.begin() + 2;
   vec.insert(it, 99);
   // vec: {1, 2, 99, 3, 4, 5}

   // Insert multiple copies
   vec.insert(vec.begin(), 3, 0);
   // vec: {0, 0, 0, 1, 2, 99, 3, 4, 5}

   // Insert elements from another container
   std::vector<int> other{10, 20};
   vec.insert(vec.end(), other.begin(), other.end());
   // vec: {0, 0, 0, 1, 2, 99, 3, 4, 5, 10, 20}

emplace()
~~~~~~~~~

``emplace()`` constructs an element **in place** at a specified position, similar to how ``emplace_back()`` works at the end.

.. code-block:: cpp

   std::vector<std::pair<int, std::string>> records{};
   records.emplace(records.begin(), 1, "Alice");

Deletion
^^^^^^^^

pop_back()
~~~~~~~~~~

``pop_back()`` removes the last element. It does **not** return the removed element.

.. code-block:: cpp

   std::vector<int> vec{1, 2, 3, 4, 5};
   vec.pop_back();
   // vec: {1, 2, 3, 4}
   // To get the last element before removing, use .back() first
   int last = vec.back();
   vec.pop_back();

erase()
~~~~~~~

``erase()`` removes elements by position or range and returns an iterator to the element following the last removed element.

.. code-block:: cpp

   std::vector<int> vec{10, 20, 30, 40, 50};

   // Erase single element
   auto it = vec.erase(vec.begin() + 1);
   // vec: {10, 30, 40, 50}, it points to 30

   // Erase a range
   vec.erase(vec.begin(), vec.begin() + 2);
   // vec: {40, 50}

clear()
~~~~~~~

``clear()`` removes all elements. The size becomes 0, but the **capacity remains unchanged**.

.. code-block:: cpp

   std::vector<int> vec{1, 2, 3, 4, 5};
   std::cout << "Before clear - Size: " << vec.size()
             << ", Capacity: " << vec.capacity() << '\n';
   // Size: 5, Capacity: 5

   vec.clear();
   std::cout << "After clear - Size: " << vec.size()
             << ", Capacity: " << vec.capacity() << '\n';
   // Size: 0, Capacity: 5 (unchanged!)

Vector Memory Management
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> vec{};

   // .reserve(n) -- pre-allocate capacity for n elements
   // Does NOT change size or add elements
   vec.reserve(100);
   std::cout << "Size: " << vec.size() << '\n';          // 0
   std::cout << "Capacity: " << vec.capacity() << '\n';  // >= 100

   // .resize(n) -- change the number of elements
   // If n > size, new elements are value-initialized (0 for int)
   // If n < size, elements are removed from the end
   vec.resize(10);
   std::cout << "Size: " << vec.size() << '\n';          // 10
   std::cout << "Capacity: " << vec.capacity() << '\n';  // >= 100

   // .shrink_to_fit() -- request to reduce capacity to match size
   // Non-binding: the implementation may ignore this request
   vec.shrink_to_fit();
   std::cout << "Size: " << vec.size() << '\n';          // 10
   std::cout << "Capacity: " << vec.capacity() << '\n';  // likely 10


Maps
----

Maps are associative containers that store key-value pairs, providing efficient lookup by key. C++ offers two main map types: ``std::map`` (ordered) and ``std::unordered_map`` (hash-based).

std::map
^^^^^^^^

``std::map`` is an ordered associative container defined in the ``<map>`` header. It stores key-value pairs where keys are unique and automatically sorted. Internally, it uses a balanced binary search tree (typically a red-black tree), giving O(log n) time for insertion, deletion, and lookup.

.. code-block:: cpp

   #include <map>

**Declaration and Initialization**

.. code-block:: cpp

   // Declaration
   std::map<std::string, int> ages;

   // Initialization with values
   std::map<std::string, int> ages{{"Alice", 25}, {"Bob", 30}};

**Insertion**

There are several ways to insert elements into a map:

.. code-block:: cpp

   // Subscript operator -- creates entry if key does not exist
   ages["Charlie"] = 35;

   // insert() -- returns a pair<iterator, bool>
   ages.insert({"Dave", 40});

   // emplace() -- constructs in place
   ages.emplace("Eve", 28);

**Access**

.. code-block:: cpp

   // Subscript operator -- WARNING: creates a default entry if key is missing!
   int alice_age{ages["Alice"]};  // 25

   // .at() -- throws std::out_of_range if key is missing
   int bob_age{ages.at("Bob")};  // 30

.. warning::

   Using ``[]`` on a map with a key that does not exist will **insert** a new element with a default-constructed value. Use ``.at()`` when you want an exception on missing keys, or check existence first.

**Checking Existence**

.. code-block:: cpp

   // count() -- returns 0 or 1 for std::map
   if (ages.count("Alice")) {
       std::cout << "Alice found\n";
   }

   // find() -- returns an iterator
   if (ages.find("Alice") != ages.end()) {
       std::cout << "Alice found\n";
   }

   // C++20: contains()
   if (ages.contains("Alice")) {
       std::cout << "Alice found\n";
   }

**Iteration**

Iterating over a ``std::map`` always visits keys in sorted order:

.. code-block:: cpp

   for (const auto& [name, age] : ages) {
       std::cout << name << ": " << age << '\n';
   }

**Erase and Size**

.. code-block:: cpp

   ages.erase("Bob");                  // Remove by key
   std::cout << ages.size() << '\n';   // Number of elements
   std::cout << ages.empty() << '\n';  // Check if empty

std::unordered_map
^^^^^^^^^^^^^^^^^^

``std::unordered_map`` is a hash-based associative container defined in the ``<unordered_map>`` header. It provides O(1) average-case lookup, insertion, and deletion, compared to O(log n) for ``std::map``. Elements are **not** stored in any particular order.

.. code-block:: cpp

   #include <unordered_map>

``std::unordered_map`` has the same interface as ``std::map`` -- you can use ``[]``, ``.at()``, ``.insert()``, ``.emplace()``, ``.erase()``, ``.find()``, ``.count()``, and ``.contains()`` in exactly the same way.

**When to Use Which**

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Criteria
     - ``std::map``
     - ``std::unordered_map``
   * - Order
     - Sorted by key
     - No guaranteed order
   * - Lookup time
     - O(log n)
     - O(1) average
   * - Use when
     - You need sorted iteration
     - You need maximum speed

Use Cases in Robotics
^^^^^^^^^^^^^^^^^^^^^

Maps are widely used in robotics applications:

- **Sensor registry**: Map sensor names to their latest readings (``std::map<std::string, double>``).
- **Robot parameters**: Store configuration parameters by name (``std::map<std::string, double>``).
- **Part inventory**: Track component counts by ID (``std::map<std::string, int>``).

Example: Sensor Registry
~~~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: Full Example
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      #include <map>
      #include <string>
      #include <iostream>

      int main() {
          std::map<std::string, double> sensor_readings{
              {"temperature", 23.5},
              {"humidity", 45.2},
              {"pressure", 1013.25}
          };

          // Add a reading
          sensor_readings["light"] = 750.0;

          // Access
          std::cout << "Temperature: " << sensor_readings.at("temperature") << '\n';

          // Check existence
          if (sensor_readings.count("humidity")) {
              std::cout << "Humidity: " << sensor_readings["humidity"] << '\n';
          }

          // Iterate (sorted by key)
          for (const auto& [sensor, value] : sensor_readings) {
              std::cout << sensor << " = " << value << '\n';
          }

          // Erase
          sensor_readings.erase("light");

          return 0;
      }


STL Algorithms
--------------

The ``<algorithm>`` header provides a rich set of generic algorithms that operate on iterators. These algorithms work with any container that supports iterators, promoting code reuse and clarity.

.. admonition:: Best Practice
   :class: tip

   Prefer algorithms over raw loops -- they are more readable, less error-prone, and often optimized by the compiler.

Overview
^^^^^^^^

Instead of writing manual loops to search, sort, or transform data, use the standard algorithms. They express intent clearly and reduce the chance of off-by-one errors or other common loop bugs.

.. code-block:: cpp

   #include <algorithm>
   #include <numeric>    // for std::accumulate

Common Algorithms
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Algorithm
     - Description
   * - ``std::sort``
     - Sort elements in ascending order (or with a custom comparator).
   * - ``std::find``
     - Find the first element equal to a value. Returns an iterator.
   * - ``std::count``
     - Count occurrences of a value.
   * - ``std::accumulate``
     - Compute a cumulative result (e.g., sum). From ``<numeric>``.
   * - ``std::transform``
     - Apply a function to each element and store the result.
   * - ``std::for_each``
     - Apply a function to each element (no output range).
   * - ``std::min_element``
     - Find the smallest element. Returns an iterator.
   * - ``std::max_element``
     - Find the largest element. Returns an iterator.
   * - ``std::reverse``
     - Reverse the order of elements in a range.

**Basic Usage**

.. code-block:: cpp

   std::vector<int> vec{5, 3, 1, 4, 2};

   // Sort
   std::sort(vec.begin(), vec.end());

   // Find
   auto it = std::find(vec.begin(), vec.end(), 42);

   // Count
   int n = std::count(vec.begin(), vec.end(), 42);

   // Sum (from <numeric>)
   int sum = std::accumulate(vec.begin(), vec.end(), 0);

   // Reverse
   std::reverse(vec.begin(), vec.end());

Combining Algorithms with Lambdas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Algorithms become especially powerful when combined with lambdas for custom operations and predicates.

.. dropdown:: Full Example
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      #include <algorithm>
      #include <numeric>
      #include <vector>
      #include <iostream>

      int main() {
          std::vector<int> readings{45, 12, 78, 34, 56, 23, 89, 67};

          // Sort
          std::sort(readings.begin(), readings.end());

          // Find
          auto it = std::find(readings.begin(), readings.end(), 34);
          if (it != readings.end()) {
              std::cout << "Found 34 at index "
                        << std::distance(readings.begin(), it) << '\n';
          }

          // Sum
          int total = std::accumulate(readings.begin(), readings.end(), 0);
          std::cout << "Total: " << total << '\n';

          // Count values above 50
          int above_50 = std::count_if(readings.begin(), readings.end(),
              [](int val) { return val > 50; });
          std::cout << "Above 50: " << above_50 << '\n';

          // Transform: double each value
          std::transform(readings.begin(), readings.end(), readings.begin(),
              [](int val) { return val * 2; });

          // Min and max
          auto [min_it, max_it] = std::minmax_element(
              readings.begin(), readings.end());
          std::cout << "Min: " << *min_it << ", Max: " << *max_it << '\n';

          return 0;
      }
