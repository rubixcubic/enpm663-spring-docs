# ENPM663 Spring 2027: What Changed

A short summary of the redesign. The predecessor was ENPM663 "Building a
Manufacturing Robot Software System" (Spring 2025, co-taught). The new version is
**ENPM663 Agentic Physical AI for Manufacturing Robotics** (Spring 2027, solo).

## The big idea

The course teaches how to build robot systems in which AI agents decide what a
factory cell does next and classical robotics carries it out. AI is concentrated
at the **task-planning layer** (LLM agents and VLM grounding); motion planning,
grasp execution and control stay **classical** (MoveIt 2). The classical-to-AI
contrast (PDDL first, then an LLM agent) is the centerpiece. The last lecture
surveys the learned side of physical AI (VLA models, robot foundation models,
world models), and the final demo uses one hosted embodied-reasoning model.

## What is new

- **New title.** "Agentic Physical AI for Manufacturing Robotics" (chosen
  2026-10-11). It brings "manufacturing" back, which matches the ARIAC 2025
  battery factory.
- **AI direction.** LLM **agents** for task planning (the observe, act, observe
  loop, tool use via MCP, structured output), VLM grounding, and agentic
  closed-loop replanning. No policy training and no GPU requirement.
- **ROS 2 assumed, not taught.** It is a prerequisite; L1 is a refresher plus an
  ungraded diagnostic, instead of three weeks of ROS 2 from scratch.
- **Python-primary.** C++ appears only where it is the industry standard (read,
  not write).
- **Team-only final project.** Four cumulative group projects (GP1 to GP4) and a
  final demo graded on an **unseen ARIAC trial**, run by the instructor from
  each team's Docker image. No individual
  assignments and no final exam.
- **Lectures only.** No in-class exercises and no lab sessions.
- **Grading.** 60% final project (GP1 to GP4 at 10% each, final demo at 20%) /
  25% quizzes / 15% peer-review contribution.
- **New content.** A Knowledge Representation lecture (L3), a Recovery,
  Robustness, and Failure Handling lecture (L11), and a Physical AI Frontier
  lecture (L13).
- **ARIAC 2025.** The projects use the EV battery factory: cell inspection, kit
  building, module construction, and its challenges (conveyor, voltage tester
  and vacuum tool malfunctions, high-priority orders).
- **Course skills package.** ARIAC 2025 gives no pick or place skills, so the
  course provides them on MoveIt 2 from GP1 on.

## What was dropped

- PlanSys2 (limited industry adoption); PDDL the language stays, executed via a
  behavior tree.
- Guest lectures (room reallocated to AI content).
- Learned grasp prediction (kept the AI surface area teachable in one semester).
- In-class exercises and the Week 14 lab.

## Stack

Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + ARIAC 2025. Behavior trees via
`py_trees_ros`; PDDL via Fast Downward or the Unified Planning Framework; motion
via MoveIt 2; LLM and VLM via hosted APIs or local open-weight models.

## Structure at a glance

Wednesdays, Jan 27 to May 5, 2027 (spring break Mar 14 to 21). 13 lectures
(L1 to L13) in Weeks 1 to 14, Week 8 spring break, and the final demo in Week 15.
