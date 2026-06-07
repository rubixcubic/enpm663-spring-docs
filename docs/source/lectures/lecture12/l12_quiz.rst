====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: ROS 2 Communication
Patterns. Topics include services (request-response), actions
(goal-feedback-result), ``.srv`` and ``.action`` file formats, async
patterns, goal handling, feedback, and CLI tools.

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

   Which ROS 2 communication pattern is best suited for streaming
   continuous sensor data such as LiDAR scans?

   A. Service

   B. Action

   C. Topic (publish-subscribe)

   D. Parameter

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Topic (publish-subscribe)

   Topics use the publish-subscribe pattern, which is designed for
   continuous, many-to-many data streams. LiDAR data is published at a
   fixed rate and consumed by any number of subscribers.


.. admonition:: Question 2
   :class: hint

   In a ``.srv`` file, what separates the request fields from the
   response fields?

   A. ``===``

   B. ``---``

   C. ``***``

   D. A blank line

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``---``

   The three-dash separator ``---`` divides the request section (above)
   from the response section (below) in a ``.srv`` file.


.. admonition:: Question 3
   :class: hint

   How many ``---`` separators does a ``.action`` file contain?

   A. 0

   B. 1

   C. 2

   D. 3

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 2

   An ``.action`` file has three sections (goal, result, feedback)
   separated by two ``---`` lines.


.. admonition:: Question 4
   :class: hint

   Which method is used to send a request from a service client in
   ``rclcpp``?

   A. ``send_request()``

   B. ``call_service()``

   C. ``async_send_request()``

   D. ``request_service()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``async_send_request()``

   In ``rclcpp``, service clients use ``async_send_request()`` to send
   a request. The method returns a future that resolves when the
   response is received.


.. admonition:: Question 5
   :class: hint

   What happens if a service server takes a long time (e.g., 30
   seconds) to process a request?

   A. The client automatically retries

   B. The client blocks waiting, and the server's executor thread is
      occupied

   C. ROS 2 automatically times out and returns an error

   D. The request is forwarded to another server

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The client blocks waiting, and the server's executor thread
   is occupied

   Services are designed for quick request-response interactions. If the
   server takes too long, the client waits and the executor thread is
   blocked. For long-running tasks, use an action instead.


.. admonition:: Question 6
   :class: hint

   Which callback in an action server decides whether to accept or
   reject an incoming goal?

   A. ``handle_cancel``

   B. ``handle_accepted``

   C. ``handle_goal``

   D. ``execute``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``handle_goal``

   The ``handle_goal`` callback receives the goal request and returns
   either ``ACCEPT_AND_EXECUTE``, ``ACCEPT_AND_DEFER``, or ``REJECT``.


.. admonition:: Question 7
   :class: hint

   In an action server, which method is used to send periodic progress
   updates to the client?

   A. ``goal_handle->send_feedback()``

   B. ``goal_handle->publish_feedback()``

   C. ``goal_handle->update()``

   D. ``goal_handle->notify()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``goal_handle->publish_feedback()``

   The ``publish_feedback()`` method on the goal handle sends a
   feedback message to the action client.


.. admonition:: Question 8
   :class: hint

   Which ROS 2 CLI command calls a service from the terminal?

   A. ``ros2 service send``

   B. ``ros2 service request``

   C. ``ros2 service call``

   D. ``ros2 service invoke``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``ros2 service call``

   The ``ros2 service call`` command sends a request to a service and
   displays the response.


.. admonition:: Question 9
   :class: hint

   What does the ``--feedback`` flag do when used with
   ``ros2 action send_goal``?

   A. It makes the action synchronous

   B. It displays feedback messages as they are published by the server

   C. It sends additional feedback data with the goal

   D. It enables verbose logging on the server

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It displays feedback messages as they are published by the
   server

   Without ``--feedback``, the CLI command waits silently for the
   result. With ``--feedback``, it also prints each feedback message as
   it arrives.


.. admonition:: Question 10
   :class: hint

   Which package must be added as a dependency when implementing an
   action server or client in C++?

   A. ``rclcpp_components``

   B. ``rclcpp_action``

   C. ``action_msgs``

   D. ``rosidl_default_generators``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``rclcpp_action``

   The ``rclcpp_action`` package provides the ``create_server`` and
   ``create_client`` functions for actions. It must be listed in both
   ``CMakeLists.txt`` (``find_package``) and ``package.xml``
   (``<depend>``).


----


True/False (Questions 11--15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** A ROS 2 service supports multiple servers
   advertising on the same service name.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A service name is served by exactly one server. If multiple servers
   advertise the same name, behavior is undefined and requests may be
   routed unpredictably.


.. admonition:: Question 12
   :class: hint

   **True or False:** An action client can cancel a goal that is
   currently being executed by the server.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Actions support goal cancellation. The client can send a cancel
   request, and the server's ``handle_cancel`` callback decides whether
   to accept it.


.. admonition:: Question 13
   :class: hint

   **True or False:** The ``---`` separator in a ``.srv`` file is
   optional if the response section is empty.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``---`` separator is always required in a ``.srv`` file, even if
   the response section has no fields (as in ``std_srvs/srv/Empty``).


.. admonition:: Question 14
   :class: hint

   **True or False:** In ``rclcpp``, ``wait_for_service()`` blocks
   until the service server is available or the timeout expires.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``wait_for_service()`` returns ``true`` when the service becomes
   available, or ``false`` if the timeout expires. It blocks the calling
   thread while waiting.


.. admonition:: Question 15
   :class: hint

   **True or False:** Actions are implemented entirely using a single
   topic under the hood.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Actions are built on a combination of **topics** (for feedback) and
   **services** (for goal submission, cancellation, and result
   retrieval). The ``rclcpp_action`` library abstracts these details.
