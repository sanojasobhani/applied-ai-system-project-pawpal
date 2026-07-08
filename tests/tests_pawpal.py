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


def test_mark_task_complete_creates_next_day_task_for_daily_recurrence():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    task = Task(
        title="Morning walk",
        category="walk",
        duration=20,
        priority=4,
        pet_name="Mochi",
        recurrence="daily",
        preferred_time=time(8, 0),
    )
    task.scheduled_start = datetime(2024, 1, 1, 8, 0)
    task.scheduled_end = datetime(2024, 1, 1, 8, 20)
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert task.status == "completed"
    assert next_task is not None
    assert next_task.status == "pending"
    assert next_task is not task
    assert next_task.recurrence == "daily"
    assert next_task.scheduled_start == datetime(2024, 1, 2, 8, 0)
    assert next_task.scheduled_end == datetime(2024, 1, 2, 8, 20)


def test_detect_overlaps_flags_duplicate_times():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)

    first = Task(title="Feed Mochi", category="feeding", duration=20, pet_name="Mochi")
    second = Task(title="Walk Biscuit", category="walk", duration=20, pet_name="Biscuit")

    first.scheduled_start = datetime(2024, 1, 1, 8, 0)
    first.scheduled_end = datetime(2024, 1, 1, 8, 20)
    second.scheduled_start = datetime(2024, 1, 1, 8, 10)
    second.scheduled_end = datetime(2024, 1, 1, 8, 30)

    overlaps = scheduler.detect_overlaps([first, second])

    assert len(overlaps) == 1
    assert overlaps[0] == (first, second)


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


def test_sort_by_time_returns_tasks_in_chronological_order():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)

    first = Task(title="Later task", category="general", duration=15, priority=1, pet_name="Mochi")
    second = Task(title="Earlier task", category="general", duration=10, priority=2, pet_name="Mochi")

    first.scheduled_start = datetime(2024, 1, 1, 9, 0)
    first.scheduled_end = datetime(2024, 1, 1, 9, 15)
    second.scheduled_start = datetime(2024, 1, 1, 8, 0)
    second.scheduled_end = datetime(2024, 1, 1, 8, 10)

    ordered_tasks = scheduler.sort_by_time([first, second])

    assert ordered_tasks[0] is second
    assert ordered_tasks[1] is first


def test_can_schedule_respects_availability_window():
    owner = Owner("Jordan")
    owner.set_availability({"start": time(8, 0), "end": time(20, 0)})

    assert owner.can_schedule(time(7, 0)) is False
    assert owner.can_schedule(time(8, 0)) is True
    assert owner.can_schedule(time(20, 0)) is True
    assert owner.can_schedule(time(20, 1)) is False
    assert owner.can_schedule(datetime(2024, 1, 1, 9, 0)) is True


def test_explain_plan_mentions_priority_and_preferred_time():
    owner = Owner("Jordan")
    task = Task(
        title="Medication",
        category="medication",
        duration=10,
        priority=4,
        pet_name="Mochi",
        preferred_time=time(8, 0),
    )
    scheduler = Scheduler(owner, tasks=[task])

    plan = scheduler.generate_plan(start_dt=datetime(2024, 1, 1, 7, 0))
    explanation = scheduler.explain_plan(plan)

    assert "placed at" in explanation
    assert "preferred time" in explanation
    assert "high-importance care task" in explanation


def test_recurring_task_completion_does_not_mutate_original_task_state():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    task = Task(
        title="Feeding",
        category="feeding",
        duration=10,
        recurrence="daily",
        pet_name="Mochi",
    )
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert task.status == "completed"
    assert next_task.status == "pending"
    assert next_task.scheduled_start is None
    assert next_task.scheduled_end is None
    assert next_task is not task


def test_scheduler_avoids_same_time_overlaps_when_conflicts_exist():
    owner = Owner("Jordan")
    owner.set_availability({"start": time(7, 0), "end": time(21, 0)})

    first = Task(title="Feed", category="feeding", duration=20, priority=4, pet_name="Mochi", preferred_time=time(8, 0))
    second = Task(title="Walk", category="walk", duration=20, priority=3, pet_name="Mochi", preferred_time=time(8, 0))

    scheduler = Scheduler(owner, tasks=[first, second])
    plan = scheduler.generate_plan(start_dt=datetime(2024, 1, 1, 8, 0))

    assert len(plan) == 2
    assert plan[0].scheduled_start == datetime(2024, 1, 1, 8, 0)
    assert plan[1].scheduled_start >= plan[0].scheduled_end


def test_availability_boundaries_are_handled_correctly():
    owner = Owner("Jordan")
    owner.set_availability({"start": time(8, 0), "end": time(20, 0)})

    assert owner.can_schedule(time(8, 0)) is True
    assert owner.can_schedule(time(20, 0)) is True
    assert owner.can_schedule(time(7, 59)) is False
    assert owner.can_schedule(time(20, 1)) is False
