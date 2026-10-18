"""An action from both sides: goal, feedback, cancel, result.

The server stands in for a robot skill: it closes a gripper from 0.085 m to the
goal position in 0.0085 m steps, one step every 0.2 s, and sends feedback after
each step. The client sends two goals. It lets the first one finish and cancels
the second one after 0.5 s, the way a behavior tree stops a running skill.

control_msgs comes with ARIAC 2025 (its joint trajectory controllers use it).
"""

import threading
import time

import rclpy
from action_msgs.msg import GoalStatus
from control_msgs.action import GripperCommand
from rclpy.action import ActionClient, ActionServer, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

OPEN, STEP, PERIOD = 0.085, 0.0085, 0.2
STATUS = {
    GoalStatus.STATUS_SUCCEEDED: "SUCCEEDED",
    GoalStatus.STATUS_CANCELED: "CANCELED",
    GoalStatus.STATUS_ABORTED: "ABORTED",
}


class GripperServer(Node):
    def __init__(self):
        super().__init__("gripper_server")
        ActionServer(
            self,
            GripperCommand,
            "gripper/command",
            self.execute,
            cancel_callback=lambda goal: CancelResponse.ACCEPT,
        )

    def execute(self, goal_handle):
        target = goal_handle.request.command.position
        position = OPEN
        feedback = GripperCommand.Feedback()
        while position > target + 1e-9:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return GripperCommand.Result(position=position)
            time.sleep(PERIOD)
            position = max(target, position - STEP)
            feedback.position = position
            goal_handle.publish_feedback(feedback)
        goal_handle.succeed()
        return GripperCommand.Result(
            position=position, reached_goal=True
        )


def wait(future):
    while not future.done():
        time.sleep(0.01)
    return future.result()


def run_goal(client, target, cancel_after=None):
    feedback = []
    goal = GripperCommand.Goal()
    goal.command.position = target
    handle = wait(
        client.send_goal_async(
            goal,
            feedback_callback=lambda msg: feedback.append(
                msg.feedback.position
            ),
        )
    )
    print(f"goal to {target:.3f} m: accepted={handle.accepted}")
    result_future = handle.get_result_async()
    if cancel_after is not None:
        time.sleep(cancel_after)
        wait(handle.cancel_goal_async())
        print(f"  cancel requested after {cancel_after} s")
    result = wait(result_future)
    print(
        f"  {len(feedback)} feedback messages, last {feedback[-1]:.4f} m"
    )
    print(
        f"  status {STATUS.get(result.status, result.status)}, "
        f"result position {result.result.position:.4f} m"
    )


def main():
    rclpy.init()
    server, client_node = GripperServer(), Node("skill_client")
    client = ActionClient(
        client_node, GripperCommand, "gripper/command"
    )
    # execute() holds one thread until the goal ends. A multi-threaded
    # executor takes the cancel request on another thread; a single-threaded
    # one sees it only after the goal has ended SUCCEEDED.
    executor = MultiThreadedExecutor()
    executor.add_node(server)
    executor.add_node(client_node)
    spinner = threading.Thread(target=executor.spin)
    spinner.start()
    client.wait_for_server()
    run_goal(client, 0.0)  # runs to the end
    run_goal(client, 0.0, cancel_after=0.5)  # stopped partway
    executor.shutdown()
    spinner.join()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
