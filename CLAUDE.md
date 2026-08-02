# CLAUDE.md - ENPM663 Spring 2027

This file gives Claude (or any collaborator using Claude) the context needed to work on
the ENPM663 "Building AI-Augmented Robotic Systems" course development project without
re-litigating the design decisions every session.

Read this file at the start of any new conversation about this course.

---

## 1. Project Overview

**Course:** ENPM663 - Building AI-Augmented Robotic Systems
**Term:** Spring 2027
**Institution:** University of Maryland, MAGE program
**Instructor:** Zeid (Rob) Kootbally, solo
**Credits:** 3
**Format:** Hands-on, in-class lectures + exercises, weekly meetings
**Predecessor:** ENPM663 "Building a Manufacturing Robot Software System" (Spring 2025,
co-taught with Craig Schlenoff)

### What is this course?

A graduate hands-on course that teaches how modern AI techniques (LLMs, VLMs, learned
manipulation components) are integrated into ROS 2 based robotic systems. The course is
structured around the ARIAC 2025 testbed but teaches general patterns for AI-augmented
robotics. Students come in with ROS 2 knowledge; this course extends classical task and
motion planning with AI-augmented counterparts at each layer.

### What is this course not?

- Not a ROS 2 from-scratch course (assumed prerequisite)
- Not a deep reinforcement learning course (no policy training)
- Not a manufacturing-specific course (the word "manufacturing" was deliberately removed
  from the title to broaden appeal and signal generality)
- Not a pure research course (engineering and integration are the focus)

---

## 2. Session Resume

This section lets a new Claude session pick up where the last one left off without
replaying the whole conversation. Section 2.1 is a fixed protocol; Section 2.2 is live
state that should be refreshed at the end of every working session.

### 2.1 Resume Protocol

At the start of a new session on this project:

1. Read this whole file. The decision log (Section 3) holds rationales that are not
   re-derivable from the file tree.
2. Read Section 2.2 (Current Status) below to see what was in flight at the end of the
   last session and what the next concrete step is.
3. Cross-check the status note against reality. Run `git status`, `git log --oneline
   -10`, and `ls` of the working directory. If the file tree disagrees with the status
   note, trust the file tree and correct the note before doing anything else.
4. Skim Section 7 (Open Items and Known Risks). Some items there can block the next
   step.
5. Confirm the working directory is `/home/zeid/github/docs/enpm663-spring-2027-docs`.
6. Before starting new work, confirm with Rob what the next step actually is. The
   status note records intent, not authorization.

At the end of every working session, update Section 2.2 (and the timestamp at the
bottom of the file) so the next session has accurate state.

### 2.2 Current Status

*Live state. Update at the end of every session. Keep it short; details belong in
commits, not here.*

**Last updated:** 2026-08-02

- **Repo state:** `main` branch. Two commits ("first push" then the Spring 2027
  redesign commit). Working tree has uncommitted edits from Session 2 (see below).
  The repo is a Sphinx + ReadTheDocs project; see Section 6 for the real file layout.
