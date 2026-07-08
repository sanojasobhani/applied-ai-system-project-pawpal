from datetime import datetime, time

import pytest
from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status():
    task = Task(title="Test task", category="feeding", duration=10)
    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "completed"


def test_pet_task_addition_increases_count():
    pet = Pet(name="Biscuit", species="Dog", age=5)
    initial_count = pet.task_count()

    task = Task(title="Feed Biscuit", category="feeding", duration=10)
    pet.add_task(task)

    assert pet.task_count() == initial_count + 1


def test_priority_score_prefers_health_and_pet_specific_tasks():
    medication_task = Task(
        title="Give medicine",
        category="medication",
        duration=10,
        priority=3,
        pet_name="Mochi",
    )

    assert medication_task.priority_score() >= 5


def test_generate_plan_respects_preferred_times_and_avoids_conflicts():
    owner = Owner("Jordan")
    owner.set_availability({"start": time(7, 0), "end": time(21, 0)})

    walk_task = Task(
        title="Morning walk",
        category="walk",
        duration=30,
        priority=5,
        pet_name="Mochi",
        preferred_time=time(8, 0),
    )
    feed_task = Task(
        title="Feed Mochi",
        category="feeding",
        duration=10,
        priority=4,
        pet_name="Mochi",
        preferred_time=time(8, 0),
    )

    scheduler = Scheduler(owner, tasks=[feed_task, walk_task])
    plan = scheduler.generate_plan(start_dt=datetime(2024, 1, 1, 8, 0))

    assert len(plan) == 2
    assert plan[0].scheduled_start == datetime(2024, 1, 1, 8, 0)
    assert plan[1].scheduled_start >= plan[0].scheduled_end


def test_mark_task_complete_creates_next_occurrence_for_recurring_task():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    task = Task(
        title="Morning walk",
        category="walk",
        duration=20,
        priority=4,
        pet_name="Mochi",
        recurrence="daily",
    )
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert task.status == "completed"
    assert next_task is not None
    assert next_task.status == "pending"
    assert next_task is not task
    assert next_task.recurrence == "daily"


def test_detect_overlaps_finds_conflicting_tasks():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)

    first = Task(title="Feed Mochi", category="feeding", duration=20, pet_name="Mochi")
    second = Task(title="Walk Biscuit", category="walk", duration=20, pet_name="Biscuit")

    first.scheduled_start = datetime(2024, 1, 1, 8, 0)
    first.scheduled_end = datetime(2024, 1, 1, 8, 20)
    second.scheduled_start = datetime(2024, 1, 1, 8, 10)
    second.scheduled_end = datetime(2024, 1, 1, 8, 30)

    overlaps = scheduler.detect_overlaps([first, second])

    assert overlaps == [(first, second)]


def test_lightweight_conflict_check_returns_warning_message():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)

    first = Task(title="Feed Mochi", category="feeding", duration=20, pet_name="Mochi")
    second = Task(title="Walk Biscuit", category="walk", duration=20, pet_name="Biscuit")

    first.scheduled_start = datetime(2024, 1, 1, 8, 0)
    first.scheduled_end = datetime(2024, 1, 1, 8, 20)
    second.scheduled_start = datetime(2024, 1, 1, 8, 10)
    second.scheduled_end = datetime(2024, 1, 1, 8, 30)

    message = scheduler.lightweight_conflict_check([first, second])

    assert "Warning" in message
    assert "overlaps" in message
