# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```text
Today's Schedule
-----------------
08:00 — Morning walk (walk) for Biscuit [30 min]
08:30 — Give Mittens medication (medication) for Mittens [15 min]
08:45 — Feed Biscuit (feeding) for Biscuit [10 min]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```
python3 -m pytest tests\tests_pawpal.py

Sample test output:

```
========================================================= test session starts ==========================================================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\sanoj\OneDrive\Desktop\vs code\ai110-module2show-pawpal-ss
plugins: anyio-4.13.0
collected 13 items                                                                                                                      

tests\tests_pawpal.py .............                                                                                               [100%]

========================================================== 13 passed in 0.07s ==========================================================
```
confidence level: 5 stars

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_tasks() and sort_by_time() | e.g., by priority, duration |
| Filtering | filter_tasks() | e.g., skip tasks if time runs out |
| Conflict handling | detect_overlaps() and lightweight_conflict_check() | e.g., overlapping time slots |
| Recurring tasks | mark_task_complete() and next_occurrence() | e.g., daily vs. weekly |

## ✨ Features

PawPal+ uses a lightweight scheduling engine to turn a list of pet-care tasks into an ordered, conflict-aware daily plan.

- Priority-based task ordering using a weighted scoring system that favors urgent care tasks such as medication and feeding.
- Preferred-time-aware scheduling so tasks can be placed around a user’s preferred start time when possible.
- Conflict detection and warning messages for overlapping task windows.
- Automatic conflict resolution by shifting tasks to the next available slot when needed.
- Chronological display of the final plan so the schedule is easy to read and follow.
- Pet-specific task filtering for viewing tasks associated with a selected pet.
- Support for recurring tasks with daily or weekly follow-up scheduling.
- Availability-aware planning based on the owner’s permitted scheduling window.
- Plan explanations that describe why each task was placed at its assigned time.

## 🎬 Demo Walkthrough

PawPal+ is designed as a simple but interactive pet-care planning experience. In the Streamlit UI, a user can enter owner and pet details, add care tasks, and generate a daily plan with explanations.

1. Open the app and enter the owner name, pet name, species, and age. The app stores this information in the owner and pet models.
2. Add one or more tasks such as a walk, feeding, or medication. Each task includes a title, duration, and priority.
3. Click “Generate schedule” to let the scheduler build a plan. The scheduler sorts tasks by priority, respects preferred times, and checks for conflicts.
4. Review the generated plan in the table view. Tasks appear in chronological order, and the app shows warning messages if overlapping tasks are detected.
5. Use the pet filter to focus on tasks for a specific pet and compare how the schedule changes.

The scheduler demonstrates several key behaviors during this workflow:
- Sorting by priority and time to decide task order
- Conflict warnings when two tasks overlap
- Automatic conflict resolution by shifting tasks into the next available slot
- Recurring-task support for daily or weekly care routines

Example CLI output from running the scheduler in main.py:

```text
1. Feeding was placed at 08:00 because it scored 7 and was ordered ahead of lower-priority work. It also matched the preferred time of 08:00. This is a high-importance care task.
2. Morning walk was placed at 08:10 because it scored 7 and was ordered ahead of lower-priority work. It also matched the preferred time of 08:00.
```