- **Recently completed (Session 2, 2026-08-02):**
  - Industry-currency review of the 15 lecture stubs, including a web check of the
    2026 agent-framework and VLA landscape.
  - Reframed the LLM thread (W9, W10) around the modern agent loop instead of the
    dated one-shot-planner framing; added MCP, plan-and-execute vs. ReAct, tool
    design, context/memory, and an explicit "when classical PDDL wins" boundary.
    Titles updated. See the new decision-log entry Section 3.13.
  - Added a VLA / robot-foundation-model survey segment to W2 (survey only, no
    hands-on; the no-learned-manipulation scope is unchanged) plus a
    multi-robot-coordination-as-multi-agent mention.
  - Fixed the four smaller flags: W10/W11 motion ordering note (PT4 uses ARIAC action
    servers), MCP in W9, multi-robot mention, W10 classical-wins honesty note.
  - Corrected stale content: Section 4.3 arcs (dropped "learned grasping" and "guest
    lecture" leftovers, re-aligned week ranges to the KR-shifted outline) and a
    "Week 2 refresher" reference in `syllabus.md` that should read "Week 1".
  - Renamed the course "AI-Augmented Robot Software Systems" -> "Building
    AI-Augmented Robotic Systems" (Rob's pick; see Section 3.1). Updated across
    `syllabus.md`, `CLAUDE.md`, `index.rst`, `README.md`.
  - Rebranded the Sphinx site from the leftover ENPM702 (C++) course to ENPM663:
    `conf.py` (project, navbar text, logo image paths, GitHub URLs), `index.rst`
    (full landing-page rewrite), `README.md`, `_templates/custom-footer.html`.
    ASSET TODO: `_static/images/enpm663_logo_{light,dark}.png` do not exist yet;
    the theme falls back to the text logo until they are added. Also confirm the
    GitHub repo slug `zeidk/enpm663-spring-2027-docs` and the RTD project name.
  - Changed the testbed from ARIAC 2026 to **ARIAC 2025** (Ubuntu 24.04) per Rob's
    instruction; reverses the 2026-06-07 call. See Section 3.7. Propagated across
    `syllabus.md`, `CLAUDE.md`, and `lecture1/l1_index.rst`. Open item #3 in
    Section 7 is now resolved.
  - Full ENPM702 -> ENPM663 site cleanup (all toctree-reachable pages). Rewrote
    `assignments/` (new `pt1.rst`..`pt5.rst` from the syllabus PT descriptions;
    `index.rst` PT table; deleted `rwa1-3.rst`, `gp1-3.rst`); `setup/` (rewrote
    `setup.rst`, trimmed `ubuntu_setup.rst` to 24.04-only, fixed `ros_setup.rst`
    to Week 1 + Gazebo Harmonic, deleted `cpp_setup.rst`, added `ariac_setup.rst`
    and `ai_setup.rst`); `reading_material/` (ENPM663 supplemental-topics index;
    deleted the `flow_control/`, `exception_handling/`, `version_control/`
    subdirs); `glossary/glossary.rst` (ENPM663 starter glossary via the Sphinx
    glossary directive); `changelog/changelog.rst`; and `syllabus/syllabus.rst`
    (ENPM663 at-a-glance: 60/25/15 + outline, pointing to the canonical
    `syllabus.md`). Deleted all 60 orphaned old per-section lecture files
    (`lN_lecture/exercises/shell/quiz/references.rst`); only `lN_index.rst`
    remain. Fixed ENPM702/en-dash header comments in the two `_static` CSS files.
  - Verified with a local Sphinx build (`cd docs && make html`): builds clean,
    0 warnings. Only remaining notice is the missing enpm663 logo PNGs (expected;
    theme falls back to text logo).
- **Repo file note:** Untracked/obsolete `syllabus_spring2027_enpm663.pdf` still in
  repo root; `syllabus.md` remains the canonical syllabus.
- **Recently completed (Session 1, 2026-06-06):**
  - Initial course redesign conversation that produced `CLAUDE.md` and a draft
    syllabus PDF.
  - Reviewed the draft syllabus and flagged inconsistencies (notably a 25% "Team
    Projects" grading line with no team project in the schedule).
  - Switched the assignment model: no individual track and no separate Final Project.
    The course now uses 5 team projects (PT1 through PT5), with PT5 as the unseen-
    ARIAC capstone replacing the old Final Project demo. Grading is now 60% team
    projects / 25% quizzes / 15% peer-review contribution. PT1 through PT4 weigh 10%
    each, PT5 weighs 20%. See Sections 3.10, 3.11, 4.1, 4.2, and 8.
  - Settled team-formation logistics: team size 3, teams formed Week 3, stable across
    all 5 PTs.
  - Designed the peer-review instrument: 5-dimension Likert (technical contribution,
    reliability/communication, quality, knowledge/skill, team-player behavior),
    required short comments, confidential concern flag, instructor review of outliers
    and sub-70 scores. Recorded in `syllabus.md`.
  - Wrote `syllabus.md` at the repo root as the canonical syllabus. The original
    `syllabus_spring2027_enpm663.pdf` is now obsolete (reference only).
  - Discovered the repo is a Sphinx + RTD project (not a flat tree); rewrote
    Section 6 to reflect actual structure.
  - User chose to keep `syllabus.md` at the repo root as working draft; porting into
    the Sphinx site (`docs/source/syllabus/syllabus.rst`) is deferred.
  - Scope correction: dropped Learned Grasp Prediction (W11). The AI surface area was
    too wide for one semester. AI is now bounded to LLM + VLM task planning with
    closed-loop replanning; motion planning and grasp execution remain classical
    (MoveIt2 with parameterized grasps). W11 was replaced with "Recovery, Robustness,
    and Failure Handling for AI-Driven Systems." The learned-grasping learning
    outcome was swapped for a recovery/robustness outcome; outcome count stays at 8.
    Cascaded updates: `syllabus.md` (Course Description, Learning Outcomes, W11 row,
    PT5 scenario paragraph), `CLAUDE.md` (Sections 3.2, 3.12, 4.1, 5.4, 7, 8).
  - Established lecture-design conventions (Section 5.7): every lecture must include
    hands-on activities and tie content to ARIAC where applicable. Primary ARIAC
    reference URLs (GitHub repo and ReadTheDocs site) added to Section 5.6 so all
    lecture authors consult them when designing exercises and ARIAC ties.
  - Added dedicated Knowledge Representation week (W3) using the 2023 KR lecture
    (`Lectures_export/KR-Lecture-Spring2023.pptx`) as source material. The 2023 NIST
    road-network examples will be re-anchored to ARIAC (orders, parts, kits as
    frame-based representations) when the new W3 lecture is authored. The Guest
    Lecture at W13 was dropped to make room. All topics from old W3 onward shift +1;
    PT1 due W5, PT2 hand W5/due W7, PT3 hand W7/due W10, PT4 hand W10/due W13. PT5
    hand stays at W12 (one week before PT4 due) to preserve the 4-week capstone
    window. Quizzes shift: Q1 W4, Q2 W5, Q3 W7, Q4 W10, Q5 W12. KR became a 9th
    learning outcome (count 8 -> 9). Cascaded updates: `syllabus.md` (Learning
    Outcomes, Course Outline), `CLAUDE.md` (Sections 3.6, 3.9, 3.12, 4.1, 4.2, 5.7,
    8).
  - Drafted high-level descriptions for all 5 Team Projects (PT1 through PT5),
    each including goal, ARIAC tie, and deliverable. Recorded as a new "Team
    Project Descriptions" section in `syllabus.md`. The old PT5 scenario-design
    paragraph in the Course Outline was removed (subsumed by the new section). The
    Section 4.2 PT table in CLAUDE.md remains the canonical hand-out/due/weight
    reference; full descriptions will eventually move to
    `docs/source/assignments/pt1.rst` through `pt5.rst` per Section 6.
  - Replaced the ENPM702 (C++/ROS-from-scratch) lecture stubs in the Sphinx site
    with ENPM663 stubs for all 15 weeks. Each `lectureN/lN_index.rst` (N=1..15)
    now has Overview, Learning Objectives, Topics, Hands-On Exercise, ARIAC
    Tie-in, References, and Next Steps sections per the Section 5.7 convention.
    New folders created for `lecture14/` (PT5 Lab) and `lecture15/` (PT5 Demo).
    `lecture8/l8_index.rst` is a Spring Break placeholder. `lectures/index.rst`
    was rewritten with an ENPM663 overview and a four-arc toctree (Foundations,
    Classical-to-AI Planning, Motion/Recovery/Evaluation, PT5 Capstone). The old
    per-section files (`lN_lecture.rst`, `lN_exercises.rst`, `lN_shell.rst`,
    `lN_quiz.rst`, `lN_references.rst`) still contain ENPM702 content and are
    now orphaned (not in any toctree); cleanup is a follow-up task.
- **In progress:** none.
- **Next step (Session 2 starting point):** begin Week 1 lecture content (Course
  Overview + ROS 2 Refresher, plus the ungraded diagnostic quiz). Expected artifacts
  are a Beamer slide deck and a lecture notes page under
  `docs/source/lectures/week01_ros2_refresher/`. Before starting, settle the Beamer
  slide-deck location convention (see Section 6, "Lecture slide decks").
- **Open follow-ups (not blocking Week 1):**
  - Late-penalty schedule: filled 2026-08-02 with a proposed default (10% per calendar
    day, up to 3 days, no credit after). Rob to confirm or adjust.
  - `syllabus.pdf` is generated from `syllabus.md` via pandoc + xelatex (repo root,
    11 pages). Regenerate after editing `syllabus.md`:
    `pandoc syllabus.md -o syllabus.pdf --pdf-engine=xelatex -V geometry:margin=1in`
    `-V fontsize=11pt -V colorlinks=true -V linkcolor=RoyalBlue -V urlcolor=RoyalBlue`
    `-V documentclass=article --toc --toc-depth=2`. Do NOT use pdflatex (pandoc's
    default template pulls in `lmodern`, which is not installed; xelatex avoids it).
  - Still TODO inside `syllabus.md` (cannot be filled without UMD info): Spring 2027
    course dates, weekly meeting time, and classroom (all marked `TODO: verify`).
  - Team contract document (signed by teams at formation in Week 3) recommended but
    not yet drafted. Reinforces the peer-review system.
  - PT5 specific challenge selection and live-demo grading rubric to be written when
    PT5 is detailed (target: before PT4 begins, so teams can plan ahead).
  - Site syllabus page (`syllabus/syllabus.rst`) is now an ENPM663 at-a-glance; a full
    port/render of `syllabus.md` into the Sphinx site is still deferred.
  - The obsolete `syllabus_spring2027_enpm663.pdf` (v1) is now superseded by the
    generated `syllabus.pdf`; safe to delete once Rob confirms.

---

## 3. Course Design Decisions and Their Rationales

This section is the decision log. When in doubt about why something is the way it is,
look here before changing it.

### 3.1 Title: "Building AI-Augmented Robotic Systems"

Chosen over alternatives like "Foundation Models for Robotic Systems" (too narrow),
"Intelligent Robotic Systems: Planning and Perception" (loses the software-engineering
emphasis), and "Building Intelligent Robot Software Systems" (kept too much of the old
title). "AI-Augmented" is accurate without overpromising: AI is added at specific layers
of an otherwise classical robotics stack. The working name was "AI-Augmented Robot
Software Systems"; on 2026-08-02 Rob chose "Building AI-Augmented Robotic Systems" to
foreground the hands-on, integration-heavy, team-project nature of the course (the
"Building" verb echoes the spirit of the 2025 predecessor title).

### 3.2 AI direction: LLM + VLM task planning, classical motion

Originally framed as "Hybrid (LLM/VLM planning + learned grasping)." Learned grasping
was removed on 2026-06-07 in a scope review (see Section 2.2). AI is now concentrated
at the task-planning layer; motion planning, grasp execution, and control stay
classical.

- AI components: LLM-based task planning (W7), VLM grounding for scene understanding
  (W9), closed-loop replanning (W9), and recovery/robustness patterns for failure
  handling (W11).
- Classical components: ROS 2 and behavior trees for execution (W1, W3, W6), OpenCV
  for low-level perception (W4), PDDL for the classical-planning baseline (W5),
  MoveIt2 for motion planning and parameterized-grasp execution (W10).

Considered alternatives:

1. Perception + classical planning (rejected: too close to a CV course).
2. LLM/VLM-driven task planning (the chosen direction).
3. Learning-based manipulation / RL (rejected: requires GPU access we cannot assume;
   opaque failure modes; out of scope for one semester).
4. Hybrid LLM/VLM + learned grasping (originally chosen; pulled back because the AI
   surface was too wide to teach with depth in one semester).

Why this scope works:

- **Industry alignment.** Manufacturing-robotics companies increasingly use LLMs for
  task reasoning while keeping motion planning and control classical. This matches
  what students will encounter in industry.
- **Gradable on unseen ARIAC scenarios.** LLM-based plans produce inspectable traces;
  learned-policy failures are opaque. We grade engineering judgment, not model
  generalization.
- **Preserves the PDDL/planning teaching investment.** Classical task planning stays
  as the contrasting baseline before introducing LLM planning.
- **Honest one-semester scope.** Adding learned grasping required a full week of new
  ML concepts (point clouds, pre-trained grasp networks) plus integration plumbing,
  which crowded out depth in the task-planning thrust that is the course's main
  thesis.

### 3.3 Language: Python primary, C++ where it is the industry standard

The 2025 course supported both languages in parallel, which doubled the work. For 2027,
Python is the primary teaching language. C++ shows up only for:

- Reading code in industry-standard libraries (BehaviorTree.CPP, MoveIt2 internals)
- Real-time control components where C++ is the dominant production choice
- Brief exposure in one lecture (BehaviorTree.CPP) so students can read and contribute
  to industry codebases

Students are not required to write substantial C++ in assignments.

### 3.4 ROS 2 prerequisite: assumed, with a Week 1 refresher

Old course taught ROS 2 from scratch over weeks 1 to 3. New course assumes incoming
knowledge and uses Week 1 only for a calibration refresher on the topics most used in
the course (lifecycle nodes, TF2, QoS, executors). A diagnostic quiz in Week 1
calibrates the actual knowledge level; it is ungraded.

If a substantial fraction of students fail the diagnostic, the instructor may need to
expand the refresher into Week 2 and cut something later. This is a known risk.

### 3.5 PlanSys2: dropped

PlanSys2 was the PDDL-execution framework in the 2025 course. Dropped for 2027 because:

- PlanSys2 has limited industry adoption; it is primarily academic
- Teaching PlanSys2 the framework takes ~2 weeks; we cannot afford that time
- The PDDL output is now consumed by a BT-based executor instead, which aligns with
  industry practice

Students still learn PDDL the language and classical planning the algorithm (Week 5),
using Fast Downward or Unified Planning Framework as the planner. The plans are
then executed via a behavior tree, not PlanSys2.

### 3.6 Behavior trees: `py_trees_ros` primary, `BehaviorTree.CPP` one lecture

BTs are the industry-standard task execution substrate in modern robotics (Nav2,
MoveIt2, Boston Dynamics, Pickle, Symbotic, Path Robotics, etc.). They are the right
choice; the alternatives (FSMs, HTNs, direct LLM loops without BTs) have specific
weaknesses for production systems.

`py_trees_ros` is the primary teaching tool because Python is the primary course
language. `BehaviorTree.CPP` is shown in one lecture so students can read industry
codebases that use it.

BTs appear in two places in the course:

- Week 4: BT foundations (language, patterns, basic execution)
- Week 7: BT-based plan execution (executing externally-produced plans, recovery)

### 3.7 ARIAC version: ARIAC 2025 (per instructor preference)

Per Zeid's instruction (2026-08-02), the course references **ARIAC 2025**, running on
Ubuntu 24.04. This reverses the earlier 2026-06-07 call that pinned "ARIAC 2026"; Rob
is closer to NIST and makes the call on the version label. NIST's cycle around this
time is "ARIAC 2025-2026"; Rob chose the "ARIAC 2025" label. If the cycle is renamed
before spring 2027, update the syllabus and lectures accordingly. The `/latest/` doc
URL pins to the active cycle and is safe to link regardless of the label.

### 3.8 Software stack: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic

This is what ARIAC currently uses (as of the 2025-2026 release). Updated from the 2025
course which used Ubuntu 22.04 + ROS 2 Iron.

### 3.9 Guest lectures: dropped (originally two)

Old course had two guest lectures in weeks 12-13. Cut to one (Week 13) early in the
2027 redesign to make room for AI content. Updated 2026-06-07: the remaining guest
lecture was dropped entirely to make room for a dedicated Knowledge Representation
week (W3); see Section 2.2. The course now has no external speaker slot. The
instructor may still invite a guest to deliver a brief segment within a regular
week's lecture if a speaker is available.

### 3.10 Assignments: 5 team projects, no individual track, no separate final

Original design (and the v1 syllabus PDF) had 4 individual assignments + 1 individual
Final Project, with a separate 25% "Team Projects" line in the grading table that did
not correspond to anything in the schedule. That inconsistency was resolved on
2026-06-06 by going team-only:

- All 4 former individual assignments become Team Projects PT1 through PT4, on the
  same handout/due schedule.
- A 5th team project, PT5, is added on weeks 12 to 15 as the capstone, replacing the
  separate Final Project. PT5 is evaluated on an unseen ARIAC scenario, demoed live in
  Week 15. This preserves the unseen-scenario pedagogy that originally lived in the
  Final Project.
- Individual accountability is preserved through Quizzes (25%, closed-notes) and a
  Peer-Review Contribution category (15%) assessed by teammates after each PT.

Rationale: integration-heavy ROS 2 robotic systems are best built in teams, mirroring
industry practice, and the v1 syllabus already implicitly assumed team work via the
peer-review system and the orphaned 25% "Team Projects" line. Going fully team also
defuses the LLM-era integrity question of "did you actually write this yourself," since
teams must defend the work in peer review and PT5's live demo.

PT4 (LLM planner) still extends PT3 (PDDL + BT executor) so the classical-to-AI
contrast remains pedagogically central.

### 3.11 Grading: 60/25/15 (Team Projects / Quizzes / Peer-Review Contribution)

Updated 2026-06-06 when individual assignments and the separate Final Project were
removed (see Section 3.10).

- **Team Projects: 60%.** PT1 through PT4 are 10% each (40% total). PT5, the unseen-
  ARIAC capstone, is 20%. The capstone is double-weighted because it integrates every
  prior component and is the only deliverable evaluated on an unseen scenario.
- **Quizzes: 25%.** Raised from 20% in the v1 grading scheme. Quizzes are the primary
  individual-accountability signal now that there is no individual assignment track.
- **Peer-Review Contribution: 15%.** Replaces the v1 ambiguous Participation line.
  Assessed by teammates after each PT; one combined category, not split into class
  participation and peer review.

The change from 25/20/25/30 to 60/25/15 reflects: (a) one combined Team Projects line
instead of separate Individual + Team + Final lines, (b) quizzes raised slightly to
strengthen individual accountability, (c) intra-team contribution replaces the
ambiguous class-participation line.

### 3.12 Learning outcomes: rewritten from scratch

The 2025 outcomes were rewritten rather than incrementally edited because the AI focus
requires different framing. 9 outcomes (was 6 in 2025), covering architectures,
knowledge representation, BTs, PDDL, LLM planning, VLM grounding, recovery and
robustness, motion planning, and evaluation. The 8th original 2027 outcome on
learned grasping was replaced with recovery/robustness (see Section 3.2). A 9th
outcome on knowledge representation was added on 2026-06-07 when a dedicated KR
week was introduced (see Section 2.2).

### 3.13 LLM thread reframed as agents; VLA frontier surveyed (2026-08-02)

An industry-currency review (with a web check of the 2026 agent-framework and VLA
landscape) found the LLM thread was framed in a pre-agentic (2022 to 2023) way: the
LLM was treated as a stateless one-shot planner with a replan trigger. That framing
is dated. The 2026 industry standard is the *agent loop* (an orchestrator runs
observe-reason-act-observe around the LLM; ReAct and plan-and-execute are the dominant
patterns), with tools exposed through MCP (Model Context Protocol), which by 2026 is
the standard tool-integration layer across LangGraph, the OpenAI Agents SDK, and the
Claude Agent SDK.

Decision: reframe W9 and W10 around the agent loop rather than add a new week (the
week count is unchanged). W9 becomes "Agent Loops, Tool Use, and Structured Output";
W10 becomes "VLM Grounding and Agentic Replanning." Added concepts: the agent loop and
orchestrator, plan-and-execute vs. ReAct, tool design, MCP, context/memory management,
and an explicit "when classical PDDL is the better tool" boundary (LLM agents earn
their place on ambiguity, novelty, and recovery, not the happy path). PT4 is now framed
as an LLM *agent*. This is a framing change, not a scope expansion; no GPU or new ML is
introduced.

VLA scope: the deliberate no-learned-manipulation decision (Section 3.2, 3.5) is
UNCHANGED. Vision-language-action models (OpenVLA, Physical Intelligence pi-0, Gemini
Robotics, Figure Helix) are added to W2 as a *survey segment only* (no policy training,
no GPU, no hands-on), to acknowledge the frontier and justify the modular choice. A
useful teaching hook surfaced in the web check: the dominant 2026 VLA design is itself
two-system (a slow VLM for semantics plus a fast reactive control policy), which mirrors
this course's deliberative-plus-reactive split. A multi-robot-coordination-as-multi-agent
mention (ARIAC floor and ceiling robots) was also added to W2.

Cascaded updates: `l2_index.rst` (VLA survey, multi-robot mention), `l9_index.rst`
(agent-loop rewrite, MCP), `l10_index.rst` (agentic replanning, classical-wins honesty
note, MoveIt2/action-server ordering note), `syllabus.md` (Course Description, LLM
learning outcome, W9/W10 outline titles, PT4 description, plus a fix of a stale "Week 2
refresher" reference that should read "Week 1"), and this file (Section 4.1 titles,
this entry, Section 2.2). The learned-manipulation scope decision and the 9-outcome
count are unchanged.

---

## 4. Course Structure

### 4.1 Week-by-week outline

| Week | Topic | Deliverables |
|------|-------|--------------|
| 1 | Course Overview and ROS 2 Refresher | Diagnostic quiz (ungraded) |
| 2 | System Architectures for AI-Augmented Robotics | PT1 handed out |
| 3 | Knowledge Representation for AI-Augmented Robotics | Teams formed |
| 4 | Behavior Trees for Task Execution | Quiz #1 |
| 5 | Sensing and Perception for Robotic Systems | Quiz #2; PT1 due; PT2 handed out |
| 6 | Task-Level Planning with PDDL | -- |
| 7 | Plan Execution Patterns with Behavior Trees | Quiz #3; PT2 due; PT3 handed out |
| 8 | SPRING BREAK | -- |
| 9 | LLM-Based Task Planning I: Agent Loops, Tool Use, and Structured Output | -- |
| 10 | LLM-Based Task Planning II: VLM Grounding and Agentic Replanning | Quiz #4; PT3 due; PT4 handed out |
| 11 | Frames, Transforms, and Motion Planning | -- |
| 12 | Recovery, Robustness, and Failure Handling for AI-Driven Systems | Quiz #5; PT5 handed out |
| 13 | Evaluation and Measurement Science for AI-Augmented Systems | PT4 due |
| 14 | PT5 Lab | -- |
| 15 | PT5 Demo and Presentation | PT5 due |

### 4.2 Team Projects

All 5 are team-based; no individual track. Peer review after each PT feeds the 15%
Peer-Review Contribution category.

| PT | Topic | Hand out | Due | Weight |
|----|-------|----------|-----|--------|
| 1 | Behavior tree for a simple kitting workflow (py_trees_ros) | Week 2 | Week 5 | 10% |
| 2 | Perception pipeline (OpenCV + part pose extraction) | Week 5 | Week 7 | 10% |
| 3 | PDDL planner + BT executor (classical baseline) | Week 7 | Week 10 | 10% |
| 4 | LLM-based task planner extending PT3 + VLM grounding | Week 10 | Week 13 | 10% |
| 5 | Integrated system on unseen ARIAC scenario (capstone) | Week 12 | Week 15 | 20% |

### 4.3 The pedagogical arcs

The course is structured in four arcs. When developing lectures, keep the arc context
in mind:

1. **Foundations (weeks 1-4):** ROS 2 refresher, architectures (with a VLA-frontier
   survey), knowledge representation, BTs. By end of Week 4 students can build a simple
   BT over the KR designed in W3.
2. **Classical-to-AI Planning (weeks 5-10):** perception, PDDL, BT-based execution,
   then LLM agents for planning, then VLM grounding and agentic replanning. The
   intentional classical-to-AI contrast is the centerpiece.
3. **Motion, Recovery, and Evaluation (weeks 11-13):** MoveIt2 and parameterized
   grasps (no learned grasping, see Section 3.2), recovery/robustness, evaluation. By
   end of Week 13 students have all the components for the capstone.
4. **PT5 Capstone (weeks 14-15):** project lab and the live demo on an unseen ARIAC
   scenario. (No guest lecture; see Section 3.9.)

---

## 5. Working Instructions for Claude

### 5.1 Style rules (always apply)

These come from Rob's user preferences and supersede default conventions:

- **No em dashes (—) anywhere.** Use commas, parentheses, or semicolons instead.
- **No en dashes (–) anywhere.** Use hyphens or "to" instead (e.g., "weeks 5 to 9").
- **No `\vspace` in slides.** If you see `\vspace` in code Rob provides, keep it. Never
  add new ones to slide content.
- **Never use `\_`.** Prefer the bare `_` character (the `underscore` LaTeX package
  enables this).
- **No bullet points when declining a task** (general Claude rule).

### 5.2 Communication style

Rob values critical engagement. Specifically:

- Be accurate. Check results for consistency.
- Be critical. Do not always go with the flow.
- Ask relevant questions before providing solutions.
- Push back if something is wrong or sub-optimal.

Concretely, when Rob asks for X, do not immediately produce X if there are better
alternatives or unclear prerequisites. Surface the trade-offs first, then proceed.

When using `ask_user_input_v0`, prefer 2-3 well-scoped questions per round over a long
list. Lead with the most consequential question.

### 5.3 LaTeX conventions

- **Beamer slides:** use the Amurmaple theme with Rob's custom macros (see his other
  course repos for examples). Never add `\vspace` in slide content.
- **Article-class documents (syllabi, handouts):** clean article template with
  `geometry`, `fancyhdr`, `booktabs`, `longtable`, `hyperref`, `xcolor`, `underscore`,
  `enumitem`, `titlesec`. `lmodern` is NOT installed in the Claude code environment;
  default Computer Modern is fine.
- **Always compile twice** for `lastpage` and `longtable` reference resolution.
- **Always grep the final .tex for em-dashes, en-dashes, `\vspace`, and `\_`** before
  declaring done.

### 5.4 ROS 2 / robotics-stack conventions

- **ROS 2 distribution:** Jazzy Jalisco (LTS).
- **OS:** Ubuntu 24.04 LTS (Noble Numbat).
- **Simulator:** Gazebo Harmonic.
- **Primary language:** Python. Show C++ only where it is genuinely the industry
  standard for that component.
- **BT library:** `py_trees_ros` for teaching; show `BehaviorTree.CPP` in one lecture.
- **Planner:** PDDL via Fast Downward or Unified Planning Framework (Python).
- **Motion planning and grasp execution:** MoveIt2 with parameterized grasps. No
  learned grasp prediction (see Section 3.2).

### 5.5 AI / LLM conventions

- **Acceptable LLM access:** hosted APIs (Claude, GPT, Gemini) or local open-weight
  models (Llama, Qwen). Students choose. Some assignments may specify.
- **Function calling / structured output:** treat as a teachable skill, not magic. One
  full lecture (Week 7) is dedicated to it.
- **VLM grounding:** use small VLMs that fit on student hardware (Qwen-VL, LLaVA) or
  hosted multimodal APIs.
- **Do NOT teach RL policy training.** That is explicitly out of scope.

### 5.6 ARIAC conventions

- The course uses ARIAC 2025 as the testbed. If you encounter ambiguity about which
  ARIAC version (2025-2026 vs. 2026-2027), defer to Rob; he is closer to NIST.
- **Primary references** (consult these when developing lecture content or PT
  problem statements):
  - Code: https://github.com/usnistgov/ARIAC
  - Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html (the
    `/latest/` URL pins to the active cycle; safe to link from lectures).
- ARIAC is the *vehicle*, not the *subject*. Lecture titles should describe general
  concepts; ARIAC examples go in lecture bodies. The word "ARIAC" should rarely appear
  in a lecture title.
- PT5 (capstone) is evaluated on an *unseen* ARIAC scenario. Keep this in mind when
  designing earlier team project problem statements: each PT should leave teams
  better prepared for the unseen scenario, not over-specialized to a fixed one.

### 5.7 Lecture design conventions

Two requirements that apply to every weekly lecture:

- **Every lecture includes hands-on activities.** Lecture time is split between
  exposition and in-class exercises students run at their laptops. Exercises reinforce
  that day's concepts on small, tractable artifacts (a single BT node, a short PDDL
  domain, a one-shot LLM prompt), not the full ARIAC stack. Students are told to
  bring a laptop to every meeting (see `syllabus.md`).
