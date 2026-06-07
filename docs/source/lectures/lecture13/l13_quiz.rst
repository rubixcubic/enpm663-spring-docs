====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 13: ROS 2 Advanced Topics.
Topics include coordinate frames, TF2 (static and dynamic transforms,
broadcasting, listening), the TransformStamped message, ``lookupTransform()``,
lifecycle node states, transitions, callback return values, and when to
use lifecycle nodes.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1--10)
====================================================

.. admonition:: Question 1
   :class: hint

   Which ROS 2 topic is used to publish **static** transforms?

   A. ``/tf``

   B. ``/tf_static``

   C. ``/transforms``

   D. ``/tf2/static``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``/tf_static``

   Static transforms are published to the ``/tf_static`` topic. They are
   latched, meaning they are published once and remain available to all
   subscribers. Dynamic transforms are published to ``/tf``.


.. admonition:: Question 2
   :class: hint

   In a ``TransformStamped`` message, what does ``header.frame_id``
   represent?

   A. The child frame

   B. The target frame for lookups

   C. The parent frame

   D. The frame being transformed

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The parent frame

   In a ``TransformStamped`` message, ``header.frame_id`` is the parent
   frame, and ``child_frame_id`` is the child frame. The transform
   describes the position and orientation of the child frame relative to
   the parent frame.


.. admonition:: Question 3
   :class: hint

   Which class should you use to publish a transform that changes over
   time (e.g., a robot moving in the world frame)?

   A. ``tf2_ros::StaticTransformBroadcaster``

   B. ``tf2_ros::TransformBroadcaster``

   C. ``tf2_ros::TransformListener``

   D. ``tf2_ros::Buffer``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``tf2_ros::TransformBroadcaster``

   ``TransformBroadcaster`` is used for dynamic transforms that change
   over time and must be published continuously.
   ``StaticTransformBroadcaster`` is for transforms that never change.


.. admonition:: Question 4
   :class: hint

   What happens if you stop publishing a dynamic transform?

   A. The last published transform is latched and remains available
      indefinitely.

   B. Consumers will eventually receive a ``TransformException`` because
      the transform becomes stale.

   C. The frame is automatically removed from the TF tree.

   D. Other nodes continue to work because the buffer caches all
      transforms permanently.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Consumers will eventually receive a ``TransformException``
   because the transform becomes stale.

   Dynamic transforms must be published continuously. The TF2 buffer
   keeps transforms for a limited time window. If no new transform
   arrives, the existing data becomes stale and ``lookupTransform()``
   calls will throw an ``ExtrapolationException``.


.. admonition:: Question 5
   :class: hint

   In the following code, what does the call return?

   .. code-block:: cpp

      auto t = tf_buffer_->lookupTransform("world", "camera_link",
                                            tf2::TimePointZero);

   A. The transform from ``camera_link`` to ``world``

   B. The transform from ``world`` to ``camera_link``

   C. The pose of ``world`` in the ``camera_link`` frame

   D. An error because the order of arguments is wrong

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The transform from ``world`` to ``camera_link``

   ``lookupTransform(target_frame, source_frame, time)`` returns the
   transform that expresses the source frame (``camera_link``) in the
   target frame (``world``). In other words, it gives you the pose of
   ``camera_link`` in the ``world`` frame.


.. admonition:: Question 6
   :class: hint

   What are the four **primary states** of a lifecycle node?

   A. Created, Running, Paused, Destroyed

   B. Unconfigured, Inactive, Active, Finalized

   C. Initialized, Configured, Active, Shutdown

   D. Starting, Ready, Running, Stopped

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Unconfigured, Inactive, Active, Finalized

   The lifecycle state machine defines four primary states:
   **Unconfigured** (initial), **Inactive** (configured but not
   processing), **Active** (fully operational), and **Finalized**
   (terminal, cannot be restarted).


.. admonition:: Question 7
   :class: hint

   Which transition moves a lifecycle node from the **Unconfigured**
   state to the **Inactive** state?

   A. ``activate``

   B. ``configure``

   C. ``cleanup``

   D. ``shutdown``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``configure``

   The ``configure`` transition takes a lifecycle node from
   **Unconfigured** to **Inactive**. During this transition, the
   ``on_configure()`` callback is executed.


.. admonition:: Question 8
   :class: hint

   What happens when a lifecycle transition callback returns
   ``CallbackReturn::ERROR``?

   A. The node stays in the current state.

   B. The node transitions to the Finalized state.

   C. The node transitions to the ErrorProcessing state.

   D. The transition is retried automatically.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The node transitions to the ErrorProcessing state.

   Returning ``ERROR`` indicates a critical failure. The node enters the
   **ErrorProcessing** state, where the ``on_error()`` callback is
   invoked if implemented. Returning ``FAILURE`` keeps the node in (or
   returns it to) the previous primary state.


.. admonition:: Question 9
   :class: hint

   Which base class must you inherit from to create a lifecycle node?

   A. ``rclcpp::Node``

   B. ``rclcpp_lifecycle::LifecycleNode``

   C. ``rclcpp::ManagedNode``

   D. ``rclcpp_lifecycle::StateMachineNode``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``rclcpp_lifecycle::LifecycleNode``

   To create a lifecycle node in C++, inherit from
   ``rclcpp_lifecycle::LifecycleNode`` instead of ``rclcpp::Node``.
   This gives you access to the lifecycle state machine and the
   transition callbacks.


.. admonition:: Question 10
   :class: hint

   What does a ``LifecyclePublisher`` do when you call ``publish()``
   and the node is in the **Inactive** state?

   A. It publishes the message normally.

   B. It throws an exception.

   C. It silently drops the message.

   D. It buffers the message until the node is activated.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It silently drops the message.

   A ``LifecyclePublisher`` only transmits messages when the node is in
   the **Active** state. In any other state, calls to ``publish()``
   are silently ignored.


----


True / False (Questions 11--15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False**: In the ROS 2 TF2 frame tree, a frame can have
   multiple parent frames.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The TF2 frame tree is a strict tree structure where each frame has
   exactly one parent (except the root frame). This ensures there is
   exactly one path between any two frames, making transform lookups
   unambiguous.


.. admonition:: Question 12
   :class: hint

   **True or False**: A static transform must be published continuously
   at a fixed rate to remain available in the TF2 buffer.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Static transforms are latched -- they only need to be published once.
   The ``/tf_static`` topic retains the message so that any new
   subscriber receives it immediately. This is what makes static
   transforms suitable for fixed relationships like sensor mounts.


.. admonition:: Question 13
   :class: hint

   **True or False**: The ``cleanup`` transition moves a lifecycle node
   from the **Inactive** state back to the **Unconfigured** state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ``cleanup`` transition takes a node from **Inactive** back to
   **Unconfigured**, invoking the ``on_cleanup()`` callback. This
   allows the node to release resources and be reconfigured.


.. admonition:: Question 14
   :class: hint

   **True or False**: You can trigger a ``shutdown`` transition only
   from the **Active** state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``shutdown`` transition can be triggered from any primary state
   except **Finalized**. It can be called from **Unconfigured**,
   **Inactive**, or **Active**, and it always transitions the node to
   the **Finalized** state.


.. admonition:: Question 15
   :class: hint

   **True or False**: The orientation in a ``TransformStamped`` message
   is represented as Euler angles (roll, pitch, yaw).

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The orientation in a ``TransformStamped`` message is represented as
   a **quaternion** (x, y, z, w), not Euler angles. Quaternions avoid
   gimbal lock and are the standard representation in ROS 2.
