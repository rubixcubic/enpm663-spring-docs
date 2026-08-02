# ENPM663 Spring 2027: What Changed

A short summary of the redesign. The predecessor was ENPM663 "Building a
Manufacturing Robot Software System" (Spring 2025, co-taught). The new version is
**ENPM663 Building AI-Augmented Robotic Systems** (Spring 2027, solo).

## The big idea

The course now teaches how modern AI is integrated into an otherwise classical
ROS 2 robotics stack. AI is concentrated at the **task-planning layer** (LLM
agents and VLM grounding); motion planning, grasp execution, and control stay
**classical** (MoveIt2). The classical-to-AI contrast (PDDL first, then an LLM
agent) is the centerpiece.

## What is new

- **New title and framing.** "Manufacturing" dropped to broaden appeal; the
  focus is general AI-augmented robotics, not manufacturing.
- **AI direction.** LLM **agents** for task planning (the observe-act-observe
  loop, tool use via MCP, structured output), VLM grounding, and agentic
  closed-loop replanning. The vision-language-action (VLA) frontier is surveyed
  but not built (no policy training, no GPU dependency).
- **ROS 2 assumed, not taught.** It is now a prerequisite; Week 1 is a refresher
  plus an ungraded diagnostic, instead of three weeks of ROS 2 from scratch.
- **Python-primary.** C++ appears only where it is the industry standard (read,
  not write).
- **Team-only.** Five cumulative team projects (PT1 to PT5), no individual
  assignments and no separate final. PT5 is the capstone, graded live on an
  **unseen ARIAC scenario**.
- **Grading.** 60% team projects / 25% quizzes / 15% peer-review contribution.
- **New content weeks.** Dedicated Knowledge Representation week (W3); a
  Recovery, Robustness, and Failure Handling week (W12) replacing learned
  grasping.

## What was dropped

- PlanSys2 (limited industry adoption); PDDL the language stays, executed via a
  behavior tree.
- Guest lectures (room reallocated to AI content).
- Learned grasp prediction (kept the AI surface area teachable in one semester).

## Stack

Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + ARIAC 2025. Behavior trees via
`py_trees_ros`; PDDL via Fast Downward or the Unified Planning Framework; motion
via MoveIt2; LLM/VLM via hosted APIs or local open-weight models.

## Structure at a glance

15 weeks (Week 8 Spring Break) in four arcs: Foundations (W1 to W4),
Classical-to-AI Planning (W5 to W10), Motion / Recovery / Evaluation (W11 to
W13), and the PT5 Capstone (W14 to W15).