- **Every lecture ties content to ARIAC where possible.** Each lecture should
  explicitly state how the day's concepts surface in ARIAC: which component, which
  scenario type, which docs tutorial. For lectures whose content has no direct ARIAC
  analog (e.g., LLM prompting theory in W9), the connection can be forward-looking:
  "this is how teams will use it in PT4."

When developing a lecture, the order of operations is:

1. Identify the 2-3 core concepts to teach.
2. For each concept, find the ARIAC reference (component, scenario, or doc page).
3. Design one hands-on exercise that practices the concept on a small artifact, not
   the full ARIAC stack.
4. Then write the lecture slides and notes.

Lectures should NOT require students to run the full ARIAC simulation as an in-class
exercise. The full ARIAC environment lives in the team projects, where students have
out-of-class time to debug it.

---

## 6. File and Folder Conventions

The repository is a Sphinx + ReadTheDocs documentation project, not a flat file tree.
The current layout (carry-over from the 2025 course, mid-migration) is:

```
enpm663-spring-2027-docs/
├── CLAUDE.md                              (this file; canonical decision log)
├── README.md, LICENSE, readthedocs.yml    (project metadata, RTD build config)
├── syllabus.md                            (canonical syllabus for the redesigned course)
├── syllabus_spring2027_enpm663.pdf        (v1 syllabus, OBSOLETE; reference only)
└── docs/
    ├── Makefile, make.bat, requirements.txt
    └── source/
        ├── conf.py, index.rst
        ├── _static/, _templates/
        ├── setup/                         (ubuntu, ros, ariac, ai setup; ENPM663)
        ├── syllabus/syllabus.rst          (ENPM663 at-a-glance; canonical is syllabus.md)
        ├── assignments/                   (pt1..pt5.rst + index; ENPM663 team projects)
        ├── lectures/                      (lectureN/lN_index.rst only; ENPM663 stubs)
        ├── reading_material/, glossary/, changelog/  (ENPM663)
```

As of 2026-08-02 the whole toctree-reachable site was migrated off the leftover
ENPM702 (C++) content; a local `make html` builds clean with 0 warnings.

Conventions for new content:

- **Canonical syllabus:** `syllabus.md` at the repo root remains canonical. The site's
  `docs/source/syllabus/syllabus.rst` is now an ENPM663 at-a-glance summary (grade
  breakdown + outline) that points to `syllabus.md`; a full port/render of the complete
  syllabus into the site (or `.md` via MyST) is still deferred until it stabilizes.
- **Team project descriptions:** live under `docs/source/assignments/` as `pt1.rst`
  through `pt5.rst` (done 2026-08-02; the 2025 `rwa*.rst`/`gp*.rst` files were deleted).
- **Lecture notes pages:** `docs/source/lectures/weekNN_topic/` for the site.
- **Lecture slide decks (Beamer):** convention TBD; decide before the first Beamer
  deck is written. Two options under consideration: (a) slides nested next to lecture
  notes at `docs/source/lectures/weekNN_topic/slides/`, or (b) a top-level `slides/`
  directory at the repo root.
- **Obsolete v1 syllabus PDF:** retain in repo root for reference; do not edit. New
  decisions go in `syllabus.md`.

The Sphinx site builds locally via `cd docs && make html` and is auto-built by
ReadTheDocs from the repository per `readthedocs.yml`.

---

## 7. Open Items and Known Risks

Things that are not yet resolved or that the course developer should watch:

1. **Spring 2027 academic calendar dates.** Not yet available from UMD. All dates in
   the syllabus are marked `TODO: verify`.
2. **Classroom and meeting time.** Marked TODO.
3. **ARIAC version naming.** Resolved 2026-08-02: the course uses "ARIAC 2025"
   (Ubuntu 24.04) per Rob (Section 3.7). Re-check the label if NIST renames the cycle
   before spring 2027.
4. **AI API access for students.** Department-level decision pending: course budget for
   API credits vs. requiring students to provision their own.
5. **Academic integrity policy.** The syllabus draft includes language permitting AI
   use for assignments while requiring student understanding. This may need to be
   reviewed by the ENPM program director or UMD graduate school.
6. **Diagnostic quiz scope.** If a significant fraction of students fail it, the Week 1
   refresher may need to expand and crowd out later content. Plan a contingency.
7. **Course evaluations.** Worth comparing 2025 ENPM663 evaluations against this
   redesign once the first 2027 cohort runs.

---

## 8. Quick Reference

**Course title:** Building AI-Augmented Robotic Systems
**Course code:** ENPM663
**Term:** Spring 2027
**Instructor:** Zeid (Rob) Kootbally, solo
**Stack:** Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + ARIAC 2025
**Primary language:** Python
**AI direction:** LLM agents for task planning (agent loop, tool use via MCP, structured output) + VLM grounding with agentic closed-loop replanning; classical motion planning. VLA frontier surveyed only, not built (see Section 3.13).
**BT library:** py_trees_ros
**Planner:** PDDL via Fast Downward or Unified Planning Framework
**Motion planner:** MoveIt2
**Grading:** 60% team projects / 25% quizzes / 15% peer-review contribution
**Weeks:** 15 (with Week 8 spring break)
**Team projects:** 5 (PT1 through PT4 at 10% each, PT5 capstone at 20% on unseen ARIAC)
**Individual assignments:** none
**Quizzes:** 5 (plus 1 ungraded diagnostic in Week 1)
**Guest lectures:** 0 (dropped to make room for the KR week; see Section 3.9)
**Learning outcomes:** 9

---

*Last updated: 2026-06-07 (Session 1: Session Resume section added; switched to
5 team projects with no individual track and no separate Final Project; grading
shifted to 60/25/15; team-formation and peer-review designed and recorded in
`syllabus.md`; Section 6 corrected to reflect actual Sphinx + RTD structure; dropped
Learned Grasp Prediction (W11) in scope review and replaced with Recovery,
Robustness, and Failure Handling; outcome on learned grasping swapped for an outcome
on recovery/robustness; established lecture-design conventions in Section 5.7
requiring hands-on activities and ARIAC ties for every lecture; added Knowledge
Representation as W3 using the 2023 KR lecture as source material, dropped the W13
Guest Lecture to make room, all post-W2 topics and PT/quiz dates shift +1, outcome
count grew to 9; drafted high-level PT1 through PT5 descriptions in `syllabus.md`;
replaced the ENPM702 lecture stubs in the Sphinx site with ENPM663 stubs for all
15 weeks under `docs/source/lectures/lecture{1..15}/lN_index.rst`).*
*Last updated: 2026-08-02 (Session 2: industry-currency review with a web check of the
2026 agent-framework and VLA landscape; reframed the LLM thread (W9, W10) around the
agent loop with MCP, ReAct vs. plan-and-execute, and a classical-wins boundary; added
a VLA-frontier survey segment and multi-robot mention to W2 (survey only, scope
unchanged); fixed the four smaller lecture flags and stale Section 4.3 arcs; new
decision-log entry Section 3.13; renamed the course to "Building AI-Augmented Robotic
Systems" (Section 3.1); rebranded the Sphinx site from the leftover ENPM702 course to
ENPM663 (conf.py, index.rst landing-page rewrite, README, footer; logo assets still
TODO); switched the testbed from ARIAC 2026 to ARIAC 2025 on Ubuntu 24.04 (Section 3.7,
reversing the 2026-06-07 call)).*
*Update this file whenever a design decision is made or revised. The decision log in
Section 3 is the most important section to keep current. Section 2.2 (Current Status)
should be refreshed at the end of every working session.*
